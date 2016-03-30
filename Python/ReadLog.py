#!/usr/bin/env python

#	Reads all unsent messages from Log table and marks them sent.
#	Returns a string made from all unsent log records.

# SELECT * FROM Log WHERE mailSent=0;
# UPDATE Log SET mailSent=1 WHERE mailSent=0;

import sys
import time
import sqlite3

#	returns log for the given device
def GetLogOfDevice(conn, deviceName, limit):
	cur = conn.cursor()

	cur.execute("SELECT * FROM Log WHERE mailSent=0 AND deviceName=? ORDER BY timeStamp desc LIMIT ?", [deviceName, limit])
	dblines = cur.fetchall();

	log = ""
	timeformat = "%B %d %H:%M:%S"
	for row in dblines:
		timestr = time.strftime(timeformat, time.localtime(row[4]))
		log += "{0}: {1}: {2}\t{3}\n".format(timestr, row[0], row[2], row[1])

	return log

#	Set mailsent to current time for a specific device
def MarkSent(conn, deviceName):
	cur = conn.cursor()
	cur.execute("UPDATE Log SET mailSent=? WHERE mailSent=0 AND deviceName=?", [int(time.time()), deviceName])
	conn.commit()


if __name__ == "__main__":
	if len(sys.argv) == 3:
		conn = sqlite3.connect(sys.argv[1])
		print(str(GetLogOfDevice(conn, sys.argv[2], 10)))
		conn.close()
	else:
		print("Usage: ./ReadLog.py [path-to-db] [device-name]")
