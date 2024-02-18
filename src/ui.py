# Project based on Youtube Video https://youtu.be/JEImn7s7x1o
# https://github.com/jengineer1/CNCTablesaw/blob/master/TableSaw_Controls_Jeremy_Fielding.py


from tkinter import (
    Tk,
    LabelFrame,
    Entry,
    Label,
    Button,
    END,
    N,
    S,
    E,
    W,
    DISABLED,
    NORMAL,
)
from enum import Enum, auto

import stepper


class MATHTYPE(Enum):
    NONE = auto()
    ADDITION = auto()
    SUBTRACTION = auto()
    MULTIPLICATION = auto()
    DIVISION = auto()


class STATE(Enum):
    IDLE = auto()
    MOVING = auto()


class UI:
    _stepper = None

    root = Tk()
    root.title("Table Saw Controls")
    _last_ui_state = STATE.IDLE

    # change the size of buttons and frames
    xpadframe = 0
    xpadbutton = 10
    xpadnums = 15
    xpadsymbols = 15
    ypadbutton = 10

    calframe = LabelFrame(root, text="Calculator", padx=xpadframe, pady=20)
    calframe.grid(row=0, column=0, padx=5, pady=10)
    buttons = {}
    always_disable = []

    fence_frame = LabelFrame(root, text="Fence", padx=xpadframe, pady=20)
    fence_frame.grid(row=0, column=1, sticky=N, padx=5, pady=10)

    # Entry panels and locations
    _entry_font = "Arial 20"
    calculator_entry = Entry(
        calframe,
        width=10,
        borderwidth=1,
        justify="right",
        font=_entry_font,
        takefocus=0,
    )
    calculator_entry.grid(row=0, column=0, columnspan=3, sticky=N + S + E + W, padx=5, pady=10)
    calculator_entry.insert(0, 0)

    fence_entry = Entry(
        fence_frame,
        width=10,
        borderwidth=1,
        justify="right",
        font=_entry_font,
        takefocus=0,
    )
    fence_entry.grid(row=0, column=0, columnspan=2, sticky=N + S + E + W, padx=5, pady=10)
    fence_entry.insert(0, 5)

    c_fence_position_label = Label(fence_frame, text="Current Position = ", font=("Arial", 12))
    c_fence_position_label.grid(row=3, column=0)

    c_fence_position_entry = Entry(fence_frame, width=7, borderwidth=2)
    c_fence_position_entry.grid(row=3, column=1)
    c_fence_position_entry.insert(0, 0)

    math_operation = MATHTYPE.NONE
    first_num = 0.0

    def __init__(self):
        self.init_layout()
        self.is_closing = False
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.is_closing = True

    def fence_move_to(self) -> None:
        loc = self.fence_entry.get()
        if loc != "":
            loc = float(loc)
            self._stepper.move_to(loc)
            self.set_current_position(loc)

    def fence_move_by(self) -> None:
        dist = self.fence_entry.get()
        if dist != "":
            dist = float(dist)
            if dist != 0:
                self._stepper.move_by(dist)
                self.set_current_position(self.get_current_position() + dist)

    def set_stepper(self, stepper: stepper.Stepper) -> None:
        self._stepper = stepper

    def set_current_position(self, position: float) -> None:
        self.c_fence_position_entry.delete(0, END)
        self.c_fence_position_entry.insert(0, str(position))

    def get_current_position(self) -> float:
        return float(self.c_fence_position_entry.get())

    # Calculator functions
    def button_click(self, number):
        current = self.calculator_entry.get()
        if current == "0":  # if we only have zero, prevent leading zeros in the display
            current = ""
        self.calculator_entry.delete(0, END)
        self.calculator_entry.insert(0, str(current) + str(number))

    def button_clear(self):
        self.calculator_entry.delete(0, END)
        self.calculator_entry.insert(0, "0")
        self.first_num = 0

    def button_equal(self):
        second_number = self.calculator_entry.get()
        self.calculator_entry.delete(0, END)

        if second_number != "":
            if self.math_operation == MATHTYPE.ADDITION:
                self.calculator_entry.insert(0, self.first_num + float(second_number))

            if self.math_operation == MATHTYPE.SUBTRACTION:
                self.calculator_entry.insert(0, self.first_num - float(second_number))

            if self.math_operation == MATHTYPE.MULTIPLICATION:
                self.calculator_entry.insert(0, self.first_num * float(second_number))

            if self.math_operation == MATHTYPE.DIVISION:
                self.calculator_entry.insert(0, self.first_num / float(second_number))

    def button_operand(self, operand: MATHTYPE) -> None:
        first_number = self.calculator_entry.get()
        self.math_operation = operand
        self.first_num = float(first_number)
        self.calculator_entry.delete(0, END)

    def Inch_to_mm(self):
        C_num = self.calculator_entry.get()
        ans_in_mm = float(C_num) * 25.4
        self.calculator_entry.delete(0, END)
        self.calculator_entry.insert(0, str(ans_in_mm))

    def mm_to_Inch(self):
        C_num = self.calculator_entry.get()
        ans_in_inch = float(C_num) / 25.4
        self.calculator_entry.delete(0, END)
        self.calculator_entry.insert(0, str(ans_in_inch))

    def fence_calc_to_fence_target(self):
        val = self.calculator_entry.get()
        if val != "":
            c_num = float(val)
            self.calculator_entry.delete(0, END)
            self.fence_entry.delete(0, END)
            self.fence_entry.insert(0, str(c_num))

    def fence_calc_to_current(self):
        calc = self.calculator_entry.get()
        if calc != "":
            c_num = float(self.calculator_entry.get())
            self.calculator_entry.delete(0, END)
            self.c_fence_position_entry.delete(0, END)
            self.c_fence_position_entry.insert(0, str(c_num))

    def fence_clear(self):
        self.fence_entry.delete(0, END)

    def fence_enable_toggle(self):
        new_state = not self._stepper.get_enabled()
        self.set_frame_state(self.fence_frame, ["Enable"], new_state)
        self._stepper.set_enabled(new_state)

    def init_layout(self) -> None:
        # define numeric buttons
        for i in range(10):
            button_temp = Button(
                self.calframe,
                text=str(i),
                padx=self.xpadnums,
                pady=self.ypadbutton,
                command=lambda x=i: self.button_click(x),
            )
            self.buttons[f"button_{i}"] = button_temp

        button_decimal = Button(
            self.calframe,
            text=".",
            padx=self.xpadnums,
            pady=self.ypadbutton,
            command=lambda: self.button_click("."),
        )
        button_add = Button(
            self.calframe,
            text="+",
            padx=self.xpadsymbols,
            pady=self.ypadbutton,
            command=lambda: self.button_operand(MATHTYPE.ADDITION),
        )
        button_equal = Button(
            self.calframe,
            text="=",
            padx=self.xpadsymbols,
            pady=self.ypadbutton,
            command=self.button_equal,
        )

        button_clear = Button(
            self.calframe,
            text="Clear",
            padx=self.xpadsymbols,
            pady=self.ypadbutton,
            command=self.button_clear,
        )

        button_subtract = Button(
            self.calframe,
            text="-",
            padx=self.xpadsymbols,
            pady=self.ypadbutton,
            command=lambda: self.button_operand(MATHTYPE.SUBTRACTION),
        )

        button_multiply = Button(
            self.calframe,
            text="*",
            padx=self.xpadsymbols,
            pady=self.ypadbutton,
            command=lambda: self.button_operand(MATHTYPE.MULTIPLICATION),
        )

        button_divide = Button(
            self.calframe,
            text="/",
            padx=self.xpadsymbols,
            pady=self.ypadbutton,
            command=lambda: self.utton_operand(MATHTYPE.DIVISION),
        )

        button_inch_to_mm = Button(
            self.calframe,
            text="Inch to mm",
            padx=self.xpadbutton,
            pady=self.ypadbutton,
            command=self.Inch_to_mm,
        )

        button_mm_to_inch = Button(
            self.calframe,
            text="mm to Inch",
            padx=self.xpadbutton,
            pady=self.ypadbutton,
            command=self.mm_to_Inch,
            state=DISABLED,
        )

        # Define Other Buttons

        button_move_fence_to = Button(
            self.fence_frame,
            text="Move To",
            padx=self.xpadbutton,
            pady=self.ypadbutton,
            command=self.fence_move_to,
        )

        button_movefence_by = Button(
            self.fence_frame,
            text="Move By",
            padx=self.xpadbutton,
            pady=self.ypadbutton,
            command=self.fence_move_by,
        )

        button_calc_to_fence_target = Button(
            self.fence_frame,
            text="Grab number",
            padx=self.xpadbutton,
            pady=self.ypadbutton,
            command=self.fence_calc_to_fence_target,
        )

        button_calc_to_fence_current = Button(
            self.fence_frame,
            text="Grab number",
            padx=self.xpadbutton,
            pady=self.ypadbutton,
            command=self.fence_calc_to_current,
        )

        button_fence_clear = Button(
            self.fence_frame,
            text="Clear",
            padx=self.xpadbutton,
            pady=self.ypadbutton,
            command=self.fence_clear,
        )

        button_fence_enable = Button(
            self.fence_frame,
            text="Enable",
            padx=self.xpadbutton,
            pady=self.ypadbutton,
            command=self.fence_enable_toggle,
        )

        # Put the numeric buttons on the screen
        for i in range(9):
            r = 4 - i // 3
            c = i % 3
            self.buttons[f"button_{i + 1}"].grid(
                row=r, column=c, columnspan=1, sticky=N + S + E + W
            )

        self.buttons["button_0"].grid(
            row=5, column=0, columnspan=2, sticky=N + S + E + W
        )
        button_decimal.grid(row=5, column=2, columnspan=1, sticky=N + S + E + W)

        button_clear.grid(row=1, column=0, columnspan=2, sticky=N + S + E + W)
        button_equal.grid(row=1, column=2, columnspan=2, sticky=N + S + E + W)

        button_add.grid(row=2, column=3, sticky=N + S + E + W)
        button_subtract.grid(row=3, column=3, sticky=N + S + E + W)
        button_multiply.grid(row=4, column=3, sticky=N + S + E + W)
        button_divide.grid(row=5, column=3, sticky=N + S + E + W)

        button_inch_to_mm.grid(row=8, column=1, columnspan=2, sticky=N + S + E + W)
        button_mm_to_inch.grid(row=7, column=1, columnspan=2, sticky=N + S + E + W)

        button_move_fence_to.grid(row=1, column=0, sticky=N + S + E + W)
        button_movefence_by.grid(row=1, column=1, sticky=N + S + E + W)

        button_calc_to_fence_target.grid(row=0, column=2, sticky=N + S + E + W)

        button_calc_to_fence_current.grid(row=4, column=1)

        button_fence_clear.grid(row=2, column=0, sticky=N + S + E + W)
        button_fence_enable.grid(row=5, column=0, columnspan=3, sticky=N + S + E + W)

    def mainloop(self, is_moving: bool) -> None:
        if is_moving:
            if self._last_ui_state != STATE.MOVING:
                self.set_ui_state(enabled=False)
                self._last_ui_state = STATE.MOVING
            else:
                pass
        else:
            if self._last_ui_state != STATE.IDLE:
                self.set_ui_state(enabled=True)
                self._last_ui_state = STATE.IDLE
            else:
                pass

        self.root.update_idletasks()
        self.root.update()

    def clean_up(self) -> None:
        self.root.destroy()

    def set_ui_state(self, enabled: bool = True) -> None:
        frames = [self.calframe, self.fence_frame]
        exclude = ["mm to Inch"]
        for frame in frames:
            self.set_frame_state(frame, exclude, enabled)

    def set_frame_state(self, frame: LabelFrame, exclude: list, enable: bool) -> None:
        for child in frame.winfo_children():
            if "text" in child.config().keys():
                if child["text"] not in exclude:
                    if enable:
                        child.configure(state=NORMAL)
                    else:
                        child.configure(state=DISABLED)

    def finalise(self):
        # Finish any initalisation
        self.set_frame_state(self.fence_frame, ["Enable"], self._stepper.get_enabled())
