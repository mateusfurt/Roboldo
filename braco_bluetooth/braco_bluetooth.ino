#include "BluetoothSerial.h"
#include <ESP32Servo.h>

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run make menuconfig to and enable it
#endif

BluetoothSerial SerialBT;  // Objeto para tratar dos dados recebidos ou enviados por Bluetooth
Servo ombro;
Servo cotovelo;
Servo braco; // Novo servo motor
char motor = ' '; // Char que receberá o caractere passado pela interface Android via Bluetooth
int grau;
int ombro1 = 13;
int cotovelo1 = 12; 
int bracoPin = 14; // Pino do terceiro motor servo
int ledInt = 2;  // LED interno do ESP32 - porta digital 2

void mexerombro(int pos){
  String mensagem = "Servo braco para "+String(pos)+ "graus";
  Serial.println(mensagem);
  ombro.write(pos);
}
void mexerbraco(int pos){
  String mensagem = "Servo braco para "+String(pos)+ "graus";
  Serial.println(mensagem);
  braco.write(pos);
}
void mexercotovelo(int pos){
  String mensagem = "Servo braco para "+String(pos)+ "graus";
  Serial.println(mensagem);
  cotovelo.write(pos);
}
void neutro(){
  Serial.println("Robolso está neutro");
  delay(500);
  ombro.write(90);
  delay(500);
  braco.write(0);
  delay(500);
  cotovelo.write(90);
  delay(500);
}
void acenar(){
  mexerombro(0);
  delay(250);
  mexerbraco(125);
  delay(250);
  mexercotovelo(90);
  delay(500);
  mexercotovelo(0);
  delay(500);
  mexercotovelo(90);
  delay(500);
  mexercotovelo(0);
  delay(500);
  mexercotovelo(90);
  delay(500);
  mexercotovelo(0);
  neutro();
}
void comemorar(){
  mexerombro(0);
  delay(250);
  mexerbraco(90);
  delay(250);
  mexercotovelo(0);
  delay(250);
  
  mexerbraco(180);
  delay(200);
  mexercotovelo(90);
  delay(500);
  
  mexerbraco(90);
  delay(100);
  mexercotovelo(0);
  delay(500);
  
  mexerbraco(180);
  delay(200);
  mexercotovelo(90);
  delay(500);
  
  mexerbraco(90);
  delay(100);
  mexercotovelo(0);
  delay(500);
  
  mexerbraco(180);
  delay(200);
  mexercotovelo(90);
  delay(500);
  
  mexerbraco(90);
  delay(100);
  mexercotovelo(0);
  delay(500);
  
  mexerbraco(180);
  delay(200);
  mexercotovelo(90);
  delay(500);
  
  mexerbraco(90);
  delay(100);
  mexercotovelo(0);
  delay(500);
  
  neutro();
  
}


void setup() {
  Serial.begin(115200);  // Velocidade padrão de comunicação serial do ESP32
  SerialBT.begin("ESP32_bt_classic"); // Habilita a porta de comunicação Bluetooth do ESP32, dando um nome de reconhecimento do Bluetooth 
  Serial.println("O dispositivo já pode ser pareado!");

  // Anexa os servos aos pinos especificados
  ombro.attach(ombro1);
  cotovelo.attach(cotovelo1);
  braco.attach(bracoPin); // Anexa o terceiro servo ao pino especificado
  
  // Inicializa os servos na posição 0 graus
  neutro();

  // Configura o LED interno
  pinMode(ledInt, OUTPUT);
}

void loop() {
  if (SerialBT.available()) { // Verifica se foi recebido algum caractere pelo Bluetooth
    String texto = SerialBT.readString();
    Serial.print("Received: ");
    motor = texto.charAt(0); // Caractere na primeira posição
    grau = texto.substring(1).toInt();
    
        
    // Controle do servo do ombro
    if(motor == 'a'){
      mexerombro(grau);
    }
    if(motor == 'b'){
      mexerbraco(grau);
    }
    // Controle do servo do braço
    if(motor == 'c'){
      mexercotovelo(grau);
    }
    if(motor == 'd'){
      neutro();
    }
    if(motor == 'e'){
      comemorar();
    }    
    if(motor == 'h'){
      acenar();
    }

    // Controle do terceiro servo motor
    

  }
  delay(30);
}
