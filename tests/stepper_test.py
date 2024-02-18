from time import sleep

try:
    import RPi.GPIO as GPIO
except ImportError:
    from RPi_debug import GPIO


def inp(mess):
    print(f"{mess}...press <enter>")
    return input()


# set this for the motor
step_angle = 1.8
microsteps = 2
steps_per_rev = (360 / step_angle) * microsteps
pulse_width = 0.001  # time between pulses

# set this for the board
pin_step = 27
pin_direction = 21
pin_enable = 13
enable_invert = False
step_invert = False
direction_invert = False

# Pulse is high by default, pull low then high to pulse.  NOT pulse up then down

pins = [pin_step, pin_direction, pin_enable]


GPIO.setmode(GPIO.BCM)
# inp("Setmode complete: board in default state")

GPIO.setup(pin_step, GPIO.OUT)
GPIO.setup(pin_direction, GPIO.OUT)
GPIO.setup(pin_enable, GPIO.OUT)

GPIO.output(pin_direction, False ^ direction_invert)
GPIO.output(pin_enable, False ^ enable_invert)
GPIO.output(pin_step, True ^ step_invert)
# inp("Init pins complete")

inp("Step test (direction = true)")
GPIO.output(pin_enable, True ^ enable_invert)
GPIO.output(pin_direction, True ^ direction_invert)
sleep(0.5)

# print(int(steps_per_rev))
for _ in range(int(steps_per_rev)):
    GPIO.output(pin_step, False ^ step_invert)
    sleep(pulse_width)
    GPIO.output(pin_step, True ^ step_invert)
    sleep(pulse_width)


GPIO.output(pin_enable, False ^ enable_invert)

inp("About to cleanup")
GPIO.cleanup()
