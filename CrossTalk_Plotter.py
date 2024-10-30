import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from scipy.stats import norm
import ROOT
from astropy import modeling
import math
from glob import glob

#
# Default Settings
#

ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)

positions = [-600, -400, -200, 0, 200, 400, 600]
channelPositions = {
	8  : -600,
	9  : -400,
	10 : -200,
	11 :  0,
	12 :  200,
	13 :  400,
	14 :  600
}

files = glob("*.root")


"""
List of all Voltages (9 root files)
210V
150V
100V
"""

#
# Creats a Dictionary to Navigate the Voltages
#
def dictionary(file):
	voltageIndex = {
		'100V': [],
		'150V': [],
		'210V': []
	}
	# Finding the Index of each voltage and adding it to "voltageIndex"
	for keys in voltageIndex:
		for i in range(len(files)):
			if files[i].split("_")[9] == keys:
				voltageIndex[keys].append(i)
	return voltageIndex
	


#
# Finds Channel then Voltage Averages
#
def voltage_averages(voltageIndex, entries):

	voltageIndexValues = {
		'100V': [],
		'150V': [],
		'210V': []
	}

	pulseIndexValues = {
		'100V': [],
		'150V': [],
		'210V': []
	}

	# Navigating the Dictionary
	for keys in voltageIndex: 

		# Creating the properly sized Array
		tempVoltageArray = []
		tempPulseArea = []
		for i in range(len(channelPositions)):
			tempVoltageArray.append([])
			tempPulseArea.append([])
		

		# Opening the same Voltage files
		for i in voltageIndex[keys]: 
			f = ROOT.TFile.Open(files[i])
			tree = f.Get('wfm')
			

			# Navigating Each Entry
			for entry in range(entries):
				print(str(keys) + " Entry: " + str(entry))
				tree.GetEntry(entry)
				#if tree.pmax11 > 25:  # 20 or 25 is above most noise
					
					# Pmax Values per entry
				pmaxValues = [tree.fallTime8, tree.fallTime9, tree.fallTime10, tree.fallTime11, tree.fallTime12, tree.fallTime13, tree.fallTime14]
				#for i in range(len(pmaxValues)):
				#		pmaxValues[i] = abs(pmaxValues[i])
				for i in range(len(channelPositions)):
						tempVoltageArray[i].append(pmaxValues[i])

					# PulseArea Values per entry
				#pulseArea = [tree.pulseArea8, tree.pulseArea9, tree.pulseArea10, tree.pulseArea12, tree.pulseArea13, tree.pulseArea14]
				#for i in range(len(pulseArea)):
				#	tempPulseArea[i].append(pulseArea[i])
		
		# Finding Number of Entries actually used
		global numOfEntries
		numOfEntries = len(tempVoltageArray[0])

		# Calcualtes Averages
		for i in range(len(tempVoltageArray)):
			tempVoltageArray[i] = np.average(tempVoltageArray[i])
		voltageIndexValues[keys] = tempVoltageArray

		#for i in range(len(tempPulseArea)):
		#	tempPulseArea[i] = np.average(tempPulseArea[i])
		#pulseIndexValues[keys] = tempPulseArea

	return voltageIndexValues #, pulseIndexValues


entries = 1000  # 100000 Max
voltageValues = voltage_averages(dictionary(files), entries)


# Normal Plotting with all channels
def plot_regular():
	"""
	Regular Plotting, the crosstalk plot. Voltage by channel, by run bias voltage
	"""
	
	colormap = cm.get_cmap("rainbow", len(voltageValues))

	fig, ax = plt.subplots()
	
	markers = ["o", "s", "^", "D", "p", "*", "v", "<", ">", "x", "+"]
	
	i=0
	for keys in voltageValues:
	
		color = colormap(i)
		marker = markers[i % len(markers)]
		ax.scatter(positions, voltageValues[keys], color=color, label=keys, marker=marker)
		i += 1
		
	ax.set_title("Rise Time: " + str(entries) + " Entries" +"| Entries used: " + str(numOfEntries))
	ax.set_xlabel("Distance from Trigger Channel (µm)")
	ax.set_ylabel("Rise Time Average")
	legend = ax.legend(title="Bias Voltages")
	for i, text in enumerate(legend.get_texts()):
		text.set_color(colormap(i))
	fig.savefig("CrossTalk_Plot_falllTime_Entries_by_Voltage" + str(entries) + ".png")


#
# Writing all values to a txt
#
#channelVoltageAveragesTxt = open('channelVoltageAveragesTxt', 'wt')
#channelVoltageAveragesTxt.write(str(voltageValues))


#
# Plots Gaussian Distribution
#
def gaussian_distribution():
	
	# Finding Average of each Position
	averageAtEachPosition = []
	for i in range(len(positions)):
		temp_array = []
		for keys in voltageValues:
			temp_array.append(voltageValues[keys][i])
		averageAtEachPosition.append(np.average(temp_array))

	#  Finding Mean
	mean_sum = 0
	for i in range(len(averageAtEachPosition)):
		mean_sum += averageAtEachPosition[i]
	x_mean = 0
	for i in range(len(averageAtEachPosition)):
		x_mean = ((averageAtEachPosition[i] / mean_sum) * positions[i])
	x_mean = x_mean / len(positions)
	print(x_mean)
#gaussian_distribution()


"""
Different Plotting Options
"""
def plot_without_trigger():
	"""
	Plots without the sensor trigger and uses it's pulseArea ratio to the strike channel 
	(in this case 10) to reduce neightbor channel (in this case channel 9)
	"""
	triggerPulseValues = []
	for keys in pulseValues:
		triggerPulseValues.append(pulseValues[keys][3])
	triggerPulseAverage = np.average(triggerPulseValues)

	strikePulseValues = []
	for keys in pulseValues:
		strikePulseValues.append(pulseValues[keys][2])
	strikePulseAverage = np.average(strikePulseValues)
	
	ratio = strikePulseAverage / triggerPulseAverage
	ratio2 = triggerPulseAverage / strikePulseAverage

	for keys in voltageValues:
		voltageValues[keys][4] = voltageValues[keys][4] / ratio2


def plot_specific_channel():
	x_axis = ["100V", "150V", "210V"]
	

	# Reference [-1500, -1000, -500, 0, 500, 1000, 1500, 2000]
	channelValues = [[], [], [], [], [], []]
	labels = ["8", "9", "10", "12", "13", "14"]

	for i in range(len(channelValues)):
		for keys in voltageValues:
			channelValues[i].append(voltageValues[keys][i])

	for l in channelValues:
		l = l.reverse()


	for i in range(len(channelValues)):
		plt.scatter(x=x_axis, y=channelValues[i], label=labels[i])

	plt.title("Pmax# Average by Bias Voltage | Entries " + str(entries))
	plt.xlabel("Run Bias Voltage")
	plt.ylabel("Pmax Average (mV)")
	plt.legend(title="Channel", loc="upper left")
	plt.savefig("Pmax Average# by Voltage | Entries: " + str(entries) + ".png")


#plot_specific_channel()
#plot_without_trigger()
plot_regular()
