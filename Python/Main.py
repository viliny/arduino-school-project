#!/usr/bin/env python

'''
Modules:
# Device sensor readings to database:
	ser.py	- Gets status string from boxes
	ParseStatus.py	- Parses string fetched and inserts it into the Data table if it is in valid form

# Check database:
	Alarm.py	- Checks values of a device from the database and logs if errors
	ReadLog.py	- Takes new log records and creates a short summary
'''
import sqlite3
import sys
import os
import time

import Database
#import Alert
import ReadLog
##########	MAIN	##
def main(pathDB):
	countError = 0

	#	Make sure that database exists
	Database.InitDataBase(pathDB)

## Open db and read all devices from table Device
	conn = sqlite3.connect(pathDB)
	cur = conn.cursor()
	cur.execute("SELECT * FROM Device ORDER BY deviceId")
	devices = cur.fetchall()

	# if Device table is empty quit
	if len(devices) == 0:
		print "Devices table is empty!"
		return 0

	print str(len(devices)) + " devices found."

## Iterate through all devices
	totalErrors = 0
	log = ""
	sendEmail = False
	for device in devices:
		print "Device: {0}\tName: {2}\tUpdated: {1}\tErr:{3}".format(*device)
		#if Alert.CheckDeviceValues(device[0], conn) > 0:  # AND EMAIL HAVEN'T BEEN SENT IN PAST HOUR
		if True:
			log += "Log records for device \'{0}\':\n".format(device[2])
			log += ReadLog.GetLogOfDevice(conn, device[2], 10) + "\n"
			totalErrors += 1
		#	If there has been an issue with this device more than an hour -> send an email
			if device[3]+3600 < time.time():
				sendEmail = True

##	Check if any errors occured and send email
	if totalErrors > 0 and sendEmail:
		#	Generate message
		message = "{0} device(s) has issues!\n".format(totalErrors)
		message += log;
		#	Send email to address defined in settings table
		print "Send email:"
		print message
	conn.close()
########## END of main

if __name__ == "__main__":
	if len(sys.argv) == 2:
		main(sys.argv[1])
	else:
		print "Usage: ./Main.py [path-to-db]"
