#!/usr/bin/env python3
import sys
import serial
import ParseStatus
import time
import Database
import subprocess


# port = '/dev/ttyUSB0'
# port = 'COM5'
# speed = 57600
def ResetSerial():
    print("Resetting serial port...")
    subprocess.call("./reset.sh", shell=True)
    time.sleep(1)
    print("Done")

def SendEpoch(serial):
    epoch = str(int(time.time()))
    print("Sending epoch to master node: ", epoch)
    serial.write(bytes(epoch,'UTF-8'))
    return int(epoch)

def ReadStatus(port, speed, pathdb):
#    ResetSerial()

    try:
        ser = serial.Serial(port, speed, timeout=60, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)
        print("Connecting to", port + " at speed:", str(speed) + "...")
    except:
      print("Could not connect ", port)
      sys.exit()

    if not ser.isOpen():
        print("Could not open serial")
        sys.exit()

    ser.flushInput()

    time.sleep(2)
    #   Send current time to nodes
    epochSentTime = SendEpoch(ser)
    time.sleep(2)
    print ("Fetching data...")
    time.sleep(1)

    try:
        while True:
            datain = ser.readline()
            datain = datain.decode().replace('\n', '').replace('\r', '') # remove line endings
            print("Received: ", datain)
            #   If database is given, try parsing
            if datain.startswith("ND") and not pathdb == "":
                ParseStatus.Parse(pathdb, datain)
            epoch = int(time.time())
            #   Update epoch every 30 mins
            if epoch-epochSentTime > 1800:
                epochSentTime = SendEpoch(ser)
    except KeyboardInterrupt:
        ser.close()
        print()
        print ("Closing serial")
        sys.exit()


if __name__ == "__main__":
    argc = len(sys.argv);
    if argc != 3 and argc != 4:
        print("Usage: ser.py <port> <baudrate> [pathtodb]")
        exit()

    dbpath = ""
    if len(sys.argv) == 4:
        dbpath = sys.argv[3]

    Database.InitDataBase(dbpath)
    ReadStatus(sys.argv[1], sys.argv[2], dbpath)
