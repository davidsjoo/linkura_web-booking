import email.MIMEText
import email.MIMEBase
from email.MIMEMultipart import MIMEMultipart
import smtplib
import datetime as dt
import icalendar
import pytz

def sendAppointment(self, subj, description):
	tz = pytz.timezone("Europe/Stockholm")
	reminderHours = 1
	startHour = 7
	start = tz.localize(dt.datetime.combine(self.date, dt.time(startHour, 0, 0)))
	cal = icalendar.Calendar()
	cal.add('prodid', '-//My calendar application//example.com//')
	cal.add('version', '2.0')
	cal.add('method', "REQUEST")
	event = icalendar.Event()
	event.add('attendee', self.getEmail())
	event.add('organizer', "me@example.com")
	event.add('status', "confirmed")
	event.add('category', "Event")
	event.add('summary', subj)
	event.add('description', description)
	event.add('location', "Room 101")
	event.add('dtstart', start)
	event.add('dtend', tz.localize(dt.datetime.combine(self.date, dt.time(startHour + 1, 0, 0))))
	event.add('dtstamp', tz.localize(dt.datetime.combine(self.date, dt.time(6, 0, 0))))
	event['uid'] = getUniqueId() # Generate some unique ID
	event.add('priority', 5)
	event.add('sequence', 1)
	event.add('created', tz.localize(dt.datetime.now()))

	alarm = icalendar.Alarm()
	alarm.add("action", "DISPLAY")
	alarm.add('description', "Reminder")
	#alarm.add("trigger", dt.timedela(hours=-reminderHours))
	# The only way to convince Outlook to do it correcty
	alarm.add("TRIGGER;RELATED=START", "-PT{0}H".format(reminderHours))
	event.add_component(alarm)
	cal.add_component(event)

	msg = MIMEMultipart("alternative")

	msg["subject"] = subj
	msg["From"] = "{0}@example.com".format(self.creator)
	msg["To"] = self.getEmail()
	msg["Content-class"] = "urn:content-classes:calendarmessage"

	msg.attach(email.MIMEText.MIMEText(description))

	filename = "invite.ics"
	part = email.MIMEBase.MIMEBase('text', "calendar", method="REQUEST", name=filename)
	part.set_payload( cal.to_ical() )
	email.Encoders.encode_base64(part)
	part.add_header('Conten-Description', filename)
	part.add_header("Content-class", "urn:content-classes:calendarmessage")
	part.add_header("Filename", filename)
	part.add_header("Path", filename)
	msg.attach(part)

	s = smtplib.SMTP('localhost')
	s.sendmail(msg["From"], [msg["To"]], msg.as_string())
	s.quit()


#If you don't want the appointment participant's Outlook to send
#you a reply when he or she accepts, you can use the following code:

#event.add("ATTENDEE;ROLE=REQ-PARTICIPANT;PARTSTAT=NEEDS-ACTION;RSVP=FALSE", email)
