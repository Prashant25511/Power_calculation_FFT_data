from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from pyqtgraph.ptime import time
import serial
import time
from scipy.fftpack import fft as fp
from scipy.fftpack import fftfreq as fpf

global data_display

app = QtGui.QApplication([])

p = pg.plot()
p.setWindowTitle('live plot from serial')
curve = p.plot()
sampling_freq = 44000
raw=serial.Serial("com5",baudrate=115200,bytesize=8,stopbits=1,timeout=1)

data_display = []


chunk_size=10# smaller chunk size = slower data
freqs = fpf(chunk_size)*sampling_freq

freq_index = np.arange(int(np.floor(chunk_size*800/sampling_freq)),int(np.ceil(chunk_size*1100/sampling_freq)+1))
power = []

def update():
	
	global  data_display,power
	
	current_data = np.zeros(chunk_size,dtype=int)
	
	for i in range(chunk_size):
		current_data[i]=raw.readline()
	# current_data=int(raw.readline()) # this makes it sloww

	freq_sig = np.abs(fp(current_data)*2*np.pi/chunk_size)
	
	power = np.append(power, np.sqrt(sum(freq_sig[freq_index]**2)))

	curve.setData(power)

	app.processEvents()


timer = QtCore.QTimer()
timer.start() 
timer.timeout.connect(update)



if __name__ == '__main__':
	import sys
	if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
		QtGui.QApplication.instance().exec_()