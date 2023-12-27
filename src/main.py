from ui import UI
from stepper import Stepper
from settings import config

from time import monotonic, perf_counter_ns

try:
    import RPi.GPIO as GPIO
except ImportError:
    from RPi_debug import GPIO as GPIO

_stepper = Stepper(GPIO,
                   config.fence_pin_step,
                   config.fence_pin_direction,
                   config.fence_pin_enable,
                   config.fence_microsteps,
                   config.fence_steps_per_rev,
                   config.fence_gear_ratio,
                   config.fence_spur_pd
                   )


# TODO: must set accel before speed otherwise calcs don't happen in correct order
_stepper._stepper.set_acceleration(config.fence_accel)
_stepper._stepper.set_max_speed(config.fence_max_speed)

_ui = UI()

_stepper._UI = _ui
_ui._stepper = _stepper

_ui.finalise()

last_is_moving = False
last_ui_update = 0
ui_update_interval_moving = 0.5 * 1e9
ui_update_interval_idle = 0.1 * 1e9

time_start = 0

total_time = 0
time_loop_start = 0

try:
    while True and _ui.is_closing is False:
        is_moving = _stepper.isr()

        if is_moving and not last_is_moving:
            last_is_moving = True
            time_start = monotonic()

        if not is_moving and last_is_moving:
            print(f"Last move time: {monotonic() - time_start:.2f}")

            time_start = 0
            last_is_moving = False

        if is_moving:
            time_now = perf_counter_ns()
            if time_now - last_ui_update > ui_update_interval_moving:
                _ui.mainloop(is_moving)
                last_ui_update = time_now
        else:
            _ui.mainloop(is_moving)


except KeyboardInterrupt:
    pass
finally:
    print("Cleaning up...")
    _stepper.clean_up()
    _ui.clean_up()
