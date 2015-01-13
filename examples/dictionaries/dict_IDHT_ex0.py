"""
This script is an example of how to use the Inverse Discrete Hartley Transform  
(IDHT) Dictionary module. |br|

In this example signal with 1 cosine tone is generated. |br|


After the generation, the signal is plotted in the time domain.

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0  | 13-JAN-2014 : * Version 1.0 released. |br|

*License*:
    BSD 2-Clause
"""
from __future__ import division
import rxcs
import numpy as np
import matplotlib.pyplot as plt


def _dict_IDHT_ex0():

    # -----------------------------------------------------------------
    # Generate settings for the IDHT dictionary

    # Start the configuration dictionary
    dCSConf = {}

    # Time of the dictionary is 10 ms
    dCSConf['tS'] = 10e-3

    # The signal representation sampling frequency is 10 kHz
    dCSConf['fR'] = 10e3

    # The frequency separation between tones is 100 Hz
    dCSConf['fDelta'] = 100

    # The number of tones in the dictionary 
    dCSConf['nTones'] = 10

    # -----------------------------------------------------------------
    # Generate the IDFT dictionary
    (mIDHT, dDict) = rxcs.cs.dict.IDHT.main(dCSConf)

    # -----------------------------------------------------------------
    # Generate the signal using the dictionary

    # Vector with Fourier coefficients
    vFcoef = np.zeros((1,2*dCSConf['nTones'])).astype(complex)
    vFcoef[0, 0] = 1     # Cosine 100Hz

    # Generate a signal and change its shape to a single vector
    vSig = np.real(np.dot(vFcoef, mIDHT))
    vSig.shape = (vSig.size,)

    # -----------------------------------------------------------------
    # Plot signal in the time domain
    vT = dDict['vT']          # Get the signal time vector from the dictionary
    hFig1 = plt.figure(1)
    hSubPlot1 = hFig1.add_subplot(111)
    hSubPlot1.grid(True)
    hSubPlot1.set_title('Signal')
    hSubPlot1.set_xlabel('Time [s]')
    hSubPlot1.plot(vT, vSig)
    hSubPlot1.set_xlim(min(vT), max(vT) + 0.01*max(vT) )
    hSubPlot1.set_ylim(-1.1, 1.1)
    plt.show(block=True)

# =====================================================================
# Trigger when start as a script
# =====================================================================
if __name__ == '__main__':
    _dict_IDHT_ex0()
