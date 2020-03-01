import serial
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy import interpolate
from scipy import linalg
import time

def start_serial(com,baud):
    """
    Initialize the serial port to receive arduino data.
    
    Args:
        com: COM port to start the serial communication with
        baud: baud rate
    
    Return:
        serialPort: the opened serial port
    """
    arduinoComPort = com
    baudRate = baud
    serialPort = serial.Serial(arduinoComPort, baudRate, timeout=1)
    return serialPort

def parse():
    """
    Parse information coming in through serial port.
    """
    
    #start reading from the serial port
    serialPort = start_serial("/dev/cu.usbmodem141101",9600) 
    time.sleep(2)
    try:
        while serialPort.isOpen() is True:
            lineOfData = serialPort.readline().decode()
            if lineOfData is not '\n': # skip the case when the only output is a new line on the serial port
                print(lineOfData)
    except KeyboardInterrupt:
        pass


def calibration(voltages:list):
    """
    Given calibration data what is the torque value.
    """
    torque_values = np.linspace(0 , 1, 50)
    f_linear = interpolate.interp1d(voltages, torque_values) # x: voltages, y: torque values
    f_cubic = interpolate.interp1d(voltages, torque_values, kind='cubic')
    return f_linear, f_cubic

def torque_value(function, function2, value):
    """
    Solve function at a particular value.
    """
    solved_torque1 = function(value)
    solved_torque2 = function2(value)
    return solved_torque1, solved_torque2

    
# parse()
f_linear, f_cubic = calibration(np.linspace(5,10,50))
torque1, torque2= torque_value(f_linear, f_cubic, 7.25)
print(torque1, torque2)