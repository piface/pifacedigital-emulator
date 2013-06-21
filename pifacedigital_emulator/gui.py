from PySide import QtGui, QtCore
from PySide.QtCore import (Qt, QThread, QObject, Slot, Signal)
from PySide.QtGui import (
    QMainWindow, QPushButton, QApplication, QPainter, QFont
)
from multiprocessing import Queue
from threading import Barrier
import pifacecommon as pfcom
import pifacedigitalio as pfdio
from .pifacedigital_emulator_ui import Ui_pifaceDigitalEmulatorWindow


# circle drawing
PIN_COLOUR = QtGui.QColor(0, 255, 255)
SWITCH_COLOUR = QtCore.Qt.yellow
CIRCLE_R = 9
INPUT_PIN_CIRCLE_COORD = (
    (5, 178), (17, 178), (29, 178), (41, 178), (53, 178), (65, 178), (77, 178),
    (89, 178))
# output coords are backwards (output port indexed (7 -> 0)
OUTPUT_PIN_CIRCLE_COORD = (
    (241, 2), (229, 2), (217, 2), (205, 2), (193, 2), (181, 2), (169, 2),
    (157, 2))
SWITCH_CIRCLE_COORD = ((13, 149), (38, 149), (63, 149), (88, 149))
RELAY_CIRCLE_COORD = (
    (286, 67), (286, 79), (286, 91), (286, 116), (286, 128), (286, 140))

# boundaries for input presses
SWITCH_BOUNDARY_Y_TOP = 148
SWITCH_BOUNDARY_Y_BOTTOM = 161
SWITCH_BOUNDARY_X_LEFT = (13, 38, 63, 89)
SWITCH_BOUNDARY_X_RIGHT = (25, 50, 75, 100)
PIN_BOUNDARY_Y_TOP = 180
PIN_BOUNDARY_Y_BOTTOM = 190
PIN_BOUNDARY_X_LEFT = (5,  19, 31, 44, 53, 68, 79, 91, 104)
PIN_BOUNDARY_X_RIGHT = (15, 27, 38, 51, 66, 74, 87, 99, 112)


class CircleDrawingWidget(QtGui.QWidget):
    def __init__(self, parent=None, emu_window=None):
        super(CircleDrawingWidget, self).__init__(parent)
        # mirror actual state
        self.emu_window = emu_window

        # 'hold' for every input
        self.input_hold = [False for i in self.emu_window.input_state]

    @property
    def switch_circles_state(self):
        return self.emu_window.input_state[:4]

    @property
    def relay_circles_state(self):
        """returns six booleans for the relay pins"""
        # relays are attached to pins 0 and 1
        if self.emu_window.output_state[0]:
            state0 = [True, True, False]
        else:
            state0 = [False, True, True]

        if self.emu_window.output_state[1]:
            state1 = [True, True, False]
        else:
            state1 = [False, True, True]

        return state0 + state1

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setBrush(QtGui.QBrush(PIN_COLOUR))
        painter.setPen(QtGui.QPen(PIN_COLOUR))
        # draw input circles
        for i, state in enumerate(self.emu_window.input_state):
            if state:
                painter.drawEllipse(
                    INPUT_PIN_CIRCLE_COORD[i][0],
                    INPUT_PIN_CIRCLE_COORD[i][1],
                    CIRCLE_R, CIRCLE_R)

        # draw output circles
        for i, state in enumerate(self.emu_window.output_state):
            if state:
                painter.drawEllipse(
                    OUTPUT_PIN_CIRCLE_COORD[i][0],
                    OUTPUT_PIN_CIRCLE_COORD[i][1],
                    CIRCLE_R, CIRCLE_R)

        # draw relay circles
        for i, state in enumerate(self.relay_circles_state):
            if state:
                painter.drawEllipse(
                    RELAY_CIRCLE_COORD[i][0],
                    RELAY_CIRCLE_COORD[i][1],
                    CIRCLE_R, CIRCLE_R)

        # draw switch circles
        painter.setBrush(QtGui.QBrush(SWITCH_COLOUR))
        painter.setPen(QtGui.QPen(SWITCH_COLOUR))
        for i, state in enumerate(self.switch_circles_state):
            if state:
                painter.drawEllipse(
                    SWITCH_CIRCLE_COORD[i][0],
                    SWITCH_CIRCLE_COORD[i][1],
                    CIRCLE_R, CIRCLE_R)
        painter.end()

    def mousePressEvent(self, event):
        self._pressed_pin, self._pressed_switch = switch = \
            get_input_index_from_mouse(event.pos())
        if self._pressed_pin is None:
            event.ignore()
            return

        # if we are over a switch, turn it on, else toggle
        if self._pressed_switch:
            self.emu_window.input_state[self._pressed_pin] = True
        else:
            self.emu_window.input_state[self._pressed_pin] = \
                not self.emu_window.input_state[self._pressed_pin]
            # hold it if we're setting it the pin high
            self.input_hold[self._pressed_pin] = \
                self.emu_window.input_state[self._pressed_pin]

        self.emu_window.update_emulator()

    def mouseReleaseEvent(self, event):
        if self._pressed_pin is None:
            event.ignore()
            return

        # if we're releasing a switch, turn off the pin (if it's not held)
        if self._pressed_switch:
            if not self.input_hold[self._pressed_pin]:
                self.emu_window.input_state[self._pressed_pin] = False
                self._pressed_pin = None
                self._pressed_switch = False
                self.emu_window.update_emulator()


class PiFaceDigitalEmulatorWindow(QMainWindow, Ui_pifaceDigitalEmulatorWindow):
    def __init__(self, parent=None):
        super(PiFaceDigitalEmulatorWindow, self).__init__(parent)
        self.setupUi(self)

        self.input_state = [False for state in range(8)]
        self.output_state = [False for state in range(8)]

        # add the circle drawing widget
        self.circleDrawingWidget = \
            CircleDrawingWidget(self.centralwidget, self)
        self.circleDrawingWidget.setGeometry(QtCore.QRect(10, 10, 301, 191))
        self.circleDrawingWidget.setObjectName("circleDrawingWidget")

        self.pifacedigital = None
        self.output_buttons = [
            self.output0Button,
            self.output1Button,
            self.output2Button,
            self.output3Button,
            self.output4Button,
            self.output5Button,
            self.output6Button,
            self.output7Button]
        self.led_labels = [
            self.led0Label,
            self.led1Label,
            self.led2Label,
            self.led3Label,
            self.led4Label,
            self.led5Label,
            self.led6Label,
            self.led7Label]

        # hide the leds
        for led in self.led_labels:
            led.setVisible(False)

        # set up signal/slots
        self.outputControlAction.toggled.connect(self.enable_output_control)
        self.inputPullupsAction.toggled.connect(self.set_input_pullups)

        for button in self.output_buttons:
            button.toggled.connect(self.output_overide)

        self.allOnButton.clicked.connect(self.all_outputs_on)
        self.allOffButton.clicked.connect(self.all_outputs_off)
        self.flipButton.clicked.connect(self.all_outputs_toggle)

        self.output_override_enabled = False

    def enable_output_control(self, enable):
        if enable:
            self._saved_output_state = list(self.output_state)
            self.update_all_output_buttons()
        else:
            self.output_state = self._saved_output_state
            self.uncheck_all_output_buttons()
            self.update_emulator()

        self.output_override_enabled = enable
        self.outputControlBox.setEnabled(enable)

    def set_input_pullups(self, enable):
        if self.pifacedigital:
            pullup_byte = 0xff if enable else 0x00
            pfcom.write(pullup_byte, pfdio.INPUT_PULLUP)
            if not enable:
                for i, s in enumerate(self.input_state):
                    self.set_input(i, False)
                self.update_emulator()

    def output_overide(self, enable):
        """sets the output to mirror the override buttons"""
        # find out output override buttons state
        # then write them to the output
        # don't use set_output since that is locked when override mode is on
        for i, button in enumerate(self.output_buttons):
            self.output_state[i] = button.isChecked()
        self.update_emulator()

    def set_output(self, index, enable):
        """Sets the specified output on or off"""
        if not self.output_override_enabled:
            self.output_state[index] = enable

    def set_input(self, index, enable):
        # don't set the input if it is being held
        if not self.circleDrawingWidget.input_hold[index]:
            self.input_state[index] = enable

    def update_piface(self):
        # TODO - Change this to use new ouput_port
        # for i, state in enumerate(self.output_state):
        #     s = 1 if state else 0
        #     self.pifacedigital.output_pins[i].value = s
        output_value = 0
        for bit_index, state in enumerate(self.output_state):
            this_bit = 1 if state else 0
            output_value |= (this_bit << bit_index)

        self.pifacedigital.output_port.value = output_value

    def update_emulator(self):
        self.update_circles()
        self.update_led_images()
        if self.pifacedigital:
            self.update_piface()

    def update_circles(self):
        self.circleDrawingWidget.input_pin_circles_state = self.input_state
        self.circleDrawingWidget.output_pin_circles_state = self.output_state
        self.circleDrawingWidget.repaint()

    def update_led_images(self):
        for index, state in enumerate(self.output_state):
            self.led_labels[index].setVisible(state)

    def all_outputs_on(self):
        self.output_state = [True for s in range(8)]
        self.update_all_output_buttons()
        self.update_emulator()

    def all_outputs_off(self):
        self.output_state = [False for s in range(8)]
        self.update_all_output_buttons()
        self.update_emulator()

    def all_outputs_toggle(self):
        self.output_state = [not s for s in self.output_state]
        self.update_all_output_buttons()
        self.update_emulator()

    def uncheck_all_output_buttons(self):
        for button in self.output_buttons:
            button.toggled.disconnect(self.output_overide)
            button.setChecked(False)
            button.toggled.connect(self.output_overide)

    def update_all_output_buttons(self):
        for i, button in enumerate(self.output_buttons):
            button.toggled.disconnect(self.output_overide)
            button.setChecked(self.output_state[i])
            button.toggled.connect(self.output_overide)

    @Slot(int)
    def set_input_enable(self, pin):
        self.set_input(pin, True)
        self.update_emulator()

    @Slot(int)
    def set_input_disable(self, pin):
        self.set_input(pin, False)
        self.update_emulator()

    @Slot(int)
    def set_output_enable(self, pin):
        self.set_output(pin, True)
        self.update_emulator()

    @Slot(int)
    def set_output_disable(self, pin):
        self.set_output(pin, False)
        self.update_emulator()

    send_input = Signal(int)

    @Slot(int)
    def get_input(self, pin):
        input_on = self.input_state[pin]
        self.send_input.emit(1 if input_on else 0)

    send_output = Signal(int)

    @Slot(int)
    def get_output(self, pin):
        pin_on = self.output_state[pin]
        self.send_output.emit(1 if pin_on else 0)


class QueueWatcher(QObject):
    """Handles the queue which talks to the main process"""
    def __init__(self, app, q_to_em, q_from_em):
        super().__init__()
        self.main_app = app
        self.q_to_em = q_to_em
        self.q_from_em = q_from_em
        self.perform = {
            'set_out': self.set_out_pin,
            'get_in': self.get_in_pin,
            'get_out': self.get_out_pin,
            'quit': self.quit_main_app
        }

    def check_queue(self):
        while True:
            action = self.q_to_em.get(block=True)
            task = action[0]

            try:
                pin = action[1]
            except IndexError:
                pin = None

            try:
                enable = action[2]
            except IndexError:
                enable = None

            self.perform[task](pin, enable)

    set_out_enable = Signal(int)
    set_out_disable = Signal(int)

    def set_out_pin(self, pin, enable):
        if enable:
            self.set_out_enable.emit(pin)
        else:
            self.set_out_disable.emit(pin)

    get_in = Signal(int)

    def get_in_pin(self, pin, enable):
        self.get_in.emit(pin)
        # now we have to rely on the emulator getting back to us

    @Slot(int)
    def send_get_in_pin_result(self, value):
        self.q_from_em.put(value)

    get_out = Signal(int)

    def get_out_pin(self, pin, enable):
        self.get_out.emit(pin)

    @Slot(int)
    def send_get_out_pin_result(self, value):
        self.q_from_em.put(value)

    def quit_main_app(self, pin, enable):
        self.main_app.quit()


class InputWatcher(QObject):
    """Handles inputs and changes the emulator accordingly"""

    set_in_enable = Signal(int)
    set_in_disable = Signal(int)

    def __init__(self):
        super().__init__()
        self.ifm = pfcom.InputFunctionMap()
        for i in range(8):
            self.ifm.register(i, pfcom.IN_EVENT_DIR_BOTH, self.set_input)

    def check_inputs(self):
        pfdio.wait_for_input(input_func_map=self.ifm)

    def set_input(self, interupt_bit, interupt_byte):
        pin_num = pfcom.get_bit_num(interupt_bit)
        value = ((interupt_bit & interupt_byte) >> pin_num) ^ 1  # active low
        if value:
            self.set_in_enable.emit(pin_num)
        else:
            self.set_in_disable.emit(pin_num)

        return True  # keep checking events


def get_input_index_from_mouse(point):
    """returns the pin number based on the point clicked, also returns a
    boolean specifying if the press occured on a switch
    Returns:
        (pin, switch?)
    """
    x = point.x()
    y = point.y()

    # check for a switch press
    if (SWITCH_BOUNDARY_Y_TOP < y and y < SWITCH_BOUNDARY_Y_BOTTOM):
        for i in range(4):
            if (SWITCH_BOUNDARY_X_LEFT[i] < x and
                    x < SWITCH_BOUNDARY_X_RIGHT[i]):
                return (i, True)

    elif (PIN_BOUNDARY_Y_TOP < y and y < PIN_BOUNDARY_Y_BOTTOM):
        # check for a pin press
        for i in range(8):
            if (PIN_BOUNDARY_X_LEFT[i] < x and x < PIN_BOUNDARY_X_RIGHT[i]):
                return (i, False)

    return (None, False)  # no pin found, press did not occur on switch


def start_q_watcher(app, emu_window, proc_comms_q_to_em, proc_comms_q_from_em):
    # need to spawn a worker thread that watches the proc_comms_q
    # need to seperate queue function from queue thread
    # http://stackoverflow.com/questions/4323678/threading-and-signals-problem
    # -in-pyqt
    q_watcher = QueueWatcher(app, proc_comms_q_to_em, proc_comms_q_from_em)
    q_watcher_thread = QThread()
    q_watcher.moveToThread(q_watcher_thread)
    q_watcher_thread.started.connect(q_watcher.check_queue)

    # now that we've set up the thread, let's set up rest of signals/slots
    q_watcher.set_out_enable.connect(emu_window.set_output_enable)
    q_watcher.set_out_disable.connect(emu_window.set_output_disable)
    q_watcher.get_in.connect(emu_window.get_input)
    q_watcher.get_out.connect(emu_window.get_output)

    emu_window.send_output.connect(q_watcher.send_get_out_pin_result)
    emu_window.send_input.connect(q_watcher.send_get_in_pin_result)

    # not sure why this doesn't work by connecting to q_watcher_thread.quit
    def about_to_quit():
        q_watcher_thread.quit()
    app.aboutToQuit.connect(about_to_quit)

    q_watcher_thread.start()


def start_input_watcher(app, emu_window):
    input_watcher = InputWatcher()
    input_watcher_thread = QThread()
    input_watcher.moveToThread(input_watcher_thread)
    input_watcher_thread.started.connect(input_watcher.check_inputs)

    # signal / slots
    input_watcher.set_in_enable.connect(emu_window.set_input_enable)
    input_watcher.set_in_disable.connect(emu_window.set_input_disable)

    # qyit setup
    def about_to_quit():
        input_watcher_thread.quit()
    app.aboutToQuit.connect(about_to_quit)

    input_watcher_thread.start()


def run_emulator(
        sysargv,
        pifacedigital,
        proc_comms_q_to_em,
        proc_comms_q_from_em):
    app = QApplication(sysargv)

    emu_window = PiFaceDigitalEmulatorWindow()
    emu_window.pifacedigital = pifacedigital

    start_q_watcher(app, emu_window, proc_comms_q_to_em, proc_comms_q_from_em)

    # only watch inputs if there is actually a piface digital
    if emu_window.pifacedigital:
        start_input_watcher(app, emu_window)

    emu_window.show()
    app.exec_()
