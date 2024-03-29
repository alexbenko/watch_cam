import smtplib
import os
from dotenv import load_dotenv

carriers = {
	'att':    '@mms.att.net',
	'verizon':  '@vtext.com',
}
#all major carries typically assign you an email address that is <your number>@<carrierdomain>. sending an email to it will forward it to the number as a text
def send_sms(message):
	load_dotenv()
	number = os.getenv("PHONE_NUMBER")
	email = os.getenv("EMAIL")
	email_password = os.getenv("EMAIL_PASSWORD")
	carrier = os.getenv("CARRIER")
	if not number or not email or not email_password or not carrier:
		raise Exception("SMS environment variables not set...")

	to_number = number + '{}'.format(carriers[carrier])
	auth = (email, email_password)
	if ":" in message:
		message = message.replace(":", " ") #colons cause the message to fail ¯\_(ツ)_/¯
	# Establish a secure session with gmail's outgoing SMTP server using your gmail account
	server = smtplib.SMTP( "smtp.gmail.com", 587 )
	server.starttls()
	server.login(auth[0], auth[1])
	# Send text message through SMS gateway of destination number
	server.sendmail( auth[0], to_number, message)
