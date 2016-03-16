#!/usr/bin/env python

import sys, os, sqlite3

#	Check if database exists if it doesn't create a new one
def InitDataBase(name):
	doInit = not os.path.isfile(name)
	conn = sqlite3.connect(name)
	if doInit:
		print "No " + name + " found, creating new."
		conn.execute('''CREATE TABLE Device(deviceId text, lastUpdate integer, deviceName text, error integer)''')
		conn.execute('''CREATE TABLE Data(deviceId text, humidity real, temp real, lidSwitchOpen integer, waterLevelLow integer, batteryStatus text, chargingStatus integer, measureTime integer)''')
		conn.execute('''CREATE TABLE Settings(email text, name text, lang text, humidityTrshld integer, tempTrshld integer, lidSwitchTrshldTime integer)''')
		conn.execute('''CREATE TABLE Log(type text, msg text, sender text, mailSent integer, timeStamp integer)''')
		conn.commit()
	conn.close()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        InitDataBase(sys.argv[1])
        sys.exit(0)
    print "Usage: ./Database.py [pathtodb]"
    sys.exit(1)
