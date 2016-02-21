#include <SD.h>
#include <Wire.h>
#define SDCS 10


String indata;

void writeSD(String data)
{
  File dataFile = SD.open("datalog.txt", FILE_WRITE);
  if (dataFile) {
    dataFile.println(data);
    dataFile.close();
    // print to the serial port too:
    Serial.println("Data written to sd");
  }
  // if the file isn't open, pop up an error:
  else {
    Serial.println("error opening datalog.txt");
  }

}

void setup() {

  Wire.begin(2);                // join i2c bus with address #8
  Wire.onReceive(receiveEvent); // register event
  Serial.begin(57600);
  
  // put your setup code here, to run once:
// see if the card is present and can be initialized:
  if (!SD.begin(SDCS)) {
    Serial.println("Card failed, or not present");
    // don't do anything more:
    return;
  }
  Serial.println("card initialized.");
  writeSD("Booted");
}




void loop() {
  // put your main code here, to run repeatedly:
delay(100);
}

void receiveEvent(int howMany) {
  while (Wire.available() > 0) { // loop 
    char c = Wire.read(); // receive byte as a character
             // print the character
    indata = indata + c;
  }
  
  Serial.println(indata);         // print the integer
  writeSD(indata);
  indata = "";
}




