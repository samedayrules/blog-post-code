# Originally posted:
# https://samedayrules.com/using-the-voltage-level-shifter-board/

# Libraries
import RPi.GPIO as GPIO
import time

# GPIO mode (BCM = use logical pin numbers, e.g., GPIO 2 (I2C1 SDA))
GPIO.setmode(GPIO.BCM)

# Set GPIO pins
GPIO_TRIGGER = 27 # make this go HIGH for at least 10us to initiate pulse
GPIO_ECHO = 17    # the amount of time this goes HIGH represents distance

# Set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

# Make sure trigger starts LOW
GPIO.output(GPIO_TRIGGER, GPIO.LOW)

# Timeouts used to stop wait loops below in case of hardware failure
TIMEOUT_RISING_EDGE = 1.5  # seconds to wait for ECHO rising edge
TIMEOUT_FALLING_EDGE = 2.0 # second to wait for ECHO falling edge

# Initiate sensor pulse, read pulse width, and return distance in cm
def distance():
    # Calculate timeouts for how long to wait for rising/falling edge of echo
    # Set trigger to HIGH, wait for 10us, then set trigger to LOW
    # Save the start time
    # Wait for echo to go HIGH
    # Save the stop time
    rising_timeout = time.perf_counter() + TIMEOUT_RISING_EDGE
    falling_timeout = time.perf_counter() + TIMEOUT_FALLING_EDGE
    GPIO.output(GPIO_TRIGGER, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, GPIO.LOW)
    while GPIO.input(GPIO_ECHO) == GPIO.LOW:
        if time.perf_counter() > rising_timeout:
            return 0.0
    start_time = time.perf_counter()
    while GPIO.input(GPIO_ECHO) == GPIO.HIGH:
        if time.perf_counter() > falling_timeout:
            return 0.0
    stop_time = time.perf_counter()

    # Calculate time difference between start and stop
    delta_T = stop_time - start_time

    # Speed of sound is nominally 34,300 cm/s
    # Multiply by the speed of sound/2 = 34300/2 = 17150.0
    # We divide by two because we're timing the round trip (there-back)
    d = delta_T * 17150.0

    return d

if __name__ == '__main__':
    try:
        while True:
            # Measure the distance, print its value, and wait for a bit
            dist = distance()
            # Sensor range is from 2 cm to 400 cm - flag anything out of range
            if dist > 2.0 and dist < 400.0:
              print("Range: %.1f cm / %.1f in" % (dist, dist/2.54))
            else:
              print("Range: invalid")
            time.sleep(1)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("\nTerminated by user")
        GPIO.cleanup()
