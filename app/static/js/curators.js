var Curators = Curators || {};


Curators.Storify = (function() {
    var api = 'http://api.storify.com/v1/stories/browse/popular?per_page=10';

    var getJSON = function(callback) {
        $.ajax({
            api: api,
            success: function(data) {
                callback(data);
            }
        });
    };

    return {
        'getJSON': getJSON
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
        return ['storify'];
    };

    /**
     * Add a feed subscription. This will add the feed to the
     * dashboard and run a timer to update it automagically.
     */
    var addFeed = function(feed) {
        if (-1 !== availableFeeds().indexOf(feed)) {
            subscribed_feeds.push(feed);
            return true;
        }
        return false;
    };

    /**
     * Update all subscribed feeds, one after the other.
     */
    var updateFeeds = function() {

    };

    return {
        'availableFeeds': availableFeeds,
        'addFeed': addFeed
    };

})();


$(document).ready(function() {
    Curators.Feeds.addFeed('storify');
});
