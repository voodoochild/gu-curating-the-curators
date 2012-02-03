from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'app.views.dashboard', name='app_dashboard'),
    
    url(r'^storify-dummy-data/$', 'feeds.views.storify_dummy_data', name='feeds_storify_dummy_data'),
    url(r'^tweetminster-dummy-data/$', 'feeds.views.tweetminster_dummy_data', name='feeds_storify_dummy_data'),
)
