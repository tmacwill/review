declare var $: any;
declare var moment: any;
declare var events: any;

module r.macros.reviewers_filter {
    export class ReviewersFilter {
        $container: any;

        constructor($container: any) {
            this.$container = $container;

            this.bind();
        }

        bind() {
            // when a row is clicked, toggle comments from that user
            this.$container.on('click', '.filter-user-row', function(e) {
                var $this = $(this);
                var $icon = $this.find('.glyphicon');
                var user = $this.attr('data-user-id');

                if ($this.attr('data-selected')) {
                    $this.removeAttr('data-selected');
                    $icon.removeClass('glyphicon-check').addClass('glyphicon-unchecked');
                    events.publish('hideCommentsFromUser', {'user_id': user});
                }

                else {
                    $this.attr('data-selected', 'true');
                    $icon.removeClass('glyphicon-unchecked').addClass('glyphicon-check');
                    events.publish('showCommentsFromUser', {'user_id': user});
                }

                return false;
            });
        }
    }
}
