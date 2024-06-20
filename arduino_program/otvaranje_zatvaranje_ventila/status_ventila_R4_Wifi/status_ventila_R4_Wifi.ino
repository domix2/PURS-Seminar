#include <Arduino.h>
#include <WiFi.h>

const char* ssid = "Wi-fi";
const char* password = "OT4EC38CEBC7A";

const char* serverName = "192.168.100.8"; // Server IP
const int serverPort = 80; // Server port

const int buttonPin = 2; // GPIO2 for the button
const int greenLEDPin = 5; // GPIO5 for the green LED
const int redLEDPin = 4; // GPIO4 for the red LED

bool lastButtonState = HIGH; // Start with not pressed
bool currentStatus = true; // Start with "Open"

WiFiClient client;

void setup() {
  pinMode(buttonPin, INPUT_PULLUP); // Set the button pin as input with internal pull-up resistor
  pinMode(greenLEDPin, OUTPUT);
  pinMode(redLEDPin, OUTPUT);

  Serial.begin(115200);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  updateLEDs();
}

void loop() {
  bool buttonState = digitalRead(buttonPin);
  if (buttonState == LOW && lastButtonState == HIGH) {
    // Button was pressed
    currentStatus = !currentStatus; // Toggle status
    sendStatusUpdate(currentStatus ? "Open" : "Closed");
  }
  lastButtonState = buttonState;
  delay(50); // Debounce delay
}

void sendStatusUpdate(const char* status) {
  if (WiFi.status() == WL_CONNECTED) {
    if (client.connect(serverName, serverPort)) {
      String httpRequestData = String("POST /test HTTP/1.1\r\n") +
                               "Host: " + serverName + "\r\n" +
                               "Content-Type: application/json\r\n" +
                               "Content-Length: " + String(strlen(status) + 15) + "\r\n\r\n" +
                               "{\"status\":\"" + String(status) + "\"}\r\n";

      client.print(httpRequestData);

      int timeout = 5000; // 5 seconds timeout
      long int time = millis();
      while (!client.available() && (millis() - time) < timeout) {
        delay(100);
      }

      if (client.available()) {
        String response = client.readString();
        Serial.println(response);
      } else {
        Serial.println("Client timeout");
      }
      client.stop();
    } else {
      Serial.println("Connection to server failed");
    }

    updateLEDs();
  }
}

void updateLEDs() {
  if (currentStatus) {
    digitalWrite(greenLEDPin, HIGH);
    digitalWrite(redLEDPin, LOW);
  } else {
    digitalWrite(greenLEDPin, LOW);
    digitalWrite(redLEDPin, HIGH);
  }
}
