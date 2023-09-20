from AccelStepper import AccelStepper

# import ui


class Stepper:
    STEPS_PER_MM = 96

    def __init__(self, gpioHandler, pinStep: int, pinDirection: int, pinEnable: int) -> None:
        self._UI = None
        self._pinStep = pinStep
        self._pinDirection = pinDirection
        self._pinEnable = pinEnable
        self._stepper = AccelStepper(
            gpioHandler, self._pinStep, self._pinDirection, self._pinEnable, True
        )

    def set_UI(self, ui) -> None:
        self._UI = ui

    def convert_dist_to_steps(self, distance: float) -> int:
        return round(distance * self.STEPS_PER_MM, 0)

    def move_to(self, newPosition: float) -> None:
        no_steps = self.convert_dist_to_steps(newPosition)
        self._stepper.move_to(no_steps)
        # print(f"Move to: {newPosition} [{no_steps} steps]")

    def move_by(self, distance: float) -> None:
        no_steps = self.convert_dist_to_steps(distance)
        self._stepper.move(no_steps)
        # print(f"Move by: {distance} [{no_steps} steps]")

    def get_speed(self) -> float:
        return self._stepper._speed

    def clean_up(self) -> None:
        self._stepper.clean_up()

    def ISR(self) -> bool:
        is_moving = self._stepper.run()
        return is_moving
