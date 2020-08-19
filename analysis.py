import numpy as np

import config as cf
import data_containers as dc
import plot as plot



def ana_peaks(min_pmt):
    
    n_peaks = len(dc.S1_peaks_list)
    event = []

    ip = 0
    
    n_events = 0
    while(ip < n_peaks):
        event.append( dc.S1_peaks_list[ip] )
        t = event[-1].bin_max
        ip += 1
        while( ip < n_peaks and abs(t - dc.S1_peaks_list[ip].bin_max) < 5 ):
            event.append( dc.S1_peaks_list[ip] )
            ip += 1

        if(len(event) < min_pmt):
            event.clear()
        else:
            print(" at ", t, " --> ", len(event), " pmts")
            if(n_events < 1):
                plot.plot_ED(event)
            n_events += 1
            event.clear()
    print(" --> ", n_events, " found")
    
        


