# Original: https://github.com/pedromneto97/AccelStepper-MicroPython/blob/master/AccelStepper.py

from math import sqrt, fabs

# from machine import Pin
# from RPi import Pin
from RPi import GPIO as gpio
from time import sleep, monotonic_ns


def sleep_ms(duration: float) -> None:
    sleep(duration / 1000)


def sleep_us(duration: float) -> None:
    sleep(duration / 1000000)


def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))


DIRECTION_CCW = False  # Counter-Clockwise
DIRECTION_CW = True  # Clockwise


class AccelStepper:
    def __init__(
        self, pinStep: int, pinDirection: int, pinEnable: int = 0xFF, enableOnStart=True
    ):
        self._currentPos = 0
        self._targetPos = 0
        self._speed = 0.0
        self._maxSpeed = 0.0
        self._acceleration = 0.0

        self._stepInterval = 0
        self._minPulseWidth = 5  # time in us
        self._minLeadTime = 10  # min time the enable pin must be ahead
        self._lastStepTime = 0

        self._n = 0
        self._c0 = 0.0
        self._cn = 0.0
        self._cmin = 1.0
        self._direction = DIRECTION_CCW
        self._lastDirection = DIRECTION_CCW

        self._pinEnable = pinEnable
        self._pinStep = pinStep
        self._pinDirection = pinDirection
        self._pinEnableInverted = True
        self._pinStepInverted = True
        self._pinDirectionInverted = True

        self._backlash = 1  # distance to take up backlash
        self._backlash_adjustment = False

        self._init_pins()

        if enableOnStart:
            self.enable_outputs()

    def _init_pins(self) -> None:
        gpio.setmode(gpio.BCM)
        gpio.setup(self._pinStep, gpio.OUT)
        gpio.setup(self._pinDirection, gpio.OUT)
        gpio.setup(self._pinEnable, gpio.OUT)

    def move_to(self, absolute: int) -> None:
        # absolute_with_backlash = absolute
        # if self._currentPos > absolute:      # we are moving towards blade, so have backlash
            # absolute_with_backlash = absolute - self._backlash
            # self._backlash_adjustment = True

        if self._targetPos != absolute:
            self._targetPos = absolute
            self.compute_new_speed()

    def move(self, relative: int) -> None:
        self.move_to(self._currentPos + relative)

    def run_speed(self) -> bool:
        if not self._stepInterval:
            return False
        time = monotonic_ns() // 1000
        if (time - self._lastStepTime) >= self._stepInterval:
            if self._direction == DIRECTION_CW:
                self._currentPos += 1
            else:
                self._currentPos -= 1
            self.step()
            self._lastStepTime = monotonic_ns() // 1000
            return True
        else:
            return False

    def distance_to_go(self) -> int:
        return self._targetPos - self._currentPos

    def target_position(self) -> int:
        return self._targetPos

    def current_position(self) -> int:
        return self._currentPos

    def set_current_position(self, position: int) -> None:
        self._targetPos = self._currentPos = position
        self._n = 0
        self._stepInterval = 0
        self._speed = 0.0

    def compute_new_speed(self) -> None:
        distance_to = self.distance_to_go()
        steps_to_stop = int((self._speed * self._speed) / (2.0 * self._acceleration))
        if distance_to == 0 and steps_to_stop <= 1:
            self._stepInterval = 0
            self._speed = 0.0
            self._n = 0
            return
        if distance_to > 0:
            if self._n > 0:
                if (steps_to_stop >= distance_to) or self._direction == DIRECTION_CCW:
                    self._n = -steps_to_stop
            elif self._n < 0:
                if (steps_to_stop < distance_to) and self._direction == DIRECTION_CW:
                    self._n = -self._n
        elif distance_to < 0:
            if self._n > 0:
                if (steps_to_stop >= -distance_to) or self._direction == DIRECTION_CW:
                    self._n = -steps_to_stop
            elif self._n < 0:
                if (steps_to_stop < -distance_to) and self._direction == DIRECTION_CCW:
                    self._n = -self._n
        if self._n == 0:
            self._cn = self._c0
            self._direction = DIRECTION_CW if distance_to > 0 else DIRECTION_CCW
        else:
            self._cn = self._cn - ((2.0 * self._cn) / ((4.0 * self._n) + 1))
            self._cn = max(self._cn, self._cmin)
        self._n += 1
        self._stepInterval = self._cn
        self._speed = 1000000.0 / self._cn
        if self._direction == DIRECTION_CCW:
            self._speed = -self._speed

    def run(self) -> bool:
        if self.run_speed():
            self.compute_new_speed()
        return self._speed != 0.0 or self.distance_to_go() != 0

    def set_max_speed(self, speed: float) -> None:
        if speed < 0.0:
            speed = -speed
        if self._maxSpeed != speed:
            self._maxSpeed = speed
            self._cmin = 1000000.0 / speed
            if self._n > 0:
                self._n = int((self._speed * self._speed) / (2.0 * self._acceleration))
                self.compute_new_speed()

    def max_speed(self):
        return self._maxSpeed

    def set_acceleration(self, acceleration: float) -> None:
        if acceleration == 0.0:
            return
        if acceleration < 0.0:
            acceleration = -acceleration
        if self._acceleration != acceleration:
            self._n = self._n * (self._acceleration / acceleration)
            self._c0 = 0.676 * sqrt(2.0 / acceleration) * 1000000.0
            self._acceleration = acceleration
            self.compute_new_speed()

    def set_speed(self, speed: float) -> None:
        if speed == self._speed:
            return
        speed = constrain(speed, -self._maxSpeed, self._maxSpeed)
        if speed == 0.0:
            self._stepInterval = 0
        else:
            self._stepInterval = fabs(1000000.0 / speed)  # adjust to use ns not us
            self._direction = DIRECTION_CW if speed > 0.0 else DIRECTION_CCW
        self._speed = speed

    def speed(self) -> float:
        return self._speed

    def step(self) -> None:
        if self._lastDirection != self._direction:
            gpio.output(
                self._pinDirection, self._direction ^ self._pinDirectionInverted
            )
            sleep_us(
                self._minLeadTime
            )  # sleep for amount to let direction change be noted

        gpio.output(self._pinStep, True ^ self._pinStepInverted)
        sleep_us(self._minPulseWidth)
        gpio.output(self._pinStep, False ^ self._pinStepInverted)

    def disable_outputs(self) -> None:
        if self._pinEnable != 0xFF:
            gpio.output(self._pinEnable, False ^ self._enableInverted)
            sleep_us(self._minEnableLeadTime)

    def enable_outputs(self) -> None:
        if self._pinEnable != 0xFF:
            gpio.output(self._pinEnable, True ^ self._enableInverted)
            sleep_us(self._minEnableLeadTime)

    def run_to_position(self) -> None:
        while self.run():
            pass

    def run_speed_to_position(self) -> bool:
        if self._targetPos == self._currentPos:
            return False
        if self._targetPos > self._currentPos:
            self._direction = DIRECTION_CW
        else:
            self._direction = DIRECTION_CCW
        return self.run_speed()

    def run_to_new_position(self, position: int) -> None:
        self.move_to(position)
        self.run_to_position()

    def stop(self) -> None:
        if self._speed != 0.0:
            steps_to_stop = (
                int((self._speed * self._speed) / (2.0 * self._acceleration)) + 1
            )
            if self._speed > 0:
                self.move(steps_to_stop)
            else:
                self.move(-steps_to_stop)

    def is_running(self) -> bool:
        return not (self._speed == 0 and self._targetPos == self._currentPos)

    def clean_up(self) -> None:
        gpio.cleanup()
