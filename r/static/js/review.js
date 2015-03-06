var r;
(function (r) {
    var comment;
    (function (comment) {
        function init(tables) {
            $(function () {
                $(tables).each(function () {
                    new CommentContainer(this);
                });
            });
        }
        comment.init = init;
        var CommentContainer = (function () {
            function CommentContainer($table) {
                this.$table = $table;
                this.$numbers = this.$table.querySelector('.linenodiv');
                this.$code = this.$table.querySelector('.code');
                this.bind();
            }
            CommentContainer.prototype.bind = function () {
                $(this.$numbers).on('click', 'a', function (e) {
                    return false;
                });
            };
            CommentContainer.prototype.layout = function () {
            };
            return CommentContainer;
        })();
        comment.CommentContainer = CommentContainer;
        var CommentBox = (function () {
            function CommentBox() {
            }
            return CommentBox;
        })();
        comment.CommentBox = CommentBox;
    })(comment = r.comment || (r.comment = {}));
})(r || (r = {}));
/// <reference path="comment" />
r.comment.init('.file table');
