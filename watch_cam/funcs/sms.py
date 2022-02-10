import smtplib
import os
from dotenv import load_dotenv

carriers = {
	'att':    '@mms.att.net',
	'tmobile':' @tmomail.net',
	'verizon':  '@vtext.com',
}
#all major carries typically assign you an email address that is <your number>@<carrierdomain>. sending an email to it will forward it to the number as a text
def send(message):
	load_dotenv()
	number = os.getenv("PHONE_NUMBER")

	to_number = number + '{}'.format(carriers['att'])
	auth = (os.getenv("EMAIL"), os.getenv("EMAIL_PASSWORD"))

	# Establish a secure session with gmail's outgoing SMTP server using your gmail account
	server = smtplib.SMTP( "smtp.gmail.com", 587 )
	server.starttls()
	server.login(auth[0], auth[1])

	# Send text message through SMS gateway of destination number
	server.sendmail( auth[0], to_number, message)
