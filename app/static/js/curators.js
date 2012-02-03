var Curators = Curators || {};


Curators.Storify = (function() {
    var tmpl = '<li data-key="%key%" ' +
                'style="background-image:url(%thumbnail%);">' +
                '<a href="%permalink%"><h2>%title%</h2></a></li>';

    /**
     * Get latest Storify stories from the database.
     */
    var getData = function(callback) {
        $.ajax({
            url: '/storify-dummy-data/',
            success: callback
        });
    };

    /**
     * Render the supplied story to a string using the template.
     */
    var renderStory = function(story) {
        return tmpl.replace('%key%', story['key'])
                   .replace('%thumbnail%', story['thumbnail'])
                   .replace('%permalink%', story['permalink'])
                   .replace('%title%', story['title']);
    };

    return {
        'getData': getData,
        'renderStory': renderStory
    };
})();


Curators.Feeds = (function() {
    var subscribed_feeds = [];
    var feed_timers = {};
    var update_every = 60; // seconds

    /**
     * Return an array listing all possible feeds that can
     * be subscribed to. At the moment that's just Storify.
     */
    var availableFeeds = function() {
        return ['Storify'];
    };

    /**
     * Add a feed subscription. This will add the feed to the
     * dashboard and run a timer to update it automagically.
     */
    var addFeed = function(feed) {
        if (-1 !== availableFeeds().indexOf(feed)) {
            subscribed_feeds.push(feed);
            updateFeeds();
        }
        return false;
    };

    /**
     * Update all subscribed feeds, one after the other.
     */
    var updateFeeds = function() {
        var ajax_gif = '<span class="ajax-loader">Refreshing stories</span>';

        $.each(subscribed_feeds, function(i, feed) {
            var $feed = $('[data-feed="' + feed + '"]');
            $feed.find('header').append(ajax_gif);
            
            Curators[feed].getData(function(data) {
                var $stories = $feed.find('ol li');
                var new_stories = '';

                $.each(data['stories'], function(i, story) {
                    new_stories += Curators[feed].renderStory(story);
                });

                var $new_stories = $(new_stories);
                $feed.find('ol').prepend($new_stories.hide());
                $stories.remove();
                $new_stories.show();
            });
            
            $feed.find('header .ajax-loader').remove();
        });
    };

    return {
        'availableFeeds': availableFeeds,
        'addFeed': addFeed,
        'updateFeeds': updateFeeds
    };

})();


$(document).ready(function() {
    Curators.Feeds.addFeed('Storify');
});
