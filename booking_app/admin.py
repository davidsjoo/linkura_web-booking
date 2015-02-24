#coding: utf8 
import os
from django.contrib import admin
from booking_app.models import Customer, Visit, Time, Booking

class TimeInline(admin.TabularInline):
    model = Time


class VisitAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['customer', 'visit_name']}),
        ('Date information', {'fields': ['visit_date']})
    ]
    list_display = ('visit_name', 'customer', 'visit_date' )
    inlines = [TimeInline]

class BookingAdmin(admin.ModelAdmin):
    list_display = ('client_firstname', 'client_lastname', 'time' )
    


admin.site.register(Customer)
admin.site.register(Visit, VisitAdmin)
admin.site.register(Time)
admin.site.register(Booking, BookingAdmin)