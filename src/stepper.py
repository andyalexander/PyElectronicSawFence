from AccelStepper import AccelStepper
import ui


class Stepper:
    currentPosition = 0
    _UI = None
    STEPS_PER_MM = 400

    def __init__(self, pin1: int, pin2: int, pinEnable: int) -> None:
        self._pin1 = pin1
        self._pin2 = pin2
        self._pinEnable = pinEnable
        self._setpper = AccelStepper(self._pin1, self._pin2, self._pinEnable, False)

    def set_UI(self, ui: ui.UI) -> None:
        self._UI = ui

    def convert_dist_to_steps(self, distance: float) -> int:
        return round(distance * self.STEPS_PER_MM, 0)

    def move_to(self, newPosition: float) -> None:
        no_steps = self.convert_dist_to_steps(newPosition)
        # self._setpper.move_to(no_steps)
        print(f"Move to: {newPosition} [{no_steps} steps]")

    def move_by(self, distance: float) -> None:
        no_steps = self.convert_dist_to_steps(distance)
        self._setpper.move(no_steps)
