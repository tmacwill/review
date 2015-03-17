declare var $: any;
declare var _: any;
declare var moment: any;
declare var nunjucks: any;
declare var current_user: any;

module r.comment {
    var DATE_FORMAT: string = 'MMMM Do, h:mma';

    export function init(tables) {
        $(function() {
            $(tables).each(function() {
                new ReviewableFile(this, $(this).attr('data-file-id'));
            });
        });
    }

    export class ReviewableFile {
        $container: any;
        $code: any;
        $commentContainer: any;
        comments: Array<any>;
        fileId: string;
        $numbers: any;
        commentPadding: number = 5;

        constructor($container: any, fileId: string) {
            this.$container = $($container);
            this.fileId = fileId;
            this.$numbers = this.$container.find('.linenodiv a');
            this.$code = this.$container.find('.code');
            this.$commentContainer = this.$container.find('#comment-container');

            // load comments already present on page load
            this.comments = [];
            var initialComments = this.$commentContainer.find('.comment-box');
            for (var i = 0, n = initialComments.length; i < n; i++) {
                var $comment = $(initialComments[i]);
                this.comments.push(new CommentBox($comment, this.fileId));
            }

            this.bind();
            this.layout();
        }

        bind() {
            var self = this;
            $(this.$container.find('.linenodiv')).on('click', 'a', function(e) {
                // determine which line was clicked
                var href = $(this).attr('href');
                var line = parseInt(href.substring(href.lastIndexOf('-') + 1));

                // render a new comment box
                var $comment = $(nunjucks.render('comment_box.html', {
                    'author': current_user.name,
                    'line': line,
                    'timestamp': moment(),
                    'contents': ''
                }));

                // render the comment box
                self.$commentContainer.append($comment);
                var box = new CommentBox($comment, self.fileId);
                self.comments.push(box);
                self.layout();
                box.focus();
                return false;
            });
        }

        layout() {
            // get the top and height of each comment box
            var bounds = [];
            for (var i = 0; i < this.comments.length; i++) {
                var comment = this.comments[i];
                var position = $(this.$numbers[comment.line - 1]).position();
                bounds.push({'top': position.top, 'height': comment.height(), 'comment': comment});
            }

            // sort comments by ascending height, then push down any overlapping comments
            var sortedBounds = _.sortBy(bounds, function(e) { return e.top });
            for (var i = 1; i < sortedBounds.length; i++) {
                var current = sortedBounds[i];
                var previous = sortedBounds[i - 1];
                if (previous.top + previous.height > current.top) {
                    current.top = previous.top + previous.height + this.commentPadding;
                }
            }

            // update DOM to reflect new bounds
            for (var i = 0; i < sortedBounds.length; i++) {
                var box = sortedBounds[i];
                box.comment.setTop(box.top);
            }
        }
    }

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

            // save comments on blur
            this.$container.on('blur', '#contents', function(e) {
                self.save();
            });
        }

        contents() {
            return this.$container.find('#contents').html();
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
