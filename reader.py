import numpy as np
import uproot

import data_containers as dc
import config as cf

class reader:
    def __init__(self, name):
        self.light_file = uproot.open(name)
        self.midas      = self.light_file["midas_data"]
        
        infos = self.light_file["run_info"]
        
        self.n_events = self.midas.numentries 

        samp = infos.array("Custom_size", 
                           entrystart=0,
                           entrystop=1)

        self.n_samples = int(samp[0]*3./2.)
        
        dec = infos.array("decimation", 
                          entrystart=0,
                          entrystop=1)

        self.sampling = pow(2, dec[0])*16.

        post = infos.array("Post_Trigger", 
                           entrystart=0,
                           entrystop=1)

        self.post_trig = post[0]
        self.pre_trig = self.n_samples - post[0]

        volt = infos.array("SlowControl_HighVoltage", 
                           entrystart=0,
                           entrystop=1)
        
        self.voltage = volt[0]

        self.keep_info()
        dc.data = np.resize(dc.data, (cf.n_PMT, self.n_samples))
        
    def keep_info(self):
        dc.the_run.run_data(self.n_events, 
                            self.sampling, 
                            self.n_samples, 
                            self.pre_trig, 
                            self.post_trig, 
                            self.voltage)

    def get_time_event(self, event):
        
        info_s = self.midas.array("timestamp_WR_sec", 
                                  entrystart = event, 
                                  entrystop  = event+1)

        info_ns = self.midas.array("timestamp_WR_nsec", 
                                   entrystart = event, 
                                   entrystop  = event+1)        
        return info_s[0][0], info_ns[0][0]
        

    def get_waveforms(self, event):
        #print(self.midas.show())
        wvf = self.midas.arrays("adc_value_*", 
                                entrystart = event, 
                                entrystop  = event+1, 
                                namedecode="utf-8")

        for ipmt in range(cf.n_PMT):
            ich = cf.nb_to_ch[ipmt]
            dc.data[ipmt] = wvf['adc_value_'+str(ich)][0]
