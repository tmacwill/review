/// <reference path="../macros/comment_box" />

declare var $: any;
declare var _: any;
declare var moment: any;
declare var nunjucks: any;
declare var current_user: any;
declare var events: any;

module r.macros.reviewable_file {
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
            this.$numbers = this.$container.find('.line-number:not(.padding) a');
            this.$code = this.$container.find('.code:not(.padding)');
            this.$commentContainer = this.$container.find('#comment-container');

            // load comments already present on page load
            this.comments = [];
            var initialComments = this.$commentContainer.find('.comment-box');
            for (var i = 0, n = initialComments.length; i < n; i++) {
                var $comment = $(initialComments[i]);
                this.comments.push(new r.macros.comment_box.CommentBox($comment, this.fileId));
            }

            this.bind();
            this.subscribe();
            this.layout();
        }

        bind() {
            var self = this;
            var $contents = $(this.$container.find('#file-contents'));
            $contents.on('click', '.line-number a', function(e) {
                self.addComment(parseInt($(this).attr('data-line'), 10));
                return false;
            });

            this.$container.on('mouseover', '.comment-box, .code', function(e) {
                var line = $(this).attr('data-line');
                self.$container.find('.comment-box[data-line="' + line + '"]').addClass('hover');
                self.$container.find('.code[data-line="' + line + '"]').addClass('hover');
            });

            this.$container.on('mouseout', '.comment-box, .code', function(e) {
                var line = parseInt($(this).attr('data-line'), 10);
                self.$container.find('.comment-box[data-line="' + line + '"]').removeClass('hover');
                self.$container.find('.code[data-line="' + line + '"]').removeClass('hover');
            });
        }

        addComment(line: number) {
            // if user is logged out, then show the login box
            if (!current_user) {
                var $overlay = $('#overlay');
                var $register = $('#register-box');
                $overlay.removeClass('hidden');
                $register.removeClass('hidden');
                return;
            }

            // render a new comment box (because we're creating the comment, we know that
            // the current user and author user are the same)
            var $comment = $(nunjucks.render('comment_box.html', {
                'contents': '',
                'current_user': current_user,
                'line': line,
                'timestamp': moment(),
                'user': current_user
            }));

            // render the comment box
            this.$commentContainer.append($comment);
            var box = new r.macros.comment_box.CommentBox($comment, this.fileId);
            this.comments.push(box);
            this.layout();
            box.focus();
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

                $(this.$code[box.comment.line - 1]).addClass('highlight');
            }
        }

        subscribe() {
            var self = this;

            // remove comment
            events.subscribe('commentRemoved', function(data) {
                var comment = _.find(self.comments, function(e) { return e.id == data.id });
                if (!comment) {
                    return;
                }

                // if there are no other comments on this line, then remove the highlight
                var others = _.filter(self.comments, function(e) { return e.line == comment.line });
                if (others.length == 1) {
                    $(self.$code[comment.line - 1]).removeClass('highlight');
                }

                self.comments = _.filter(self.comments, function(e) { return e.id != data.id });
                self.layout();
            });

            // let other components trigger layouts
            events.subscribe('layout', function(data) {
                self.layout();
            });

            // show comments from a user
            events.subscribe('showCommentsFromUser', function(data) {
                self.$container.find('.comment-box[data-user-id="' + data.user_id + '"]').removeClass('hidden');
                self.layout();
            });

            // hide comments from a user
            events.subscribe('hideCommentsFromUser', function(data) {
                self.$container.find('.comment-box[data-user-id="' + data.user_id + '"]').addClass('hidden');
                self.layout();
            });
        }
    }
}
