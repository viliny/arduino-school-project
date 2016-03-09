#!/usr/bin/env python3
import sys
import serial
import ParseStatus
# import time
# import signal
# from time import gmtime, strftime

# def signal_handler(signum, frame):
#     raise Exception("Timed out!")

# signal.signal(signal.SIGALRM, signal_handler)
# signal.alarm(20)

# port = '/dev/ttyUSB0'
# port = 'COM5'
# speed = 57600

def ReadStatus(port, speed, pathdb):
    # epoch = str(int(time.time()))
    # dataout = epoch

    try:
        ser = serial.Serial(port, speed)
        print("Connecting to", port + " at speed:", str(speed) + "...")

    except:
      print("Could not connect ", port)
      sys.exit()

    if not ser.isOpen():
        print("Could not open serial")
        sys.exit()

    while 1:
    	datain = ser.readline()
    	datain = datain.decode().replace('\n', '').replace('\r', '')
    	print(datain)
    	if not pathdb == "":
    	   ParseStatus.Parse(pathdb, datain)


if __name__ == "__main__":
    argc = len(sys.argv);
    if argc != 3 and argc != 4:
        print("Usage: ser.py <port> <baudrate> [pathtodb]")
        exit()

    dbpath = ""
    if len(sys.argv) == 4:
        dbpath = sys.argv[3]

    ReadStatus(sys.argv[1], sys.argv[2], dbpath)
