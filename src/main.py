from ui import UI
from stepper import Stepper

from time import monotonic, perf_counter_ns

try:
    import RPi.GPIO as gpio
except ImportError:
    from RPi_debug import GPIO as gpio

_stepper = Stepper(gpio, 17, 27, 22)

_stepper._stepper.set_acceleration(3000.0)
_stepper._stepper.set_max_speed(4800.0)

_ui = UI()

_stepper._UI = _ui
_ui._stepper = _stepper

last_is_moving = False
last_ui_update = 0
ui_update_interval_moving = 0.5 * 1e9
ui_update_interval_idle = 0.1 * 1e9

time_start = 0
time_max_speed = 0
max_speed = 0

total_time = 0
time_loop_start = 0

try:
    while True and _ui.isClosing is False:
        is_moving = _stepper.ISR()

        max_speed = max(max_speed, _stepper.get_speed())
        # if max_speed == 4800.0 and time_max_speed == 0:
        # time_max_speed = monotonic()

        if is_moving and not last_is_moving:
            time_start = monotonic()
            last_is_moving = True

        if not is_moving and last_is_moving:
            print(
                f"Last move time: {monotonic() - time_start:.2f}, max speed:{max_speed:.1f}"
            )
            # print(f"Time to accel to max:  {time_max_speed-time_start:.2f}")

            time_max_speed = 0
            time_start = 0
            max_speed = 0
            last_is_moving = False

        time_now = perf_counter_ns()
        if is_moving:
            if time_now - last_ui_update > ui_update_interval_moving:
                _ui.mainloop(is_moving)
                last_ui_update = time_now
            else:
                pass
        else:
            _ui.mainloop(is_moving)


except KeyboardInterrupt:
    pass
finally:
    _stepper.clean_up()
    _ui.clean_up()
