/// <reference path="../macros/typeahead" />

declare var $: any;
declare var initialTags: any;

class Browse {
    $container: any;
    typeahead: any;
    tags: Array<any> = [];
    filter: string;
    allTags: any = {};

    templates = {
        'tag': nunjucks.compile(`
            <span class="btn-tag" data-id="{{ id }}"><a href="#" class="btn-remove">×</a>{{ name }}</span>
        `)
    };

    constructor($container, initialTags) {
        var self = this;
        this.$container = $container;
        this.typeahead = new r.macros.typeahead.Typeahead(
            this.$container.find('#input-search'),
            '/tags/autocomplete',
            function(row) {
                self.typeaheadClicked(row);
            },
            false
        );

        // we may have landed on a page with tags in the URL, so load them
        this.allTags = initialTags;
        this.bind();
        this.loadTagsFromURL(false);
    }

    bind() {
        var self = this;

        // when a sidebar tag is clicked, add it to the filter
        this.$container.on('click', '#popular-tags a', function(e) {
            self.addTag($(this).attr('data-id'), $(this).attr('data-name'));
            self.refresh();
            return false;
        });

        // remove tag when tag close button is pressed
        this.$container.on('click', '#tags-container .btn-tag .btn-remove', function(e) {
            // get the id of the tag and remove it
            var id = $(this).parent('[data-id]').attr('data-id');
            self.removeTag(id);
            self.refresh();
            return false;
        });

        // reload stories when filters are changed
        this.$container.on('click', '#filter-container a', function(e) {
            self.filter = $(this).attr('data-filter');
            self.pushQueryString();
            self.refresh();
            return false;
        });

        // when we go back, re-load the tags from the current URL
        window.onpopstate = function(e) {
            self.loadTagsFromURL(false);
        };
    }

    addTag(id, name, push?) {
        // if tag already exists, then ignore it
        if (_.some(this.tags, function(e) { return e.id == id; })) {
            return;
        }

        // add the tag to the list of currently-applied tags
        this.tags.push({
            'id': id,
            'name': name
        });

        // keep around data for the tag in case the user hits back
        this.allTags[id] = {
            'id': id,
            'name': name
        };

        if (push || push === undefined) {
            this.pushQueryString();
        }
    }

    loadStories() {
        var self = this;
        $.get(window.location.pathname + window.location.search, function(response) {
            var data = JSON.parse(response);
            var html = '';
            for (var i = 0; i < data.uploads.length; i++) {
                html += nunjucks.render('upload_story.html', {
                    'upload': data.uploads[i]
                });
            }

            self.$container.find('#uploads-list').html(html);
        });
    }

    loadTagsFromURL(push?) {
        var $tags = this.$container.find('#tags-container');
        if (!window.location.search) {
            return;
        }

        var idString = window.location.search.split('=')[1];
        if (!idString) {
            return;
        }

        // for each tag ID in the URL, add it
        var ids = idString.split(',');
        this.tags = [];
        for (var i = 0; i < ids.length; i++) {
            var tag = this.allTags[ids[i]];
            this.addTag(tag.id, tag.name, push);
        }

        if (push) {
            this.refresh();
        }
    }

    pushQueryString() {
        // render the current tag list in the URL
        var tags = _.map(this.tags, function(e) { return e.id; });
        var path = window.location.pathname;
        if (tags.length) {
            path += '?q=' + tags.join(',');
        }
        if (this.filter) {
            path += (tags.length == 0 ? '?' : '&') + 'filter=' + this.filter;
        }

        window.history.pushState(null, '', path);
    }

    removeTag(id) {
        this.tags = _.filter(this.tags, function(e) { return e.id != id });
        this.pushQueryString();
    }

    refresh() {
        this.loadStories();
        this.renderTags();
    }

    renderTags() {
        var html = '';
        for (var i = 0; i < this.tags.length; i++) {
            var tag = this.tags[i];
            html += this.templates.tag.render({
                'id': tag.id,
                'name': tag.name
            });
        }

        // hide the tags container if there aren't any tags
        var $tags = this.$container.find('#tags-container');
        $tags.html(html);
    }

    typeaheadClicked(row: Element) {
        this.addTag($(row).attr('data-id'), $(row).attr('data-name'));
        this.refresh();
        this.typeahead.clear();
    }
}

$(function() {
    new Browse($('#browse-container'), initialTags);
});
