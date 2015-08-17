"""
This script is an example of how to use the saturation block. |br|

In this example 1 random multitone signal is generated. The signal contains 3 random tones,
the highest possible frequency in the signal is 10 kHz. |br|

The signal is then sampled by a uniform sampler. The average sampling frequency equals 40kHz,
the signal's Nyquist rate is 20kHz, hence the oversampling ratio (OSR) is 2.0.
|br|

After the signal sampling, the signal is pushed through a saturation block,
which limits the minimum and maximum values of the observed signal.
Additionally, the saturation block takes care of removing saturated sampling points
from the saturated sampling patterns.
|br|

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0  | 04-MAR-2015 : * Version 1.0 released. |br|
    2.0  | 17-AUG-2015 : * Adjusted to saturation block v2.0 (objectified)  |br|

*License*:
    BSD 2-Clause
"""
from __future__ import division
import rxcs
import matplotlib.pyplot as plt
import numpy as np

def _saturation_ex1():

    # Put the stuff on board
    gen = rxcs.sig.randMult()      # Signal generator
    samp = rxcs.acq.uniform()      # Uniform sampler
    satur = rxcs.acq.satur()       # Saturation block

    # General settings    
    TIME = 1e-3  # Time of the signal is 1 ms    
    FSMP = 1e6   # The signal representation sampling frequency is 1 MHz
    
    # Settings for the generator
    gen.tS = TIME      # Time of the signal is 1 ms
    gen.fR = FSMP      # The signal representation sampling frequency is 1 MHz
    gen.fMax = 10e3    # The highest possible frequency in the signal is 10 kHz
    gen.fRes = 1e3     # The signal spectrum resolution is 1 kHz
    gen.nTones = 5     # The number of random tones
    gen.iMinAmp = 0.1   # The minimum amplitude of a tone
    gen.iMaxAmp = 1.0   # The maximum amplitude of a tone
    gen.nSigPack = 1    # The number of signals to be generated

    # Generate settings for the uniform sampler
    samp.tS = TIME     # Time of the signal
    samp.fR = FSMP     # The signal representation sampling freuqnecy
    samp.Tg = 1e-6      # The sampling grid period
    samp.fSamp = 40e3   # The average sampling frequency

    # Generate settings for the saturation block
    satur.iMinAmp = -0.8   # Minimum amplitude
    satur.iMaxAmp = 0.8    # Maximum amplitude

    # -----------------------------------------------------------------
    # Run the system
    gen.run()                # Run the generator
    samp.mSig = gen.mSig     # Connect the signal from the generator to the sampler
    samp.run()               # Run the sampler

    satur.mSig = samp.mObSig      # Connect the sampler output with the saturation input
    satur.mPattsT = samp.mPattsT  # Connect the sampling pattern (ass time moments) to the saturation block 
    satur.run()                   # Run the saturation block

    # -----------------------------------------------------------------
    # Plot the results of sampling

    # Get the original signal and its time vector
    vSig = gen.mSig[0, :]
    vT = gen.vTSig

    # Get the observed signal (uniformly sampled) from the uniform sampler
    vObSig = samp.mObSig[0, :]    # The observed signal
    vPattsT = samp.mPattsT[0, :]  # The sampling moments
    
    # Get the observed limited signal and saturation markers
    vObSigSatur = satur.mObSig[0, :]      # Get the observed signal
    vSaturMark = satur.mSaturMark[0, :]   # Get the first set ot saturation markers (in fact, there where only 1)

    vObSigClean = satur.lObSigClean[0]   #  Get the observed signal with saturated sampled removed
    vPattTClean = satur.lPattsTClean[0]  #  Get the sampling pattern with saturated samples removed

    # ----------------------------------------
    hFig1 = plt.figure(1)

    # --------
    hSubPlot1 = hFig1.add_subplot(211)
    hSubPlot1.grid(True)
    hSubPlot1.plot(vT, vSig, 'k-', label='original signal')
    hSubPlot1.plot(vPattsT, vObSig, 'g*', label='observed samples')
    hSubPlot1.legend(prop={'size':8})

    # --------
    hSubPlot2 = hFig1.add_subplot(212)
    hSubPlot2.grid(True)
    hSubPlot2.set_xlabel('Time [s]')
    (markerline, stemlines, _) = hSubPlot2.stem(vPattsT, np.ones(vPattsT.shape), linefmt='b-', markerfmt='bo', basefmt='-',
                                                label='The uniform sampling pattern')
    hSubPlot2.set_ylim(0, 1.6)
    hSubPlot2.set_xlim(0, 0.001)
    hSubPlot2.legend(prop={'size':8})
    plt.setp(stemlines, color='b', linewidth=2.0)
    plt.setp(markerline, color='b', markersize=10.0)

    # ----------------------------------------
    hFig2 = plt.figure(2)
    hSubPlot1 = hFig2.add_subplot(311)
    hSubPlot1.grid(True)
    hSubPlot1.plot(vT, vSig, 'k-', label='original signal')
    (markerline, stemlines, _) = hSubPlot1.stem(vPattsT, vObSig, linefmt='g-', markerfmt='bo', basefmt='-',
                                                label='observed samples')
    plt.setp(stemlines, color='b', linewidth=2.0)
    plt.setp(markerline, color='g', markersize=10.0)

    (markerline, stemlines, _) = hSubPlot1.stem(vPattsT, vObSigSatur, linefmt='r-', markerfmt='bo', basefmt='-',
                                                label='saturated observed samples')
    plt.setp(stemlines, color='r', linewidth=2.0)
    plt.setp(markerline, color='r', markersize=10.0)
    hSubPlot1.legend(prop={'size':8})

    # --------
    hSubPlot2 = hFig2.add_subplot(312)
    hSubPlot2.plot(vPattsT, np.abs(vSaturMark), 'g-', label='Saturation markers in the time domain (absolute values)')
    hSubPlot2.set_ylim(-0.2, 1.2)
    hSubPlot2.legend(prop={'size':8})

    # --------
    hSubPlot3 = hFig2.add_subplot(313)
    hSubPlot3.plot(vPattsT, vSaturMark, 'g-', label='Saturation markers in the time domain')
    hSubPlot3.set_ylim(-1.2, 1.2)
    hSubPlot3.legend(prop={'size':8})

    # ----------------------------------------
    hFig3 = plt.figure(3)

    hSubPlot1 = hFig3.add_subplot(411)
    hSubPlot1.grid(True)
    hSubPlot1.plot(vT, vSig, 'k-', label='original signal')
    hSubPlot1.plot(vPattTClean, vObSigClean, 'g*', label='observed samples without the saturated samples')
    hSubPlot1.legend(prop={'size':8})

    # --------
    hSubPlot2 = hFig3.add_subplot(412)
    hSubPlot2.grid(True)
    (markerline, stemlines, _) = hSubPlot2.stem(vPattTClean, np.ones(vPattTClean.shape), linefmt='b-', markerfmt='bo', basefmt='-',
                                                label='The sampling pattern without saturated samples')
    hSubPlot2.set_ylim(0, 1.6)
    hSubPlot2.set_xlim(0, 0.001)
    plt.setp(stemlines, color='b', linewidth=2.0)
    plt.setp(markerline, color='b', markersize=10.0)
    hSubPlot2.legend(prop={'size':8})

    # --------
    hSubPlot3 = hFig3.add_subplot(413)
    hSubPlot3.plot(vPattsT, abs(vSaturMark), 'g-', label='Saturation markers in the time domain (absolute values)')
    hSubPlot3.set_ylim(-1.2, 1.2)
    hSubPlot3.legend(loc=4,prop={'size':8})

    # --------
    hSubPlot4 = hFig3.add_subplot(414)
    (markerline, stemlines, _) = hSubPlot4.stem(vPattsT, np.ones(vPattsT.shape), linefmt='b-', markerfmt='bo', basefmt='-',
                                                label='The uniform sampling pattern')
    hSubPlot4.set_ylim(0, 1.6)
    hSubPlot4.set_xlim(0, 0.001)
    hSubPlot4.legend(prop={'size':8})
    hSubPlot4.set_xlabel('Time [s]')

    plt.setp(stemlines, color='b', linewidth=2.0)
    plt.setp(markerline, color='b', markersize=10.0)

    # -----------------------------------------------------------------
    plt.show(block=True)


# =====================================================================
# Trigger when start as a script
# =====================================================================
if __name__ == '__main__':
    _saturation_ex1()
