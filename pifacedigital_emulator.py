#!/usr/bin/env python3
import sys
import pifacedigitalio as pfio
from pfemgui import run_emulator
from multiprocessing import Process, Queue
from time import sleep


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


def init(init_board=True):
    pfio.init(init_board)

    global proc_comms_q
    proc_comms_q = Queue()

    # start the gui in another process
    emulator = Process(target=run_emulator, args=(sys.argv, proc_comms_q))
    emulator.start()

    # testing
    sleep(3)
    proc_comms_q.put("test")
    

def deinit():
    # somehow stop the gui
    # stop the input thread
    global emulator
    emulator.join()
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
    pass

def write(data, address, board_num=0):
    pass

def spisend(bytes_to_send):
    pass

def wait_for_input(input_func_map=None, loop=False, timeout=None):
    pass

def call_mapped_input_functions(input_func_map):
    pass

def clear_interupts():
    pass

def enable_interupts():
    pass

def disable_interupts():
    pass



if __name__ == '__main__':
    init()
