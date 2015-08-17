"""
This script is an example of how to use the saturation block. |br|

In this example 1 random multitone signal is generated. The signal contains 3 random tones,
the highest possible frequency in the signal is 10 kHz. |br|

After the signal generation, the signal is pushed through a saturation block,
which limits the signal's minimum and maximum values. |br|

The clean observed signal, which is cleaned from the saturated samples, 
is additionally plotted. |br|

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0  | 17-AUG-2015 : * Version 1.0 released. |br|

*License*:
    BSD 2-Clause
"""
from __future__ import division
import rxcs
import matplotlib.pyplot as plt

def _saturation_ex2():

    # Put the stuff on board
    gen = rxcs.sig.randMult()    # Signal generator
    satur = rxcs.acq.satur()     # Saturation block

    # General settings    
    TIME = 1e-3  # Time of the signal is 1 ms    
    FSMP = 1e6   # The signal representation sampling frequency is 1 MHz
    
    # Settings for the generator
    gen.tS = TIME      # Time of the signal is 1 ms
    gen.fR = FSMP      # The signal representation sampling frequency is 1 MHz
    gen.fMax = 10e3    # The highest possible frequency in the signal is 10 kHz
    gen.fRes = 1e3     # The signal spectrum resolution is 1 kHz
    gen.nTones = 3     # The number of random tones
    gen.iMinAmp = 0.1   # The minimum amplitude of a tone
    gen.iMaxAmp = 1.0   # The maximum amplitude of a tone
    gen.nSigPack = 1    # The number of signals to be generated

    # Generate settings for the saturation block
    satur.iMinAmp = -0.8   # Minimum amplitude
    satur.iMaxAmp = 0.8    # Maximum amplitude

    # -----------------------------------------------------------------
    # Run the multitone signal generator and the saturation block
    gen.run()               # Run the generator
    satur.mSig = gen.mSig   # Connect the generator output with the saturation input
    satur.vT = gen.vT       # Connect the signal time vector with the saturation block
    satur.run()             # Run the saturation block

    # -----------------------------------------------------------------
    # Plot the results of sampling
    vSig = gen.mSig[0, :]   # Get the original signal
    vT = gen.vTSig          # ... and its time vector

    vObSig = satur.mObSig[0, :]           # Get the observed signal
    
    vObSigClean = satur.lObSigClean[0]    # Get the cleaned observed signal
    vTClean = satur.lvTClean[0]           # Get the time vector for the cleaned signal
    
    vSaturMark = satur.mSaturMark[0, :]   # Get the first set ot saturation markers

    hFig1 = plt.figure(1)
    # Plot the original signal and the saturated signal
    hSubPlot1 = hFig1.add_subplot(311)
    hSubPlot1.grid(True)
    hSubPlot1.set_title('Signals in the time domain')
    hSubPlot1.plot(vT, vSig, 'b-', label='original signal')
    hSubPlot1.plot(vT, vObSig, 'r-', label='signal after the saturation block')
    hSubPlot1.legend()

    hSubPlot2 = hFig1.add_subplot(312)
    hSubPlot2.set_title('Saturation markers in the time domain')
    hSubPlot2.plot(vT, vSaturMark, 'g-')
    hSubPlot2.set_ylim(-1.2, 1.2)

    hSubPlot3 = hFig1.add_subplot(313)
    hSubPlot3.set_title('Cleaned signal in the time domain')
    hSubPlot3.plot(vTClean, vObSigClean, 'b.')
    hSubPlot3.set_xlabel('Time')
    hSubPlot3.set_ylim(-2.0, 2.0)

    # -----------------------------------------------------------------
    plt.show(block=True)


# =====================================================================
# Trigger when start as a script
# =====================================================================
if __name__ == '__main__':
    _saturation_ex2()
