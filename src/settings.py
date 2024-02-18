import logging

class Config():
    fence_accel = 1000.0
    fence_max_speed = 750.0
    fence_pin_step = 27
    fence_pin_direction = 21
    fence_pin_enable = 13

    fence_microsteps = 2.0
    fence_steps_per_rev = 200.0
    fence_gear_ratio = 3.0  # ratio of stepper rotation to spur
    fence_spur_pd = 25.0  # pitch diameter of spur

    fence_backlash = 2.0        # number of steps for backlash
    fence_backlash_mult = 2     # number of times backlash to move first

    ui_update_interval_moving = 0.5 * 1e9
    ui_update_interval_idle = 0.1 * 1e9

    log_level = logging.DEBUG

    version = "0.0.3"


config = Config()
