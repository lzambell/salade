import numpy as np
import matplotlib.pyplot as plt

from matplotlib.colors import LinearSegmentedColormap
import matplotlib.gridspec as gridspec


import data_containers as dc
import config as cf

light_blue_red_dict = {
    'red': ((0.,    65./255.,  65./255.),
            (0.15, 123./255., 123./255.),
            (0.25, 160./255., 160./255.),
            (0.375, 222./255.,222./255.),
            (0.5, 214./255., 214./255.),
            (0.625, 199./255., 199./255.),
            (0.75, 183./255., 183./255.),
            (0.875, 153./255., 153./255.),
            (1., 78./255., 78./255.)),

    'green':  ((0.,  90./255.,  90./255.),
              (0.15, 171./255., 171./255.),
              (0.25,  211./255., 211./255.),
              (0.375,  220./255.,  220./255.),
              (0.5, 190./255., 190./255.),
              (0.625,  132./255., 132./255.),
              (0.75,  65./255.,  65./255.),
              (0.875, 0./255., 0./255.),
               (1.,  0./255., 0./255.)),
        
    
    
    'blue':   ((0.,  148./255., 148./255.),
               (0.15, 228./255., 228./255.),
               (0.25, 222./255., 222./255.),
               (0.375,  160./255.,  160./255.),
               (0.5, 105./255., 105./255.),
               (0.625, 60./255., 60./255.),
               (0.75, 34./255., 34./255.),
               (0.875, 0./255., 0./255.),
               (1.,  0./255., 0./255.))
    
}
lbr_cmp = LinearSegmentedColormap('lightBR', light_blue_red_dict)



def plot_wvf_and_S1(pmt, sigma, option=None):
    fig = plt.figure( figsize = (12,6))
    ax = []
    
    times = [x.bin_max for x in dc.S1_peaks_list if x.pmt == pmt]
    amp   = [x.amp for x in dc.S1_peaks_list if x.pmt == pmt]
    
    ax.append( fig.add_subplot(2, 1, 1) )
    ax[-1].plot(np.arange(0,dc.the_run.n_samples, 1), dc.data[pmt,:], c='black')

    thr = sigma*dc.event_list[-1].ped_rms[pmt]
    ax[-1].plot([0,dc.the_run.n_samples], [thr, thr], c = 'c', ls='dotted')

    ymin, ymax = ax[-1].get_ylim()
    
    for t in times:
        ax[-1].plot([t,t], [ymin, ymax], ls="--",c='r')


    ax.append( fig.add_subplot(2, 1, 2) )
    ax[-1].hist(amp, 100, color='cyan', histtype='stepfilled', edgecolor='blue', log=True)

    run = dc.the_run.run
    sub = dc.the_run.run
    evt = dc.event_list[-1].evt


    if(option):
        option = "_"+option
    else:
        option = ""


    plt.savefig('plot/wvf_S1_peaks'+option+'_run_'+str(run)+'_sub_'+str(sub)+'_evt_'+str(evt)+'_pmt'+str(pmt)+'.png')
    plt.show()
    plt.close()    



def plot_timeline(option=None):
    fig = plt.figure( figsize=(12,4))
    
    times = [x.t_max*1.e-3 for x in dc.S1_peaks_list]

    win_min = -(dc.the_run.pre_trig)*dc.the_run.sampling
    win_max = (dc.the_run.post_trig)*dc.the_run.sampling

    
    nbins = int(dc.the_run.n_samples*dc.the_run.sampling/400.)
      
    if(nbins > 1000):
        nbins = 1000

    plt.hist(times, nbins, color='black', range=(win_min*1.e-3, win_max*1.e-3) )
    plt.xlabel("Time [mus]")
    plt.ylabel("N PMTs")

    run = dc.the_run.run
    sub = dc.the_run.run
    evt = dc.event_list[-1].evt
    
    if(option):
        option = "_"+option
    else:
        option = ""


    plt.savefig('plot/S1_timeline'+option+'_run_'+str(run)+'_sub_'+str(sub)+'_evt_'+str(evt)+'.png')
    plt.show()
    plt.close()    
          #, histtype='stepfilled', edgecolor='blue', log=True)
        


def plot_ED(event, option=None):
    #fig = plt.figure( figsize=(8,8) )
    
    fig, ax = plt.subplots( figsize=(8,8) )

    pen_amp = [x.amp for x in event if dc.pmt_list[x.pmt].isPEN is True]
    pen_x   = [dc.pmt_list[x.pmt].x for x in event if dc.pmt_list[x.pmt].isPEN is True]
    pen_y   = [dc.pmt_list[x.pmt].y for x in event if dc.pmt_list[x.pmt].isPEN is True]
        
    tpb_amp = [x.amp for x in event if dc.pmt_list[x.pmt].isTPB is True]
    tpb_x   = [dc.pmt_list[x.pmt].x for x in event if dc.pmt_list[x.pmt].isTPB is True]
    tpb_y   = [dc.pmt_list[x.pmt].y for x in event if dc.pmt_list[x.pmt].isTPB is True]
    
    max_amp = max(tpb_amp) if max(tpb_amp) > max(pen_amp) else max(pen_amp)
    min_amp = min(tpb_amp) if min(tpb_amp) > min(pen_amp) else min(pen_amp)

    all_tpb_x = [x.x for x in dc.pmt_list if x.isTPB is True]
    all_tpb_y = [x.y for x in dc.pmt_list if x.isTPB is True]
    all_pen_x = [x.x for x in dc.pmt_list if x.isPEN is True]
    all_pen_y = [x.y for x in dc.pmt_list if x.isPEN is True]

    ax.fill([-3000, -3000, 3000, 3000, 1000, 1000, 0, 0], [0, -3000, -3000, 0, 0, -1000, -1000, 0], c='gray', alpha=0.2)

    pen = ax.scatter(pen_x, pen_y, c=pen_amp, cmap=lbr_cmp, s=160, marker="o", vmin = min_amp, vmax = max_amp)
    tpb = ax.scatter(tpb_x, tpb_y, c=tpb_amp, cmap=lbr_cmp, s=160, marker="D", vmin = min_amp, vmax = max_amp)

    ax.scatter(all_pen_x, all_pen_y, facecolors='none', edgecolors='k', s=160, marker="o")
    ax.scatter(all_tpb_x, all_tpb_y, facecolors='none', edgecolors='k', s=160, marker="D")

    ax.plot([0, 0], [-3000, 3000], c='k')
    ax.plot([-3000, 3000], [0,0], c='k')

    ax.plot([0, 1000], [-1000, -1000], c='k', ls="--")
    ax.plot([1000, 1000], [-1000, -0], c='k', ls="--")

    ax.text( 2750,  2850, 'CRP 1', horizontalalignment='center', verticalalignment='center')
    ax.text(-2750,  2850, 'CRP 2', horizontalalignment='center', verticalalignment='center')
    ax.text(-2750, -2850, 'CRP 3', horizontalalignment='center', verticalalignment='center')
    ax.text( 2750, -2850, 'CRP 4', horizontalalignment='center', verticalalignment='center')

    ax.set_xlabel("x [mm]")
    ax.set_ylabel("y [mm]")

    ax.set_title("At t = %.3f mus"%(event[0].t_max*1e-3))

    ax.set_xlim(-3000., 3000.)
    ax.set_ylim(-3000., 3000.)

    cb = fig.colorbar(tpb)
    cb.set_label("S1 Amplitude [ADC]")
    run = dc.the_run.run
    sub = dc.the_run.run
    evt = dc.event_list[-1].evt

    bin_time = event[0].bin_max

    if(option):
        option = "_"+option
    else:
        option = ""


    plt.savefig('plot/S1_amplitudes'+option+'_run_'+str(run)+'_sub_'+str(sub)+'_evt_'+str(evt)+'_bin_'+str(bin_time)+'.png')
    plt.show()
    plt.close()    
          #, histtype='stepfilled', edgecolor='blue', log=True)
