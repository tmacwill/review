declare var $: any;

class Profile {
    $container: any;
    $tabs: Array<any>;
    $contents: Array<any>;

    constructor($container) {
        this.$container = $container;
        this.$tabs = this.$container.find('#tabs [data-tab]').toArray();
        this.$contents = this.$container.find('#tab-contents [data-tab]').toArray();

        // hide every tab except the first one
        var n = this.$tabs.length;
        for (var i = 1; i < n; i++) {
            $(this.$contents[i]).addClass('hidden');
        }

        this.bind();
    }

    bind() {
        var self = this;

        // switch tabs
        this.$container.on('click', '#tabs [data-tab]', function(e) {
            // highlight the selected tab
            var tab = $(this).attr('data-tab');
            self.$container.find('#tabs [data-tab]').removeClass('selected');
            $(this).addClass('selected');

            // show the selected contents
            self.$container.find('#tab-contents [data-tab]').addClass('hidden');
            self.$container.find('#tab-contents [data-tab="' + tab + '"]').removeClass('hidden');

            return false;
        });
    }
}

$(function() {
    new Profile($('#user-stream'));
});
