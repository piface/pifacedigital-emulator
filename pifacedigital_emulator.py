#!/usr/bin/env python3
import sys
import pifacedigitalio as pfio
from PySide.QtGui import QMainWindow, QPushButton, QApplication
from pifacedigital_emulator_ui import Ui_MainWindow
 

class pifaceDigitalEmulatorWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(pifaceDigitalEmulatorWindow, self).__init__(parent)
        self.setupUi(self)
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
        self.outputControlAction.toggled.connect(self.set_enable_output_control)
        self.inputPullupsAction.toggled.connect(self.set_input_pullups)
        
        self.output0Button.toggled.connect(self.set_output0)
        self.output1Button.toggled.connect(self.set_output1)
        self.output2Button.toggled.connect(self.set_output2)
        self.output3Button.toggled.connect(self.set_output3)
        self.output4Button.toggled.connect(self.set_output4)
        self.output5Button.toggled.connect(self.set_output5)
        self.output6Button.toggled.connect(self.set_output6)
        self.output7Button.toggled.connect(self.set_output7)

        self.allOnButton.clicked.connect(self.check_all_output_buttons)
        self.allOffButton.clicked.connect(self.uncheck_all_output_buttons)
        self.flipButton.clicked.connect(self.toggle_all_output_buttons)

    def set_enable_output_control(self, enable):
        if not enable:
            # return to original values
            # but for now just turn them all off
            self.uncheck_all_output_buttons()

        self.outputControlBox.setEnabled(enable)

    def set_input_pullups(self, enable):
        if self.pifacedigital:
            pullup_byte = 0xff if enable else 0x00
            pfio.write(pullup_byte, pfio.INPUT_PULLUP)

    # tp - there has to be a better way of doing this
    def set_output0(self, checked):
        self.set_output(0, checked)
    def set_output1(self, checked):
        self.set_output(1, checked)
    def set_output2(self, checked):
        self.set_output(2, checked)
    def set_output3(self, checked):
        self.set_output(3, checked)
    def set_output4(self, checked):
        self.set_output(4, checked)
    def set_output5(self, checked):
        self.set_output(5, checked)
    def set_output6(self, checked):
        self.set_output(6, checked)
    def set_output7(self, checked):
        self.set_output(7, checked)

    def set_output(self, index, enable):
        """Sets the specified output on or off"""
        self.led_labels[index].setVisible(enable)
        if self.pifacedigital:
            self.pifacedigital.output_pin[index].value = 1 if enable else 0

    def check_all_output_buttons(self):
        for output_button in self.output_buttons:
            output_button.setChecked(True) # also fires the signal

    def uncheck_all_output_buttons(self):
        for output_button in self.output_buttons:
            output_button.setChecked(False)

    def toggle_all_output_buttons(self):
        for output_button in self.output_buttons:
            output_button.toggle()

       


# replicate pifacedigital functions/classes
# force the classes to use the functions in this module, not the pfio
class EmulatorItem:
    @property
    def handler(self):
        return sys.modules[__name__]

class InputItem(EmulatorItem, pfio.Item):
    pass

class InputItem(EmulatorItem, pfio.InputItem):
    pass

class OutputItem(EmulatorItem, pfio.OutputItem):
    pass

class LED(EmulatorItem, pfio.LED):
    pass

class Relay(EmulatorItem, pfio.Relay):
    pass

class Switch(EmulatorItem, pfio.Switch):
    pass

class PiFaceDigital(EmulatorItem, pfio.PiFaceDigital):
    pass

class InputFunctionMap(EmulatorItem, pfio.InputFunctionMap):
    pass

# USE MULTIPROCESS TO GET THREADING RIGHT
def init(init_board=True):
    pfio.init(init_board)

    app = QApplication(sys.argv)
    frame = pifaceDigitalEmulatorWindow()
    frame.show()
    frame.pifacedigital = pfio.PiFaceDigital()
    app.exec_()

def deinit():
    # somehow stop the gui
    # stop the input thread
    pfio.deinit()

def digital_read(pin_num, board_num=0):
    return read_bit(pin_num, pfio.INPUT_PORT, board_num) ^ 1

def digital_write(pin_num, value, board_num=0):
    write_bit(value, pin_num, pfio.OUTPUT_PORT, board_num)

def digital_read_pullup(pin_num, board_num=0):
    return read_bit(pin_num, pfio.INPUT_PULLUP, board_num)

def digital_write_pullup(pin_num, value, board_num=0):
    write_bit(value, pin_num, pfio.INPUT_PULLUP, board_num)

def get_bit_mask(bit_num):
    return pfio.get_bit_mask(bit_num)

def get_bit_num(bit_pattern):
    return pfio.get_bit_num(bit_pattern)

def read_bit(bit_num, address, board_num=0):
    value = read(address, board_num)                                                                       
    bit_mask = get_bit_mask(bit_num)                                           
    return 1 if value & bit_mask else 0

def write_bit(value, bit_num, address, board_num=0):
    bit_mask = get_bit_mask(bit_num)
    old_byte = read(address, board_num)
    # generate the new byte
    if value:
        new_byte = old_byte | bit_mask
    else:
        new_byte = old_byte & ~bit_mask
    write(new_byte, address, board_num)

def read(address, board_num=0):
def write(data, address, board_num=0):
def spisend(bytes_to_send):
def wait_for_input(input_func_map=None, loop=False, timeout=None):
def call_mapped_input_functions(input_func_map):
def clear_interupts():
def enable_interupts():
def disable_interupts():


if __name__ == '__main__':
    init()
