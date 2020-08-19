import numpy as np

import data_containers as dc
import config as cf



def get_pedestal(slice_size):

    if(slice_size >= dc.the_run.n_samples):
        """temporary"""
        return 
        
    if(dc.the_run.n_samples%slice_size == 0):
        n_slices = int(dc.the_run.n_samples/slice_size)
        tmp = np.reshape(dc.data, (cf.n_PMT, n_slices, slice_size))
        
    else:
        rest = dc.the_run.n_samples%slice_size
        n_slices = int((dc.the_run.n_samples-rest)/slice_size)        
        tmp = np.reshape(dc.data[:, 0:-rest], (cf.n_PMT, n_slices, slice_size))
        
    mean_slices = np.mean(tmp, axis=2)
    rms_slices  = np.std(tmp, axis=2)

    min_rms_idx = np.argmin(rms_slices, axis=1)


    mean = mean_slices[np.arange(mean_slices.shape[0]), min_rms_idx]
    rms  = rms_slices[np.arange(rms_slices.shape[0]), min_rms_idx]

    dc.event_list[-1].ped_rms(mean, rms)



    
def subtract_ped():
    dc.data *= -1.
    dc.data += dc.event_list[-1].ped_mean[:, None]
