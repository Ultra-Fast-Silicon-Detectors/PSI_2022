import ROOT
from glob import glob
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)

# Options
file_in = "stats_PSI_Run_120_TI_LGAD_strips_29MeV_u_150V_18uA_trig_front_gate_trig_5mV_250um_degrader.root"
run = file_in.split("_")[3]
sensor_ch = "11"
strip_nebh = ['8', '9', '10', '12', '13', '14'] #In order from farthest to closest not including sensor channel
colors = [4, 7, 3, 5, 2, 6, 9]
rangx = [112000, 155000]
rangy = [-50, 100]

# Open File
f = ROOT.TFile.Open(file_in)
tree = f.Get("wfm")

# Run
entry = "411"
h_name = "wavename"
	

h_tmp = ROOT.TH1F(h_name, "Example", 1500, 0, 1500)

h_tmp.SetLineColor(1)
h_tmp.SetLineWidth(2)
h_tmp.SetLineStyle(9)

c = ROOT.TCanvas("c", "LGAD response")
c.cd()

leg = ROOT.TLegend(0.11, 0.7, 0.275, 0.899)
leg.SetTextAlign(13)

#for i in strip_nebh:
tree.Draw("w" + sensor_ch + ":timeTrigger_ps", "Entry$==" + entry, "")
leg.AddEntry(h_tmp,"Ch" + sensor_ch)

# Needed
vx = tree.GetV2()
vy = tree.GetV1()
g = ROOT.TGraph(1024, vx, vy)
g.SetLineStyle(9)
g.Draw("Al")



# Plot
n=0
h_names = []
h_tmps = []
h_tmps2 = []

for i in range(len(strip_nebh)):
	h_names.append(str(strip_nebh[i]))
	h_tmps.append(ROOT.TH1F(h_names[i], h_name, 1500, 0, 1500))
	h_tmps[i].SetLineColor(colors[n])

	h_tmps[i].SetLineColor(colors[n])
	h_tmps[i].SetMarkerStyle(0)
	h_tmps[i].SetLineWidth(2)
	h_tmps[i].SetMarkerColor(colors[n])

	tree.SetLineColor(colors[n])
	if i == 20:
		tree.SetLineStyle(1)
		h_tmps[i].SetLineStyle(1)
		tree.Draw("w" + strip_nebh[i][0] + ":time_ps", "Entry$==" + entry, "samel")
		
		h_tmps2.insert(i,ROOT.TH1F(h_names[i], h_name, 1500, 0, 1500))
		tree.SetLineStyle(7)
		h_tmps2[i].SetLineStyle(7)
		tree.Draw("w" + strip_nebh[i][1] + ":time_ps", "Entry$==" + entry, "samel")
		#leg.AddEntry(h_tmps[i], str(strip_nebh[i][0]) +", "+ str(strip_nebh[i][1]))

		leg.AddEntry(h_tmps[i], str(strip_nebh[i][0])) 
		leg.AddEntry(h_tmps2[i], str(strip_nebh[i][1])) 
	else: 
		tree.SetLineStyle(1)
		h_tmps[i].SetLineStyle(1)
		tree.Draw("w" + strip_nebh[i] + ":time_ps", "Entry$==" + entry, "samel")
		leg.AddEntry(h_tmps[i], str(strip_nebh[i]))
	n += 1


g.GetXaxis().SetRangeUser(rangx[0],rangx[1])
g.GetXaxis().SetTitle("Time (ps)")
g.GetYaxis().SetRangeUser(rangy[0],rangy[1])
g.GetYaxis().SetTitle("Amplitude (mV)")
leg.SetHeader("Channel Color Index")


leg.Draw()
c.Draw()
c.Update()

# Save
c.SaveAs(f"MultiWaveFormPlot_Run{run}_Entry" + entry + ".png")

g.GetXaxis().SetRangeUser(0,300000)
c.SaveAs(f"MultiWaveFormPlot_Run{run}_Entry" + entry + "_unzoomed.png")
print('Done!')
