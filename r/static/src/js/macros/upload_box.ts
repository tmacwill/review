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

            // show visual feedback when a file is dragged over the area
            $fileContainer.on('dragover', function(e) {
                $(this).addClass('dragover');
                return false;
            });

            $fileContainer.on('dragend', function(e) {
                $(this).removeClass('dragover');
                return false;
            });

            // show paste area when paste file is pressed
            this.$container.on('click', '#btn-paste-file', function(e) {
                var $container = self.$container.find('#container-paste');
                if ($container.is(':hidden')) {
                    self.$container.find('#container-paste textarea, #container-paste input').val('');
                    $container.show();
                }

                return false;
            });

            // create a file from a pasted row
            this.$container.on('click', '#btn-paste-file-done', function(e) {
                var filename = self.$container.find('#input-paste-filename').val();
                var contents = self.$container.find('#textarea-paste').val();
                if (!filename || !contents) {
                    return;
                }

                self.addFile(filename, contents);
                self.$container.find('#container-paste').hide();
                return false;
            });

            // hide paste container
            this.$container.on('click', '#btn-paste-file-cancel', function(e) {
                self.$container.find('#container-paste').hide();
                return false;
            });
        }

        addFile(filename: string, contents: string) {
            if (!filename || !contents) {
                return;
            }

            this.$container.find('#files-list').append(this.templates.fileRow.render({
                'name': filename,
                'value': encodeURI(JSON.stringify({'filename': filename, 'contents': contents}))
            }));
        }

        handleFile(file: File) {
            var self = this;

            // once the file is read, display a removable row in the form
            var reader = new FileReader();
            reader.onload = function(f) {
                self.addFile(file.name, reader.result);
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
