#include <Arduino.h>

#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>

#include <SPI.h>
#include <MFRC522.h>

#define SSID "tbc_iot"
#define PASSWORD "wifi_password"
#define SERVER_IP "http://192.168.1.1:8000"

#define SS_PIN D10
#define RST_PIN D9
#define BUZZER D8

ESP8266WiFiMulti WiFiMulti;
 
MFRC522 mfrc522(SS_PIN, RST_PIN);   // MFRC522 instance.
 
void setup() 
{
  Serial.begin(9600);   // Begin serial communication with computer
  SPI.begin();          // Begin SPI bus

  // Intiate Wifi
  for (uint8_t t = 4; t > 0; t--) {
    Serial.printf("[SETUP] WAIT %d...\n", t);
    Serial.flush();
    delay(1000);
  }

  WiFi.mode(WIFI_STA);
  WiFiMulti.addAP(SSID, PASSWORD);

  // Intiate RFID Reader
  mfrc522.PCD_Init();
  Serial.println("Initializing RFID Reader...");
  Serial.println();

  // Set buzzer
  pinMode(BUZZER, OUTPUT);

  // Notify User that the System is Ready to be used
  tone(BUZZER, 600);
  delay(500);
  tone(BUZZER, 500);
  delay(500);
  tone(BUZZER, 400);
  delay(500);
  tone(BUZZER, 500);
  delay(500);
  noTone(BUZZER);
}

void get(String url)
{
    WiFiClient client;

    HTTPClient http;

    Serial.print("[HTTP] begin...\n");
    if (http.begin(client, url)) {

      // start connection
      int httpCode = http.GET();

      // httpCode will be negative on error
      if (httpCode > 0) {
        // HTTP header has been send and Server response header has been handled
        Serial.printf("[HTTP] code: %d\n", httpCode);

        // file found at server
        if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY) {
          String payload = http.getString();
          Serial.println(payload);
        }
      } else {
        Serial.printf("[HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
      }

      http.end();
    } else {
      Serial.printf("[HTTP} Unable to connect\n");
    }
}

void loop() 
{
  // wait for WiFi connection
  if ((WiFiMulti.run() == WL_CONNECTED)) {
    // Look for new cards
    if ( ! mfrc522.PICC_IsNewCardPresent()) 
    {
      return;
    }
    
    // Select one of the cards
    if ( ! mfrc522.PICC_ReadCardSerial()) 
    {
      return;
    }
  
    String content= "";
    byte letter;
    
    for (byte i = 0; i < mfrc522.uid.size; i++) 
    {
       content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : ""));
       content.concat(String(mfrc522.uid.uidByte[i], HEX));
    }
    Serial.println();
    content.toUpperCase();
    if(content.substring(1)){
      // Handle RFID
      Serial.println(content.substring(1));
      
      // Send 1KHz sound signal...
      tone(BUZZER, 1000);
      delay(500);
      noTone(BUZZER);

      // Send RFID to Server
      get(String(SERVER_IP) + "/v1/arduino/scan?rfid=" + content.substring(1));
    }
  }
} 