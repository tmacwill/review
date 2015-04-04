/// <reference path="typeahead" />

declare var $: any;
declare var nunjucks: any;
declare var _: any;

module r.macros.upload_box {
    export class UploadBox {
        $container: any;
        $tagsContainer: any;
        tags: Array<any> = [];
        typeahead: any;

        templates = {
            'fileRow': nunjucks.compile(`
                <div class="file-row">
                    <a class="btn-remove" href="#">×</a>
                    <h4 class="file-name">{{ name }}</h4>
                    <input type="hidden" name="files[]" value="{{ value }}" />
                </div>
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
                self.$container.find('#input-file').trigger('click');
                return false;
            });

            // when files are selected from the hidden input, render them
            this.$container.on('change', '.input-file', function() {
                for (var i = 0; i < this.files.length; i++) {
                    self.handleFile(this.files[i]);
                }

                return false;
            });

            // remove tag when tag close button is pressed
            this.$container.on('click', '#tags-container .btn-tag .btn-remove', function(e) {
                // get the id of the tag and remove it
                var id = $(this).parent('[data-id]').attr('data-id');
                self.tags = _.filter(self.tags, function(e) { return e.id != id });
                self.renderTags();

                return false;
            });

            // remove a file when the remove button is pressed
            this.$container.on('click', '.file-row .btn-remove', function(e) {
                $(this).parents('.file-row').remove();
                return false;
            });

            // handle drag and drops into the file container
            var $fileContainer = this.$container.find('#files-container');
            $fileContainer.on('drop', function(e) {
                var files = e.originalEvent.dataTransfer.files;
                for (var i = 0; i < files.length; i++) {
                    self.handleFile(files[i]);
                }

                $(this).removeClass('dragover');
                return false;
            });

            $fileContainer.on('dragover', function(e) {
                $(this).addClass('dragover');
                return false;
            });

            $fileContainer.on('dragend', function(e) {
                $(this).removeClass('dragover');
                return false;
            });
        }

        handleFile(file: File) {
            var self = this;

            // once the file is read, display a removable row in the form
            var reader = new FileReader();
            reader.onload = function(f) {
                self.$container.find('#files-list').append(self.templates.fileRow.render({
                    'name': file.name,
                    'value': encodeURI(JSON.stringify({'filename': file.name, 'contents': reader.result}))
                }));
            };

            reader.readAsText(file);
        }

        renderTags() {
            // render tags in alphabetical order
            var tagHtml = '';
            var inputHtml = ''
            for (var i = 0; i < this.tags.length; i++) {
                // render user-displayed pills
                var tag = this.tags[i];
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

            // if tag already exists, then ignore it
            if (_.some(this.tags, function(e) { return e.id == id; })) {
                return;
            }

            this.tags.push({
                'id': id,
                'name': name
            });

            this.renderTags();
            this.typeahead.clear();
        }
    }
}
