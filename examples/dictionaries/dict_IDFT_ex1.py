"""
This script is an example on how to use the Inverse Discrete Fourier Transform
(IDFT) Dictionary module. |br|

In this example a IDFT dictionary is generated. There is a time shift in time
represented by the dictionary.
Then, a signal with 1 tone is generated using the dictionary. |br|

After the generation, the signal is plotted in the time domain.


*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0      | 30-MAY-2014 : * Version 1.0 released. |br|
    1.0-r1   | 23-FEB-2015 : * Header is added

*License*:
    BSD 2-Clause
"""


from __future__ import division
import rxcs
import numpy as np
import matplotlib.pyplot as plt

def _dict_IDFT_ex1():

    # -----------------------------------------------------------------
    # Generate settings for the IDFT dictionary

    # Start the configuration dictionary
    dCSConf = {}

    # Time of the dictionary is 1 ms
    dCSConf['tS'] = 1e-3

    # Time start is 10 us
    dCSConf['tStart'] = 10e-6

    # The signal representation sampling frequency is 1 MHz
    dCSConf['fR'] = 1e6

    # The frequency separation between tones
    dCSConf['fDelta'] = 1e3

    # The number of tones in the dictionary
    dCSConf['nTones'] = 100

    # -----------------------------------------------------------------
    # Generate the IDFT dictionary
    (mIDFT, dDict) = rxcs.cs.dict.IDFToNoDC.main(dCSConf)

    # -----------------------------------------------------------------
    # Generate the signal using the dictionary

    # Vector with Fourier coefficients
    vFcoef = np.zeros((1,200)).astype(complex)
    vFcoef[0, 1] = -1j
    vFcoef[0, 18] = 1j

    # Generate a signal and change its shape to a signle vector
    vSig = np.real(np.dot(vFcoef,mIDFT))
    vSig.shape = (vSig.size,)

    # Get the signal time vector
    vT = dDict['vT']

    # -----------------------------------------------------------------
    # Plot signal in the time domain
    hFig1 = plt.figure(1)
    hSubPlot1 = hFig1.add_subplot(111)
    hSubPlot1.grid(True)
    hSubPlot1.set_title('Signal')
    hSubPlot1.set_xlabel('Time [s]')
    hSubPlot1.plot(vT, vSig)
    hSubPlot1.set_xlim(min(vT), max(vT))
    hSubPlot1.set_ylim(-1.1, 1.1)

    plt.show(block=True)

# =====================================================================
# Trigger when start as a script
# =====================================================================
if __name__ == '__main__':
    _dict_IDFT_ex1()
