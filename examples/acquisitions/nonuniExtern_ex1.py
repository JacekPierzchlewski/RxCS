"""
This script is an example of how to use the nonuniform sampler with the 
external sampling scheme. |br|

In this example 1 random multitone signal is generated and sampled |br|

The signal contains 3 random tones, the highest possible frequency in the
signal is 10 kHz.

The signal is nonuniformly sampled with an external sampling pattern.
There are 2 sampling pattens defined, the sampler chooses randomly between 
these sampling patterns.

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0    | 19-AUG-2015 : * Version 1.0 released. |br|


*License*:
    BSD 2-Clause
"""

from __future__ import division
import rxcs
import numpy as np
import matplotlib.pyplot as plt


def nonuniExtern_ex1():

    # Put the stuff on board
    gen = rxcs.sig.randMult()      # Signal generator
    samp = rxcs.acq.nonuniExtern()  # Sampler 
    
    # General settings
    TIME = 1e-3  # Time of the signal is 1 ms    
    FSMP = 1e6   # The signal representation sampling frequency is 1 MHz
    
    # Settings for the generator
    gen.tS = TIME      # Time of the signal is 1 ms
    gen.fR = FSMP      # The signal representation sampling frequency is 1 MHz
    gen.fMax = 10e3    # The highest possible frequency in the signal is 10 kHz
    gen.fRes = 1e3     # The signal spectrum resolution is 1 kHz
    gen.nTones = 3     # The number of random tones
    gen.nSigs = 4      # The number of signals to be generated 

    # Generate settings for the sampler
    samp.tS = TIME     # Time of the signal
    samp.fR = FSMP     # The signal representation sampling freuqnecy
    samp.Tg = 1e-5     # The sampling grid period
   
    lPatt1 = [20, 25, 57, 65, 88]   # Pattern #1
    lPatt2 = [1,  10, 45, 60, 99]   # Pattern #2
    samp.mPatterns = np.array([lPatt1, lPatt2])

    # -----------------------------------------------------------------
    # Run the multitone signal generator and the sampler
    gen.run()               # Run the generator    
    samp.mSig = gen.mSig    # Connect the signal from the generator to the sampler 
    samp.run()              # Run the sampler

    # -----------------------------------------------------------------
    # Plot the results of sampling
    inxSig = 2

    vSig = gen.mSig[inxSig, :]           # The signal from the generator
    vT = gen.vTSig                       # The time vector of the original signal
    vObSig = samp.mObSig[inxSig, :]      # The observed signal

    iPatInx = samp.vPattInx[inxSig]      # Index of the used sampling patterns
    vPattsT = samp.mPattsT[iPatInx, :]   # The sampling moments

    # Plot the signal and the observed sampling points    
    hFig1 = plt.figure(1)

    hSubPlot1 = hFig1.add_subplot(211)
    hSubPlot1.grid(True)
    strTitle = 'Signal #%d and the observed sampling points' % inxSig
    hSubPlot1.set_title(strTitle)
    hSubPlot1.plot(vT, vSig, '-')
    hSubPlot1.plot(vPattsT, vObSig, 'r*', markersize=10)

    # Plot the sampling pattern
    hSubPlot2 = hFig1.add_subplot(212)
    hSubPlot2.grid(True)
    strTitle = 'The sampling pattern #%d ' % iPatInx
    hSubPlot2.set_title(strTitle)
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

    mPhi = samp.lPhi[inxSig]  # Get the observation matrix
    vObSigPhi = np.dot(mPhi, vSig)  # Sample the signal using the observation matrix

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
    nonuniExtern_ex1()
