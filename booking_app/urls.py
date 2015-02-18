from django.conf.urls import patterns, url
from booking_app import views


urlpatterns = patterns('booking_app.views',
    url(r'^$', views.IndexView.as_view(), name='index'),
    
    #url(r'^(?P<pk>\d+)/$', views.VisitView.as_view(), name='visit'),
    
    url(r'^(?P<customer_id>\d+)/$', views.visit, name='visit'),
    url(r'^(?P<customer_id>\d+)/besok/$', views.besok, name='besok'),
    
    url(r'^(?P<customer_id>\d+)/(?P<visit_id>\d+)/$', views.detail, name='detail'),
    url(r'^(?P<customer_id>\d+)/(?P<visit_id>\d+)/tider/$', views.tider, name='tider'),
    url(r'^(?P<customer_id>\d+)/(?P<visit_id>\d+)/(?P<time_id>\d+)/bokningar/$', views.bokningar, name='bokningar'),
    url(r'^bookinglist/$', views.BookingsView.as_view(), name='bookinglist'),
    url(r'^foretag/$', views.CustomerView.as_view(), name='foretag'),
    url(r'^(?P<customer_id>\d+)/(?P<visit_id>\d+)/submit$', views.submit, name='submit'),
    #url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<customer_id>\d+)/(?P<visit_id>\d+)/(?P<booking_id>\d+)/results/$', views.results, name='results'),
    url(r'^(?P<customer_id>\d+)/(?P<visit_id>\d+)/(?P<booking_id>\d+)/$', views.update_booking, name='update_booking'),
    url(r'^(?P<customer_id>\d+)/(?P<visit_id>\d+)/(?P<time_id>\d+)/timelist/$', views.timelist, name='timelist'),
    url(r'^(?P<customer_id>\d+)/(?P<visit_id>\d+)/(?P<booking_id>\d+)/new_submit/$', views.new_submit, name='new_submit'),

    
)