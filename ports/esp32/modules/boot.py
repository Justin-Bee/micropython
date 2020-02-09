###########################################################################
#
# boot.py
# Author: Justin Bee
# Date: 1/24/2020
#
# This script will run at startup and will initialize the bluetooth module
# also sets the bluetooth to advertise
#
###########################################################################

import ubluetooth
from ubluetooth import BLE

from micropython import const
import struct

# Advertising payloads are repeated packets of the following form:
#   1 byte data length (N + 1)
#   1 byte type (see constants below)
#   N bytes type-specific data

_ADV_TYPE_FLAGS = const(0x01)
_ADV_TYPE_NAME = const(0x09)
_ADV_TYPE_UUID16_COMPLETE = const(0x3)
_ADV_TYPE_UUID32_COMPLETE = const(0x5)
_ADV_TYPE_UUID128_COMPLETE = const(0x7)
_ADV_TYPE_UUID16_MORE = const(0x2)
_ADV_TYPE_UUID32_MORE = const(0x4)
_ADV_TYPE_UUID128_MORE = const(0x6)
_ADV_TYPE_APPEARANCE = const(0x19)

# These are constants for the BLE IRQ
_IRQ_ALL = const(0xffff)
_IRQ_CENTRAL_CONNECT                 = const(1 << 0)
_IRQ_CENTRAL_DISCONNECT              = const(1 << 1)
_IRQ_GATTS_WRITE                     = const(1 << 2)
_IRQ_GATTS_READ_REQUEST              = const(1 << 3)
_IRQ_SCAN_RESULT                     = const(1 << 4)
_IRQ_SCAN_COMPLETE                   = const(1 << 5)
_IRQ_PERIPHERAL_CONNECT              = const(1 << 6)
_IRQ_PERIPHERAL_DISCONNECT           = const(1 << 7)
_IRQ_GATTC_SERVICE_RESULT            = const(1 << 8)
_IRQ_GATTC_CHARACTERISTIC_RESULT     = const(1 << 9)
_IRQ_GATTC_DESCRIPTOR_RESULT         = const(1 << 10)
_IRQ_GATTC_READ_RESULT               = const(1 << 11)
_IRQ_GATTC_WRITE_STATUS              = const(1 << 12)
_IRQ_GATTC_NOTIFY                    = const(1 << 13)
_IRQ_GATTC_INDICATE                  = const(1 << 14)


# create BLE variable
bt= BLE()
# set active to True initializing the bluetooth module
bt.active(1)

#define the bt_irq
def bt_irq(event, data):
    if event == _IRQ_CENTRAL_CONNECT:
        print("IRQ_CENTRAL_CONNECT")
    elif event == _IRQ_CENTRAL_DISCONNECT:
        print("IRQ_CENTRAL_DISCONNECT")
    elif event == _IRQ_GATTS_WRITE:
        print("IRQ_GATTS_WRITE")
    elif event == _IRQ_GATTS_READ_REQUEST:
        print("IRQ_GATTS_READ_REQUEST")

bt.irq(bt_irq)





def adv_encode(adv_type, value):
    return bytes((len(value) + 1, adv_type,)) + value


def adv_encode_name(name):
    return adv_encode(const(0x09), name.encode())



# set the UUID for the GATT Service
# Bluetooth SIG GATT Service  - 0x1825 is Object Transfer Service
_adv_service = ubluetooth.UUID(0x1825)
# Bluetooth SIG GATT Characteristic - 0x2AC8 is Object Changed
_adv_characteristic = (ubluetooth.UUID(0x2AC8), ubluetooth.FLAG_WRITE,)
# MicroTrynkit Service
_my_service = ((_adv_service, (_adv_characteristic,),),)
#start the gatt service
((handle,),)= bt.gatts_register_services(_my_service)

#cannot advertise until after registering services
# set gap_advertise(interval, adv_data?)
bt.gap_advertise(100000, adv_encode_name('MicroTrynkit'))  #works correctly


#ubluetooth.UUID() 16 bit or 128 bit

# building now with ESP-IDF 3.3.1 has support for BLE and WiFi
# this could be a better option going forward incase BLE does not work out with the upload time