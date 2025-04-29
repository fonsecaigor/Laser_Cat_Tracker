#include <Servo.h>

Servo x_servo;
Servo y_servo;

const int laserPin = 3;
const int xPin = 9;
const int yPin = 6;

int laserPower = 100;

// Limites de movimento
float min_x = 90;
float max_x = 160;

float min_y = 70;
float max_y = 160;

int min_freeze = 400;
int max_freeze = 1200;

float minimal_movement = 1;

void setup() {
  Serial.begin(9600);

  y_servo.attach(yPin);
  x_servo.attach(xPin);

  pinMode(laserPin, OUTPUT);
  analogWrite(laserPin, laserPower);

  // Posição inicial
  y_servo.write((min_y + max_y) / 2);
  x_servo.write((min_x + max_x) / 2);

  delay(1000);
}

void loop() {
  int movement_time = random(10, 30);
  int random_delay = random(min_freeze, max_freeze);

  float x_new_position = random(min_x + minimal_movement, max_x - minimal_movement);
  float y_new_position = random(min_y, max_y);

  float x_old_position = x_servo.read();
  float y_old_position = y_servo.read();

  float x_speed = (x_new_position - x_old_position) / movement_time;
  float y_speed = (y_new_position - y_old_position) / movement_time;

  for (int pos = 0; pos < movement_time; pos++) {
    x_old_position += x_speed;
    y_old_position += y_speed;

    x_servo.write(constrain(x_old_position, min_x, max_x));
    y_servo.write(constrain(y_old_position, min_y, max_y));

    // Envia posições durante o movimento
    Serial.print("X:");
    Serial.print((int)x_old_position);
    Serial.print(",Y:");
    Serial.println((int)y_old_position);

    delay(30);
  }

  // Após terminar o movimento, envia "END"
  Serial.println("END");

  delay(random_delay);
}
