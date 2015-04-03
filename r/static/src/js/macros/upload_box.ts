/// <reference path="typeahead" />

declare var $: any;
declare var nunjucks: any;
declare var _: any;

module r.macros.upload_box {
    export class UploadBox {
        $container: any;
        $tagsContainer: any;
        tags: any = {};
        typeahead: any;

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
            `)
        };

        constructor($container) {
            var self = this;
            this.$container = $container;
            this.$container.find('#upload-form').append(this.templates.fileInput.render());
            this.$container.find('#typeahead').css({'width': this.$container.find('#input-tags').outerWidth() - 20 + 'px'});
            this.$tagsContainer = this.$container.find('#tags-container');

            // initialize typeahead for the tags input
            this.typeahead = new r.macros.typeahead.Typeahead(
                this.$container.find('#input-tags'),
               '/tags/autocomplete',
               function(row) {
                   self.typeaheadClicked(row)
               },
               false
            );

            this.bind();
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

        typeaheadClicked(row: Element) {
            // add tag to list
            var id = $(row).attr('data-id');
            var name = $(row).attr('data-name');
            this.tags[id] = {
                'id': id,
                'name': name
            };

            this.renderTags();
            this.typeahead.clear();
        }
    }
}
