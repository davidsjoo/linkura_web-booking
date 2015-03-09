from django import forms
from datetimewidget.widgets import DateTimeWidget

from booking_app.models import Booking
from booking_app.models import Time
from booking_app.models import Visit
from booking_app.models import Customer


class BookingForm(forms.ModelForm):
	class Meta:
		model = Booking
		fields = ['client_firstname', 'client_lastname', 'client_phone', 'client_mail']

#class TimeForm(forms.ModelForm):
#	class Meta:
#		model = Time
#		fields = ['datetime', 'capacity', 'location', 'description']

class VisitForm(forms.ModelForm):
	class Meta:
		model = Visit
		fields = ['visit_name', 'visit_date']

class CustomerForm(forms.ModelForm):
	class Meta:
		model = Customer
		fields = ['customer_name']

class TimeForm(forms.ModelForm):
    class Meta:
        model = Time
 
        fields = ['datetime', 'capacity', 'location', 'description']
        widgets = {
            #Use localization and bootstrap 3
            'datetime': DateTimeWidget(attrs={'id':"visit"}, usel10n = True, bootstrap_version=3)
        }

