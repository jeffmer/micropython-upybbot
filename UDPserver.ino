/*

 Udp  Server =passes on OSC messages to serial link


 */

#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

char ssid[] = “ssid”;  //  your network SSID (name)
char pass[] = “password”;       // your network password


unsigned int localPort = 8000;      // local port to listen for UDP packets

const int PACKET_SIZE = 64; 

byte packetBuffer[PACKET_SIZE]; //buffer to hold incoming packets

// A UDP instance to let us send and receive packets over UDP
WiFiUDP udp;

void setup()
{
  Serial.begin(115200);
  Serial.println();
  Serial.println();

  // We start by connecting to a WiFi network
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, pass);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  Serial.println("Starting UDP");
  udp.begin(localPort);
  Serial.print("Local port: ");
  Serial.println(localPort);
  Serial.println("begin");
}

void loop()
{
  // is there a packet
  delay(10);
  int cb = udp.parsePacket();
  if (cb) {
    // We've received a packet, write to serial uart
    Serial.print("#");
    Serial.write(cb);
    udp.read(packetBuffer, PACKET_SIZE); // read the packet into the buffer
    Serial.write(packetBuffer,cb);
    Serial.write("\n");
  }
}


