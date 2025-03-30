#include <DHT.h>
#include <Wire.h>
#include <Adafruit_MLX90614.h>

#define DHTPIN 4
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

#define RP1 27
#define RP2 26
#define RP3 25

#define SW420_PIN 33

const int soundSensorPin = 34;

const int ldrSensorPin = 35;

const int motionSensorPin = 32;

Adafruit_MLX90614 mlx = Adafruit_MLX90614();

float tempDHT11 = 0.0;
float humedadDHT11 = 0.0;
int vibracionSW420 = 0;
float tempInfrarrojo = 0.0;
float tempAmbienteMLX = 0.0;
int luzLDR = 0;
int sonidoGY057 = 0;
int movimientoHCS501 = 0;
bool humedadActive = false;

int contadorVibracion = 0;
int contadorMovimiento = 0;

void setup() {
  Serial.begin(115200);

  dht.begin();
  mlx.begin();

  pinMode(RP1, OUTPUT);
  pinMode(RP2, OUTPUT);
  pinMode(RP3, OUTPUT);

  digitalWrite(RP3, LOW);

  pinMode(SW420_PIN, INPUT);
  pinMode(soundSensorPin, INPUT);
  pinMode(ldrSensorPin, INPUT);
  pinMode(motionSensorPin, INPUT);
}

void loop() {
  leerSensores();
  controlarReles();

  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    
    if (command == "GET_DATA") {
      leerSensores();
      mostrarDatos();
    }
  }

  sleep(1);
}

void leerSensores() {
  tempDHT11 = dht.readTemperature();
  humedadDHT11 = dht.readHumidity();
  vibracionSW420 = digitalRead(SW420_PIN);
  tempInfrarrojo = mlx.readObjectTempC();
  tempAmbienteMLX = mlx.readAmbientTempC();
  luzLDR = analogRead(ldrSensorPin);
  sonidoGY057 = analogRead(soundSensorPin);
  movimientoHCS501 = digitalRead(motionSensorPin);

  if (vibracionSW420 == HIGH) {
    contadorVibracion++;
  }

  if (movimientoHCS501 == HIGH) {
    contadorMovimiento++;
  }
}

void mostrarDatos() {
  Serial.print("TAM01:"); Serial.println(tempDHT11);
  Serial.print("HAM01:"); Serial.println(humedadDHT11);
  Serial.print("TBB01:"); Serial.println(tempInfrarrojo);
  Serial.print("LDR01:"); Serial.println(luzLDR);
  Serial.print("SON01:"); Serial.println(sonidoGY057);
  Serial.print("VRB01:"); Serial.println(vibracionSW420);
  Serial.print("PRE01:"); Serial.println(movimientoHCS501);
}

void controlarReles() {
  /*
    relays: {
      RP1: {
        "actuador": "Ventilador calor",
        "pin": 27
      },
      RP2: {
        "actuador": "Ventilador frio",
        "pin": 26
      }
      PR3: {
        "actuador": "Ventilador humedad",
        "pin": 25
      }
    }
  */

  if (tempAmbienteMLX > 32.0) {
    Serial.println("Encender calor");
    digitalWrite(RP1, HIGH);
  } else if (tempAmbienteMLX < 31.0) {
    Serial.println("Apagar calor");
    digitalWrite(RP1, LOW);
  }

  if (tempAmbienteMLX < 32.0) {
    Serial.println("Encender frio");
    digitalWrite(RP2, HIGH);
  } else if (tempAmbienteMLX > 33.0) {
    Serial.println("Apagar frio");
    digitalWrite(RP2, LOW);
  }

  if (humedadDHT11 < 60 && !humedadActive) {
    digitalWrite(RP3, HIGH);
    delay(1000);
    digitalWrite(RP3, LOW);
    humedadActive = true;
  } else if (humedadDHT11 > 70 && humedadActive) {
    digitalWrite(RP3, HIGH);
    delay(1000);
    digitalWrite(RP3, LOW);
    humedadActive = false;
  }
}
