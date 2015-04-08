declare var $: any;
declare var moment: any;
declare var events: any;

var DATE_FORMAT: string = 'MMMM Do, h:mma';

module r.macros.comment_box {
    export class CommentBox {
        $container: any;
        fileId: string;
        id: string;
        line: number;

        constructor($container, fileId) {
            this.$container = $($container);
            this.fileId = fileId;
            this.id = this.$container.attr('data-id');
            this.line = parseInt(this.$container.attr('data-line'), 10);

            // format timestamp to human-readable time
            var $timestamp = this.$container.find('#timestamp');
            var timestamp = $timestamp.html()
            if (/^\d+$/.test(timestamp)) {
                $timestamp.html(moment(new Date(parseInt(timestamp, 10))).format(DATE_FORMAT));
            }

            this.bind();
        }

        bind() {
            var self = this;

            // show save button on focus
            this.$container.on('focus', '#contents', function(e) {
                self.$container.find('#btn-save').removeClass('hidden');
            });

            // save comment on blur
            this.$container.on('blur', '#contents', function(e) {
                self.save();
                setTimeout(function() {
                    // if we're no longer focused, then remove the save button
                    if (!self.focused()) {
                        self.$container.find('#btn-save').addClass('hidden');
                    }
                }, 300);
            });

            // save comment when save button presseed
            this.$container.on('click', '#btn-save', function(e) {
                // since blurring the comment will trigger a save, we don't need to do anything here
                self.focus();
                return false;
            });

            // remove comment when the x is clicked
            this.$container.on('click', '.btn-remove', function(e) {
                self.remove();
                return false;
            });
        }

        contents() {
            return this.$container.find('#contents').html();
        }

        focused() {
            return this.$container.find('#contents').is(':focus');
        }

        remove() {
            this.$container.hide();
            events.publish('commentRemoved', {'id': this.id});

            $.ajax({
                'url': '/comment/' + this.id,
                'type': 'delete'
            });
        }

        empty() {
            // comments containing only empty space or <br> tags are empty
            var contents = this.contents();
            return /^\s*(<br\s*\/>)*\s*$/.test(contents);
        }

        focus() {
            this.$container.find('#contents').focus();
        }

        height() {
            return this.$container.outerHeight();
        }

        save() {
            // don't save empty comments
            if (this.empty()) {
                return;
            }

            // construct comment payload
            var data = {
                'file_id': this.fileId,
                'line': this.line,
                'contents': this.contents()
            }

            // if we have an ID, then include that in the request so an existing comment is updated
            if (this.id) {
                data['id'] = this.id;
            }

            $.post('/comment', data, (response) => {
                // we might have an ID now, so save that
                this.id = JSON.parse(response).id;
            });
        }

        setTop(top: number) {
            this.$container.css({'top': top + 'px'});
        }
    }
}
