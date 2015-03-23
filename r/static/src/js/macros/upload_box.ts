declare var $: any;
declare var nunjucks: any;
declare var _: any;

module r.macros.upload_box {
    export function init(container) {
        $(function() {
            new UploadBox($(container));
        });
    }

    export class UploadBox {
        $container: any;
        $tagsContainer: any;
        $typeahead: any;
        tags: any = {};
        typeaheadContents: Array<any>;
        highlightPosition: number = -1;

        templates = {
            'fileRow': nunjucks.compile(`
                <div class="file-row">
                    <!-- a class="btn-remove" href="#">×</a -->
                    <h4 class="file-name">{{ name }}</h4>
                    <!-- div class="file-progress"></div -->
                </div>
            `),

            'fileInput': nunjucks.compile(`
                <input class="input-file current-input" type="file" name="files[]" multiple />
            `),

            'tag': nunjucks.compile(`
                <span class="btn-tag" data-id="{{ id }}"><a href="#" class="btn-remove">×</a>{{ name }}</span>
            `),

            'tagInput': nunjucks.compile(`
                <input type="hidden" name="tags[]" value="{{ id }}" />
            `),

            'typeaheadRow': nunjucks.compile(`
                <li><a data-id="{{ id }}" data-name="{{ name }}" href="#">{{ name }}</a></li>
            `)
        };

        constructor($container) {
            this.$container = $container;
            this.$typeahead = this.$container.find('#typeahead-list');
            this.$container.find('#upload-form').append(this.templates.fileInput.render());
            this.$container.find('#typeahead').css({'width': this.$container.find('#input-tags').outerWidth() - 20 + 'px'});
            this.$tagsContainer = this.$container.find('#tags-container');

            this.bind();
            this.updateTypeahead('');
        }

        bind() {
            var self = this;

            // submit the form when submit is pressed
            this.$container.find('#btn-submit').on('click', function() {
                self.$container.find('#upload-form').submit();
                return false;
            });

            // clicking the add file button triggers a click on the hidden file input
            this.$container.find('#btn-add-file').on('click', function() {
                self.$container.find('.input-file.current-input').trigger('click');
            });

            // when files are selected from the hidden input, render them
            this.$container.on('change', '.input-file', function() {
                for (var i = 0; i < this.files.length; i++) {
                    var file = this.files[i];
                    self.$container.find('#files-list').append(self.templates.fileRow.render({
                        name: file.name,
                    }));
                }

                // create a new hidden input that will be triggered next time
                self.$container.find('.input-file.current-input').removeClass('current-input');
                self.$container.find('#upload-form').append(self.templates.fileInput.render());
            });

            // update the typeahead during typing
            this.$container.find('#input-tags').on('keyup', function(e) {
                var down = 40;
                var up = 38;
                var enter = 13;

                if (e.which == up || e.which == down) {
                    if (e.which == up) {
                        self.highlightPosition = Math.max(self.highlightPosition - 1, 0);
                    }
                    else if (e.which == down) {
                        self.highlightPosition = Math.min(self.highlightPosition + 1, self.typeaheadContents.length - 1);
                    }

                    self.$typeahead.find('li a').removeClass('hover');
                    self.$typeahead.find('li:nth-child(' + (self.highlightPosition + 1) + ') a').addClass('hover');
                }

                else if (e.which == enter) {
                    self.$typeahead.find('li:nth-child(' + (self.highlightPosition + 1) + ') a').trigger('click');
                }

                else {
                    self.updateTypeahead($(this).val());
                }
            });

            // typeahead highlights
            this.$typeahead.on('mouseover', 'a', function() {
                $(this).addClass('hover');
            });
            this.$typeahead.on('mouseout', 'a', function() {
                self.$typeahead.find('a').removeClass('hover');
            });

            // add tag when typeahead row is clicked
            this.$typeahead.on('click', 'a', function(e) {
                // add tag to list
                var id = $(this).attr('data-id');
                var name = $(this).attr('data-name');
                self.tags[id] = {
                    'id': id,
                    'name': name
                };

                self.renderTags();
                self.$container.find('#input-tags').val('');
                self.updateTypeahead('');
                return false;
            });

            // remove tag when tag close button is pressed
            this.$container.on('click', '#tags-container .btn-tag .btn-remove', function(e) {
                // get the id of the tag and remove it
                var parent = $(this).parent('[data-id]');
                delete self.tags[$(parent).attr('data-id')];
                self.renderTags();

                return false;
            });
        }

        renderTags() {
            // render tags in alphabetical order
            var values = _.sortBy(_.values(this.tags), function(e) { return e['name'].toLowerCase(); });
            var tagHtml = '';
            var inputHtml = ''
            for (var i = 0; i < values.length; i++) {
                // render user-displayed pills
                var tag = values[i];
                tagHtml += this.templates.tag.render({
                    'id': tag.id,
                    'name': tag.name
                });

                // render hidden form values
                inputHtml += this.templates.tagInput.render({
                    'id': tag.id
                });
            }

            this.$container.find('#tags-container').html(tagHtml);
            this.$container.find('#tags-input-container').html(inputHtml);
        }

        updateTypeahead(q: string) {
            var self = this;
            var $parent = this.$typeahead.parent();
            if (q == '') {
                $parent.hide();
                return;
            }

            // reset highlight position whenever the text changes
            this.highlightPosition = -1;

            // fire query to tags autocomplete endpoint
            $.get('/tags/autocomplete', {'q': q}, function(response) {
                var rows = JSON.parse(response);
                if (rows.tags.length) {
                    $parent.show();
                }

                // render a row for each tag
                var html = '';
                for (var i = 0; i < rows.tags.length; i++) {
                    html += self.templates.typeaheadRow.render({
                        'id': rows.tags[i].id,
                        'name': rows.tags[i].name
                    });
                }

                // replace the typeahead list with the rendered suggestions
                self.$typeahead.html(html);
                self.typeaheadContents = rows.tags;
            });
        }
    }
}
