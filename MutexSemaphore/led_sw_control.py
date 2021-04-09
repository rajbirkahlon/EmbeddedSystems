#
# GUI to show a switch status and control a LED on LaunchPad 
#
import argparse, struct, os, time, sys, serial
import datetime
import re
import os
import subprocess
import sys
import tkinter as tk
import webbrowser

parser = argparse.ArgumentParser (description="Get temperature from LaunchPad.")
parser.add_argument('--baud', default=115200, help="Set baudrate")
parser.add_argument('--port', default='com5', help="Com port to use")
parserArgs = parser.parse_args()

port = parserArgs.port
baudrate = parserArgs.baud
serialPort = None
Switch_status_text = None

class TermWindow(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__ (self, master)
        self.buffer = ''
        self.after(1000, self.update)

    def update(self):
        out = '' 
        while serialPort.inWaiting () > 0  :
            out += serialPort.read(1).decode('utf-8')

        if out != '' :                      # Received something
            self.buffer += out
            if out.find('\n') >= 0:
                #print(self.buffer)
                temps = self.buffer.split()
                if len(temps) > 0:
                    if temps[0].find("OPEN") == 0:
                        Switch_status_text.set("Switch Not Pressed")
                    if temps[0].find("CLOSE") == 0:
                        Switch_status_text.set("Switch Pressed")
                self.buffer = ''

        self.after(200, self.update)         # Wake up once a while to check the input

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.pack()
        self.createWidgets()
        self.master.title('LaunchPad switch and LED control')

    def createWidgets(self):
        global Switch_status_text
        Switch_status_text = tk.StringVar()
        Switch = tk.Button(self, text='', textvariable=Switch_status_text, fg='blue')
        LedOn = tk.Button(self, text="LED ON", fg='red', command=self.TurnLedOn)
        LedOff = tk.Button(self, text="LED OFF", fg='red', command=self.TurnLedOff)
        
        Switch.pack(side = tk.LEFT, padx=10)
        LedOn.pack(side = tk.LEFT, padx=10)
        LedOff.pack(side = tk.LEFT, padx=10)
        termWindow = TermWindow(self.master)

    def TurnLedOn(self):
        if serialPort != None:
            serialPort.write(str.encode('1'))

    def TurnLedOff(self):
        if serialPort != None:
            serialPort.write(str.encode('0'))

# Program entry point
if __name__ == '__main__' :
    # First, try to open the serial port.
    try:
        serialPort = serial.Serial(port=port, baudrate=baudrate)
    except:
        print("Failed to open serial port " + port)
        sys.exit(-1)

    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
    #root.destroy()
