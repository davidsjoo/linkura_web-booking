#coding: utf8 
import os
from django.db import models
from django.forms import ModelForm
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from autoslug import AutoSlugField

class Customer(models.Model):
	customer_name = models.CharField(max_length=50)
	created_date = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return self.customer_name

class Visit(models.Model):
	customer = models.ForeignKey(Customer)
	visit_name = models.CharField(max_length=50)
	visit_date = models.DateField('Date')
	slug = AutoSlugField(populate_from='customer')
	def __unicode__(self):
		return self.visit_name


class Time(models.Model):
	visit = models.ForeignKey(Visit)
	datetime = models.DateTimeField('Date and time')
	capacity = models.IntegerField(default=1)
	location = models.CharField(max_length=50)
	def __unicode__(self):
		return "%s" % self.datetime
	class Meta:
		ordering = ['datetime']
	def is_capacity_filled(self):
		return self.booking_set.all().count() >= self.capacity

class Booking(models.Model):
	CLIENT_REMINDER_CHOICES = (
		('ten_m', '10 minuter'),
		('thirty_m', '30 minuter'),
        ('one_h', '1 timme'),
        ('two_h', '2 timmar'),
        ('one_d', '1 dag'),
        ('two_d', '2 dagar'),
        ('one_w', '1 vecka'),
        )
	time = models.ForeignKey(Time)
	client_firstname = models.CharField(max_length=50)
	client_lastname = models.CharField(max_length=50)
	client_mail = models.EmailField(max_length=100, blank=True)
	client_phone = models.CharField(max_length=50, blank=True)
	client_reminder = models.DateTimeField(null=True, choices=CLIENT_REMINDER_CHOICES)
	def __unicode__(self):
		return self.client_firstname

