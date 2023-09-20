from stepper import Stepper
from time import time

try:
    import RPi.GPIO as gpio
except ImportError:
    from RPi_debug import GPIO as gpio

try:
    max_speeds = [3000, 4000, 5000, 10000]

    stepper = Stepper(gpio, 17, 27, 22)
    stepper._stepper.set_acceleration(3000.00)

    for max_speed in max_speeds:
        stepper._stepper.stop()
        stepper._stepper.set_max_speed(max_speed)
        stepper.move_by(1000)

        start_time = time()

        while stepper.ISR():
            pass
        end_time = time()

        print(max_speed, end_time - start_time)

except KeyboardInterrupt:
    pass
finally:
    stepper.clean_up()
