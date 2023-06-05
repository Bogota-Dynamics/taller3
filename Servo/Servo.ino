#include <Servo.h>

// Pines donde están conectados los servos
const int servoPin1 = 3;
const int servoPin2 = 5;
const int servoPin3 = 6;

// Objetos de los servos
Servo servoMotor1;
Servo servoMotor2;
Servo servoMotor3;

int servo_control1 = 0;
int servo_control2 = 0;
int servo_control3 = 0;

// Variables para controlar los ángulos de los servos
int angulo1 = 90;
int angulo2 = 90;
int angulo3 = 75;

void setup() {
  // Inicializar la comunicación serial
  Serial.begin(250000);
  
  // Esperar a que llegue un mensaje de ROS 2
  while (!Serial.available()) {
    delay(100);
  }


    // Inicializar los objetos de los servos
  servoMotor1.attach(servoPin1);
  servoMotor2.attach(servoPin2);
  servoMotor3.attach(servoPin3);
  servoMotor1.write(angulo1);
  servoMotor2.write(angulo2);
  servoMotor3.write(angulo3);

  
}

void loop() {

  if (Serial.available() > 0) {

  String inputString = Serial.readString();
  int values[4]; // array to store the four parsed floats
  int valueIndex = 0; // index to keep track of which float is being parsed
  int commaIndex = 0; // index to keep track of the comma position

  while (commaIndex >= 0) {
    commaIndex = inputString.indexOf(","); // find the next comma in the input string
    if (commaIndex >= 0) {
      values[valueIndex] = atoi(inputString.substring(0, commaIndex).c_str()); // parse the float between the start of the string and the comma
      inputString = inputString.substring(commaIndex + 1); // remove the parsed float and the comma from the input string
      valueIndex++; // increment the index to parse the next float
    }
  }

  values[valueIndex] = atoi(inputString.c_str()); // parse the final float in the input string

  // destructure
  servo_control1 = values[0];
  servo_control2 = values[1];
  servo_control3 = values[2];

  }

  if (servo_control1 ==1) {

  abrir();
  delay(300);
  cerrar();
  delay(300);
  subir();
  delay(5500);
  servoMotor1.write(110);
  delay(300);
  servoMotor2.write(35);
  servoMotor3.write(65);
  delay(300);
  abrir();
  servo_control1 = 0;
    servoMotor1.write(90);
  servoMotor2.write(90);
  servoMotor3.write(75);
  }
}

// Secuencia "cerrar"
void cerrar() {
  // Asignar los ángulos para cerrar
  angulo1 = 90;
  angulo2 =15;
  angulo3 = 115;

  // Posicionar los servos a los ángulos correspondientes
  servoMotor1.write(angulo1);
  servoMotor2.write(angulo2);
  servoMotor3.write(angulo3);
}

// Secuencia "abrir"
void abrir() {
  // Asignar los ángulos para abrir
  angulo1 = 90;
  angulo2 = 15;
  angulo3 = 50;
  

  // Posicionar los servos a los ángulos correspondientes
  servoMotor1.write(angulo1);
  servoMotor2.write(angulo2);
  delay(150);
  servoMotor3.write(angulo3);
}

// Secuencia "subir"
void subir() {
  // Asignar los ángulos para subir
  angulo1 = 90;
  angulo3 = 120;
  int objetivo = 50; // Ángulo objetivo a alcanzar
  int incremento = 5; // Incremento de ángulo

  // Incrementar el ángulo2 gradualmente hasta alcanzar el objetivo
  for (int angulo = angulo2; angulo <= objetivo; angulo += incremento) {
    angulo2 = angulo;

    // Verificar los límites del ángulo2
    if (angulo2 > 180) angulo2 = 180;

    // Posicionar el servo2 al ángulo correspondiente
      servoMotor1.write(angulo1);
      servoMotor2.write(angulo2);
      servoMotor3.write(angulo3);

    delay(100); // Tiempo de espera entre incrementos
  }
  // Posicionar los servos a los ángulos correspondientes


 
}
