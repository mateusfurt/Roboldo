#include "LedControl.h"

LedControl lc = LedControl(13, 12, 11, 5); // Pino 13 = DIN, Pino 12 = CLK, Pino 11 = CS. 5 = número de displays

#define NUM_EYES 4
#define NUM_MOUTHS 6

//************************
//  Definição das faces
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
void loop()
{
  if (Serial.available() > 0) {
    // Ler o comando serial
    String input = Serial.readStringUntil('\n');
    input.trim(); // Remove espaços em branco no início e no fim
    int spaceIndex = input.indexOf(' ');
    
    if (spaceIndex > 0) {
      String eyeIndexStr = input.substring(0, spaceIndex);
      String mouthIndexStr = input.substring(spaceIndex + 1);
      
      int eyeIndex = eyeIndexStr.toInt();
      int mouthIndex = mouthIndexStr.toInt();
      
      // Verificar se os índices são válidos
      if (eyeIndex >= 0 && eyeIndex < NUM_EYES && mouthIndex >= 0 && mouthIndex < NUM_MOUTHS) {
        selectedEye = eyeIndex;
        selectedMouth = mouthIndex;
        
        display_eyes(eyes[selectedEye], eyes[selectedEye]);
        display_mouth(mouths[selectedMouth]);
      } else {
        Serial.println("Índices inválidos. Digite novamente.");
      }
    } else {
      Serial.println("Entrada inválida. Digite o índice do olho e da boca separados por espaço.");
    }
  }
}

//*******************
// Funções auxiliares
//*******************

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
