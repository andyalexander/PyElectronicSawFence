from AccelStepper import AccelStepper
from math import pi
import logging
from settings import config
from enum import Enum, auto

logger = logging.getLogger(__name__)


class Direction(Enum):
    NONE = auto()
    LEFT = auto()
    RIGHT = auto()
    BACKLASH = auto()


class Stepper:
    def __init__(
            self, gpio_handler, pin_step: int, pin_direction: int, pin_enable: int,
            microsteps: int, steps_per_rev: int, gear_ratio: float, spur_pd: int
    ) -> None:

        self._microsteps = microsteps
        self._steps_per_rev = steps_per_rev
        self._gear_ratio = gear_ratio  # ratio of stepper rotation to spur
        self._spur_pd = spur_pd  # pitch diameter of spur

        self._UI = None
        self._pin_step = pin_step
        self._pin_direction = pin_direction
        self._pin_enable = pin_enable
        self._stepper = AccelStepper(
            gpio_handler, self._pin_step, self._pin_direction, self._pin_enable, False
        )

        self.was_moving = False
        self.last_direction = Direction.NONE

    def set_ui(self, ui) -> None:
        self._UI = ui

    def convert_dist_to_steps(self, distance: float) -> int:
        return round(
            self._steps_per_rev * self._microsteps * (distance / (self._spur_pd * pi))
        )

    def set_direction(self, no_steps: int) -> None:
        if no_steps < 0:
            self.last_direction = Direction.LEFT
        elif no_steps > 0:
            self.last_direction = Direction.RIGHT
        else:
            self.last_direction = Direction.NONE

    def move_to(self, new_position: float) -> None:
        no_steps = self.convert_dist_to_steps(new_position)
        self.set_direction(no_steps)
        self._stepper.move_to(no_steps)

    def move_by(self, distance: float) -> None:
        no_steps = self.convert_dist_to_steps(distance)
        self.set_direction(no_steps)
        self._stepper.move(no_steps)

    def run_backlash(self) -> bool:
        is_moving = False
        if self.last_direction == Direction.RIGHT:
            no_steps = -(config.fence_backlash_mult * config.fence_backlash)
            logger.info(f"Starting backlash compensation: {no_steps} steps")
            self.last_direction = Direction.BACKLASH
            self._stepper.move(no_steps)
            is_moving = True
        elif self.last_direction == Direction.BACKLASH:
            no_steps = (config.fence_backlash_mult - 1) * config.fence_backlash
            logger.info(f"finishing backlash compensation: {no_steps} steps")
            self.last_direction = Direction.NONE
            self._stepper.move(no_steps)
            is_moving = True

        return is_moving

    def get_speed(self) -> float:
        return self._stepper.speed

    def clean_up(self) -> None:
        self._stepper.clean_up()

    def set_enabled(self, enabled: bool) -> None:
        if enabled:
            self._stepper.enable_outputs()
        else:
            self._stepper.disable_outputs()

    def get_enabled(self) -> bool:
        return self._stepper.isEnabled

    def isr(self) -> bool:
        is_moving = self._stepper.run()

        if not is_moving:
            # if we have just stopped, run the backlash comp
            if self.was_moving:
                is_moving = self.run_backlash()

        self.was_moving = is_moving
        return is_moving
