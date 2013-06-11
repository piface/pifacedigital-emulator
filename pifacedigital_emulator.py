#!/usr/bin/env python3
import sys
import pifacecommon as pfcom
import pifacedigitalio as pfdio
from pfemgui import run_emulator
from multiprocessing import Process, Queue
from time import sleep

from pifacedigitalio import OUTPUT_PORT, INPUT_PORT, INPUT_PULLUP


class EmulatorAddressError(Exception):
    pass

# replicate pifacedigitalio functions/classes
# force the classes to use the functions in this module, not the pfdio
class EmulatorItem:
    @property
    def handler(self):
        return sys.modules[__name__]  # TODO perhaps move pfcom functions into own module


class DigitalInputPort(EmulatorItem, pfcom.DigitalInputPort):
    pass


class DigitalOutputPort(EmulatorItem, pfcom.DigitalOutputPort):
    pass


class DigitalInputItem(EmulatorItem, pfcom.DigitalInputItem):
    pass


class DigitalOutputItem(EmulatorItem, pfcom.DigitalOutputItem):
    pass


class LED(EmulatorItem, pfdio.LED):
    pass


class Relay(EmulatorItem, pfdio.Relay):
    pass


class Switch(EmulatorItem, pfdio.Switch):
    pass


# does not inherit from pfdio.PiFaceDigital because attributes need
# to be handled here
class PiFaceDigital():
    def __init__(self, board_num=0):
        self.board_num   = board_num
        self.input_pins  = [DigitalInputItem(i, INPUT_PORT, board_num) 
                for i in range(8)]
        self.output_pins = [DigitalOutputItem(i, OUTPUT_PORT, board_num)
                for i in range(8)]
        self.leds     = [LED(i, board_num)    for i in range(8)]
        self.relays   = [Relay(i, board_num)  for i in range(2)]
        self.switches = [Switch(i, board_num) for i in range(4)]


def init(init_board=True):
    try:
        pfdio.init(init_board)
        pfd = pfdio.PiFaceDigital()
    except pfcom.InitError:
        pfd = None
    except pfdio.NoPiFaceDigitalDetectedError:
        pfd = None

    global proc_comms_q_to_em
    global proc_comms_q_from_em
    proc_comms_q_to_em   = Queue()
    proc_comms_q_from_em = Queue()

    # start the gui in another process
    global emulator
    emulator = Process(
            target=run_emulator,
            args=(sys.argv, pfd, proc_comms_q_to_em, proc_comms_q_from_em))
    emulator.start()

def deinit():
    # stop the gui
    global proc_comms_q_to_em
    proc_comms_q_to_em.put(('quit',))
    global emulator
    emulator.join()
    pfdio.deinit()

def digital_read(pin_num, board_num=0):
    return read_bit(pin_num, INPUT_PORT, board_num) ^ 1

def digital_write(pin_num, value, board_num=0):
    write_bit(value, pin_num, OUTPUT_PORT, board_num)

def digital_read_pullup(pin_num, board_num=0):
    return read_bit(pin_num, INPUT_PULLUP, board_num)

def digital_write_pullup(pin_num, value, board_num=0):
    write_bit(value, pin_num, INPUT_PULLUP, board_num)

def get_bit_mask(bit_num):
    # This is  a function that belongs to pifacecommon
    return pfcom.get_bit_mask(bit_num)

def get_bit_num(bit_pattern):
    # This is actually a function that belongs to pifacecommon
    return pfcom.get_bit_num(bit_pattern)

def read_bit(bit_num, address, board_num=0):
    # This is  a function that belongs to pifacecommon
    global proc_comms_q_to_em
    global proc_comms_q_from_em

    if address is INPUT_PORT:
        proc_comms_q_to_em.put(('get_in', bit_num))
        return proc_comms_q_from_em.get(block=True)
    elif address is OUTPUT_PORT:
        proc_comms_q_to_em.put(('get_out', bit_num))
        return proc_comms_q_from_em.get(block=True)
    else:
        raise EmulatorAddressError(
            "Reading to 0x%X is not supported in the PiFace Digital emulator" % \
                    address)

   
def write_bit(value, bit_num, address, board_num=0):
    """This is a function that belongs to pifacecommon"""
    global proc_comms_q_to_em
    global proc_comms_q_from_em

    if address is OUTPUT_PORT:
        proc_comms_q_to_em.put(('set_out', bit_num, True if value else False))
    else:
        raise EmulatorAddressError(
            "Writing to 0x%X is not supported in the PiFace Digital emulator" % \
                    address)

def read(address, board_num=0):
    if address is INPUT_PORT or address is OUTPUT_PORT:
        value = 0x00
        for i in range(8):
            value |= read_bit(i, address, board_num) << i

        return value

    else:
        raise EmulatorAddressError(
            "Reading from 0x%X is not supported in the PiFace Digital emulator" % \
                    address)

def write(data, address, board_num=0):
    if address is OUTPUT_PORT:
        for i in range(8):
            value = (data >> i) & 1
            write_bit(value, i, address, board_num)

    else:
        raise EmulatorAddressError(
            "Writing to 0x%X is not supported in the PiFace Digital emulator" % \
                    address)


def spisend(bytes_to_send):
    raise FunctionNotImplemented("spisend")

"""
TODO have not yet implemented interupt functions in emulator
"""
def wait_for_input(input_func_map=None, loop=False, timeout=None):
    raise FunctionNotImplemented("wait_for_input")


if __name__ == '__main__':
    init()
