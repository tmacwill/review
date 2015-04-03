declare var $: any;
declare var nunjucks: any;
declare var _: any;

module r.macros.typeahead {
    export class Typeahead {
        $container: any;
        highlight: number = -1;
        $results: any;
        clickCallback: Function;
        updateCallback: Function;
        url: string;

        templates = {
            'results': nunjucks.compile(`
                <div class="typeahead">
                    <ul class="typeahead-list"></ul>
                </div>
            `),

            'row': nunjucks.compile(`
                <li><a data-id="{{ id }}" data-name="{{ name }}" href="#">{{ name }}</a></li>
            `)
        };

        constructor($container, url, clickCallback, updateCallback) {
            this.$container = $container;
            this.url = url;
            this.clickCallback = clickCallback;
            this.updateCallback = updateCallback;
            this.$results = $(this.templates.results.render());

            this.$container.after(this.$results);
            this.bind();
            this.clear();
        }

        bind() {
            // update the typeahead during typing
            var self = this;
            this.$container.on('keyup', function(e) {
                var down = 40;
                var up = 38;
                var enter = 13;

                if (e.which == up || e.which == down) {
                    if (e.which == up) {
                        self.highlight = Math.max(self.highlight - 1, 0);
                    }
                    else if (e.which == down) {
                        self.highlight = Math.min(self.highlight + 1, self.$results.find('li').length - 1);
                    }

                    self.$results.find('li a').removeClass('hover');
                    self.$results.find('li:nth-child(' + (self.highlight + 1) + ') a').addClass('hover');
                }

                else if (e.which == enter) {
                    self.$results.find('li:nth-child(' + (self.highlight + 1) + ') a').trigger('click');
                }

                else {
                    self.update($(this).val());
                }
            });

            // when a row is clicked, trigger the click callback
            this.$results.on('click', 'a', function(e) {
                self.clickCallback(this);
                self.clear();
                return false;
            });

            // typeahead highlights
            this.$results.on('mouseover', 'a', function() {
                $(this).addClass('hover');
            });
            this.$results.on('mouseout', 'a', function() {
                self.$results.find('a').removeClass('hover');
            });
        }

        clear() {
            this.$container.val('');
            this.update('');
        }

        update(q: string) {
            // reset highlight position whenever the text changes
            var self = this;
            this.highlight = -1;

            // if the input is empty, then hide the results container
            if (q == '') {
                this.$results.hide();
                return;
            }

            // fire query to tags autocomplete endpoint
            $.get(this.url, {'q': q}, function(response) {
                var data = JSON.parse(response);
                if (self.updateCallback) {
                    var filtered = self.updateCallback(q, data);
                    if (filtered) {
                        data = filtered;
                    }
                }

                // render a row for each tag
                var html = '';
                for (var i = 0; i < data.results.length; i++) {
                    var row = data.results[i];
                    html += self.templates.row.render({
                        'id': row.id,
                        'name': row.name
                    });
                }

                // if we got back no results, then hide
                if (!html) {
                    self.$results.hide();
                    return;
                }

                // replace the typeahead list with the rendered suggestions
                self.$results.find('ul').html(html);
                self.$results.show();
            });
        }
    }
}
