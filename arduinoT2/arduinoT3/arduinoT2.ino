#include <Servo.h>

//Incluir libreria control de servos


//Pines servos;
#define servo_pin1 3 
#define servo_pin2 5
#define servo_pin3 6 

//Inicializar objetos servo
Servo servo1;//Base
Servo servo2;//Medio
Servo servo3;//Garra

//Guardar posicion servos 
int servo_pos1 = 90;
int servo_pos2 = 90;
int servo_pos3 = 100;

//Variables para guardar las instrucciones
int servo_control1 = 0;
int servo_control2 = 0;
int servo_control3 = 0;

//Variables para recibir el comando
String delimiter = ",";
String substr;
int delimiterIndex;


//Para manipulador
const float msRightSpin = 738;          //Tiempo en dar una vuelta hacia la derecha
const float msLeftSpin = 1330;          //Tiempo en dar una vuelta hacia la izquierda
const float numLaps = 4;                //Número de vueltas para abrir la garra

const int rightVal = 86;          //Sentido horario
const int leftVal = 100;          //Sentido anti-horario
const int stopVal = 90;           //Valor en el que el servo se mantiene quieto

char data = '\0';
unsigned long now;
unsigned long lastTime;
unsigned long stopTime;

//Mandar angulos
String hola1 = " ";
String hola2 = " ";

int tiempo1 = 0;
int tiempo2 = 0;
int intervalo = 1000;


void setup() {
  //Inicializar el serial
  Serial.begin(250000);
  Serial.setTimeout(1);

  //Inicializar los servos 
  servo1.attach(servo_pin1);
  servo2.attach(servo_pin2);
  servo3.attach(servo_pin3);

  //Posicion inical servos;
  servo1.write(servo_pos1);
  servo2.write(servo_pos2);
  servo3.write(stopVal);

}

void loop() {

  //Recibir y parsear los controles
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



  //Mover los servos dependiendo del input

  if (servo_control1 == 1 || servo_control1 == -1){
    servo_pos1 = servo_pos1 + servo_control1;
    servo1.write(servo_pos1);
    }

  if (servo_control2 == 1 || servo_control2 == -1){
    servo_pos2 = servo_pos2 + servo_control2;
    servo2.write(servo_pos2);
    }

  if (servo_control3 == 1 || servo_control3 == -1){
    servo_pos3 = servo_pos3 + servo_control3;
    servo3.write(servo_pos3);

  }

  if(servo_control1 > 1)
  {
    servo1.write(servo_control1);
  }
    if(servo_control3 > 1 || servo_control3 < -1)
  {
    servo1.write(servo_control3);
  }
  if(servo_control2 > 1 || servo_control2 < -1)
  {
    servo2.write(servo_control2);
  }



  char buffer[20];
  dtostrf(servo_pos1, 5, 2, buffer);
  String cadena1 = String(buffer);
  dtostrf(servo_pos2, 5, 2, buffer);
  String cadena2 = String(buffer);



  hola1 = cadena1 +"," +cadena2;


  tiempo1 = millis();
  if (tiempo1-tiempo2>intervalo){
      tiempo2 = tiempo1;
      Serial.println(hola1);
      hola2 = hola1;
      }


  delay(10);

}
