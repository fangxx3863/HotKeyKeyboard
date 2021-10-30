/*

PIN 3      <----->         7   （行）   

PIN 4      <----->         6   （行）

PIN 5      <----->         5   （行）

PIN 6      <----->         4   （列）

PIN 7      <----->         3   （列）

PIN 8      <----->         2   （列）

PIN 9      <----->         1   （列）

*/

#include <Keypad.h>
#include <Adafruit_NeoPixel.h>
#include <RotaryEncoder.h>

#define ROWS 3 // rows
#define COLS 4 // columns

#define PIN_IN1 A1  //1号旋转编码器A
#define PIN_IN2 A2  //1号旋转编码器B
#define PIN_IN3 A4  //2号旋转编码器A
#define PIN_IN4 A5  //2号旋转编码器B

#define PIN_SW1 A0  //1号旋转编码器SW
#define PIN_SW2 A3  //2号旋转编码器SW

RotaryEncoder encoder1(PIN_IN1, PIN_IN2, RotaryEncoder::LatchMode::TWO03);
RotaryEncoder encoder2(PIN_IN3, PIN_IN4, RotaryEncoder::LatchMode::TWO03);

#define NEOPIXEL_PIN 2
#define NUM_PIXELS (ROWS * COLS)


int SW1 = 0;
int SW2 = 0;

unsigned long loopCount;
unsigned long startTime;
String msg;

Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_PIXELS, NEOPIXEL_PIN, NEO_GRB + NEO_KHZ800);


//define the symbols on the buttons of the keypads
char keys[ROWS][COLS] = {
  {'A','B','C','D'},
  {'E','F','G','H'},
  {'I','J','K','L'}
};

uint8_t rowPins[ROWS] = {5, 4, 3}; //connect to the row pinouts of the keypad
uint8_t colPins[COLS] = {6, 7, 8, 9}; //connect to the column pinouts of the keypad

//initialize an instance of class NewKeypad
Keypad keypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );

bool lit[ROWS*COLS] = {0};

void setup()
{
    Serial.begin(115200);
    pinMode(PIN_SW1, INPUT);
    pinMode(PIN_SW2, INPUT);
    msg = "";
}

void loop()
{
    if (keypad.getKeys())
    {
        for (int i=0; i<LIST_MAX; i++)   // Scan the whole key list.
        {
            if ( keypad.key[i].stateChanged )   // Only find keys that have changed state.
            {
                switch (keypad.key[i].kstate) {  // Report active key state : IDLE, PRESSED, HOLD, or RELEASED
                    case PRESSED:
                    msg = "_P"; //按下
                break;
                    case HOLD:
                    msg = "_H"; //停留
                break;
                    case RELEASED:
                    msg = "_R"; //抬起
                break;
                    case IDLE:
                    msg = "_I"; //闲置
                }
                Serial.print(keypad.key[i].kchar);
                Serial.println(msg);
            }
        }
    }
    
    static int pos1 = 0;
    encoder1.tick();
    int newPos1 = encoder1.getPosition();
    if (pos1 != newPos1) {
        Serial.print("D1_");
        Serial.print((int)(encoder1.getDirection()));
        Serial.println("_P");
        pos1 = newPos1;
    }
    if(digitalRead(PIN_SW1) == LOW && SW1 == 0) {
        SW1 = 1;
        Serial.println("SW1_P");
    }else if(digitalRead(PIN_SW1) == HIGH && SW1 == 1) {
        SW1 = 0;
        Serial.println("SW1_R");
    }
    
    
    


    static int pos2 = 0;
    encoder2.tick();
    int newPos2 = encoder2.getPosition();
    if (pos2 != newPos2) {
        Serial.print("D2_");
        Serial.print((int)(encoder2.getDirection()));
        Serial.println("_P");
        pos2 = newPos2;
    }
    if(digitalRead(PIN_SW2) == LOW && SW2 == 0) {
        SW2 = 1;
        Serial.println("SW2_P");
    }else if(digitalRead(PIN_SW2) == HIGH && SW2 == 1) {
        SW2 = 0;
        Serial.println("SW2_R");
    }
}
