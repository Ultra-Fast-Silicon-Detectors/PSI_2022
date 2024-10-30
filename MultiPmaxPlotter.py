#
# Imports
#
import ROOT
import math


#
# Changeable settings
#



# Default Settings
#
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)


files=[	'stats_PSI_Run_131_TI_LGAD_strips_29MeV_u_210V_18uA_trig_front_gate_trig_5mV_250um_plus_250um_degrader_in_front.root', 
	'stats_PSI_Run_130_TI_LGAD_strips_29MeV_u_210V_18uA_trig_front_gate_trig_5mV_100um_plus_250um_degrader_in_front.root', 
	'stats_PSI_Run_129_TI_LGAD_strips_29MeV_u_210V_18uA_trig_front_gate_trig_5mV_250um_degrader_in_front.root', 
	'stats_PSI_Run_133_TI_LGAD_strips_29MeV_u_210V_18uA_trig_front_gate_trig_5mV_500um_plus_250um_degrader_in_front.root', 
	'stats_PSI_Run_128_TI_LGAD_strips_29MeV_u_210V_18uA_trig_front_gate_trig_5mV_300um_degrader.root', 
	'stats_PSI_Run_132_TI_LGAD_strips_29MeV_u_210V_18uA_trig_front_gate_trig_5mV_500um_plus_250um_degrader_in_front.root', 
	'stats_PSI_Run_127_TI_LGAD_strips_29MeV_u_210V_18uA_trig_front_gate_trig_5mV_350um_degrader.root'
]

"""
List of all Voltages (9 root files)
230V
210V
200V
190V
180V
150V
100V
"""
openFiles = [
	ROOT.TFile.Open(files[0]),
	ROOT.TFile.Open(files[1]),
	ROOT.TFile.Open(files[2]),
	ROOT.TFile.Open(files[3]),
	ROOT.TFile.Open(files[4]),
	ROOT.TFile.Open(files[5]),
	ROOT.TFile.Open(files[6])
]


#
# Creats a Dictionary to Navigate the Voltages
#
def dictionary(file):
	voltageIndex = {
		'250um': [2],
		'300um': [4],
		'350um': [1, 6],
		'500um': [0],
		'750um': [3, 5]
	}
	# Finding the Index of each voltage and adding it to "voltageIndex"
	#for keys in voltageIndex:
	#	for i in range(len(files)):
	#		if files[i].split("_")[7] == keys:
	#			voltageIndex[keys].append(i)
	return voltageIndex


#
# Averages all histograms in each voltage level, returns an array of histograms by voltage
#
def create_histograms(voltageIndex, channel):
	# Creating an array that will be returned
	histogramVoltage = []

	# Navigating through each voltage
	for keys in voltageIndex:
		voltage = str(keys)  # Creating a new variable for naming simplicity
		n = 1  # Index for more than one file(s) in voltage
		histogramArray = []  # Temp array for each histogram for each file(s) in voltage level

		# Navigating through each file in voltage level
		for values in voltageIndex[keys]:
			tree = openFiles[values].Get("wfm")  # Getting waveform
			# Creating blank histogram
			htemp = ROOT.TH1F(voltage + str(n), "Histogram " + voltage + str(n), 500, 0, 3000)
			tree.Draw("pmax" + str(channel) + ">>" + voltage + str(n), "", "")  # Drawing into blank histogram
			if n > 1:
				htemp.SetLineStyle(9)
			histogramVoltage.append(htemp)  # Adding drawn histogram into temp array
			n += 1  # Index

		# Averaging all temp histograms
		#h = ROOT.TH1F(voltage, "Histogram " + voltage, 1500, 0, 1500)  # Creating blank histogram
		# Averaging loop
		#for i in histogramArray:
		#	h = h + i
		#h = h * (1 / len(histogramArray))

		#h.GetXaxis().SetTitle(keys) # 
		#histogramVoltage.append(h)
	
	return histogramVoltage


#
# Plotting Histograms
#
def plot_histograms(histogram_array, channel):
	# Initializing
	color = 1
	c = ROOT.TCanvas("c", "LGAD response")
	leg = ROOT.TLegend(0.70, 0.4, 0.89, 0.89)

	mx = 0
	for i in histogram_array:
		high = i.GetMaximum()
		mx = max(mx, high)

	histogram_array[0].GetXaxis().SetRangeUser(-20, 450)
	histogram_array[0].GetYaxis().SetRangeUser(0, mx * 1.05) # mx * 1.05

	for i in range(len(histogram_array)):
		if i == 20 or i == 50:
			histogram_array[i].SetLineColor(color)
		else:
			histogram_array[i].SetLineColor(color)
			color += 1

		
		leg.AddEntry(histogram_array[i])
		histogram_array[i].Draw("samel")

	leg.SetHeader("Pmax" + str(channel) + " Per Degrader", "C")
	leg.Draw()

	c.SetTitle("Pmax" + str(channel) + " Per Degrader")
	c.Draw()
	c.Update
	c.SaveAs("Pmax" + str(channel) + " 210V by Degrader.png")


plot_histograms(create_histograms(dictionary(files), 6), 6)
