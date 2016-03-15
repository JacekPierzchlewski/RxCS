"""
This script is an example of how to use the random gaussian noise generator (type 3)
module. |br|

This is the simplest example, with only one signal generated. 

After the generation, spectrum fo the signal is analyzed with an Welch analysis
and ploted.

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    0.01    | 15-MAR-2016  : * Version 0.01 released |br|

*License*:
    BSD 2-Clause
"""

import rxcs
import scipy.signal as scsig
import matplotlib.pyplot as plt
import numpy as np

def _gaussNoise_ex0():

    # Things on the table:
    gaussNoise = rxcs.sig.gaussNoise3()  # Gaussian noise generator

    # Configure the generator...
    gaussNoise.fR = 1e6          # Representation sampling frequency [100 MHz]
    gaussNoise.tS = 1            # Time [1 sec]
    gaussNoise.fMin = 20e3       # Minimum possible frequency of the noise signal
    gaussNoise.fWidth = 20e3     # Width of the noise signal
    gaussNoise.fMax = 180e3      # Maximum possible frequency component in the signal
    gaussNoise.fGrad = 10e3
    gaussNoise.nSigs = int(1e1)
    gaussNoise.nFiltOrd = 100

    gaussNoise.run()              # ... and run it!
    vSig0 = gaussNoise.mSig[0, :]  # take the generated signal #0
    vSig1 = gaussNoise.mSig[1, :]  # take the generated signal #1
    vSig2 = gaussNoise.mSig[2, :]  # take the generated signal #3
    vSig3 = gaussNoise.mSig[3, :]  # take the generated signal #4
    

    # -----------------------------------------------------------------
    # Analyze the signal and plot it
    fRR=gaussNoise.fR
    #fRR = 2*10e3    

    iScale = 20
    (vFxx0, vPxx0) = scsig.welch(vSig0, fs=fRR, nperseg=iScale * 1024, noverlap=iScale * 512)
    (vFxx1, vPxx1) = scsig.welch(vSig1, fs=fRR, nperseg=iScale * 1024, noverlap=iScale * 512)
    (vFxx2, vPxx2) = scsig.welch(vSig2, fs=fRR, nperseg=iScale * 1024, noverlap=iScale * 512)
    (vFxx3, vPxx3) = scsig.welch(vSig3, fs=fRR, nperseg=iScale * 1024, noverlap=iScale * 512)

    # Figure 1
    FMAX = 200
    hFig1 = plt.figure(1)

    hSubPlot = hFig1.add_subplot(411)
    hSubPlot.grid(True)
    hSubPlot.set_title('Spectrum of the signal (psd)')
    hSubPlot.set_xlabel('Frequency [kHz]')
    hSubPlot.plot(vFxx0/1e3, vPxx0, '-')
    hSubPlot.set_xlim(0, FMAX)

    hSubPlot = hFig1.add_subplot(412)
    hSubPlot.grid(True)
    hSubPlot.set_title('Spectrum of the signal (psd)')
    hSubPlot.set_xlabel('Frequency [kHz]')
    hSubPlot.plot(vFxx1/1e3, vPxx1, '-')
    hSubPlot.set_xlim(0, FMAX)

    hSubPlot = hFig1.add_subplot(413)
    hSubPlot.grid(True)
    hSubPlot.set_title('Spectrum of the signal (psd)')
    hSubPlot.set_xlabel('Frequency [kHz]')
    hSubPlot.plot(vFxx2/1e3, vPxx2, '-')
    hSubPlot.set_xlim(0, FMAX)

    hSubPlot = hFig1.add_subplot(414)
    hSubPlot.grid(True)
    hSubPlot.set_title('Spectrum of the signal (psd)')
    hSubPlot.set_xlabel('Frequency [kHz]')
    hSubPlot.plot(vFxx3/1e3, vPxx3, '-')
    hSubPlot.set_xlim(0, FMAX)

    plt.show(block=True)


# =====================================================================
# Trigger when start as a script
# =====================================================================
if __name__ == '__main__':
    _gaussNoise_ex0()
