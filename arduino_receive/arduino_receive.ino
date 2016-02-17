#include <RF24Network.h>
#include <RF24.h>
#include <SPI.h>


RF24 radio(7,8);                // nRF24L01(+) radio attached using Getting Started board 

RF24Network network(radio);      // Network uses that radio
const uint16_t this_node = 00;    // Address of our node in Octal format ( 04,031, etc)
//const uint16_t other_node = 02;   // Address of the other node in Octal format
const uint16_t other_nodes[5] = {01, 02, 03, 04, 05};

const unsigned long interval = 10000; //ms  // How often to send
unsigned long last_sent;             // When did we last send?

struct payload_t {                 // Structure of our payload
  unsigned int h;
  unsigned int t;
  unsigned int n;
};

struct payload_p {                  // Structure of our payload
  unsigned int ac;
  unsigned long aac;
};



unsigned long serialdata;
int inbyte;

bool NetworkNeedsEpoch = 0;
unsigned long ReceivedEpoch = 0;

void setup(void)
{
  Serial.begin(57600);
  Serial.println("Receiver");
 
  SPI.begin();
  radio.setPALevel(RF24_PA_HIGH);
  radio.setDataRate(RF24_250KBPS);
  radio.setCRCLength(RF24_CRC_8);
  radio.begin();
  network.begin(/*channel*/ 90, /*node address*/ this_node);

  
}


void loop(void){
  network.update();                  // Check the network regularly

   unsigned long now = millis(); // If it's time to send a message, send it!
   
    if ( now - last_sent >= interval  )
     {
        last_sent = now;
        for (int node = 0; node < 4; node++) {
        sendReq(other_nodes[node]);
      }   
    }

  while ( network.available() ) {     // Is there anything ready for us?
    
    RF24NetworkHeader header;        // If so, grab it and print it out
    payload_t payload;
    network.read(header,&payload,sizeof(payload));
    Serial.print("ND;");
    int sNode = payload.n;
    Serial.print(sNode);
    Serial.print(";");
    Serial.print("HU;");
    float h0 = payload.h / 100.00;
    Serial.print(h0);
    Serial.print(";");
    Serial.print("TP;");
    float t0 = payload.t / 100.00;
    Serial.println(t0);
  }
  
  
    if (Serial.available() > 0)
    {
      unsigned long DATA = getSerial();
      Serial.println(DATA);
    }
    
  

  if (NetworkNeedsEpoch == 1)
  {
    NetworkNeedsEpoch = 0;
    for (int node = 0; node < 4; node++) {
    sendEpo(other_nodes[node], ReceivedEpoch);
  }
  }
}

long getSerial()
{
  unsigned long start = millis(); 
  serialdata = 0;
  while (inbyte != ';' && (millis() - start) < 3000)
  {
    inbyte = Serial.read(); 
    if (inbyte > 0 && inbyte != ';')
    {
      serialdata = serialdata * 10 + inbyte - '0';
    }
  }
  inbyte = 0;
  return serialdata;
}

void sendReq(uint16_t other_node)
{
    int action = 99;
    int additional_action = 00;
    
    Serial.print("RQ;");
    Serial.print(other_node);
    Serial.print(";");
    payload_p payload = { action, additional_action};
    RF24NetworkHeader header(/*to node*/ other_node);
    bool ok = network.write(header,&payload,sizeof(payload));
    if (ok) {
      Serial.println("TX;1");     
    }
    else
      Serial.println("TX;0");
  
}


void sendEpo(uint16_t other_node, long epoch)
{
    int action = 50;
    int additional_action = epoch;
    
    Serial.print("EP;");
    Serial.print(other_node);
    Serial.print(";");
    payload_p payload = { action, additional_action};
    RF24NetworkHeader header(/*to node*/ other_node);
    bool ok = network.write(header,&payload,sizeof(payload));
    if (ok) {
      Serial.println("TX;1");     
    }
    else
      Serial.println("TX;0");
  
}



