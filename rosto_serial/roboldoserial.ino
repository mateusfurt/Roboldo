#include "LedControl.h"

LedControl lc = LedControl(13, 12, 11, 5); // Pino 13 = DIN, Pino 12 = CLK, Pino 11 = CS. 5 = número de displays

#define NUM_EYES 4
#define NUM_MOUTHS 6

//************************
//  Definição das faces


tenho esse programa que controla o rosto de um robô quero um programa python que ative as funções das expressões, e quero que faça de modo que uma função fique executando enquanto o arduino ainda espera por outro caractere


//************************

// olho neutro
byte neutral_eye[8] = {B00000000,
                       B00011000,
                       B00111100,
                       B01111110,
                       B01111110,
                       B00111100,
                       B00011000,
                       B00000000
                      };

// olho esbugalhado
byte spooky_eye[8] = {B00111100,
                      B01111110,
                      B11111111,
                      B11111111,
                      B11111111,
                      B11111111,
                      B01111110,
                      B00111100
                     };

// olho fechado (para cima)
byte closed_eye_up[8] = {B00000000,
                         B00001100,
                         B00011000,
                         B00011000,
                         B00011000,
                         B00011000,
                         B00001100,
                         B00000000
                        };

// olho fechado (para baixo)
byte closed_eye_down[8] = {B00000000,
                           B00001100,
                           B00001100,
                           B00000110,
                           B00000110,
                           B00001100,
                           B00001100,
                           B00000000
                          };

// boca triste            //parte 1
byte sad_mouth[24] = { B00000000,
                         B00000000,
                         B00000000,
                         B00000000,
                         B01100000,
                         B00110000,
                         B00011000,
                         B00001100,
                         //parte 2
                         B00001110,
                         B00000110,
                         B00000110,
                         B00000110,
                         B00000110,
                         B00000110,
                         B00000110,
                         B00001100,
                         //parte 3
                         B00001100,
                         B00011000,
                         B00110000,
                         B01100000,
                         B00000000,
                         B00000000,
                         B00000000,
                         B00000000
                       };


// boca feliz           //parte 1
byte happy_mouth[24] = {   B00000000,
                         B00000000,
                         B00000000,
                         B00000000,
                         B00000110,
                         B00001100,
                         B00011000,
                         B00110000,
                         //parte 2
                         B00110000,
                         B01100000,
                         B01100000,
                         B01100000,
                         B01100000,
                         B01100000,
                         B01100000,
                         B00110000,
                         //parte 3
                         B00110000,
                         B00011000,
                         B00001100,
                         B00000110,
                         B00000000,
                         B00000000,
                         B00000000,
                         B00000000
                     };
byte lingua_mouth[24] = {B00000000,
                         B00000000,
                         B00000000,
                         B00111000,
                         B00111110,
                         B00011100,
                         B00011000,
                         B00110000,
                         //parte 2
                         B00110000,
                         B01100000,
                         B01100000,
                         B01100000,
                         B01100000,
                         B01100000,
                         B01100000,
                         B00110000,
                         //parte 3
                         B00110000,
                         B00011000,
                         B00001100,
                         B00000110,
                         B00000000,
                         B00000000,
                         B00000000,
                         B00000000
                     };

// boca muito feliz           //parte 1
byte very_happy_mouth[24] = { B00000000,
                              B00000000,
                              B00001110,
                              B00111110,
                              B01100110,
                              B01100110,
                              B11000110,
                              B11000110,
                              //parte 2
                              B11000110,
                              B11000110,
                              B11000110,
                              B11000110,
                              B11000110,
                              B11000110,
                              B11000110,
                              B11000110,
                              //parte 3
                              B11000110,
                              B11000110,
                              B01100110,
                              B01100110,
                              B00111110,
                              B00001110,
                              B00000000,
                              B00000000
                            };

// boca neutra                //parte 1
byte neutral_mouth[24] = {    B00000000,
                              B00000000,
                              B00010000,
                              B00010000,
                              B00010000,
                              B00010000,
                              B00010000,
                              B00010000,
                              //parte 2
                              B00010000,
                              B00010000,
                              B00010000,
                              B00010000,
                              B00010000,
                              B00010000,
                              B00010000,
                              B00010000,
                              //parte 3
                              B00010000,
                              B00010000,
                              B00010000,
                              B00010000,
                              B00010000,
                              B00010000,
                              B00000000,
                              B00000000
                         };


// boca aberta             //parte 1
byte opened_mouth[24] = {  B00000000,
                           B00000000,
                           B00000000,
                           B00000000,
                           B00000000,
                           B00000000,
                           B00000000,
                           B00000000,
                           //parte 2
                           B00000000,
                           B00011100,
                           B00100010,
                           B01000001,
                           B01000001,
                           B00100010,
                           B00011100,
                           B00000000,
                           //parte 3
                           B00000000,
                           B00000000,
                           B00000000,
                           B00000000,
                           B00000000,
                           B00000000,
                           B00000000,
                           B00000000
                        };
// língua para fora
byte tongue_mouth[24] = {B00000000,
                         B00000000,
                         B00000000,
                         B00111000,
                         B00111110,
                         B00011100,
                         B00011000,
                         B00110000,
                         //parte 2
                         B00110000,
                         B01100000,
                         B01100000,
                         B01100000,
                         B01100000,
                         B01100000,
                         B01100000,
                         B00110000,
                         //parte 3
                         B00110000,
                         B00011000,
                         B00001100,
                         B00000110,
                         B00000000,
                         B00000000,
                         B00000000,
                         B00000000
                     };

// Arrays de olhos e bocas
byte* eyes[] = {neutral_eye, spooky_eye, closed_eye_up, closed_eye_down};
byte* mouths[] = {sad_mouth, happy_mouth, very_happy_mouth, neutral_mouth, tongue_mouth, opened_mouth};

// Variáveis de controle
int selectedEye = 0;
int selectedMouth = 0;

//*****************
// Setup do Arduino
//*****************
void setup()
{
  // inicializar displays (configurar a intensidade de brilho e limpar tudo)
  for (int i = 0; i < 5; i++) {
    lc.shutdown(i, false);
    lc.setIntensity(i, 1);
    lc.clearDisplay(i);
  }
  
  // iniciar comunicação serial
  Serial.begin(9600);
  Serial.println("Digite o índice do olho (0-3) e o índice da boca (0-5) separados por espaço:");
}

//***************
// Loop principal
//***************
{
  if (Serial.available() > 0) {
    char input = Serial.read();
    
    if (input == 'A') {
      feliz();
      executandoFalar = false;  // Para outras animações, se necessário
    }
    if (input == 'B') {
      triste();
      executandoFalar = false;
    }
    if (input == 'C') {
      bocaberta();
      executandoFalar = false;
    }
    if (input == 'D') {
      serio();
      executandoFalar = false;
    }
    if (input == 'E') {
      lingua();
      executandoFalar = false;
    }
    if (input == 'F') {
      surpreso();
      executandoFalar = false;
    }
    if (input == 'G') {
      executandoFalar = true;  // Ativa a animação de "falar"
    }
  }

  // Se estiver falando, continua executando a animação
  if (executandoFalar) {
    falar();  // A função "falar" continua executando até receber novo comando
  }
}

//*******************
// Funções auxiliares
//*******************
void feliz() {
  display_eyes(eyes[0],eyes[0]);
  display_mouth(mouths[1]);
}
void triste() {
  display_eyes(eyes[0],eyes[0]);
  display_mouth(mouths[0]);
}
void bocaberta() {
  display_eyes(eyes[0],eyes[0]);
  display_mouth(mouths[2]);
}
void serio() {
  display_eyes(eyes[0],eyes[0]);
  display_mouth(mouths[3]);
}
void lingua() {
  display_eyes(eyes[0],eyes[0]);
  display_mouth(mouths[4]);
}
void surpreso() {
  display_eyes(eyes[0],eyes[0]);
  display_mouth(mouths[5]);
}

void falar() {
  while(1){
    display_eyes(eyes[0],eyes[0]);
    display_mouth(mouths[2]);
    delay(500);
    display_mouth(mouths[3]);
    delay(500);
  }
  
}


// mudar olhos
void display_eyes(byte right_eye[], byte left_eye[]) {
  for (int i = 0; i < 8; i++) {
    lc.setRow(0, i, left_eye[i]);
    lc.setRow(1, i, right_eye[i]);
  }
}

// mudar boca
void display_mouth(byte mouth[]) {
  for (int i = 0; i < 8; i++) {
    lc.setRow(2, i, mouth[i]);
    lc.setRow(3, i, mouth[i + 8]);
    lc.setRow(4, i, mouth[i + 16]);
  }
}

// apaga todos os LEDs
void apagar_leds() {
  for (int i = 0; i < 5; i++) {
    lc.clearDisplay(i);
  }
}
