from django import forms

from booking_app.models import Booking


class BookingForm(forms.ModelForm):
	class Meta:
		model = Booking
		fields = ['client_firstname', 'client_lastname', 'client_phone', 'client_mail']
