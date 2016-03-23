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

	totalErrors = 0
	log = ""
	sendEmail = False
	timeNow = time.time()

	#	fetch time of last sent email
	cur.execute("SELECT mailSent FROM Log ORDER BY mailSent DESC")
	timeEmailSent = cur.fetchone()[0]

## Iterate through all devices
	for device in devices:
		print "Device: {0}\tName: {2}\tUpdated: {1}\tErr:{3}".format(*device)
		#	Check latest values from db
		#if Alert.CheckDeviceValues(device[0], conn) > 0:
		if True:
			# If time from the last email is >1h and device error has been >1h
			if timeEmailSent+3600 < timeNow and device[3]+3600 < timeNow:
				log += "Log records for the device \'{0}\':\n".format(device[2])
				log += ReadLog.GetLogOfDevice(conn, device[2], 10) + "\n"
				ReadLog.MarkSent(conn, device[2]);
				totalErrors += 1
				sendEmail = True # An email will be sent

##	Check if any errors occured and send an email
	if sendEmail:
		#	Generate message
		message = "{0} device(s) has issues!\n".format(totalErrors)
		message += log;
		#	Send an email to the address defined in settings table
		print "Send email:"
		print message
	conn.close()
########## END of main

if __name__ == "__main__":
	if len(sys.argv) == 2:
		main(sys.argv[1])
	else:
		print "Usage: ./Main.py [path-to-db]"
