"""
This script is an example of how to use the nonuniform sampler with the ANGIE
scheme. |br|

In this example 1000 random multitone signals are generated and sampled |br|

The signals contain 3 random tones, the highest possible frequency in the
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
    1.0    | 13-AUG-2015 : * Version 1.0 released. |br|
    2.1    | 17-AUG-2015 : * Adjusted to ANGIE sampler v2.1 (observation matrices in a list) |br|

*License*:
    BSD 2-Clause
"""

from __future__ import division
import rxcs
import numpy as np
import matplotlib.pyplot as plt


def nonuniANGIE_ex1():

    # Put the stuff on board
    gen = rxcs.sig.randMult()      # Signal generator
    samp = rxcs.acq.nonuniANGIE()  # Sampler   
    
    # General settings    
    TIME = 1e-3  # Time of the signal is 1 ms    
    FSMP = 1e6   # The signal representation sampling frequency is 1 MHz
    NSIG = 1e3   # The numer of signals to be generated    
    
    # Settings for the generator
    gen.tS = TIME            # Time of the signal is 1 ms
    gen.fR = FSMP            # The signal representation sampling frequency is 1 MHz
    gen.fMax = 10e3          # The highest possible frequency in the signal is 10 kHz
    gen.fRes = 1e3           # The signal spectrum resolution is 1 kHz
    gen.nTones = 3           # The number of random tones
    gen.nSigs = int(NSIG)    # The number of signals
    
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
    iSigInx1 = np.random.randint(NSIG)   # 1st signal index
    iSigInx2 = np.random.randint(NSIG)   # 2nd signal index

    vT = gen.vTSig                 # The time vector of the signals

    # First signal:
    vSig1 = gen.mSig[iSigInx1, :]          # The 1st signal from the generator
    vObSig1 = samp.mObSig[iSigInx1, :]     # The corresponding observed signal
    vPattsT1 = samp.mPattsT[iSigInx1, :]   # The corresponding sampling moments
    plotSigPattObs(1, vT, vSig1, vPattsT1, vObSig1, iSigInx1)

    # Second signal:
    vSig2 = gen.mSig[iSigInx2, :]          # The 2nd signal from the generator
    vObSig2 = samp.mObSig[iSigInx2, :]     # The corresponding observed signal
    vPattsT2 = samp.mPattsT[iSigInx2, :]   # The corresponding sampling moments
    plotSigPattObs(2, vT, vSig2, vPattsT2, vObSig2, iSigInx2)


    # -----------------------------------------------------------------
    # APPENDIX:
    # This part is to show how to use the observation matrix, if it is needed
    # (for example in compressed sensing systems)

    mPhi1 = samp.lPhi[iSigInx1]          # Get the observation matrix for the 1st signal
    vObSigPhi1 = np.dot(mPhi1, vSig1)    # Sample the 1st signal using the observation matrix

    mPhi2 = samp.lPhi[iSigInx2]          # Get the observation matrix for the 2nd signal
    vObSigPhi2 = np.dot(mPhi2, vSig2)    # Sample the 2nd signal using the observation matrix

    # Plot the 1st signal and the observed sampling points
    hFig3 = plt.figure(3)
    hSubPlot1 = hFig3.add_subplot(111)
    hSubPlot1.grid(True)
    strTitle = 'Signal #%d and the observed sampling points' % iSigInx1
    hSubPlot1.set_title(strTitle)
    hSubPlot1.plot(vT, vSig1, '-')
    hSubPlot1.plot(vPattsT1, vObSigPhi1, 'ro', markersize=10)

    # Plot the 2nd signal and the observed sampling points
    hFig4 = plt.figure(4)
    hSubPlot1 = hFig4.add_subplot(111)
    hSubPlot1.grid(True)
    strTitle = 'Signal #%d and the observed sampling points' % iSigInx2
    hSubPlot1.set_title(strTitle)
    hSubPlot1.plot(vT, vSig2, '-')
    hSubPlot1.plot(vPattsT2, vObSigPhi2, 'ro', markersize=10)

    # -----------------------------------------------------------------
    plt.show(block=True)


def plotSigPattObs(iFig, vT, vSig, vPattsT, vObSig, iSigInx):
    """
        This function plots a sampler signal, observed sampling points and
        a sampling pattern.
        
        Args:
            iFig (number):      index of the figure 
            vT (vector) :       time vector for the input signal
            vSig (vector):      the sampled signal samplingS
            vPattsT (vector):   time moments of sampling
            vObSig (vector):    observed signals samples
            iSigInx (number):   index of the sampled signal

        Returns:
                none
    """
    hFig = plt.figure(iFig)   # Start the figure
    
    # Plot the signal and the observed sampling points
    hSubPlot1 = hFig.add_subplot(211)
    hSubPlot1.grid(True)
    strTitle = 'Signal #%d and the observed sampling points' % iSigInx
    hSubPlot1.set_title(strTitle)
    hSubPlot1.plot(vT, vSig, '-')
    hSubPlot1.plot(vPattsT, vObSig, 'r*', markersize=10)

    # Plot the sampling pattern
    hSubPlot2 = hFig.add_subplot(212)
    hSubPlot2.grid(True)
    hSubPlot2.set_title('The sampling pattern')
    hSubPlot2.set_xlabel('Time [s]')
    (markerline, stemlines, _) = hSubPlot2.stem(vPattsT, np.ones(vPattsT.shape),
                                                linefmt='b-', markerfmt='bo', basefmt='-')
    hSubPlot2.set_ylim(0, 1.1)
    hSubPlot2.set_xlim(0, 0.001)
    plt.setp(stemlines, color='b', linewidth=2.0)
    plt.setp(markerline, color='b', markersize=10.0)


# =====================================================================
# Trigger when start as a script
# =====================================================================
if __name__ == '__main__':
    nonuniANGIE_ex1()
