from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'app.views.dashboard', name='app_dashboard'),
)
