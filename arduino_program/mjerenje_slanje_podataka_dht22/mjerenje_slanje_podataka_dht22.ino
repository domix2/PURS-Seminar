#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>

#define DHTPIN 2     // Digital pin connected to the DHT sensor
#define DHTTYPE DHT22   // DHT 22 (AM2302)

const char* ssid = "Wi-fi";
const char* password = "OT4EC38CEBC7A";

const char* serverName = "http://192.168.100.8/obrada";

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected to WiFi");

  dht.begin();
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    // Test with a simple GET request first
    HTTPClient http;
    http.begin("http://192.168.100.8/");
    int httpResponseCode = http.GET();

    if (httpResponseCode > 0) {
      Serial.print("GET request successful, response code: ");
      Serial.println(httpResponseCode);
      String response = http.getString();
      Serial.println(response);
    } else {
      Serial.print("Error on sending GET: ");
      Serial.println(httpResponseCode);
    }
    http.end();

    // Now send the POST request
    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");

    // Set timeout for HTTP connection
    http.setTimeout(5000); // 5 seconds timeout

    // Reading temperature and humidity from DHT22
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();

    // Check if any reads failed and exit early (to try again).
    if (isnan(temperature) || isnan(humidity)) {
      Serial.println("Failed to read from DHT sensor!");
      return;
    }

    StaticJsonDocument<200> doc;
    doc["temperatura"] = temperature;
    doc["vlaga"] = humidity;

    String requestBody;
    serializeJson(doc, requestBody);

    Serial.print("Request Body: ");
    Serial.println(requestBody);

    httpResponseCode = http.POST(requestBody);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println(httpResponseCode);
      Serial.println(response);
    } else {
      Serial.print("Error on sending POST: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  } else {
    Serial.println("WiFi not connected");
  }

  delay(20000); // Send data every 10 seconds
}
