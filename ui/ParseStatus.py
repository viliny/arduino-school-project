#!/usr/bin/env python
import sys
import os.path
import sqlite3

pathDB = "monitor.db"

class DataRecord:
    def __init__(self):
        self.types = {"deviceId" : str, "humidity" : "numeral", "temp" : "numeral", "lidSwitchOpen" : "bool", "waterLevelLow" : "bool", "batteryStatus" : str, "measureTime" : "numeral"}
        self.data = {};
    def ValidateData(self):
        for key, val in self.types.iteritems():
            #   If required variable not set
            if not key in self.data:
                print key + " not given"
                return False

            #  Try converting str to correct type
            try:
                if val is "numeral":
                    self.data[key] = float(self.data[key])
                elif val is "bool":
                    self.data[key] = int(self.data[key])
                    if self.data[key] is not 1 and self.data[key] is not 0:
                        return False
                elif type(self.data[key]) is not val:
                    return False
            except ValueError:
                print "Value error: " + key
                return False
        return True
    def InsertDB(self, conn):
        tupl = (self.data['deviceId'], self.data['humidity'], self.data['temp'], self.data['lidSwitchOpen'], self.data['waterLevelLow'], self.data['batteryStatus'], self.data['measureTime'])
        conn.execute("INSERT INTO Data VALUES (?, ?, ?, ?, ?, ?, ?)", tupl);

# if db not found make a new one
doInit = not os.path.isfile(pathDB)
print "Connecting to database: " + pathDB
conn = sqlite3.connect(pathDB)
if doInit:
    print "No " + pathDB + " found, creating a new db."
    conn.execute('''CREATE TABLE Device(deviceId text, lastUpdate integer, deviceName text, error integer)''')
    conn.execute('''CREATE TABLE Data(deviceId text, humidity real, temp real, lidSwitchOpen integer, waterLevelLow integer, batteryStatus text, measureTime integer)''')
    conn.execute('''CREATE TABLE User(email text, name text, lang text)''')
    conn.commit()

print sys.argv[1]
in_data = sys.argv[1]
# in_data = raw_input()
# in_data = "humidity=12.3;deviceId=ass;lidSwitchOpen=1;temp=45;waterLevelLow=0;batteryStatus=OK;measureTime=23;"

record = DataRecord()
#   Split given string
for statement in in_data.split(";"):
    statement = statement.split('=')
    #   Jump to next statement if current contains errors
    if len(statement) != 2:
        continue
    if len(statement[0]) == 0 or len(statement[1]) == 0:
        print "Key or value was null."
        continue
    #   Add valid statement to record
    record.data[statement[0]] = statement[1]

#   Make sure data is in correct type and put it into database
if record.ValidateData():
    record.InsertDB(conn)
    conn.commit() # Apply changes to database
else:
    print "Check input."

conn.close()
print "Connection to " + pathDB + " closed."
