declare var $: any;
declare var _: any;

module r.comment {
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
            $(this.$numbers).on('click', 'a', function(e) {
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
        line: number;

        constructor($container, fileId) {
            this.$container = $($container);
            this.fileId = fileId;
            this.line = parseInt(this.$container.attr('data-line'), 10);
        }

        height() {
            return this.$container.outerHeight();
        }

        setTop(top: number) {
            this.$container.css({'top': top + 'px'});
        }
    }
}
