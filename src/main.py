from ui import UI
from stepper import Stepper

_stepper = Stepper(1,2,3)
_ui = UI()

_stepper._UI = _ui
_ui._stepper = _stepper


_ui.mainloop()