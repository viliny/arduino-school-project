#!/usr/bin/env python3
import sys
import serial
import ParseStatus
import time


# port = '/dev/ttyUSB0'
# port = 'COM5'
# speed = 57600

def ReadStatus(port, speed, pathdb):
    try:
        ser = serial.Serial(port, speed, parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)
        print("Connecting to", port + " at speed:", str(speed) + "...")
    except:
      print("Could not connect ", port)
      sys.exit()

    if not ser.isOpen():
        print("Could not open serial")
        sys.exit()

    ser.flushInput()

    time.sleep(2)
    print("Sending epoch to master node: ", epoch)
    epoch = str(int(time.time()))
    ser.write(bytes(epoch,'UTF-8'))
    time.sleep(2)
    print ("Fetching data...")
    time.sleep(1)

    try:
        while True:
        	datain = ser.readline()
        	datain = datain.decode().replace('\n', '').replace('\r', '')
        	print("Received: ", datain)
        	if datain.startswith("ND") and not pathdb == "":
        	   ParseStatus.Parse(pathdb, datain)
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

    ReadStatus(sys.argv[1], sys.argv[2], dbpath)
