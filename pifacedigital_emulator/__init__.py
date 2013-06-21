from pifacedigitalio import OUTPUT_PORT, INPUT_PORT, INPUT_PULLUP

# classes
from .core import (
    DigitalInputPort,
    DigitalOutputPort,
    DigitalInputItem,
    DigitalOutputItem,
    LED,
    Relay,
    Switch,
    PiFaceDigital,
)

# functions
from .core import (
    init,
    deinit,
    digital_read,
    digital_write,
    digital_read_pullup,
    digital_write_pullup,
)


if __name__ == '__main__':
    init()
