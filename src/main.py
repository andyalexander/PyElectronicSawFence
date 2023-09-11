from ui import UI
from stepper import Stepper

from time import monotonic

_stepper = Stepper(1, 2, 3)

_stepper._stepper.set_acceleration(3000.0)
_stepper._stepper.set_max_speed(4800.0)

_ui = UI()

_stepper._UI = _ui
_ui._stepper = _stepper

last_is_moving = False
time_start = 0
time_max_speed = 0
max_speed = 0

try:
    while True:
        is_moving = _stepper.ISR()

        max_speed = max(max_speed, _stepper.get_speed())
        if (max_speed == 4800.0 and time_max_speed ==0 ):
            time_max_speed = monotonic()

        if is_moving and not last_is_moving:
            time_start = monotonic()
            last_is_moving = True

        if not is_moving and last_is_moving:
            print(f"Last move time: {monotonic() - time_start:.2f}, max speed:{max_speed:.1f}")
            print(f"Time to accel to max:  {time_max_speed-time_start:.2f}")

            time_max_speed = 0
            time_start = 0
            max_speed = 0
            last_is_moving = False

        if is_moving:
            print(f"Dist left:{_stepper._stepper.distance_to_go():.2f}  Speed:{_stepper.get_speed():.1f}  Interval:{_stepper._stepper._stepInterval:.0f}")
        _ui.mainloop()
except KeyboardInterrupt:
    pass
finally:
    _stepper.clean_up()
    _ui.clean_up()
