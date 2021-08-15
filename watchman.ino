#include "AsyncStream.h"
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>
#include <WiFiUdp.h>
#include <NTPClient.h>

const char *ssid = "ASUS";
const char *password = "1234567890";
const char *serverName = "http://192.168.1.24:5000/";
const long utcOffsetInSeconds = 10800;

unsigned long lastTime = 0;
unsigned long timerDelay = 5000;

AsyncStream<128> serial(&Serial, '\n');
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org", utcOffsetInSeconds);

void setup() {
  Serial.begin(9600);
  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());
}

//char* formjsonData() {
//  timeClient.update();
//  StaticJsonDocument<128> doc;
//  char jsonData[128];
//
//  //  if (serial.available()) {
//  //
//  //  }
//  doc["jsonDataFromSerial"] = serial.buf;
//  doc["timestamp"] = timeClient.getEpochTime();
//  serializeJson(doc, jsonData);
//  Serial.println(jsonData);
//  if (serial.available()) {     // если данные получены
//    Serial.println(serial.buf); // выводим их (как char*)
//  }
//  return jsonData;
//}

void loop() {
  timeClient.update();
  StaticJsonDocument<128> doc;
  char jsonData[128];
  if (serial.available()) {     // если данные получены
    Serial.println(serial.buf); // выводим их (как char*)
    doc["jsonDataFromSerial"] = serial.buf;
    doc["timestamp"] = timeClient.getEpochTime();
  }


  serializeJson(doc, jsonData);

  if ((millis() - lastTime) > timerDelay) {
    if (WiFi.status() == WL_CONNECTED) {
      WiFiClient client;
      HTTPClient http;
      http.begin(client, serverName);
      http.addHeader("Content-Type", "application/json");
      int httpResponseCode = http.POST(jsonData);
      http.end();
    }
    else {
      Serial.println("WiFi Disconnected");
    }
    lastTime = millis();
  }
}
