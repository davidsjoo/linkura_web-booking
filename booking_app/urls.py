from django.conf.urls import patterns, url
from booking_app import views
from booking_app.views import CustomerUpdate
from booking_app.views import VisitUpdate
from booking_app.views import TimeUpdate
from booking_app.views import CustomerDelete
from booking_app.views import VisitDelete
from booking_app.views import TimeDelete
from booking_app.views import TimeDetail
from booking_app.views import VisitDetail
<<<<<<< HEAD
=======
from booking_app.views import CustomerDetail
from booking_app.views import BookingDetail
>>>>>>> d74bd5a9b3e7c93cf5205861547e2d68dec4b23a



urlpatterns = patterns('booking_app.views',

    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^coach_index/$', views.coach_index, name='coach_index'),
    url(r'^add_customer/$', views.add_customer, name='add_customer'),
    url(r'^(?P<pk>\d+)/customer_update/$', CustomerUpdate.as_view(), name='customer_update'),
    url(r'^(?P<pk>\d+)/customer_delete/$', CustomerDelete.as_view(), name='customer_delete'),
    
    url(r'^(?P<customer_id>\d+)/$', views.visit, name='visit'),
    url(r'^(?P<customer_id>\d+)/new_visit/$', views.new_visit, name='new_visit'),
    url(r'^(?P<customer_id>\d+)/add_visit/$', views.add_visit, name='add_visit'),
    url(r'^(?P<pk>\d+)/visit_update/$', VisitUpdate.as_view(), name='visit_update'),
    url(r'^(?P<pk>\d+)/visit_delete/$', VisitDelete.as_view(), name='visit_delete'),
    
    url(r'^(?P<slug>[-\w]+)/(?P<visit_id>\d+)/$', views.detail, name='detail'),
    url(r'^(?P<visit_id>\d+)/new_time/$', views.new_time, name='new_time'),
    url(r'^(?P<visit_id>\d+)/add_time/$', views.add_time, name='add_time'),
    url(r'^(?P<pk>\d+)/time_update/$', TimeUpdate.as_view(), name='time_update'),
    url(r'^(?P<pk>\d+)/time_delete/$', TimeDelete.as_view(), name='time_delete'),

    url(r'^(?P<time_id>\d+)/(?P<booking_id>\d+)/bokningar/$', views.bokningar, name='bokningar'),
    url(r'^(?P<visit_id>\d+)/submit$', views.submit, name='submit'),
    url(r'^(?P<customer_id>\d+)/(?P<visit_id>\d+)/(?P<booking_id>\d+)/new_submit/$', views.new_submit, name='new_submit'),
    url(r'^(?P<customer_id>\d+)/(?P<visit_id>\d+)/(?P<booking_id>\d+)/$', views.update_booking, name='update_booking'),
    url(r'^(?P<customer_id>\d+)/(?P<visit_id>\d+)/(?P<time_id>\d+)/(?P<booking_id>\d+)/results/$', views.results, name='results'),

    url(r'^(?P<pk>\d+)/time_detail/$', TimeDetail.as_view(), name='time_detail'),
    url(r'^(?P<pk>\d+)/visit_detail/$', VisitDetail.as_view(), name='visit_detail'),
<<<<<<< HEAD
=======
    url(r'^(?P<pk>\d+)/customer_detail/$', CustomerDetail.as_view(), name='customer_detail'),
>>>>>>> d74bd5a9b3e7c93cf5205861547e2d68dec4b23a
    url(r'^bookinglist/$', views.BookingsView.as_view(), name='bookinglist'),
     
    url(r'^(?P<pk>\d+)/booking_detail/$', BookingDetail.as_view(), name='booking_detail'),  
    url(r'^(?P<customer_id>\d+)/(?P<visit_id>\d+)/(?P<time_id>\d+)/(?P<booking_id>\d+)/create_reminder/$', views.create_reminder, name='create_reminder'),
)