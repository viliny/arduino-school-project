#!/usr/bin/env python3
import sys
import os.path
import sqlite3

class DataRecord:
    def __init__(self):
        self.aliases = {"ND" : "deviceId", "HU" : "humidity", "TP" : "temp", "LS" : "lidSwitchOpen", "WL" : "waterLevelLow", "BC" : "batteryStatus", "EP" : "measureTime"}
        self.types = {"deviceId" : str, "humidity" : "numeral", "temp" : "numeral", "lidSwitchOpen" : "bool", "waterLevelLow" : "bool", "batteryStatus" : str, "measureTime" : "numeral"}
        self.data = {};
    def ValidateData(self):
        for key, alias in self.aliases.items():
            if not key in self.data:
                print(key + " not given")
                return False

            dbtype = self.types[alias]
            self.data[alias] = self.data[key]

            #   Correct type
            try:
                if dbtype == "numeral":
                    self.data[alias] = float(self.data[alias])
                elif dbtype == "bool":
                    self.data[alias] = int(self.data[alias])
                    if self.data[alias] is not 1 and self.data[alias] is not 0:
                        return False
                elif type(self.data[key]) is not dbtype:
                    return False
            except ValueError:
                print("Value error: " + key)
                return False

            print(key, " ", alias, " ", dbtype, " ", self.data[alias])
        return True
    def InsertDB(self, conn):
        tupl = (self.data['deviceId'], self.data['humidity'], self.data['temp'], self.data['lidSwitchOpen'], self.data['waterLevelLow'], self.data['batteryStatus'], self.data['measureTime'])
        conn.execute("INSERT INTO Data VALUES (?, ?, ?, ?, ?, ?, ?)", tupl);

def Parse(pathDB, status):
    # if db not found make return
    if not os.path.isfile(pathDB):
        print("No database: '{0}' found".format(pathDB))
        return

    # status = ND;1;HU;94.60;TP;23.80;EP;2043;LS;0;WL;0;BC;87;BL;0

    record = DataRecord()
    key = ""
    val = ""
    #   Split given string
    for part in status.split(";"):
        if key != "":
            val = part
        else:
            key = part

        if val != "":
            print(key, " = ", val)
            #   Add key and value to list
            record.data[key] = val
            val = ""
            key = ""

    #   Make sure data is in correct type and put it into database
    if record.ValidateData():
        print("Connecting to database: " + pathDB)
        conn = sqlite3.connect(pathDB)
        record.InsertDB(conn)
        conn.commit() # Apply changes to database
        conn.close()
        print("Connection to " + pathDB + " closed.")
        return True
    else:
        print("Check input.")
        return False

if __name__ == "__main__":
    if len(sys.argv) == 2:
        Parse("./monitor.db", sys.argv[1])
    else:
        print("Error: Check arguments")
