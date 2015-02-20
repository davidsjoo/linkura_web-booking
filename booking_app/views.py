from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.views import generic
from itertools import chain
from django.core.exceptions import ObjectDoesNotExist

from booking_app.models import Customer
from booking_app.models import Visit
from booking_app.models import Time
from booking_app.models import Booking
from booking_app.forms import BookingForm


def timelist(request, customer_id, visit_id, time_id):
    visit = get_object_or_404(Visit, pk=visit_id)
    customer = get_object_or_404(Customer, pk=customer_id)
    time = get_object_or_404(Time, pk=time_id)
    return render(request, 'booking_app/timelist.html', {'visit': visit, 'customer': customer, 'time': time})

class IndexView(generic.ListView):
    template_name = 'booking_app/index.html'
    context_object_name = 'latest_customer_list'
    def get_queryset(self):
        return Customer.objects.order_by('customer_name')[:5]

class CustomerView(generic.ListView):
    context_object_name = 'latest_customer_list'
    template_name = 'booking_app/foretag.html'
    def get_queryset(self):
        return Customer.objects.order_by('customer_name')[:5]

def besok(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    return render(request, 'booking_app/besok.html', {'customer': customer})

def visit(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    return render(request, 'booking_app/visit.html', {'customer': customer})

def tider(request, customer_id, visit_id):
    visit = get_object_or_404(Visit, pk=visit_id)
    customer = get_object_or_404(Customer, pk=customer_id)
    sort_time = Time.objects.order_by('datetime')
    return render(request, 'booking_app/tider.html', {'visit': visit, 'customer': customer, 'sort_time': sort_time})

def bokningar(request, customer_id, visit_id, time_id, booking_id):
    visit = get_object_or_404(Visit, pk=visit_id)
    customer = get_object_or_404(Customer, pk=customer_id)
    time = get_object_or_404(Time, pk=time_id)
    booking = get_object_or_404(Booking, pk=booking_id)
    return render(request, 'booking_app/bokningar.html', {'visit': visit, 'customer': customer, 'time': time, 'booking': booking})

class BookingsView(generic.ListView):
    template_name = 'booking_app/bookinglist.html'
    context_object_name = 'bookinglist'
    def get_queryset(self):
        client = Booking.objects.order_by('time')

        
        result_list = list(chain(client))
        return result_list

def update_booking(request, customer_id, visit_id, booking_id):
    visit = get_object_or_404(Visit, pk=visit_id)
    customer = get_object_or_404(Customer, pk=customer_id)
    booking = get_object_or_404(Booking, pk=booking_id)
    return render(request, 'booking_app/update_booking.html', {'visit': visit, 'customer': customer, 'booking': booking,})


def detail(request, customer_id, visit_id):
    visit = get_object_or_404(Visit, pk=visit_id)
    customer = get_object_or_404(Customer, pk=customer_id)
    form = BookingForm(request.POST or None)
    return render(request, 'booking_app/detail.html', {'visit': visit, 'customer': customer, 'form': form,})

#class ResultsView(generic.DetailView):
 #   model = Customer
  #  template_name = 'booking_app/results.html'

def results(request, customer_id, visit_id, booking_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    visit = get_object_or_404(Visit, pk=visit_id)
    booking = get_object_or_404(Booking, pk=booking_id)

    print "test", visit

    return render(request, 'booking_app/results.html', {'visit': visit, 'customer': customer, 'booking': booking, 'form': form,})



class VisitView(generic.DetailView):
    model = Customer
    template_name = 'booking_app/visit.html'

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
                selected_time.capacity -=1
                selected_time.save()
                time_id = selected_time.id
                time = Time.objects.get(id=time_id)
                client_firstname = request.POST['client_firstname']
                client_lastname = request.POST['client_lastname']
                client_phone = request.POST['client_phone']
                client_mail = request.POST['client_mail']
                create_booking = Booking.objects.create(time = time, client_firstname = client_firstname, client_lastname = client_lastname, client_phone = client_phone, client_mail = client_mail)
                booking = create_booking.id
                return HttpResponseRedirect(reverse('booking_app:results', args=(customer.id, p.id, booking,)))
            else:
                return render(request, 'booking_app/detail.html', {
                'visit': p,
                'form_error_message': "Du har inte fyllt i alla falt.",
                'customer': customer,
                'form': form,
                })


def new_submit(request, customer_id, visit_id, booking_id):
    p = get_object_or_404(Visit, pk=visit_id)
    customer = get_object_or_404(Customer, pk=customer_id)
    booking = get_object_or_404(Booking, pk=booking_id)
    
    try:
        selected_time = p.time_set.get(pk=request.POST['time'])
        
    except (KeyError, Time.DoesNotExist):


        return render(request, 'booking_app/update_booking.html', {
            'visit': p,
            'time_error_message': "Du har inte valt en tid.", 
            'customer': customer,
            'booking': booking,
            
        })

    else:
        get_time_id = booking.time_id
        old_time = Time.objects.get(pk=get_time_id)
        old_time.capacity +=1
        old_time.save()
        selected_time.capacity -=1
        selected_time.save()
        new_time = Booking.objects.get(pk=booking.id)
        new_time.time = selected_time
        new_time.save()

        return render(request, 'booking_app/results.html', {
        'visit': p,
        'selected_time': selected_time,
        'customer': customer,
        'booking': booking,
        'new_time': new_time,
        
        })
