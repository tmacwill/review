declare var $: any;
declare var nunjucks: any;

module r.macros.upload_box {
    export function init(container) {
        $(function() {
            new UploadBox($(container));
        });
    }

    export class UploadBox {
        $container: any;

        fileRowTemplate: any = nunjucks.compile(`
            <div class="file-row">
                <!-- a class="btn-remove" href="#">×</a -->
                <h4 class="file-name">{{ name }}</h4>
                <!-- div class="file-progress"></div -->
            </div>
        `);

        inputTemplate: any = nunjucks.compile(`
            <input class="input-file current-input" type="file" name="files[]" multiple />
        `);

        constructor($container) {
            this.$container = $container;
            this.$container.find('#upload-form').append(this.inputTemplate.render());

            this.bind();
        }

        bind() {
            var self = this;
            this.$container.find('#btn-add-file').on('click', function() {
                self.$container.find('.input-file.current-input').trigger('click');
            });

            this.$container.on('change', '.input-file', function() {
                for (var i = 0; i < this.files.length; i++) {
                    var file = this.files[i];
                    self.$container.find('#files-list').append(self.fileRowTemplate.render({
                        name: file.name,
                    }));
                }

                self.$container.find('.input-file.current-input').removeClass('current-input');
                self.$container.find('#upload-form').append(self.inputTemplate.render());
            });
        }
    }
}
