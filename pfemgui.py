import pifacedigitalio as pfio
from PySide.QtCore import QThread, QObject
from PySide.QtGui import QMainWindow, QPushButton, QApplication
from multiprocessing import Queue
from pifacedigital_emulator_ui import Ui_MainWindow

class PiFaceDigitalEmulatorWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(PiFaceDigitalEmulatorWindow, self).__init__(parent)
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

       
class QueueHandler(QObject):
    def __init__(self, q):
        QObject.__init__(self)
        self.q = q

    def run(self):
        msg = self.q.get(block=True)

        print(msg)


def run_emulator(sysargv, proc_comms_q):
    app = QApplication(sysargv)

    emu_window = PiFaceDigitalEmulatorWindow()
    emu_window.pifacedigital = pfio.PiFaceDigital()
    emu_window.show()

    # need to spawn a worker thread that watches the proc_comms_q
    q_handler = QueueHandler(proc_comms_q)

    # qt thread set up
    q_handler_thread = QThread()
    q_handler.moveToThread(q_handler_thread)
    """
    q_handler_thread.error.connect(SIGNAL(error(QString)), this, SLOT(errorString(QString)));
    connect(thread, SIGNAL(started()), worker, SLOT(process()));
    connect(worker, SIGNAL(finished()), thread, SLOT(quit()));
    connect(worker, SIGNAL(finished()), worker, SLOT(deleteLater()));

    connect(thread, SIGNAL(finished()), thread, SLOT(deleteLater()));
    """
    q_handler_thread.start()

    app.exec_()
