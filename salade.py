import sys
import os
import numpy as np
import time 
import tables as tables


import config as cf
import data_containers as dc
import store as store
import plot as plot

import pmt_map as pm
import reader as read
import pedestal as ped
import S1_peak_finder as peak
import analysis as ana

def need_help():
    print("Usage: python reader.py ")
    print(" -run <light run number ex:1970> ")
    print(" -sub <sub file ex: 0001> ")
    print(" -n   <number of event to process>  [default (or -1) is all]")
    print(" -out <output name optn>")
    print(" -h print this message")

    sys.exit()
    

if len(sys.argv) == 1:
    need_help()
else:
    for index, arg in enumerate(sys.argv):
        if arg in ['-h'] :
            need_help()



outname_option = ""
nevent  = -1
for index, arg in enumerate(sys.argv):
    if arg in ['-run'] and len(sys.argv) > index + 1:
        run_n = sys.argv[index + 1]
    elif arg in ['-sub'] and len(sys.argv) > index + 1:
        sub_file = sys.argv[index + 1]
    elif arg in ['-n'] and len(sys.argv) > index + 1:
        nevent = int(sys.argv[index + 1])
    elif arg in ['-out'] and len(sys.argv) > index + 1:
        outname_option = sys.argv[index + 1]
    
t_start = time.time()

run = int(run_n)
sub = int(sub_file)
name_in = cf.data_path + "%03d"%int(run/1000) + "/output_" + "%06d"%run + "_" + "%04d"%sub + ".root"
print("input file: ", name_in)

if(os.path.exists(name_in) is False):
    print(" ERROR ! file ", name_in, " do not exists ! ")
    sys.exit()



if(outname_option):
    outname_option = "_"+outname_option
else:
    outname_option = ""
    
name_out = cf.store_path + "/" + run_n + "_" + sub_file + outname_option + ".h5"

print("output file: ", name_out)

output = tables.open_file(name_out, mode="w", title="Reconstruction Output")

dc.the_run.run_sub(run, sub)

""" open root file and extract data taking conditions """
reading = read.reader(name_in)

nb_evt = dc.the_run.n_events
if( nevent > nb_evt or nevent < 0):
    nevent = nb_evt

print("---> Will process ", nevent, " events [out of ", nb_evt, "]")

dc.the_run.dump()
store.store_run_infos(output, time.time())
pm.build_map()


for iev in range(nevent):
    print("* * * * * * * * * *")
    print("  EVENT ", iev, "  ")
    print("* * * * * * * * * *")

    dc.reset_event()
    gr = store.new_event(output, iev)
    
    ts, tns = reading.get_time_event(iev)
    dc.event_list.append(dc.event(iev, ts, tns))
    store.store_event(output, gr)

    dc.event_list[-1].dump_time()
    
    """ extract raw data from ROOT file and store as np array """
    reading.get_waveforms(iev)

    """ compute pedestal and RMS for each PMT """
    ped.get_pedestal(100)
    store.store_pedestal(output, gr)

    """
    dc.event_list[-1].dump_ped_rms(0)
    dc.event_list[-1].dump_ped_rms(2)
    dc.event_list[-1].dump_ped_rms(3)
    dc.event_list[-1].dump_ped_rms(4)
    """

    """ subtract pedestal to waveforms """
    ped.subtract_ped()


    """ find S1 peaks """
    """ arguments: Nsigma signal, min width (nb bins),  Nsigma ped"""
    peak.find_peaks(10, 5, 3)
    
    #plot.plot_wvf_and_S1(3, 10)

    np = []
    for ipmt in range(36):
        np.clear()
        [np.append(1) for x in dc.S1_peaks_list if x.pmt == ipmt]
        print("PMT ", ipmt, " -> ", len(np))


    #[x.dump() for x in dc.S1_peaks_list if x.pmt == 3]
    
    """ sort S1 peaks list by increasing time """
    dc.S1_peaks_list.sort()

    #[x.dump() for x in dc.S1_peaks_list]
    #plot.plot_timeline()
    store.store_S1_peaks(output, gr)
    
    ana.ana_peaks(10)

output.close()
tottime = time.time() - t_start
print(" TOTAL RUNNING TIME %.2f s == %.2f s/evt"% (tottime, tottime/nevent))

