"""
This script is an example of how to use the nonuniform sampler with the ANGIE
scheme. |br|

In this example 1 random multitone signal is generated and sampled |br|

The signal contains 3 random tones, the highest possible frequency in the
signal is 10 kHz.

The signal is nonuniformly sampled with the average sampling frequency
equal to 8 kHz. The sampling gird is 1 us. A sampling patterns is generated
using ANGIE scheme.

After the signal generation and sampling, the original signal and the observed
signal is plotted in the time domain. Additionally, the sampling pattern is
plotted.

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0    | 27-MAY-2014 : * Version 1.0 released. |br|
    2.0    | 11-AUG-2015 : * Version 2.0 released (adjusted to signal generator v2.0)  |br|
    2.0r1  | 11-AUG-2015 : * File name changed |br|


*License*:
    BSD 2-Clause
"""

from __future__ import division
import rxcs
import numpy as np
import matplotlib.pyplot as plt


def nonuniANGIE_ex0():

    # Put the generator on board
    gen = rxcs.sig.randMult()
    
    # Settings for the generator
    gen.tS = 1e-3     # Time of the signal is 1 ms
    gen.fR = 1e6      # The signal representation sampling frequency is 1 MHz
    gen.fMax = 10e3   # The highest possible frequency in the signal is 10 kHz
    gen.fRes = 1e3    # The signal spectrum resolution is 1 kHz

    gen.nTones = 3    # The number of random tones

    # -----------------------------------------------------------------
    # Generate settings for the sampler

    # Start the dictionary with signal acquisition configuration
    dAcqConf = {}

    # The sampling grid period
    dAcqConf['Tg'] = 1e-6

    # The average sampling frequency
    dAcqConf['fSamp'] = 8e3

    # -----------------------------------------------------------------
    # Run the multitone signal generator and the sampler
    dSig = gen.run()  # Run the generator    
    vSig = gen.mSig[0, :]   # Get the signal from the generator
  
    dObSig = rxcs.acq.nonuniANGIE.main(dAcqConf, dSig)    # the sampler

    # -----------------------------------------------------------------
    # Plot the results of sampling

    # Get the time vector of the original signal 
    vT = gen.vTSig

    # Get the observed signal and sampling moments
    mObSig = dObSig['mObSig']  # the observed signal
    vObSig = mObSig[0, :]

    mPattsT = dObSig['mPattsT']  # the sampling moments
    vPattsT = mPattsT[0, :]

    hFig1 = plt.figure(1)

    # Plot the signal and the observed sampling points
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

    # -----------------------------------------------------------------
    # APPENDIX:
    # This part is to show how to use the observation matrix, if it is needed
    # (for example in compressed sensing systems)

    # Get a 3D matrix with observation matrices
    m3Phi = dObSig['m3Phi']

    # Get the first observation matrix (1st page of the m3Phi matrix)
    mPhi = m3Phi[0, : ,:]

    # Sample the signal using the observation matrix
    vObSigPhi = np.dot(mPhi, vSig)

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
    nonuniANGIE_ex0()
