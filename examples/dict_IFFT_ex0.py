from __future__ import division
import rxcs
import numpy as np
import matplotlib.pyplot as plt

def _dict_IFFT_ex0():

    # -----------------------------------------------------------------
    # Generate settings for the IFFT dictionary

    # Start the dictionary with dictionary configuration
    dCSConf = {}

    # Time of the dictionary is 1 ms
    dCSConf['tS'] = 1e-3

    # The signal representation sampling frequency is 1 MHz
    dCSConf['fR'] = 1e4

    # The frequency separation between tones
    dCSConf['fDelta'] = 1e3

    # The number of tones in the dictionary
    dCSConf['nTones'] = 10

    # -----------------------------------------------------------------
    # Generate the IFFT dictionary
    rxcs.cs.dict.IFFTdict.main(dCSConf)
    #mIFFT = rxcs.cs.dict.IFFTdict.main(dCSConf)

    # -----------------------------------------------------------------
    # Generate the signal using the dictionary

    # -----------------------------------------------------------------
    # Plot the signal


# =====================================================================
# Trigger when start as a script
# =====================================================================
if __name__ == '__main__':
    _dict_IFFT_ex0()
