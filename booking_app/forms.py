from django import forms
from datetimewidget.widgets import DateTimeWidget, DateWidget

from booking_app.models import Booking
from booking_app.models import Time
from booking_app.models import Visit
from booking_app.models import Customer


class BookingForm(forms.ModelForm):
	class Meta:
		model = Booking
		fields = [
			'client_firstname', 
			'client_lastname', 
			'client_phone', 
			'client_mail',
			
		]

class ReminderForm(forms.ModelForm):
	class Meta:
		model = Booking
		fields = [
			'client_reminder']

class VisitForm(forms.ModelForm):
	class Meta:
		model = Visit
		fields = ['visit_name', 'visit_date']
		dateTimeOptions = {
		'format': 'yyyy-mm-dd',
		'autoclose': True,
		'weekStart': 1,
		'pickerPosition': 'bottom-left',
		}
		widgets = {
			'visit_date': DateWidget(
				options = dateTimeOptions, 
				attrs={'id':"customer"}, 
				bootstrap_version=3
			)
		}

class CustomerForm(forms.ModelForm):
	class Meta:
		model = Customer
		fields = ['customer_name']

class TimeForm(forms.ModelForm):
    class Meta:
		model = Time
		fields = ['datetime', 'capacity', 'location', 'description']
		dateTimeOptions = {
		'format': 'yyyy-mm-dd hh:ii',
		'autoclose': True,
		'weekStart': 1,
		}
		widgets = {
			'datetime': DateTimeWidget(
				options = dateTimeOptions, 
				attrs={'id':"visit"}, 
				bootstrap_version=3, 
			)
		}

