/*
 Copyright (C) 2012 James Coliz, Jr. <maniacbug@ymail.com>

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License
 version 2 as published by the Free Software Foundation.
 
 Update 2014 - TMRh20
 */

/**
 * Simplest possible example of using RF24Network 
 *
 * TRANSMITTER NODE
 * Every 2 seconds, send a payload to the receiver node.
 */

#include <RF24Network.h>
#include <RF24.h>
#include <SPI.h>
#include <DHT.h>;

#define DHTPIN 4 

#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

RF24 radio(7,8);                    // nRF24L01(+) radio attached using Getting Started board 

RF24Network network(radio);          // Network uses that radio

const uint16_t this_node = 03;        // Address of our node in Octal format
const uint16_t other_node = 00;       // Address of the other node in Octal format

//const unsigned long interval = 10000; //ms  // How often to send 'hello world to the other unit

unsigned long last_sent;             // When did we last send?
unsigned long packets_sent;          // How many have we sent already

unsigned long myCurrentEpoch;
unsigned long loopStartMillis;
unsigned long loopEndMillis;

struct payload_t {                  // Structure of our payload
  unsigned int t;
  unsigned int h;
  unsigned int n;
};

struct payload_p {                  // Structure of our payload
  unsigned int ac;
  unsigned long aac;
};

void setup(void)
{
  Serial.begin(57600);
  Serial.println("Transmitter");
 
  SPI.begin();
  radio.setPALevel(RF24_PA_HIGH);
  radio.setDataRate(RF24_250KBPS);
  radio.setCRCLength(RF24_CRC_8);
  radio.begin();
  network.begin(/*channel*/ 90, /*node address*/ this_node);
  dht.begin();
}

void loop() {
  loopStartMillis = millis();
  
  network.update();                          // Check the network regularly

  while ( network.available() ) {     // Is there anything ready for us?
    
    RF24NetworkHeader header;        // If so, grab it and print it out
    payload_p payload;
    network.read(header,&payload,sizeof(payload));

    Serial.println("Received packet");
    
    if ((int)payload.ac == 99)
    {
      Serial.println("Payload indicated request for temperature to base node");
      delay(2000);
      unsigned long now = millis();
      last_sent = now;
      sendTemp();
      
    }
    else if ((int)payload.ac == 50)
    {
      Serial.println("Payload contains epoch time syncronization data");
      delay(2000);
      myCurrentEpoch = (long)payload.aac;
      Serial.println((long)payload.aac);
      Serial.print("My new epoch time is: ");
      Serial.println((long)myCurrentEpoch);
    }
  }

  loopEndMillis = millis();

  myCurrentEpoch += (loopEndMillis - loopStartMillis);
}

void sendTemp()
{
  
    float h0 = dht.readHumidity() * 100;
    float t0 = dht.readTemperature() * 100;
    delay(2000);
    int h = (int) h0;
    int t = (int) t0;
    int n = (int)this_node;
    


   
    
    Serial.print("Sending...");
    payload_t payload = { h, t, n };
    RF24NetworkHeader header(/*to node*/ other_node);
    bool ok = network.write(header,&payload,sizeof(payload));
    if (ok) {
      Serial.println("ok.");
      
    }
    else
      Serial.println("failed.");
  
}



