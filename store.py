import config as cf
from tables import *
import numpy as np
import data_containers as dc



class Infos(IsDescription):
    run          = UInt16Col()
    subfile      = UInt16Col()
    n_events     = UInt8Col()
    process_date = UInt32Col()
    n_samples    = UInt32Col()
    sampling     = Float16Col()
    pre_trig     = UInt32Col()
    voltage      = Float16Col(shape=(cf.n_PMT))

def store_run_infos(h5file, now):
    table = h5file.create_table("/", 'infos', Infos, 'Run Infos')
    inf   = table.row

    inf['run']      = dc.the_run.run
    inf['subfile']  = dc.the_run.sub
    inf['n_events'] = dc.the_run.n_events

    inf['process_date'] = now
    
    inf['n_samples'] = dc.the_run.n_samples
    inf['sampling']  = dc.the_run.sampling
    inf['pre_trig']  = dc.the_run.pre_trig
    inf['voltage']   = dc.the_run.voltage
    
    inf.append()
    table.flush()


def new_event(h5file, event_nb):
    return h5file.create_group("/", 'event_'+str(event_nb), 'Event '+str(event_nb))    



class Event(IsDescription):
    evt_nb  = UInt32Col()
    time_s  = UInt32Col()
    time_ns = UInt32Col()


def store_event(h5file, group):
    table = h5file.create_table(group, 'event', Event, "Event")

    evt = table.row

    evt['evt_nb']  = dc.event_list[-1].evt
    evt['time_s']  = dc.event_list[-1].time_s
    evt['time_ns'] = dc.event_list[-1].time_ns

    evt.append()
    table.flush()


class Pedestal(IsDescription):

    mean = Float16Col(shape=(cf.n_PMT))
    rms  = Float16Col(shape=(cf.n_PMT))


def store_pedestal(h5file, group):
    table = h5file.create_table(group, 'pedestals', Pedestal, 'Pedestals')

    ped = table.row
    ped['mean'] = dc.event_list[-1].ped_mean
    ped['rms'] = dc.event_list[-1].ped_rms
    ped.append()
    table.flush()


class S1Peaks(IsDescription):
    pmt       = UInt8Col()
    bin_max   = UInt32Col()
    t_max     = Float32Col()
    amplitude = Float16Col()
    width     = Float32Col()
    integral  = Float32Col()

def store_S1_peaks(h5file, group):
    table = h5file.create_table(group, 'S1_peaks', S1Peaks, 'S1 Peaks')
    
    peaks = table.row
    for p in dc.S1_peaks_list:
        peaks['pmt']       = p.pmt
        peaks['bin_max']   = p.bin_max
        peaks['t_max']     = p.t_max
        peaks['amplitude'] = p.amp
        peaks['width']     = p.width * dc.the_run.sampling
        peaks['integral']  = p.integral
        peaks.append()
    table.flush()
        



