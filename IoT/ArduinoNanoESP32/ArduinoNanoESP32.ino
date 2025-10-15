#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "*****";
const char* password = "****";

// URL de tu API FastAPI (ajusta IP y puerto)
const char* serverName = "http://192.168.1.10:8000/api/acceso";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  Serial.print("Conectando a Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n✅ Conectado al Wi-Fi");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");

    // Simulación de datos de acceso permitido
    String postData = R"({
      "codigo_estudiante": "20250123",
      "direccion": "ENTRA",
      "distancia_s1": 8.5,
      "distancia_s2": 12.0
    })";

    int httpResponseCode = http.POST(postData);
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("Respuesta del servidor:");
      Serial.println(response);
    } else {
      Serial.print("Error al enviar datos: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  }

  // Esperar 10 segundos antes de la siguiente simulación
  delay(10000);
}

