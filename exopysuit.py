import RPi.GPIO as GPIO
from smbus2 import SMBus
import time
from Adafruit_PCA9685 import PCA9685  # Uncomment if using PCA9685
import spidev  # For MCP3008 ADC

# Servo Configuration
SERVO_HIP_RIGHT = 0
SERVO_HIP_LEFT = 1
SERVO_KNEE_RIGHT = 2
SERVO_KNEE_LEFT = 3

# ADC Configuration (MCP3008 for FSRs)
SPI = spidev.SpiDev()
SPI.open(0, 0)
SPI.max_speed_hz = 1350000

# MPU-6050 Configuration
MPU_ADDRESS = 0x68
bus = SMBus(1)

# Servo Neutral Positions
SERVO_NEUTRAL = 90
SERVO_FORWARD = 120
SERVO_BACKWARD = 60

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Helper Functions
def read_adc(channel):
    """Reads an analog value from the MCP3008 ADC."""
    adc = SPI.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

def move_servo(pwm, channel, angle):
    """Moves a servo to the specified angle using PCA9685."""
    pulse = int((angle * 2.5) + 150)
    pwm.set_pwm(channel, 0, pulse)

# MPU-6050 Functions
def init_mpu():
    """Initializes the MPU-6050."""
    bus.write_byte_data(MPU_ADDRESS, 0x6B, 0)

def read_mpu():
    """Reads accelerometer data from the MPU-6050."""
    accel_x = bus.read_word_data(MPU_ADDRESS, 0x3B)
    accel_y = bus.read_word_data(MPU_ADDRESS, 0x3D)
    return accel_x, accel_y

# Main Loop
if __name__ == "__main__":
    # Initialize peripherals
    init_mpu()
    pwm = PCA9685()  # Uncomment if using PCA9685
    pwm.set_pwm_freq(50)

    while True:
        # Read FSR values
        fsr_right = read_adc(0)
        fsr_left = read_adc(1)

        # Control servos based on FSR input
        if fsr_right > 200:  # Adjust threshold as needed
            move_servo(pwm, SERVO_HIP_RIGHT, SERVO_FORWARD)
            time.sleep(0.5)
            move_servo(pwm, SERVO_HIP_RIGHT, SERVO_NEUTRAL)

        if fsr_left > 200:
            move_servo(pwm, SERVO_HIP_LEFT, SERVO_FORWARD)
            time.sleep(0.5)
            move_servo(pwm, SERVO_HIP_LEFT, SERVO_NEUTRAL)

        # Read MPU-6050 data for autonomous movement
        accel_x, accel_y = read_mpu()
        if accel_y > 10000:
            move_servo(pwm, SERVO_HIP_RIGHT, SERVO_FORWARD)
            move_servo(pwm, SERVO_HIP_LEFT, SERVO_BACKWARD)
            time.sleep(0.5)
            move_servo(pwm, SERVO_HIP_RIGHT, SERVO_NEUTRAL)
            move_servo(pwm, SERVO_HIP_LEFT, SERVO_NEUTRAL)
        elif accel_y < -10000:
            move_servo(pwm, SERVO_HIP_RIGHT, SERVO_BACKWARD)
            move_servo(pwm, SERVO_HIP_LEFT, SERVO_FORWARD)
            time.sleep(0.5)
            move_servo(pwm, SERVO_HIP_RIGHT, SERVO_NEUTRAL)
            move_servo(pwm, SERVO_HIP_LEFT, SERVO_NEUTRAL)

        time.sleep(0.1)
