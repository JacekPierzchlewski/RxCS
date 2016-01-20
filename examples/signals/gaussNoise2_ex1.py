"""
This script is an example of how to use the random gaussian noise generator (type 2)
module. |br|

In this example only one signal is generated. 
Both  the minimum  and the maximum frequency component in the signal is regulated.


After the generation, spectrum fo the signal is analyzed with an Welch analysis
and ploted.

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0    | 20-JAN-2016  : * Version 1.0 released. |br|

*License*:
    BSD 2-Clause
"""

import rxcs
import scipy.signal as scsig
import matplotlib.pyplot as plt


def _gaussNoise2_ex1():

    # Things on the table:
    gaussNoise = rxcs.sig.gaussNoise2()  # Gaussian noise generator

    # Configure the generator...
    gaussNoise.fR = 100e6      # Representation sampling frequency [100 MHz]
    gaussNoise.tS = 1        # Time [1 sec]
    gaussNoise.fMin = 100e3  # Minimum frequency component [100 kHz]
    gaussNoise.fMax = 200e3  # Maximum frequency component [200 kHz]

    gaussNoise.run()              # ... and run it!
    vSig = gaussNoise.mSig[0, :]  # take the generated signal

    # -----------------------------------------------------------------
    # Analyze the signal and plot it
    (vFxx, vPxx) = scsig.welch(vSig, fs=gaussNoise.fR, nperseg=100*1024, noverlap=100*512)
    hFig1 = plt.figure(1)
    hSubPlot1 = hFig1.add_subplot(111)
    hSubPlot1.grid(True)
    hSubPlot1.set_title('Spectrum of the signal (psd)')
    hSubPlot1.set_xlabel('Frequency [kHz]')
    hSubPlot1.plot(vFxx/1e3, vPxx, '-')
    hSubPlot1.set_xlim(0, 1e3)
    plt.show(block=True)


# =====================================================================
# Trigger when start as a script
# =====================================================================
if __name__ == '__main__':
    _gaussNoise2_ex1()
