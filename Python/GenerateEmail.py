#!/usr/bin/env python

#	Reads all unsent messages from Log table and marks them sent.
#	Returns a string made from all unsent log records.

# SELECT * FROM Log WHERE mailSent=0;
# UPDATE Log SET mailSent=1 WHERE mailSent=0;

import time
import sqlite3

def GenerateEmail(pathDB):
	conn = sqlite3.connect(pathDB)
	cur = conn.cursor()

	cur.execute("SELECT * FROM Log WHERE mailSent=0")
	dblines = cur.fetchall();

	log = ""
	timeformat = "%B %d %H:%M:%S"
	for row in dblines:
		timestr = time.strftime(timeformat, time.localtime(row[4]))
		log += "{0}: {1}: {2}\t{3}\n".format(timestr, row[0], row[2], row[1])

	cur.execute("UPDATE Log SET mailSent=1 WHERE mailSent=0")
	conn.commit()
	conn.close()

	return log

if __name__ == "__main__":
    print GenerateEmail("monitor.db")
