"""
This script is an example of how to use the nonuniform sampler with the ARS
(additive random sampling) scheme. |br|

In this example 1 random multitone signal is generated and sampled |br|

The signal contains 3 random tones, the highest possible frequency in the
signal is 10 kHz.

The signal is nonuniformly sampled with the average sampling frequency
equal to 8 kHz. The sampling gird is 1 us. A sampling patterns is generated
using ARS scheme.

After the signal generation and sampling, the original signal and the observed
signal is plotted in the time domain. Additionally, the sampling pattern is
plotted.

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0  | 28-JAN-2015 :  * Version 1.0 released. |br|
    1.1  |  9-MAR-2015 :  * Adjusted to the new format of observation matrices from ARS sampler |br|
    2.0  | 14-AUG-2015 :  * Adjusted to ARS sampler v2.0  |br|

*License*:
    BSD 2-Clause
"""

from __future__ import division
import rxcs
import numpy as np
import matplotlib.pyplot as plt


def _nonuniJS_ex0():

    # Put the stuff on board
    gen = rxcs.sig.randMult()      # Signal generator
    samp = rxcs.acq.nonuniJS()     # Sampler   

    # General settings    
    TIME = 1e-3  # Time of the signal is 1 ms    
    FSMP = 1e6   # The signal representation sampling frequency is 1 MHz
    
    # Settings for the generator
    gen.tS = TIME      # Time of the signal is 1 ms
    gen.fR = FSMP      # The signal representation sampling frequency is 1 MHz
    gen.fMax = 10e3    # The highest possible frequency in the signal is 10 kHz
    gen.fRes = 1e3     # The signal spectrum resolution is 1 kHz
    gen.nTones = 1     # The number of random tones

    # Generate settings for the sampler
    samp.tS = TIME     # Time of the signal
    samp.fR = FSMP     # The signal representation sampling freuqnecy
    samp.Tg = 1e-6     # The sampling grid period
    samp.fSamp = 8e3   # The average sampling frequency

    # -----------------------------------------------------------------
    # Run the multitone signal generator and the sampler
    gen.run()               # Run the generator    
    samp.mSig = gen.mSig    # Connect the signal from the generator to the sampler 
    samp.run()              # Run the sampler

    # -----------------------------------------------------------------
    # Plot the results of sampling
    vSig = gen.mSig[0, :]   # The signal from the generator
    vT = gen.vTSig          # The time vector of the original signal
    vObSig = samp.mObSig[0, :]    # The observed signal
    vPattsT = samp.mPattsT[0, :]  # The sampling moments

    # Plot the signal and the observed sampling points    
    hFig1 = plt.figure(1)

    hSubPlot1 = hFig1.add_subplot(211)
    hSubPlot1.grid(True)
    hSubPlot1.set_title('Signal and the observed sampling points')
    hSubPlot1.plot(vT, vSig, '-')
    hSubPlot1.plot(vPattsT, vObSig, 'r*', markersize=10)

    # Plot the sampling pattern
    hSubPlot2 = hFig1.add_subplot(212)
    hSubPlot2.grid(True)
    hSubPlot2.set_title('The sampling pattern')
    hSubPlot2.set_xlabel('Time [s]')
    (markerline, stemlines, baseline) = hSubPlot2.stem(vPattsT,
                                                       np.ones(vPattsT.shape),
                                                       linefmt='b-',
                                                       markerfmt='bo',
                                                       basefmt='-')
    hSubPlot2.set_ylim(0, 1.1)
    hSubPlot2.set_xlim(0, 0.001)
    plt.setp(stemlines, color='b', linewidth=2.0)
    plt.setp(markerline, color='b', markersize=10.0)

    # -----------------------------------------------------------------
    # APPENDIX:
    # This part is to show how to use the observation matrix, if it is needed
    # (for example in compressed sensing systems)

    lPhi = samp.lPhi   # Get a 3D matrix with observation matrices
    mPhi = lPhi[0]     # Get the first observation matrix (1st element of lPhi list)

    vObSigPhi = np.dot(mPhi, vSig)   # Sample the signal using the observation matrix

    # Plot the signal and the observed sampling points
    hFig2 = plt.figure(2)
    hSubPlot1 = hFig2.add_subplot(111)
    hSubPlot1.grid(True)
    hSubPlot1.set_title('Signal and the observed sampling points')
    hSubPlot1.plot(vT, vSig, '-')
    hSubPlot1.plot(vPattsT, vObSigPhi, 'ro', markersize=10)

    # -----------------------------------------------------------------
    plt.show(block=True)

# =====================================================================
# Trigger when start as a script
# =====================================================================
if __name__ == '__main__':
    _nonuniJS_ex0()
