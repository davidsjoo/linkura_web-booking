#coding: utf8 
import os
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.views import generic
from itertools import chain
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
import pytz
import datetime
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from django.core.urlresolvers import reverse_lazy
from django.utils.functional import lazy

#from booking_app.mail_inv import sendAppointment
import datetime as dt
import icalendar
import uuid

from booking_app.models import Customer
from booking_app.models import Visit
from booking_app.models import Time
from booking_app.models import Booking
from booking_app.forms import BookingForm
from booking_app.forms import TimeForm
from booking_app.forms import VisitForm
from booking_app.forms import CustomerForm

#Customer
class IndexView(generic.ListView):
    template_name = 'booking_app/index.html'
    context_object_name = 'latest_customer_list'
    def get_queryset(self):
        return Customer.objects.order_by('-created_date')

def coach_index(request,):
    form = CustomerForm(request.POST or None)
    customer_list = Customer.objects.order_by('-created_date')
    return render(request, 'booking_app/coach_index.html', {
        'form': form, 
        'customer_list': customer_list
    })

def add_customer(request,):
    form = CustomerForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            customer_name = request.POST['customer_name']
            
            Customer.objects.create(customer_name = customer_name)
            return HttpResponseRedirect(reverse('booking_app:coach_index',))
        else:
            return HttpResponseRedirect(reverse('booking_app:coach_index',))

class CustomerUpdate(UpdateView):
    model = Customer
    def get_success_url(self):
        return reverse('booking_app:coach_index')

class CustomerDelete(DeleteView):
    model = Customer
    def get_success_url(self):
        return reverse('booking_app:coach_index')

#Visit
def visit(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    return render(request, 'booking_app/visit.html', {
        'customer': customer
    })

def new_visit(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    form = VisitForm(request.POST or None)
    return render(request, 'booking_app/new_visit.html', {
        'customer': customer, 
        'form': form
    })

def add_visit(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    form = VisitForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            visit_name = request.POST['visit_name']
            visit_date = request.POST['visit_date']
            Visit.objects.create(
                customer = customer,
                visit_name = visit_name, 
                visit_date = visit_date
            )
            return HttpResponseRedirect(reverse('booking_app:new_visit', 
                args=(customer.id,)
            ))
        else:
            return HttpResponseRedirect(reverse('booking_app:new_visit', 
                args=(customer.id,)
            ))

class VisitUpdate(UpdateView):
    model = Visit
    fields = ['visit_name', 'visit_date']
    def get_success_url(self):
        customer_id =  self.object.customer_id
        return reverse('booking_app:new_visit', args={customer_id})


def update_booking(request, customer_id, visit_id, booking_id):
	visit = get_object_or_404(Visit, pk=visit_id) 
	customer = get_object_or_404(Customer, pk=customer_id)
	booking = get_object_or_404(Booking, pk=booking_id)
	form = BookingForm(request.POST or None, instance=booking)
	return render(request, 'booking_app/update_booking.html', {'visit': visit, 'customer': customer, 'booking': booking, 'form': form,})

class VisitDelete(DeleteView):
    model = Visit
    def get_success_url(self):
        customer_id =  self.object.customer_id
        return reverse('booking_app:new_visit', args={customer_id})

#Time
def detail(request, customer_id, visit_id):
	visit = get_object_or_404(Visit, pk=visit_id)
	customer = get_object_or_404(Customer, pk=customer_id)
	form = BookingForm(request.POST or None)
	return render(request, 'booking_app/detail.html', {'visit': visit, 'customer': customer, 'form': form,})

def results(request, customer_id, visit_id, time_id, booking_id):
    customer = get_object_or_404(Customer, pk=customer_id)
        #Customer: Företaget t.ex. Linkura
    visit = get_object_or_404(Visit, pk=visit_id)
        #Visit: typ av möte t.ex. uppstart
    booking = get_object_or_404(Booking, pk=booking_id)
        #Booking: Person uppgifter till den som bokat
    time = get_object_or_404(Time, pk=time_id)
        #Time: Tiden man valt. (time.datetime = datumet man valt)

    # Kalender inbjudan
    tz = pytz.timezone("Europe/Stockholm")
    reminderHours = 1
    startHour = 7
    start = time.datetime
    cal = icalendar.Calendar()
    cal.add('prodid', '-//My calendar application//example.com//') #Ändra!
    cal.add('version', '2.0')
    cal.add('method', "REQUEST")

    event = icalendar.Event()
    event.add('attendee', booking.client_mail)
    event.add('organizer', "me@example.com") #Ändra till Linkuras mail
    event.add('status', "confirmed") 
    event.add('category', "Event")
    event.add('summary', 'Möte med coach') #Ändra till något bättre
    event.add('description', 'description') #Ändra eller använd email.html som description
    event.add('location', time.location)
    event.add('dtstart', start)
    event.add('dtend', dt.time(startHour + 1, 0, 0))
    event.add('dtstamp', start) #Indikerar tiden när kalender objektet skapades
    event['uuid'] = uuid.uuid4() # Generate some unique ID
    event.add('priority', 5)
    event.add('sequence', 1)
    event.add('created', tz.localize(dt.datetime.now())) #Skillnad på denna och dtstamp?

    cal.add_component(event)
    print cal #Skriver ut cal objektet till terminalen

    # / Kalender inbjudan

    link = 'http://lia.linkura.se:8080/booking_app/'+customer_id+'/'+visit_id+'/'+booking_id
    # send_inv = sendAppointment(time.datetime)
    mail = booking.client_mail
    from_email = settings.EMAIL_HOST_USER
    to_email = [mail]

    #msg_plain = render_to_string('booking_app/email.txt', {'booking': booking})
    msg_html = render_to_string(
        'booking_app/email.html',
        {
            'booking': booking,
            'customer': customer,
            'booking': booking,
            'visit': visit,
            'time': time,
            'link': link,
            #'sendAppointment': sendAppointment,
        })
    msg = EmailMultiAlternatives('Tidsbokning för Linkura', msg_html, from_email, to_email)
    msg.attach_alternative(cal.to_ical(), 'text/calendar')
    msg.send()
    visit = get_object_or_404(Visit, pk=visit_id)
    customer = get_object_or_404(Customer, pk=customer_id)
    form = BookingForm(request.POST or None)
    return render(request, 'booking_app/detail.html', {
        'visit': visit, 
        'customer': customer, 
        'form': form,
    })

def new_time(request, visit_id):
    visit = get_object_or_404(Visit, pk=visit_id)
    form = TimeForm(request.POST or None)
    customer_id = visit.customer_id
    return render(request, 'booking_app/new_time.html', {
        'visit': visit, 
        'form': form, 
        'customer_id': customer_id
    })

def add_time(request, visit_id):
    visit = get_object_or_404(Visit, pk=visit_id)
    form = TimeForm(request.POST or None)
    customer_id = visit.customer_id
    if request.method == 'POST':
        if form.is_valid():
            datetime = request.POST['datetime']
            capacity = request.POST['capacity']
            location = request.POST['location']
            description = request.POST['description']
            Time.objects.create(
                visit = visit, 
                datetime = datetime, 
                capacity = capacity, 
                location = location, 
                description = description
            )
            return render(request, 'booking_app/new_time.html', {
                'visit': visit,
                'form': form,
                'customer_id': customer_id
            })
        else:
            return HttpResponseRedirect(reverse('booking_app:new_time', 
                args=(visit.id,)
            ))

class TimeUpdate(UpdateView):
    model = Time
    fields = ['datetime', 'capacity', 'location', 'description']
    def get_success_url(self):
        visit_id =  self.object.visit_id
        return reverse('booking_app:new_time', args={visit_id})

class TimeDelete(DeleteView):
    model = Time
    def get_success_url(self):
        visit_id =  self.object.visit_id
        return reverse('booking_app:new_time', args={visit_id})

#Booking
def bokningar(request, time_id, booking_id):
    time = get_object_or_404(Time, pk=time_id)
    booking = get_object_or_404(Booking, pk=booking_id)
    visit_id = time.visit_id
    return render(request, 'booking_app/bokningar.html', {
        'time': time, 
        'booking': booking, 
        'visit_id': visit_id
    })

def submit(request, customer_id, visit_id):
    p = get_object_or_404(Visit, pk=visit_id)
    customer = get_object_or_404(Customer, pk=customer_id)
    form = BookingForm(request.POST or None)
    try:
        selected_time = p.time_set.get(pk=request.POST['time'])
    except (KeyError, Time.DoesNotExist):
        customer = get_object_or_404(Customer, pk=customer_id)
        return render(request, 'booking_app/detail.html', {
            'visit': p,
            'time_error_message': "Du har inte valt en tid.", 
            'customer': customer,
            'form': form,
            })
    else:
        if request.method == 'POST':
            if form.is_valid():
                count_bookings = selected_time.booking_set.all().count()
                print count_bookings
                if count_bookings == selected_time.capacity:
                    return render(request, 'booking_app/detail.html', {
                    'visit': p,
                    'capacity_error_message': "Tyvärr har någon redan bokat den tiden",
                    'customer': customer,
                    'form': form,
                    })
                time_id = selected_time.id
                time = Time.objects.get(id=time_id)
                client_firstname = request.POST['client_firstname']
                client_lastname = request.POST['client_lastname']
                client_phone = request.POST['client_phone']
                client_mail = request.POST['client_mail']
                create_booking = Booking.objects.create(
                    time = time, 
                    client_firstname = client_firstname, 
                    client_lastname = client_lastname, 
                    client_phone = client_phone, 
                    client_mail = client_mail
                )
                booking = create_booking.id
                return HttpResponseRedirect(reverse('booking_app:results', 
                    args=(customer.id, p.id, time_id, booking,)
                ))
            else:
                return render(request, 'booking_app/detail.html', {
                'visit': p,
                'form_error_message': "Du måste ange för- och efternamn",
                'customer': customer,
                'form': form,
                })
        

def new_submit(request, customer_id, visit_id, booking_id):
    p = get_object_or_404(Visit, pk=visit_id)
    customer = get_object_or_404(Customer, pk=customer_id)
    booking = get_object_or_404(Booking, pk=booking_id)
    form = BookingForm(request.POST or None)
    pub_from = request.GET.get('pub_date_from')
    if request.method == 'POST':
        if form.is_valid():
            
            
            #Hämtar id på nuvarnade bokning
            get_time_id = booking.time_id
            
            #selected_time blir den nya tiden man har valt eller den man hade innan om man inte väljer någon tid.
            selected_time = request.POST.get('time', get_time_id)

            #Hämtar tiden selected time
            new_time = Time.objects.get(pk=selected_time)

            #Om man har bytt tid
            if get_time_id != new_time.id:
                count_bookings = new_time.booking_set.all().count()

                #Om någon har bokat den tiden redan, medans du valde tid
                if count_bookings == new_time.capacity:
                    return render(request, 'booking_app/update_booking.html',{
                        'visit': p, 
                        'customer': customer, 
                        'booking': booking, 
                        'form': form, 
                        'error_message': "Tyvärr har någon redan valt den tiden",
                    })
            
            booking.time = new_time
            booking.client_firstname = request.POST.get('client_firstname')
            booking.client_lastname = request.POST.get('client_lastname')
            booking.client_mail = request.POST.get('client_mail')
            booking.client_phone = request.POST.get('client_phone')
            booking.save()
            return HttpResponseRedirect(reverse('booking_app:results', 
                args=(customer.id, p.id, new_time.id, booking_id,)))
        else:
            return render(request, 'booking_app/update_booking.html', {
            'visit': p,
            'form_error_message': "Du måste ange för- och efternamn",
            'customer': customer,
            'form': form,
            'booking': booking,
            'pub_from': pub_from,
            })

def update_booking(request, customer_id, visit_id, booking_id):
    visit = get_object_or_404(Visit, pk=visit_id)
    customer = get_object_or_404(Customer, pk=customer_id)
    booking = get_object_or_404(Booking, pk=booking_id)
    form = BookingForm(request.POST or None, instance=booking)
    return render(request, 'booking_app/update_booking.html', {
        'visit': visit, 
        'customer': customer, 
        'booking': booking, 
        'form': form,
    })

def results(request, customer_id, visit_id, time_id, booking_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    visit = get_object_or_404(Visit, pk=visit_id)
    booking = get_object_or_404(Booking, pk=booking_id)
    time = get_object_or_404(Time, pk=time_id)

    link = 'http://lia.linkura.se:8080/booking_app/'+customer_id+'/'+visit_id+'/'+booking_id
    mail = booking.client_mail
    from_email = settings.EMAIL_HOST_USER
    to_email = [mail]
    msg_plain = render_to_string('booking_app/email.txt', {
        'booking': booking
    })
    msg_html = render_to_string('booking_app/email.html', {
        'booking': booking, 
        'customer': customer, 
        'booking': booking, 
        'visit': visit, 
        'time': time, 
        'link': link})
    send_mail(msg_plain, msg_html, from_email, to_email, fail_silently=True)

    return render(request, 'booking_app/results.html', {
        'visit': visit, 
        'customer': customer, 
        'booking': booking, 
        'time': time,
    })

class BookingsView(generic.ListView):
    template_name = 'booking_app/bookinglist.html'
    context_object_name = 'bookinglist'
    def get_queryset(self):
        client = Booking.objects.all()
        result_list = list(chain(client))
        return result_list

class TimeDetail(DetailView):
    model = Time
    def get_queryset(self):
        return Time.objects.all()

class VisitDetail(DetailView):
    model = Visit
    def get_queryset(self):
        return Visit.objects.all()


        










    









