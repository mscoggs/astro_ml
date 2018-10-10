import sys
import os
from glob import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from astropy.io import fits
import warnings
warnings.filterwarnings('ignore')

def main():

    crossMatch = "allStar_l31c2_GaiaDR2_crossmatch_withpms.fits"
    JKH = "allStar-l31c.2.fits" #J,kh valshdul2
    HDU1 = fits.open(crossMatch)
    HDU2 = fits.open(JKH)

    ID1 = HDU1[1].data['APOGEE_ID']
    ID2 = HDU2[1].data['APOGEE_ID']
    ID_count = len(ID1)

    #get rid of the IDs not in both
    ID1 = np.sort(ID1)
    ID2 = np.sort(ID2)

    ID2_index = []
    ID1_index = []
    index = 0
    for x in range(len(ID2)):
        if ID2[x] == ID1[index]:
            ID1_index.append(index)
            ID2_index.append(x)
            index += 1
        elif ID2[x] > ID1[index]:
            index += 1
        if (x+1>=ID_count):
            break

    parallax = HDU1[1].data['parallax'][ID1_index]
    distance = 1/parallax
    distance_mod = 5*np.log10(distance)-5
    K_app = HDU2[1].data['K'][ID2_index]
    J_app = HDU2[1].data['J'][ID2_index]
    H_app = HDU2[1].data['H'][ID2_index]
    K_abs = distance_mod-K_app
    J_abs = distance_mod-J_app
    H_abs = distance_mod-H_app
    plt.title("all IDs")
    plt.xlabel("K_abs")
    plt.ylabel("J-K")
    plt.xlim(-27,5)
    plt.ylim(-1,8)
    plt.scatter(K_abs, J_app-K_app, s=0.01)
    plt.show()


    par_over_error = parallax = HDU1[1].data['parallax_over_error'][ID1_index]
    sort = np.where(par_over_error>10)
    K_app10 = K_app[sort]
    J_app10 = J_app[sort]
    K_abs10 = K_abs[sort]
    J_abs10 = J_abs[sort]
    plt.title("pi/sigma>10")
    plt.xlabel("K_abs")
    plt.ylabel("J-K")
    plt.xlim(-27,5)
    plt.ylim(-1,8)
    plt.scatter(K_abs10, J_app10-K_app10, s=0.01)
    plt.show()

    par_over_error = parallax = HDU1[1].data['parallax_over_error'][ID1_index]
    sort = np.where(par_over_error>100)
    K_app100 = K_app[sort]
    J_app100 = J_app[sort]
    K_abs100 = K_abs[sort]
    J_abs100 = J_abs[sort]
    plt.title("pi/sigma>100")
    plt.xlabel("K_abs")
    plt.ylabel("J-K")
    plt.xlim(-27,5)
    plt.ylim(-1,8)
    plt.scatter(K_abs100, J_app100-K_app100, s=0.01)
    plt.show()

main()
