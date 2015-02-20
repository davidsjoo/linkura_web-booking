from django.db import models
from django.forms import ModelForm


class Customer(models.Model):
	customer_name = models.CharField(max_length=50)
	def __str__(self):
		return self.customer_name

class Visit(models.Model):
	customer = models.ForeignKey(Customer)
	visit_name = models.CharField(max_length=50)
	visit_date = models.DateTimeField('Date')
	def __str__(self):
		return self.visit_name

class Time(models.Model):
	visit = models.ForeignKey(Visit)
	datetime = models.DateTimeField('Date and time')
	capacity = models.IntegerField(default=1)
	location = models.CharField(max_length=50)
	description = models.TextField()
	def __unicode__(self):
		return "%s" % self.datetime
	class Meta:
		ordering = ['datetime']
	def time_list3(self):
		return Time.objects.filter(datetime__week_day=2)[:1].get()

class Booking(models.Model):
	time = models.ForeignKey(Time)
	client_firstname = models.CharField(max_length=50)
	client_lastname = models.CharField(max_length=50)
	client_mail = models.EmailField(max_length=100)
	client_phone = models.CharField(max_length=50)
	def __str__(self):
		return self.client_firstname

