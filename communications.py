import serial
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
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

style.use('fivethirtyeight')
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def parse_and_plot():
    """
    Parse information coming in through serial port.
    """
    
    #start reading from the serial port
    serialPort = start_serial("/dev/cu.usbmodem141101",9600) 
    time.sleep(2)

    times = []
    information = []

    times = 0

    try:
        while serialPort.isOpen() is True:
            lineOfData = serialPort.readline().decode()
            if lineOfData is not '\n': # skip the case when the only output is a new line on the serial port
                times.append(time)
                information.append(lineOfData)
                time = times + 1
            ax1.clear()
            ax1.plot(times, information)
    except KeyboardInterrupt:
        pass

animation = animation.FuncAnimation(fig, parse_and_plot, interval = 1000)
plt.show()

def calibration(torque_values:list, voltages:list):
    """
    Given calibration data identify the torque value.
    """
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


# f_linear, f_cubic = calibration(np.linspace(0 , 1, 50), np.linspace(5,10,50))
# torque1, torque2= torque_value(f_linear, f_cubic, 7.25)
# print(torque1, torque2)