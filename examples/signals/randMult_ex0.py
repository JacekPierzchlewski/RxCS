"""
This script is an example of how to use the Random Multitone Signal
Generator module. |br|

In this example 1 random multitone signal is generated. |br|

Time of the signal is 1 ms, the signal representation sampling frequency is
1 MHz. The highest possible frequency of a tone in the signal is 10 kHz,
the signal spectrum resolution is 1 kHz. |br|

The signal contains 1 random tone.

The noise is added to the signal, the SNR of the signal is 5 [dB]. |br|

After the generation, spectrum fo the signal is analyzed with an FFT
and ploted. The signal is also plotted in the time domain.

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0    | 21-MAY-2014 : * Version 1.0 released. |br|
    1.1    | 15-JUL-2015 : * Adjusted to new name of random multitone gen. |br|
    2.0    | 21-JUL-2015 : * Version 2.0 released (adjusted to v2.0 of the generator) |br|
    2.0r1  | 04-AUG-2015 : * File name changed |br|

*License*:
    BSD 2-Clause
"""
from __future__ import division
import rxcs
import numpy as np
import matplotlib.pyplot as plt


def _randMult_ex0():

    # Put the generator on board
    gen = rxcs.sig.randMult()
    
    # Settings for the generator
    gen.tS = 1e-3     # Time of the signal is 1 ms
    gen.fR = 1e6      # The signal representation sampling frequency is 1 MHz
    gen.fMax = 10e3   # The highest possible frequency in the signal is 10 kHz
    gen.fRes = 1e3    # The signal spectrum resolution is 1 kHz

    gen.nTones = 1    # The number of random tones
    
    gen.iSNR = 5      # The noise added to the signal

    # Run the generator and get the output    
    gen.run()    
    vSig = gen.mSig[0, :]  # Get the generated signal
    vTSig = gen.vTSig      # Get the time vector of the signal
    fFFTR =  gen.fFFTR     # Signal FFT frequency resolution

    # -----------------------------------------------------------------
    # Analyze the signal and plot it

    vFFT = np.fft.fft(vSig)  # Analyze the spectrum of the signal
    iS = vFFT.size           # Get the size of the spectrum

    # Compute the amplitudes of tones
    vFFTa = 2*np.abs(vFFT[np.arange(iS/2).astype(int)])/iS   # Get 

    # Create a vector with frequencies of the signal spectrum
    vF = fFFTR * np.arange(iS/2)

    # -----------------------------------------------------------------
    # Plot half of the spectrum
    hFig1 = plt.figure(1)
    hSubPlot1 = hFig1.add_subplot(111)
    hSubPlot1.grid(True)
    hSubPlot1.set_title('Spectrum of a random multitone signal')
    hSubPlot1.set_xlabel('Frequency [Hz]')
    (markerline, stemlines, baseline) = hSubPlot1.stem(vF, vFFTa,
                                                       linefmt='b-',
                                                       markerfmt='bo',
                                                       basefmt='r-')
    hSubPlot1.set_xlim(-1*1e3, 51*1e3)
    hSubPlot1.set_ylim(-0.1, 3.1)
    plt.setp(stemlines, color='b', linewidth=2.0)
    plt.setp(markerline, color='b', markersize=10.0)

    # -----------------------------------------------------------------
    # Plot signal in the time domain
    hFig2 = plt.figure(2)
    hSubPlot1 = hFig2.add_subplot(111)
    hSubPlot1.grid(True)
    hSubPlot1.set_title('Random multitone signal in the time domain')
    hSubPlot1.set_xlabel('Frequency [Hz]')
    hSubPlot1.plot(vTSig, vSig, 'b-')

    # -----------------------------------------------------------------
    plt.show(block=True)

# =====================================================================
# Trigger when start as a script
# =====================================================================
if __name__ == '__main__':
    _randMult_ex0()
