#!/usr/bin/env python3
import sys
from time import sleep
from multiprocessing import Process, Queue
import pifacecommon.interrupts
import pifacecommon.core
import pifacecommon.mcp23s17
import pifacedigitalio
from .gui import run_emulator

from pifacedigitalio import OUTPUT_PORT, INPUT_PORT


_pifacedigitals = dict()


class EmulatorAddressError(Exception):
    pass


class PiFaceDigitalEmulator(object):
    def read_bit(self, bit_num, address, hardware_addr=0):
        # This is  a function that belongs to pifacecommon
        if address is INPUT_PORT:
            self.proc_comms_q_to_em.put(('get_in', bit_num, hardware_addr))
            return self.proc_comms_q_from_em.get(block=True)
        elif address is OUTPUT_PORT:
            self.proc_comms_q_to_em.put(('get_out', bit_num, hardware_addr))
            return self.proc_comms_q_from_em.get(block=True)
        else:
            raise EmulatorAddressError(
                "Reading to 0x%X is not supported in the "
                "PiFace Digital emulator" % address)

    def write_bit(self, value, bit_num, address, hardware_addr=0):
        """This is a function that belongs to pifacecommon"""
        if address is OUTPUT_PORT:
            self.proc_comms_q_to_em.put(
                ('set_out', bit_num, True if value else False, hardware_addr))
        else:
            raise EmulatorAddressError(
                "Writing to 0x%X is not supported in the PiFace Digital "
                "emulator" % address)

    def read(self, address, hardware_addr=0):
        if address is INPUT_PORT or address is OUTPUT_PORT:
            value = 0x00
            for i in range(8):
                value |= self.read_bit(i, address, hardware_addr) << i

            return value

        else:
            raise EmulatorAddressError(
                "Reading from 0x%X is not supported in the PiFace Digital "
                "emulator" % address)

    def write(self, data, address, hardware_addr=0):
        if address is OUTPUT_PORT:
            for i in range(8):
                value = (data >> i) & 1
                self.write_bit(value, i, address, hardware_addr)

        else:
            raise EmulatorAddressError(
                "Writing to 0x%X is not supported in the PiFace Digital "
                "emulator" % address)

    def spisend(self, bytes_to_send):
        raise FunctionNotImplemented("spisend")

"""
# TODO have not yet implemented interupt functions in emulator
def wait_for_input(input_func_map=None, loop=False, timeout=None):
    raise FunctionNotImplemented("wait_for_input")
"""


class PiFaceDigital(PiFaceDigitalEmulator, pifacedigitalio.PiFaceDigital):
    def __init__(self,
                 hardware_addr=0,
                 bus=pifacedigitalio.DEFAULT_SPI_BUS,
                 chip_select=pifacedigitalio.DEFAULT_SPI_CHIP_SELECT,
                 init_board=True):
        self.hardware_addr = hardware_addr
        try:
            # check if we can access a real PiFaceDigital
            pifacedigitalio.PiFaceDigital(
                hardware_addr, bus, chip_select, init_board)
            use_pfd = True
        except pifacecommon.spi.SPIInitError as e:
            print("Error initialising PiFace Digital: ", e)
            print("Running without hardware PiFace Digital.")
            use_pfd = False
        except pifacedigitalio.NoPiFaceDigitalDetectedError:
            print("No PiFace Digital detected, running without "
                  "PiFace Digital.")
            use_pfd = False

        # create this false PiFace Digital
        super(PiFaceDigital, self).__init__(hardware_addr,
                                            bus,
                                            chip_select,
                                            init_board=False)

        self.proc_comms_q_to_em = Queue()
        self.proc_comms_q_from_em = Queue()

        # start the gui in another process
        self.emulator = Process(target=run_emulator,
                                args=(sys.argv, use_pfd, init_board, self))

        global _pifacedigitals
        _pifacedigitals[self.hardware_addr] = self

        self.emulator.start()


class InputEventListener(object):
    """PicklingError: Can't pickle <class 'method'>: attribute lookup
    builtins.method failed
    """
    def __init__(self):
        raise NotImplementedError(
            "Interrupts are not implemented in the emulator.")
    # def register(self, pin_num, direction, callback):
    #     global proc_comms_q_to_em
    #     proc_comms_q_to_em.put(
    #         ('register_interrupt', pin_num, direction, callback))

    # def activate(self):
    #     global proc_comms_q_to_em
    #     proc_comms_q_to_em.put(('activate_interrupt',))

    # def deactivate(self):
    #     global proc_comms_q_to_em
    #     proc_comms_q_to_em.put(('deactivate_interrupt',))


def digital_read(pin_num, hardware_addr=0):
    return _pifacedigitals[hardware_addr].read_bit(pin_num,
                                                   INPUT_PORT,
                                                   hardware_addr) ^ 1


def digital_write(pin_num, value, hardware_addr=0):
    _pifacedigitals[hardware_addr].write_bit(value,
                                             pin_num,
                                             OUTPUT_PORT,
                                             hardware_addr)


def digital_read_pullup(pin_num, hardware_addr=0):
    return _pifacedigitals[hardware_addr].read_bit(pin_num,
                                                   INPUT_PULLUP,
                                                   hardware_addr)


def digital_write_pullup(pin_num, value, hardware_addr=0):
    _pifacedigitals[hardware_addr].write_bit(value,
                                             pin_num,
                                             INPUT_PULLUP,
                                             hardware_addr)
