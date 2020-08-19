import config as cf
import numpy as np
import time

#don't know yet the size of the data
data = np.zeros( (36, 1) )
S1_peaks_list = []
event_list = []

pmt_list = []

def reset_event():
    data[:,:] = 0.
    S1_peaks_list.clear()



class pmt:
    def __init__(self, ana_nb, hv_nb):
        self.nb = ana_nb
        self.ch = hv_nb
        
    def xy_pos(self, x, y):
        self.x = x
        self.y = y
        
    def name(self, name):
        self.name = name

    def crp(self, crp):
        self.crp = crp
    
    def wls(self, isPEN, isTPB):
        self.isPEN = isPEN
        self.isTPB = isTPB


    def dump(self):
        print(" PMT ", self.nb, " channel ", self.ch, " name ", self.name)
        print(" at x = ", self.x, ", y = ", self.y, " CRP ", self.crp)
        print(" Is PEN ? ", self.isPEN, " is TPB ? ", self.isTPB)


class run_info:
    def __init__(self):
        self.run       = -1
        self.sub       = -1
        self.n_events  = -1
        self.sampling  = -1
        self.n_samples = -1
        self.pre_trig  = -1
        self.post_trig = -1
        
    def run_sub(self, run, sub):
        self.run      = run
        self.sub      = sub

    def run_data(self, n_events, sampling, n_samples, pre_trig, post_trig, voltage):
        self.n_events  = n_events
        self.sampling  = sampling
        self.n_samples = n_samples
        self.pre_trig  = pre_trig
        self.post_trig = post_trig
        self.voltage   = voltage
    
    def dump(self):
        print("\n-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°- ")
        print(" Run ", self.run, " Sub-File ", self.sub)
        print(" Total nb of events: ", self.n_events,"\n")
        print(" Nb of samples: ", self.n_samples)
        print(" Pre-trigger: ", self.pre_trig)
        print(" Sampling: ", self.sampling, " ns")
        print(" -> Acquisition window = [-", self.pre_trig*self.sampling*1.e-3, " ; +", self.post_trig*self.sampling*1.e-3, "] mus\n")
        print(" PMT Voltages: ")
        print(self.voltage)
        print("-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°-°- \n")

the_run = run_info()


class event:
    def __init__(self, evt, time_s, time_ns):
        self.evt     = evt
        self.time_s  = time_s
        self.time_ns = time_ns
    
    def ped_rms(self, mean, rms):
        self.ped_mean = mean
        self.ped_rms  = rms

    def dump_time(self):
        print(" Taken on ", self.time_s, " + ", self.time_ns)
        print("   ", time.ctime(self.time_s),"\n")


    def dump_ped_rms(self, ipmt):
        print(" PMT ", ipmt, " pedestal = %.2f ADC, RMS = %.2f ADC "%(self.ped_mean[ipmt], self.ped_rms[ipmt]))



class S1_peak:
    def __init__(self, pmt, bin_max, amp, width, integral):
        self.pmt      = pmt
        self.bin_max  = bin_max
        self.amp      = amp
        self.width    = width
        self.integral = integral
        
    def dump(self):
        print(self.pmt, " at ", self.bin_max, " : %.3f"%(self.t_max*1e-3), " %.2f"% self.amp, " ", self.width) 

    def compute_time(self):
        self.t_max = (self.bin_max - the_run.pre_trig)*the_run.sampling

    def __lt__(self, other):
        """sort S1 peaks by increasing time """
        return (self.bin_max < other.bin_max) or (self.bin_max == other.bin_max and self.amp > other.amp)

    
