#!/usr/bin/env python

import sys
import os.path
import sqlite3
import time

# Parameters; c = Database reference

#function returns amount of errors

def CheckDeviceValues(conn, devId):
	deviceId = 0
	humidity = 1
	temp = 2
	lidSwitchOpen = 3
	waterLevelLow = 4
	batterStatus = 5
	measureTime = 6

	ts = int(time.time())

	c = conn.cursor()
	c.execute('''SELECT deviceName FROM Device WHERE deviceId=?''', [devId])
	deviceName = c.fetchone()[0]
	c.execute('''SELECT * FROM Data WHERE deviceId=? ORDER BY measureTime DESC LIMIT 1''', [devId])
	deviceinfo = c.fetchall()

	c.execute('''SELECT * FROM Settings''')
	a = c.fetchone()

	#user settings
	email = a[0]
	humidityTrshld = a[3]
	tempTrshld = a[4]
	lidSwitchTrshldTime = a[5]

	errorCount=0
	type="Ok"
	for row in deviceinfo:
		type="Ok"
		msg="Status: "
		if row[humidity]<humidityTrshld:
			type="error"
			msg+="Tarkista kosteus. "
			errorCount += 1
		if row[humidity]<0 or row[humidity]>99:
			type="error"
			msg+="Kosteussensorivirhe. "
			errorCount += 1
		if row[temp]<tempTrshld:
			type="error"
			msg+="Tarkista lampotila. "
			errorCount += 1
		if row[lidSwitchOpen]:
			type="error"
			msg+="Kansi auki. "
			errorCount += 1
		if row[waterLevelLow]:
			type="error"
			msg+="Alhainen veden taso. "
			errorCount += 1

		# print msg+"\n"
		sender=devId
		mailSent=0
		if type=="error":
			conn.execute('''INSERT INTO Log (type, msg, deviceName, mailSent, timeStamp) VALUES (?, ?, ?, ?, ?)''', (type, msg, deviceName, mailSent, ts))


	c.execute('''SELECT error FROM Device WHERE deviceId=?''', [devId])
	errorflag = c.fetchone()[0];
	if type=="error":
		if errorflag == 0:
			c.execute('''UPDATE Device SET error=? WHERE deviceId=?''', [ts, devId])
	else:
		c.execute('''UPDATE Device SET error=0 WHERE deviceId=?''', [devId])
	conn.commit()

	return errorCount


if __name__ == "__main__":
	if len(sys.argv) == 3:
		conn = sqlite3.connect(sys.argv[1])
		print str(CheckDeviceValues(conn, sys.argv[2]))
		conn.close()
	else:
		print "Usage: ./alert.py [path-to-db] [device-id]"
