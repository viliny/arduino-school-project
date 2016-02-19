#!/usr/bin/env python
import os.path
import sqlite3

pathDB = "monitor.db"


doInit = not os.path.isfile(pathDB)
print "Connecting to database: " + pathDB
conn = sqlite3.connect(pathDB)
if doInit:
    print "No " + pathDB + " found, creating new."
    conn.execute('''CREATE TABLE Device(deviceId text, lastUpdate integer, deviceName text, error integer)''')
    conn.execute('''CREATE TABLE Data(deviceId text, humidity real, temp real, lidSwitchOpen integer, waterLevelLow integer, batteryStatus text, measureTime integer)''')
    conn.execute('''CREATE TABLE User(email text, name text, lang text)''')
    conn.commit()

for row in conn.execute('''SELECT * FROM Data'''):
    print row

conn.close()
print "Connection to " + pathDB + " closed."
