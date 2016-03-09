#include <RF24Network.h>
#include <RF24.h>
#include <SPI.h>


RF24 radio(7,8);                // nRF24L01(+) radio attached using Getting Started board 

RF24Network network(radio);      // Network uses that radio
const uint16_t this_node = 00;    // Address of our node in Octal format ( 04,031, etc)
//const uint16_t other_node = 02;   // Address of the other node in Octal format
const uint16_t other_nodes[5] = {01, 02, 03, 04, 05};

const unsigned long interval = 8000; //ms  // How often to send
unsigned long last_sent;             // When did we last send?
unsigned long last_sync;

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


int RoundAbout = 0;

unsigned long serialdata;

int inbyte;

bool NetworkNeedsEpoch = 0;
unsigned long ReceivedEpoch = 0;



void smartDelay(long milliseconds)
{
  unsigned long sDelay = 0;
  sDelay = millis();
    while ((millis() - sDelay) < milliseconds)
    {}
}

void setup(void)
{
  Serial.begin(57600);
  Serial.println("Receiver");
 
  SPI.begin();
  radio.setPALevel(RF24_PA_LOW);
  radio.setDataRate(RF24_2MBPS);
  radio.setCRCLength(RF24_CRC_16);
  radio.enableDynamicPayloads();
  radio.setRetries (500, 3);
  radio.setAutoAck(true);
  radio.begin();
  network.begin(/*channel*/ 108, /*node address*/ this_node);

  
}


void loop(void){
  
   // Check the network regularly

   unsigned long now = millis(); // If it's time to send a message, send it!
   
    if ( now - last_sent >= interval  )
     {
        last_sent = now;
        
        sendReq(other_nodes[RoundAbout]);

        if (RoundAbout < 4)
        {
          RoundAbout++;
        }
        else 
        {
          RoundAbout = 0;
        }
      
    }

    smartDelay(1000);

    network.update();
    int sNode;
    float h0;
    float t0;
    long e0;
    int l0;
    int w0;
    int b0;
    int bl0;
  while ( network.available() ) {     // Is there anything ready for us?

    RF24NetworkHeader header;        // If so, grab it and print it out
    payload_t payload;
    network.read(header,&payload,sizeof(payload));
    
    sNode = payload.n;
    
    h0 = payload.h / 100.00;
    
    t0 = payload.t / 100.00;

    e0 = payload.e;

    l0 = payload.l;

    w0 = payload.w;

    b0 = payload.b;

    bl0 = payload.bl;

    Serial.print("ND;");
    Serial.print(sNode);
    Serial.print(";");
    Serial.print("HU;");
    Serial.print(h0);
    Serial.print(";");
    Serial.print("TP;");
    Serial.print(t0);
    Serial.print(";");
    Serial.print("EP;");
    Serial.print(e0);
    Serial.print(";");
    Serial.print("LS;");
    Serial.print(l0);
    Serial.print(";");
    Serial.print("WL;");
    Serial.print(w0);
    Serial.print(";");
    Serial.print("BC;");
    Serial.print(b0);
    Serial.print(";");
    Serial.print("BL;");
    Serial.println(bl0);

    
    
  }
  

    
    if (Serial.available() > 0)
    {
      unsigned long DATA = getSerial();
      ReceivedEpoch = DATA;
      NetworkNeedsEpoch = 1;
    }
    
  

  if (NetworkNeedsEpoch == 1)
  {
    NetworkNeedsEpoch = 0;
    for (int node = 0; node < 5; node++) {
    sendEpo(other_nodes[node], ReceivedEpoch);
    smartDelay(1000);
  }
  
  }
  
}

long getSerial()
{
  unsigned long start = millis(); 
  serialdata = 0;
  while (inbyte != '&' && (millis() - start) < 3000)
  {
    inbyte = Serial.read(); 
    if (inbyte > 0 && inbyte != '&')
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
    int additional_action = 99;
    
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
    long additional_action = epoch;
    
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
    {
      Serial.println("TX;0");
    }
  
}



