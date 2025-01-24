import serial
import smbus
import time

# Servo and Sensor Configurations
SERVO_HIP_RIGHT = 0
SERVO_HIP_LEFT = 1
SERVO_KNEE_RIGHT = 2
SERVO_KNEE_LEFT = 3

# MPU-6050 Addresses
MPU_ADDRESS = 0x68
bus = smbus.SMBus(1)  # I2C bus for MPU-6050

# Arduino Serial Connection
arduino = serial.Serial('COM3', 9600, timeout=1)

# Initialize MPU-6050
def init_mpu():
    bus.write_byte_data(MPU_ADDRESS, 0x6B, 0)  # Wake up MPU-6050

# Read accelerometer and gyroscope data from MPU-6050
def read_mpu():
    accel_x = bus.read_byte_data(MPU_ADDRESS, 0x3B)
    accel_y = bus.read_byte_data(MPU_ADDRESS, 0x3D)
    return accel_x, accel_y

# Move a servo to a specified angle
def move_servo(servo_id, angle):
    command = f"{servo_id}:{angle}\n"
    arduino.write(command.encode())

# Smoothly move a servo from start_angle to end_angle
def smooth_move_servo(servo_id, start_angle, end_angle, step=5):
    if start_angle < end_angle:
        for angle in range(start_angle, end_angle + 1, step):
            move_servo(servo_id, angle)
            time.sleep(0.05)
    else:
        for angle in range(start_angle, end_angle - 1, -step):
            move_servo(servo_id, angle)
            time.sleep(0.05)

# Simulated FSR reading (replace with actual sensor input)
def read_fsr(handle):
    # Replace with logic to read analog input for FSR
    if handle == "right":
        return 1  # Example: Handle is being pulled
    if handle == "left":
        return 0  # Example: Handle is idle

# Autonomous walking logic
def autonomous_walk():
    accel_x, accel_y = read_mpu()
    if accel_y > 50:  # Example: Detect forward tilt
        smooth_move_servo(SERVO_HIP_RIGHT, 0, 90)
        time.sleep(0.5)
        smooth_move_servo(SERVO_HIP_RIGHT, 90, 0)
    if accel_y < -50:  # Example: Detect backward tilt
        smooth_move_servo(SERVO_HIP_LEFT, 0, 90)
        time.sleep(0.5)
        smooth_move_servo(SERVO_HIP_LEFT, 90, 0)

# Main Loop
if __name__ == "__main__":
    init_mpu()
    mode = "manual"  # Default to manual mode

    while True:
        # Check mode and perform actions accordingly
        if mode == "manual":
            # Read FSR inputs for manual control
            if read_fsr("right"):
                smooth_move_servo(SERVO_HIP_RIGHT, 0, 90)
            else:
                smooth_move_servo(SERVO_HIP_RIGHT, 90, 0)

            if read_fsr("left"):
                smooth_move_servo(SERVO_HIP_LEFT, 0, 90)
            else:
                smooth_move_servo(SERVO_HIP_LEFT, 90, 0)
        elif mode == "autonomous":
            # Perform autonomous walking
            autonomous_walk()

        time.sleep(0.1)
