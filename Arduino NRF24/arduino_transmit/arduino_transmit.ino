
#include <RF24Network.h>
#include <RF24.h>
#include <SPI.h>
#include <DHT.h>
#include <Wire.h>


#define DHTPIN 4 

#define DHTTYPE DHT22

#define lidPin A1

DHT dht(DHTPIN, DHTTYPE);

RF24 radio(7,8);                    // nRF24L01(+) radio attached using Getting Started board 

RF24Network network(radio);          // Network uses that radio

const uint16_t this_node = 01;        // Address of our node in Octal format
const uint16_t other_node = 00;       // Address of the other node in Octal format

//const unsigned long interval = 10000; //ms  // How often to send 'hello world to the other unit

unsigned long last_sent;             // When did we last send?
unsigned long packets_sent;          // How many have we sent already

unsigned long myCurrentEpoch;
unsigned long loopStartMillis;
unsigned long loopEndMillis;

struct payload_t {                 // Structure of our payload
  //Humidity
  unsigned int h;
  //Temperature
  unsigned int t;
  //Node id
  unsigned int n;
  //Epoch
  unsigned long e;
  // Lid status
  unsigned int l;
  //Water level
  unsigned int w;
  //Charging status
  unsigned int b;
  //Charge level
  unsigned int bl;
};

struct payload_p {                  // Structure of our payload
  unsigned int ac;
  unsigned long aac;
};

const int voltPin = 0;

const int ledPin = 2;


void setup(void)
{
  
  Serial.begin(57600);
  Wire.begin(); // join i2c bus (address optional for master)
  Serial.println("Transmitter");

  pinMode(ledPin, OUTPUT);
   
  digitalWrite(ledPin, HIGH);
  
  SPI.begin();
  radio.setPALevel(RF24_PA_LOW);
  radio.setDataRate(RF24_2MBPS);
  radio.setCRCLength(RF24_CRC_16);
  radio.enableDynamicPayloads();
  radio.setRetries (500, 3);
  radio.setAutoAck(true);
  
  radio.begin();
  network.begin(/*channel*/ 108, /*node address*/ this_node);
  dht.begin();

  
}

void smartDelay(long milliseconds)
{
  unsigned long sDelay = 0;
  sDelay = millis();
    while ((millis() - sDelay) < milliseconds)
    {}
}



void loop() {
  loopStartMillis = millis();

  int lStatus = analogRead(lidPin);

  if (lStatus > 1000)
  {
    digitalWrite(ledPin, LOW);
    Serial.println("Lid open!");
  }
  else
  {
    digitalWrite(ledPin, HIGH);
  }
  
  network.update();                          // Check the network regularly

  while ( network.available() ) {     // Is there anything ready for us?
    
    RF24NetworkHeader header;        // If so, grab it and print it out
    payload_p payload;
    network.read(header,&payload,sizeof(payload));

    Serial.println("Received packet");
    
    if ((int)payload.ac == 99)
    {
      Serial.println("Payload indicated request for temperature to base node");
      unsigned long now = millis();
      last_sent = now;
      sendTemp();
      
    }
    else if ((int)payload.ac == 50)
    {
      Serial.println("Payload contains epoch time syncronization data");
      myCurrentEpoch = (long)payload.aac;
      Serial.println((long)payload.aac);
      Serial.print("My new epoch time is: ");
      Serial.println((long)myCurrentEpoch);
    }
  }

  smartDelay(1500);
  myCurrentEpoch += ((millis() - loopStartMillis) / 1000);

}

void sendTemp()
{
    smartDelay(2000);
    
    float h0 = dht.readHumidity() * 100;
    float t0 = dht.readTemperature() * 100;
    
    int h = (int) h0;
    Serial.println(h0);
    int t = (int) t0;
    Serial.println(t0);
    int n = (int)this_node;
    

    float voltage;
  //Obtain RAW voltage data
  voltage = analogRead(voltPin);
  //Convert to actual voltage (0 - 5 Vdc)
  voltage = (voltage / 1024) * 5.0;
  //Convert to voltage before divider
  //  Divide by divider = multiply
  //  Divide by 1/5 = multiply by 5
  Serial.print("Voltage: ");
  Serial.println(voltage);  //Output to serial
  voltage = (voltage / 4.2) * 100; 
  Serial.print("Voltage %: ");
  Serial.println(voltage);

  int lidState = digitalRead(lidPin);

    Serial.print("lid: ");
  Serial.println(lidState);
    
    Serial.print("Sending...");
    payload_t payload = { h, t, n, myCurrentEpoch, lidState, 0, voltage };
    RF24NetworkHeader header(/*to node*/ other_node);
    bool ok = network.write(header,&payload,sizeof(payload));
    if (ok) {
      Serial.println("ok.");
      Serial.print("My epoch time is currently: ");
      Serial.println(myCurrentEpoch);
    }
    else
    {
      Serial.println("failed.");
      //writeSD(String(h)+";"+String(t)+";"+String(n)+";"+(String)myCurrentEpoch);
    }

    Wire.beginTransmission(2); // transmit to device #8
      String MessageToSend = String(n)+";"+String(h)+";"+String(t)+";"+(String)myCurrentEpoch+";"+String(0)+";"+String(0)+";"+String(87);
      Wire.write(MessageToSend.c_str());        
      Wire.endTransmission();    // stop transmitting
}








