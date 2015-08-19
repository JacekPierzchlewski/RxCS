"""
This script is an example of how to use the nonuniform sampler with the 
external sampling scheme. 
The sampler is run in the 'dummy' mode - the signal is not sampled, only an
observation matrix is generated. |br|

In this example 1 random multitone signal is generated and sampled |br|

The signal contains 3 random tones, the highest possible frequency in the
signal is 10 kHz.

The signal is nonuniformly sampled with an external sampling pattern.

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


def nonuniExtern_ex0():

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

    # Generate settings for the sampler
    samp.tS = TIME     # Time of the signal
    samp.fR = FSMP     # The signal representation sampling freuqnecy
    samp.Tg = 1e-5     # The sampling grid period
    samp.mPatterns = np.array([[20, 25, 57, 65, 88]])

    # -----------------------------------------------------------------
    # Run the multitone signal generator and the sampler
    gen.run()               # Run the generator    
    samp.run()              # Run the sampler

    mPhi = samp.lPhi[0]     # Get the observation matrix from the sampler
    vSig = gen.mSig[0, :]   # Get the generated signal
    vObSig = np.dot(mPhi, vSig)   # Apply the observation matrix onto the 
                                  # generated signal
    # -----------------------------------------------------------------
    # Plot the results of sampling
    vT = gen.vTSig          # The time vector of the original signal
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

    plt.show(block=True)


# =====================================================================
# Trigger when start as a script
# =====================================================================
if __name__ == '__main__':
    nonuniExtern_ex0()
