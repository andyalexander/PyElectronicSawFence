# Written By: Jeremy Fielding
# Project based on Youtube Video https://youtu.be/JEImn7s7x1o
# https://github.com/jengineer1/CNCTablesaw/blob/master/TableSaw_Controls_Jeremy_Fielding.py


from tkinter import Tk, LabelFrame, Entry, Label, Button, END, N, S, E, W
from enum import Enum, auto

import stepper

# from RPi import GPIO


class MATHTYPE(Enum):
    NONE = auto()
    ADDITION = auto()
    SUBTRACTION = auto()
    MULTIPLICATION = auto()
    DIVISION = auto()


class UI:
    _stepper = None

    root = Tk()
    root.title("Table Saw Controls")

    # change the size of buttons and frames
    xpadframe = 0
    xpadbutton = 10
    xpadnums = 15
    xpadsymbols = 15
    ypadbutton = 10

    calframe = LabelFrame(root, text="Calculator", padx=xpadframe, pady=20)
    calframe.grid(row=0, column=0, padx=5, pady=10)
    buttons = {}

    fenceframe = LabelFrame(root, text="Fence", padx=xpadframe, pady=20)
    fenceframe.grid(row=0, column=1, sticky=N, padx=5, pady=10)

    # Entry panels and locations
    _entry_font = "Arial 20"
    cal = Entry(
        calframe,
        width=10,
        borderwidth=1,
        justify="right",
        font=_entry_font,
        takefocus=0,
    )
    cal.grid(row=0, column=0, columnspan=3, sticky=N + S + E + W, padx=5, pady=10)
    cal.insert(0, 0)

    fen = Entry(
        fenceframe,
        width=10,
        borderwidth=1,
        justify="right",
        font=_entry_font,
        takefocus=0,
    )
    fen.grid(row=0, column=0, columnspan=2, sticky=N + S + E + W, padx=5, pady=10)
    fen.insert(0, 0)

    C_fence_position = Label(fenceframe, text="Current Position = ", font=("Arial", 12))
    C_fence_position.grid(row=3, column=0)

    Current_fence_position = Entry(fenceframe, width=7, borderwidth=2)
    Current_fence_position.grid(row=3, column=1)
    Current_fence_position.insert(0, 0)

    math_operation = MATHTYPE.NONE
    first_num = 0.0

    def __init__(self):
        self.init_layout()

    def move_fence_to_location(self) -> None:
        loc = self.fen.get()
        loc = float(loc)
        self._stepper.move_to(loc)

    def set_stepper(self, stepper:stepper.Stepper) -> None:
        self._stepper = stepper

    def set_current_position(self, position):
        self.Current_fence_position.delete(0, END)
        self.Current_fence_position.insert(0, str(position))

    # Calculator functions
    def button_click(self, number):
        current = self.cal.get()
        if current == "0":  # if we only have zero, prevent leading zeros in the display
            current = ""
        self.cal.delete(0, END)
        self.cal.insert(0, str(current) + str(number))

    def button_clear(self):
        self.cal.delete(0, END)
        self.cal.insert(0, "0")
        self.first_num = 0

    def button_equal(self):
        second_number = self.cal.get()
        self.cal.delete(0, END)

        if second_number != "":
            if self.math_operation == MATHTYPE.ADDITION:
                self.cal.insert(0, self.first_num + float(second_number))

            if self.math_operation == MATHTYPE.SUBTRACTION:
                self.cal.insert(0, self.first_num - float(second_number))

            if self.math_operation == MATHTYPE.MULTIPLICATION:
                self.cal.insert(0, self.first_num * float(second_number))

            if self.math_operation == MATHTYPE.DIVISION:
                self.cal.insert(0, self.first_num / float(second_number))

    def button_operand(self, operand: MATHTYPE) -> None:
        first_number = self.cal.get()
        self.math_operation = operand
        self.first_num = float(first_number)
        self.cal.delete(0, END)

    def Inch_to_mm(self):
        C_num = self.cal.get()
        ans_in_mm = float(C_num) * 25.4
        self.cal.delete(0, END)
        self.cal.insert(0, ans_in_mm)

    def mm_to_Inch(self):
        C_num = self.cal.get()
        ans_in_inch = float(C_num) / 25.4
        self.cal.delete(0, END)
        self.cal.insert(0, ans_in_inch)

    def move_cal_to_fence(self):
        C_num = float(self.cal.get())
        self.cal.delete(0, END)
        self.fen.delete(0, END)
        self.fen.insert(0, C_num)

    def move_cal_to_fence_reset(self):
        calc = self.cal.get()
        if calc != "":
            C_num = float(self.cal.get())
            self.cal.delete(0, END)
            self.Current_fence_position.delete(0, END)
            self.Current_fence_position.insert(0, C_num)

    def clear_fen(self):
        self.fen.delete(0, END)

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

        inch_to_mm = Button(
            self.calframe,
            text="Inch to mm",
            padx=self.xpadbutton,
            pady=self.ypadbutton,
            command=self.Inch_to_mm,
        )

        mm_to_inch = Button(
            self.calframe,
            text="mm to Inch",
            padx=self.xpadbutton,
            pady=self.ypadbutton,
            command=self.mm_to_Inch,
        )

        # Define Other Buttons

        button_movefence = Button(
            self.fenceframe,
            text="Move To",
            padx=self.xpadbutton,
            pady=self.ypadbutton,
            command=self.move_fence_to_location,
        )

        cal_to_fen_but = Button(
            self.fenceframe,
            text="Grab number",
            padx=self.xpadbutton,
            pady=self.ypadbutton,
            command=self.move_cal_to_fence,
        )

        cal_to_fen_but_reset = Button(
            self.fenceframe,
            text="Grab number",
            padx=self.xpadbutton,
            pady=self.ypadbutton,
            command=self.move_cal_to_fence_reset,
        )

        clear_fen_but = Button(
            self.fenceframe,
            text="Clear",
            padx=self.xpadbutton,
            pady=self.ypadbutton,
            command=self.clear_fen,
        )

        # Put the numeric buttons on the screen
        for i in range(9):
            r = 4 - i // 3
            c = i % 3
            self.buttons[f"button_{i+1}"].grid(
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

        inch_to_mm.grid(row=8, column=1, columnspan=2, sticky=N + S + E + W)
        mm_to_inch.grid(row=7, column=1, columnspan=2, sticky=N + S + E + W)

        button_movefence.grid(row=1, column=0)

        cal_to_fen_but.grid(row=1, column=1)

        cal_to_fen_but_reset.grid(row=4, column=1)

        clear_fen_but.grid(row=2, column=0, sticky=N + S + E + W)

    def mainloop(self):
        self.root.mainloop()
