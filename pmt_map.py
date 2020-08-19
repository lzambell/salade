import numpy as np

import config as cf
import data_containers as dc



def which_crp(x,y):
    if(x >= 0):
        if(y >= 0):
            return 1
        else:
            return 4
    else:
        if(y >= 0):
            return 2
        else:
            return 3
    return -1

def build_map():
    for inb in range(cf.n_PMT):
        ich = cf.nb_to_ch[inb]
        dc.pmt_list.append( dc.pmt(inb, ich) )


    for ipm in dc.pmt_list:

        ipm.name(cf.pmt_name[ipm.nb])

        if(ipm.ch in cf.tpb):
            ipm.wls(False, True)
        else:
            ipm.wls(True, False)


    x_start = -2380.
    y_start = 2380.
    x_delta = 680.
    y_delta = 680.

    for ir in range(8):
        y = y_start - ir*y_delta
        
        for ic in range(8):
            x = x_start + ic*x_delta

            if(cf.mapping2D[ir][ic] >= 0):
                nb = cf.mapping2D[ir][ic]
                if(dc.pmt_list[nb].nb != nb):
                    print(" there is a problem")
                else:
                    dc.pmt_list[nb].xy_pos(x, y)
        

    for ipm in dc.pmt_list:
        ipm.crp( which_crp(ipm.x, ipm.y) )

    """
    for ipm in dc.pmt_list:
        ipm.dump()
    """
