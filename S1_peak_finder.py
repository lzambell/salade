import numpy as np
import numexpr as ne

import config as cf
import data_containers as dc


def find_peaks(n_sigma, dt_min, n_sigma_ped):
    dc.event_list[-1].ped_rms = dc.event_list[-1].ped_rms[:,None]
    ROI = ne.evaluate( "where(data > n_sigma*rms, 1, 0)", global_dict={'data':dc.data, 'rms':dc.event_list[-1].ped_rms}).astype(bool)
    
    dc.event_list[-1].ped_rms = np.squeeze(dc.event_list[-1].ped_rms, axis=1)


    falses = np.zeros((cf.n_PMT, 1),dtype=int)
    
    ROIs = np.r_['-1',falses,np.asarray(ROI,dtype=int),falses]
    d = np.diff(ROIs)
    
    """ a change from false to true in difference is = 1 """
    start = np.where(d==1)
    """ a change from true to false in difference is = -1 """
    end   = np.where(d==-1)
    """ look at long enough sequences of trues """
    gpe = (end[1]-start[1])>=dt_min


    assert len(start[0])==len(end[0]), " Mismatch in groups of hits"
    assert len(gpe)==len(start[0]), "Mismatch in groups of hits"


    for g in range(len(gpe)):
        if(gpe[g]): #why
            
            
            """ make sure starts and ends of hit group are for same PMT """
            assert start[0][g] == end[0][g], "PMT Mismatch"

            pmt = start[0][g]

            bin_start = start[1][g]
            bin_stop = end[1][g]


            """
            if(pmt==3):
                print(" at first: ", bin_start, " to ", bin_stop)
                print(dc.data[pmt, bin_start:bin_start+4])
            """
            thr = n_sigma_ped*dc.event_list[-1].ped_rms[pmt]

            """ extend on both side until thr is reached """
            add_left = 0
            while(bin_start-add_left > 0 and dc.data[pmt, bin_start-add_left] > thr):
                add_left += 1

            if(add_left > 5):
                continue
            else:
                bin_start -= add_left

            while(bin_stop < dc.the_run.n_samples and dc.data[pmt, bin_stop] > thr):
                bin_stop += 1

            """
            if(pmt==3):
                print(" padding --> ", bin_start, " to ", bin_stop)
            """

            adc = dc.data[pmt, bin_start:bin_stop+1]
            
            bmax  = np.argmax(adc) 
            vmax  = adc[bmax]
            bmax += bin_start
            intgl = np.sum(adc)
            width = len(adc)
            
            dc.S1_peaks_list.append( dc.S1_peak(pmt, bmax, vmax, width, intgl) )
            
    [x.compute_time() for x in dc.S1_peaks_list]
