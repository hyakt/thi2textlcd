#!/usr/bin/env python

"""Copyright 2010 Phidgets Inc.
This work is licensed under the Creative Commons Attribution 2.5 Canada License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by/2.5/ca/
"""

__author__ = 'Adam Stelmack'
__version__ = '2.1.8'
__date__ = 'May 17 2010'

# Basic imports
from ctypes import *
import sys
import random
from time import sleep
# Phidget specific imports
from Phidgets.Phidget import PhidgetID
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, InputChangeEventArgs, OutputChangeEventArgs, SensorChangeEventArgs
from Phidgets.Devices.InterfaceKit import InterfaceKit
from Phidgets.Devices.TextLCD import TextLCD, TextLCD_ScreenSize

# Create an interfacekit object
try:
    interfaceKit = InterfaceKit()
    textLCD = TextLCD()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

# Information Display Function


def dispalyifkinfo():
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" %
          (interfaceKit.isAttached(), interfaceKit.getDeviceName(), interfaceKit.getSerialNum(), interfaceKit.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")
    print("Number of Digital Inputs: %i" % (interfaceKit.getInputCount()))
    print("Number of Digital Outputs: %i" % (interfaceKit.getOutputCount()))
    print("Number of Sensor Inputs: %i" % (interfaceKit.getSensorCount()))

# Information Display Function


def displaylcdinfo():
    try:
        isAttached = textLCD.isAttached()
        name = textLCD.getDeviceName()
        serialNo = textLCD.getSerialNum()
        version = textLCD.getDeviceVersion()
        rowCount = textLCD.getRowCount()
        columnCount = textLCD.getColumnCount()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        return 1
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" %
          (isAttached, name, serialNo, version))
    print("|------------|----------------------------------|--------------|------------|")
    print("Number of Rows: %i -- Number of Columns: %i" %
          (rowCount, columnCount))

# Event Handler Callback Functions


def TextLCDAttached(e):
    attached = e.device
    print("TextLCD %i Attached!" % (attached.getSerialNum()))
    if textLCD.getDeviceID() == PhidgetID.PHIDID_TEXTLCD_ADAPTER:
        textLCD.setScreenIndex(0)
        textLCD.setScreenSize(TextLCD_ScreenSize.PHIDGET_TEXTLCD_SCREEN_2x8)


def TextLCDDetached(e):
    detached = e.device
    print("TextLCD %i Detached!" % (detached.getSerialNum()))


def TextLCDError(e):
    try:
        source = e.device
        print("TextLCD %i: Phidget Error %i: %s" %
              (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))


def interfaceKitAttached(e):
    attached = e.device
    print("InterfaceKit %i Attached!" % (attached.getSerialNum()))


def interfaceKitDetached(e):
    detached = e.device
    print("InterfaceKit %i Detached!" % (detached.getSerialNum()))


def interfaceKitError(e):
    try:
        source = e.device
        print("InterfaceKit %i: Phidget Error %i: %s" %
              (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))


def interfaceKitInputChanged(e):
    source = e.device
    print("InterfaceKit %i: Input %i: %s" %
          (source.getSerialNum(), e.index, e.state))


def interfaceKitSensorChanged(e):
    source = e.device
    tmp = "TMP: " + \
        str(round((source.getSensorValue(1) * 0.22222) - 61.11, 2)) + " c"
    tmp = tmp.encode()
    hmd = "HMD: " + \
        str(round((source.getSensorValue(0) * 0.1906) - 40.2, 2)) + " %"
    hmd = hmd.encode()

    textLCD.setDisplayString(0, tmp)
    textLCD.setDisplayString(1, hmd)
    print("InterfaceKit %i: Sensor %i: %i" %
          (source.getSerialNum(), e.index, e.value))


def interfaceKitOutputChanged(e):
    source = e.device
    print("InterfaceKit %i: Output %i: %s" %
          (source.getSerialNum(), e.index, e.state))


if __name__ == '__main__':
    # Main Program Code
    try:
        textLCD.setOnAttachHandler(TextLCDAttached)
        textLCD.setOnDetachHandler(TextLCDDetached)
        textLCD.setOnErrorhandler(TextLCDError)
        interfaceKit.setOnAttachHandler(interfaceKitAttached)
        interfaceKit.setOnDetachHandler(interfaceKitDetached)
        interfaceKit.setOnErrorhandler(interfaceKitError)
        interfaceKit.setOnInputChangeHandler(interfaceKitInputChanged)
        interfaceKit.setOnOutputChangeHandler(interfaceKitOutputChanged)
        interfaceKit.setOnSensorChangeHandler(interfaceKitSensorChanged)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)

    try:
        textLCD.openPhidget()
        interfaceKit.openPhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)

    print("Waiting for attach....")

    try:
        textLCD.waitForAttach(10000)
        interfaceKit.waitForAttach(10000)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        try:
            interfaceKit.closePhidget()
            textLCD.closePhidget()
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            print("Exiting....")
            exit(1)
        print("Exiting....")
        exit(1)
    else:
        displaylcdinfo()
        dispalyifkinfo()

    print("Setting the data rate for each sensor index to 4ms....")
    for i in range(interfaceKit.getSensorCount()):
        try:
            interfaceKit.setDataRate(i, 4)
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))

    print("Press Enter to quit....")

    sys.stdin.read(1)

    print("Closing...")

    try:
        textLCD.setDisplayString(0, b"")
        textLCD.setDisplayString(1, b"")
        interfaceKit.closePhidget()
        textLCD.closePhidget()

    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)

    print("Done.")
    exit(0)
