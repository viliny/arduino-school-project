#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Full script

import sys, smtplib
from email.mime.text import MIMEText

def SendMail(receiver, message):
	from_address = 'administrator@pritek.fi'
	to_address = receiver
	text = message
	username = 'administrator@pritek.fi'
	password = 'plsgiefpsswd'
	msg = MIMEText(message)
	msg['From'] = from_address
	msg['To'] = to_address
	msg['Subject'] = 'Hälytys kosteusmittauksessa!'
	server = smtplib.SMTP('mail.mynebula.fi', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login(username, password)
	server.send_message(msg)
	server.quit()

if __name__ == "__main__":
	if(len(sys.argv) == 3):
		SendMail(sys.argv[1], sys.argv[2])
	else:
		print("./smtp.py [receiver] [message]")
