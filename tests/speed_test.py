from stepper import Stepper
from time import monotonic_ns


###
# Determine the min loop time in order to calculate the max speed
###

try:
    import RPi.GPIO as gpio
except ImportError:
    from RPi_debug import GPIO as gpio

try:
    stepper = Stepper(gpio, 27, 21, 13)
    stepper._stepper.set_acceleration(1000000.0)
    stepper._stepper.set_max_speed(1000000.0)

    n = 100000

    stepper.move_by(1000)
    time_start = monotonic_ns()

    for _ in range(n):
        stepper.isr()

    time_end = monotonic_ns()

    print(f"{(time_end-time_start)/n}ns/step theoretical max speed")


except KeyboardInterrupt:
    pass
finally:
    stepper.clean_up()
