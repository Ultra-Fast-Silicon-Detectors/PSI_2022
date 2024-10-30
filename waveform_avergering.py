import ROOT
import numpy as np
import argparse
import os
import glob
from array import array
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm

#file = "stats_PSI_Run_122_TI_LGAD_strips_29MeV_u_150V_18uA_trig_front_gate_trig_5mV_100um_degrader.root"

files = glob.glob("*120*.root")


def wave_form_averager(input_file, num_evt_to_avg, dut_channel, pmax_cut_channel, pmax_cut, cfd_percent, index_to_zero, negative_cfd):
    # Retrieve the TTree
    i_file = ROOT.TFile.Open(input_file,"READ")
    tree = i_file.Get("wfm")    
    averager = [array('d', [] * 1) for _ in range(1024)]
    time = array('d', [-99] * 1024) 
    pmax_zeroing_index = -1
    #print(averager)
    evt_count = 0
    for index, event in enumerate(tree):
        w_attr_name = f"w{dut_channel}"
        pmax_attr_name = f"pmax{dut_channel}"
        pmin_attr_name = f"negPmax{dut_channel}"
        pmax_cut_attr_name = f"pmax{pmax_cut_channel}"
        pmax_index_attr_name = f"max_indexing{dut_channel}"

        tree_w = getattr(event, w_attr_name)
        tree_pmax = getattr(event, pmax_attr_name)
        tree_pmin = getattr(event, pmin_attr_name)
        tree_pmax_cut = getattr(event, pmax_cut_attr_name)
        tree_pmax_index = getattr(event, pmax_index_attr_name)


        if (tree_pmax_cut>pmax_cut and tree_pmin != 0):
            evt_count=evt_count+1
        else:
            continue
        
        if negative_cfd == False:
            cfd_val = cfd_percent * tree_pmax
            cfd_index_found = False
            cfd_index = tree_pmax_index
        
            #print("pmax:",tree_pmax)
            #print("cfd_val:",cfd_val)
            while cfd_index_found == False:
                if (tree_w[cfd_index] > cfd_val):
                    #print(cfd_index)
                    #print(tree_w[cfd_index])
                    cfd_index -= 1
                else:
                    cfd_index_found = True
                    #print("TRUE:", tree_w[cfd_index])
        elif negative_cfd == True:
            cfd_val = cfd_percent * tree_pmin
            cfd_index_found = False
            cfd_index = tree_pmax_index
            
            while tree_w[cfd_index] != tree_pmin:
                #print(tree_pmin, tree_w[cfd_index],index)
                cfd_index -= 1
            #print("pmax:",tree_pmax)
            #print("cfd_val:",cfd_val)
            while cfd_index_found == False:
                if (tree_w[cfd_index] > cfd_val):
                    #print(cfd_index)
                    #print(tree_w[cfd_index])
                    cfd_index -= 1
                else:
                    cfd_index_found = True
                    #print("TRUE:", tree_w[cfd_index])
            

            
        if evt_count == 1:
            time = event.time_ps
            pmax_zeroing_index = index_to_zero
        elif evt_count>num_evt_to_avg:
            break
        

        pmax_difference = - pmax_zeroing_index + cfd_index
        #print(pmax_difference)
        for m in range(len(tree_w)):
            #print(m+pmax_difference)
            if m+pmax_difference < 0:
                averager[m].append(0.0)
            elif m+pmax_difference >1023:
                averager[m].append(0.0)
            else:
                averager[m].append(tree_w[m+pmax_difference])



       
    av_wfm = array('d', [-99] * 1024) 

    for n in range(len(averager)):
        av_wfm[n]=sum(averager[n])/len(averager[n])
    #print(time)
    #print(av_wfm)
    ax.plot(time[50:974],av_wfm[50:974], color=color, label=dut_channel)
    i_file.Close()


def full_plot_and_save(num_evnt_to_avg, pmax_cut):

	for file in files:
		plt.clf()
		runNumber = file.split("_")[3]
		
		colormap = cm.get_cmap("rainbow", 5)
		global fig, ax
		fig, ax = plt.subplots()
		global color
			
			#wave_form_averager(file, num_evnt_to_avg, 6, pmax_cut, False)
		color = colormap(0)
		wave_form_averager(file, num_evnt_to_avg, 9,  10, pmax_cut, 0.2, 628, False)
		color = colormap(1)
		wave_form_averager(file, num_evnt_to_avg, 10, 10, pmax_cut, 0.2, 628, True)
		color = colormap(2)
		wave_form_averager(file, num_evnt_to_avg, 11, 10, pmax_cut, 0.2, 628, False)
		color = colormap(3)
		wave_form_averager(file, num_evnt_to_avg, 12, 10, pmax_cut, 0.2, 628, False)
		color = colormap(4)
		wave_form_averager(file, num_evnt_to_avg, 13, 10, pmax_cut, 0.2, 628, False)
			
		ax.set_title(f"Run{runNumber} Average Wave Form | Events: {num_evnt_to_avg}")
		ax.set_xlabel("Time (ps)")
		ax.set_ylabel("Voltage (mV)")
		ax.set_xlim(240000, 260000)
		legend = plt.legend(title="Chanel")
		
		for i, text in enumerate(legend.get_texts()):
			text.set_color(colormap(i))
			
		fig.savefig(f"Waveform_average_Run{runNumber}_Entries{num_evnt_to_avg}.png")
		print(f"Run{runNumber} Done")


full_plot_and_save(1000, 60)




