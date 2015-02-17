from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'web_booking4.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^booking_app/', include('booking_app.urls', namespace='booking_app')),
    #url(r'^booking_app/', include('booking_app.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
