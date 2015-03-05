from django.conf.urls import patterns, url
from booking_app import views
from booking_app.views import CustomerUpdate
from booking_app.views import VisitUpdate
from booking_app.views import TimeUpdate
from booking_app.views import CustomerDelete
from booking_app.views import VisitDelete
from booking_app.views import TimeDelete


urlpatterns = patterns('booking_app.views',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<customer_id>\d+)/$', views.visit, name='visit'),
    url(r'^(?P<customer_id>\d+)/besok/$', views.besok, name='besok'),
    url(r'^(?P<customer_id>\d+)/new_visit/$', views.new_visit, name='new_visit'),
    url(r'^(?P<customer_id>\d+)/(?P<visit_id>\d+)/$', views.detail, name='detail'),
    url(r'^(?P<customer_id>\d+)/(?P<visit_id>\d+)/tider/$', views.tider, name='tider'),
    url(r'^(?P<customer_id>\d+)/(?P<visit_id>\d+)/new_time/$', views.new_time, name='new_time'),
    url(r'^(?P<customer_id>\d+)/(?P<visit_id>\d+)/(?P<time_id>\d+)/(?P<booking_id>\d+)/bokningar/$', views.bokningar, name='bokningar'),
    url(r'^bookinglist/$', views.BookingsView.as_view(), name='bookinglist'),
    url(r'^foretag/$', views.ForetagView.as_view(), name='foretag'),
    url(r'^customer/$', views.CustomerView.as_view(), name='customer'),
    url(r'^coach_index/$', views.CoachIndexView.as_view(), name='coach_index'),
    url(r'^new_customer/$', views.new_customer, name='new_customer'),
    url(r'^(?P<customer_id>\d+)/(?P<visit_id>\d+)/submit$', views.submit, name='submit'),
    url(r'^(?P<customer_id>\d+)/(?P<visit_id>\d+)/add_time/$', views.add_time, name='add_time'),
    url(r'^(?P<customer_id>\d+)/add_visit/$', views.add_visit, name='add_visit'),
    url(r'^add_customer/$', views.add_customer, name='add_customer'),
    url(r'^(?P<customer_id>\d+)/(?P<visit_id>\d+)/(?P<time_id>\d+)/(?P<booking_id>\d+)/results/$', views.results, name='results'),
    url(r'^(?P<customer_id>\d+)/(?P<visit_id>\d+)/(?P<booking_id>\d+)/$', views.update_booking, name='update_booking'),
    url(r'^(?P<customer_id>\d+)/(?P<visit_id>\d+)/(?P<booking_id>\d+)/new_submit/$', views.new_submit, name='new_submit'),
    url(r'^(?P<pk>\d+)/customer_update/$', CustomerUpdate.as_view(), name='customer_update'),
    url(r'^(?P<pk>\d+)/visit_update/$', VisitUpdate.as_view(), name='visit_update'),
    url(r'^(?P<pk>\d+)/time_update/$', TimeUpdate.as_view(), name='time_update'),
    url(r'^(?P<pk>\d+)/customer_delete/$', CustomerDelete.as_view(), name='customer_delete'),
    url(r'^(?P<pk>\d+)/visit_delete/$', VisitDelete.as_view(), name='visit_delete'),
    url(r'^(?P<pk>\d+)/time_delete/$', TimeDelete.as_view(), name='time_delete'),


    
)