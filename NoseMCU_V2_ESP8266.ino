#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <BH1750.h>
#include "Adafruit_SGP30.h"
#include <Wire.h>
#include "DHT.h"

const char* ssid = "smallwindOPPO";
const char* password = "12345678";
const char* mqtt_server = "120.108.111.227";
#define MQTT_PORT 1883 //輸入MQTT Broker埠號
#define CLINT_ID "test";
#define MQTT_USER "test" //輸入MQTT用戶名
#define MQTT_PASS "test" //輸入MQTT密碼
#define MQTT_publuicTopic "pub/sw_esp32";

WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);

BH1750 lightMeter;
Adafruit_SGP30 sgp;

#define DHTPIN 14
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

TwoWire Wire1 = TwoWire();
TwoWire Wire2 = TwoWire();

void setup() {
  Serial.begin(115200);
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("WiFi connected");

  mqttClient.setServer(mqtt_server, MQTT_PORT);
  while (!mqttClient.connected()) {
    Serial.println("Attempting MQTT connection...");
    if (mqttClient.connect("ESP32Client", MQTT_USER, MQTT_PASS)) {
      Serial.println("Connected to MQTT Broker!");
    } else {
      Serial.println("MQTT connection failed!");
      delay(1000);
    }
  }

  dht.begin();
  
  Wire1.begin(12,13);

  lightMeter.begin();

  Wire2.begin(4,5);
  
  if (!sgp.begin()){
    Serial.println("SGP30 初始化失敗");
    delay(0);
    while (1);
  }
  Serial.print("Found SGP30 serial #");
  Serial.print(sgp.serialnumber[0], HEX);
  Serial.print(sgp.serialnumber[1], HEX);
  Serial.println(sgp.serialnumber[2], HEX);
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  
  char message[length+1];
  for (int i=0;i<length;i++) {
    message[i] = (char)payload[i];
    Serial.print(message[i]);
  }
  message[length] = '\0';
  Serial.println();

}

int counter = 0;
void loop() {
  Wire2.begin(4,5);
  if (! sgp.IAQmeasure()) {
    Serial.println("Measurement failed");
    delay(500);
    return;
  }
  float co2 = sgp.eCO2;
  Wire1.begin(12,13);
  float lux = lightMeter.readLightLevel();
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  Serial.print("temp : ");
  Serial.println(t);
  Serial.print("\nhumi : ");
  Serial.println(h);
  Serial.print("\nlux : ");
  Serial.println(lux);
  Serial.print("\nco2 : ");
  Serial.println(co2);

  // 將數據轉換為字串
  String humidityStr = String(h);
  String temperatureStr = String(t);
  String CO2Str = String(co2);
  String luxStr = String(lux);
  String msg = temperatureStr + "," + humidityStr + "," + luxStr + "," + CO2Str;

  mqttClient.publish("pub/sw_esp32", msg.c_str());
  
  delay(30000);
}
