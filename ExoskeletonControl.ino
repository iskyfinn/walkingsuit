#include <Servo.h>
#include <Wire.h>
#include <MPU6050.h>

// Create servo objects
Servo hipRight, hipLeft, kneeRight, kneeLeft;

// Define pins
#define FSR_RIGHT A0
#define FSR_LEFT A1

// Initialize MPU-6050
MPU6050 mpu;

// Thresholds
int fsrThreshold = 200;  // Adjust based on testing
int servoNeutral = 90;   // Neutral position
int servoForward = 120;  // Forward position
int servoBackward = 60;  // Backward position

void setup() {
  // Initialize serial communication
  Serial.begin(9600);

  // Attach servos to pins
  hipRight.attach(9);
  hipLeft.attach(10);
  kneeRight.attach(11);
  kneeLeft.attach(12);

  // Initialize MPU-6050
  Wire.begin();
  mpu.initialize();

  if (!mpu.testConnection()) {
    Serial.println("MPU6050 connection failed!");
    while (1);
  }
  Serial.println("MPU6050 connected successfully!");

  // Set servos to neutral
  hipRight.write(servoNeutral);
  hipLeft.write(servoNeutral);
  kneeRight.write(servoNeutral);
  kneeLeft.write(servoNeutral);
}

void loop() {
  // Read FSR values
  int fsrRight = analogRead(FSR_RIGHT);
  int fsrLeft = analogRead(FSR_LEFT);

  // Control servos based on FSR input
  if (fsrRight > fsrThreshold) {
    hipRight.write(servoForward);
    delay(500);  // Simulate step duration
    hipRight.write(servoNeutral);
  }

  if (fsrLeft > fsrThreshold) {
    hipLeft.write(servoForward);
    delay(500);  // Simulate step duration
    hipLeft.write(servoNeutral);
  }

  // Read MPU-6050 data for autonomous mode
  int16_t ax, ay, az;
  mpu.getAcceleration(&ax, &ay, &az);

  if (ay > 10000) {  // Forward tilt detected
    hipRight.write(servoForward);
    hipLeft.write(servoBackward);
    delay(500);  // Simulate step duration
    hipRight.write(servoNeutral);
    hipLeft.write(servoNeutral);
  } else if (ay < -10000) {  // Backward tilt detected
    hipRight.write(servoBackward);
    hipLeft.write(servoForward);
    delay(500);
    hipRight.write(servoNeutral);
    hipLeft.write(servoNeutral);
  }

  // Small delay to stabilize the loop
  delay(100);
}
