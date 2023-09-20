import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
pins = [17, 27, 22]

for pin in pins:
    GPIO.setup(pin, GPIO.OUT)


try:
    while True:
        for pin in pins:
            print(pin)
            GPIO.output(pin, GPIO.LOW)
            time.sleep(0.5)
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(0.5)

except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
