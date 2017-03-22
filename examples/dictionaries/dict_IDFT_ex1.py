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
    1.0-r1   | 23-FEB-2015 : * Header is added.  |br|
    2.0      | 20-AUG-2015 : * Version 2.0 released
                               (adjusted to v2.0 of the dictionary generator) |br|
    2.1      | 23-MAR-2017 : * Symmetrical frequency distribution is set


*License*:
    BSD 2-Clause
"""
from __future__ import division
import rxcs
import numpy as np
import matplotlib.pyplot as plt

def _dict_IDFT_ex1():

    # Things on the table:
    IDFT = rxcs.cs.dict.IDFT() # IDFT dictionary generator

    # Configure the IDF generator
    IDFT.tS = 1e-3     # Time of the dictionary is 1 ms
    IDFT.fR = 1e6      # Representation sampling frequency is 1 MHz
    IDFT.fDelta = 1e3     # The frequency separation between tones
    IDFT.nTones = 100     # The number of tones in the dictionary
    IDFT.tStart = 10e-6   # Time start is 10 us

    IDFT.bFreqSym = 1  # Symmetrical frequency distribution
    IDFT.run()   # Generate the dictionary

    # -----------------------------------------------------------------
    # Generate the signal using the dictionary

    # Vector with Fourier coefficients
    vFcoef = np.zeros((1,200)).astype(complex)
    vFcoef[0, 1] = -1j
    vFcoef[0, 198] = 1j

    # Get the dictionary matrix
    mIDFT = IDFT.mDict

    # Generate a signal and change its shape to a single vector
    vSig = np.real(np.dot(vFcoef,mIDFT))
    vSig.shape = (vSig.size,)

    # -----------------------------------------------------------------
    # Plot signal in the time domain
    vT = IDFT.vT         # Get the time vector
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
