"""
This script is an example of how to use the random gaussian noise generator
module. |br|

In this example only one signal is generated. 
Both  the minimum  and the maximum frequency component in the signal is regulated.


After the generation, spectrum fo the signal is analyzed with an Welch analysis
and ploted.

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0    | 03-SEP-2015  : * Version 1.0 released. |br|

*License*:
    BSD 2-Clause
"""

import rxcs
import scipy.signal as scsig
import matplotlib.pyplot as plt


def _gaussNoise_ex1():

    # Things on the table:
    gaussNoise = rxcs.sig.gaussNoise() # Gaussian noise generator

    # Configure the generator...
    gaussNoise.fR = 1e6      # Representation sampling frequency [1 MHz]
    gaussNoise.tS = 1        # Time [1 sec]
    gaussNoise.fMin = 100e3  # Minimum frequency component [100 kHz]
    gaussNoise.fMax = 200e3  # Maximum frequency component [200 kHz]

    gaussNoise.run()              # ... and run it!
    vSig = gaussNoise.mSig[0, :]  # take the generated signal

    # -----------------------------------------------------------------
    # Analyze the signal and plot it
    (vFxx, vPxx) = scsig.welch(vSig, fs=gaussNoise.fR, nperseg=1024, noverlap=512)
    hFig1 = plt.figure(1)
    hSubPlot1 = hFig1.add_subplot(111)
    hSubPlot1.grid(True)
    hSubPlot1.set_title('Spectrum of the signal (psd)')
    hSubPlot1.set_xlabel('Frequency [kHz]')
    hSubPlot1.plot(vFxx/1e3, vPxx, '-')
    plt.show(block=True)


# =====================================================================
# Trigger when start as a script
# =====================================================================
if __name__ == '__main__':
    _gaussNoise_ex1()
