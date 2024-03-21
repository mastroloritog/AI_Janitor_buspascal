// Nota: Arduino legge carattere per carattere dal flusso seriale tra pc e controllore

#include <Stepper.h>


bool sxRotationState = false;
bool dxRotationState = false;
String receivedString = ""; // Variabile per memorizzare la stringa ricevuta

// utilizzo dello stepper motor per controllare la direzione del robot (controllo della ruota anteriore)
//Set how many steps it takes to make a full revolution
//Divide the degrees per step by 360 to get the steps
const int stepsPerRevolution = 2048;
//Use pin 8-11 to IN1-IN4
Stepper stepper = Stepper(stepsPerRevolution, 8, 10, 9, 11);
const int motorSpeed = 5; // Velocità del motore stepper (in RPM)

void setup() {
  //Set the RPM of the stepper motor
  stepper.setSpeed(motorSpeed);
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // Esegui uno step del motore stepper
  if (sxRotationState) {
    // Rotazione a sinistra
    stepper.step(stepsPerRevolution); // Ruota in senso orario di una rivoluzione
    sxRotationState = false; // Resetta lo stato di rotazione a sinistra
  } else if (dxRotationState) {
    // Rotazione a destra
    stepper.step(-stepsPerRevolution); // Ruota in senso antiorario di una rivoluzione
    dxRotationState = false; // Resetta lo stato di rotazione a destra
  }
  
  // Controlla lo stato del LED
  digitalWrite(LED_BUILTIN, sxRotationState || dxRotationState); // Accendi il LED se il motore sta ruotando

  // Leggi i dati seriali carattere per carattere
  while (Serial.available() > 0) {
    char receivedChar = Serial.read(); // Leggi il carattere disponibile

    // Se il carattere è un terminatore di riga, processa la stringa ricevuta
    if (receivedChar == '\n') {
      processMessage(receivedString);
      receivedString = ""; // Resetta la stringa ricevuta
    } else {
      receivedString += receivedChar; // Aggiungi il carattere alla stringa ricevuta
    }
  }
}

void processMessage(String msg) {
  Serial.println("Messaggio ricevuto: " + msg);

  // comanda arduino da python
  if (msg == "sx") {
    sxRotationState = true;
    dxRotationState = false;
  } else if (msg == "dx") {
    dxRotationState = true;
    sxRotationState = false;
  } else if(msg == "ok") {
    dxRotationState = false;
    sxRotationState = false;
  }
}
