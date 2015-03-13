declare var $: any;

module r.comment {
    export function init(tables) {
        $(function() {
            $(tables).each(function() {
                new CommentContainer(this);
            });
        });
    }

    export class CommentContainer {
        $table: Element;
        $numbers: Element;
        $code: Element;

        constructor($table: Element) {
            this.$table = $table;
            this.$numbers = this.$table.querySelector('.linenodiv');
            this.$code = this.$table.querySelector('.code');

            this.bind();
        }

        bind() {
            $(this.$numbers).on('click', 'a', function(e) {
                return false;
            });
        }

        layout() {
        }
    }

    export class CommentBox {
    }
}
