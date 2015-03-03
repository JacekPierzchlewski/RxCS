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

*License*:
    BSD 2-Clause
"""
from __future__ import division
import rxcs
import matplotlib.pyplot as plt
import numpy as np

def _saturation_ex1():

    # -----------------------------------------------------------------
    # Generate the signal

    # Generate settings for the generator
    dSigConf = {}
    dSigConf['tS'] = 1e-3     # Time of the signal is 1 ms
    dSigConf['fR'] = 1e6      # The signal representation sampling frequency is 1 MHz
    dSigConf['fMax'] = 10e3   # The highest possible frequency in the signal is 10 kHz
    dSigConf['fRes'] = 1e3    # The signal spectrum resolution is 1 kHz

    dSigConf['nTones'] = 3    # The number of tones

    dSigConf['iMinAmp'] = 0.1  # Minimum amplitude of a single tone
    dSigConf['iMaxAmp'] = 1.0  # Maximum amplitude of a single tone

    dSigConf['nSigPack'] = 1  # The number of signals to be generated

    # Generate the signal
    dSig = rxcs.sig.sigRandMult.main(dSigConf)

    # -----------------------------------------------------------------
    # Sample the signal

    # Start the dictionary with signal acquisition configuration
    dAcqConf = {}
    dAcqConf['Tg'] = 1e-6      # The sampling grid period
    dAcqConf['fSamp'] = 40e3   # The average sampling frequency
    dAcqConf['iAlpha'] = 0.5   # The alpha parameter

    # Sample the signal
    dObSig = rxcs.acq.uniform.main(dAcqConf, dSig)

    # -----------------------------------------------------------------
    # Pushed the observed signal through the saturation block

    # Generate settings for the saturation block
    dAcqConf = {}
    dAcqConf['iMinAmp'] = -0.8  # Minimum amplitude
    dAcqConf['iMaxAmp'] = 0.8   # Maximum amplitude

    # Run the saturation block
    dObSigSatur = rxcs.acq.satur.main(dAcqConf, dObSig)

    # -----------------------------------------------------------------
    # Plot the results of sampling

    # Get the original signal and its time vector
    mSig = dSig['mSig']
    vSig = mSig[0, :]
    vT = dSig['vTSig']

    # Get the observed signal (uniformly sampled)
    mObSig = dObSig['mObSig']  # the observed signal
    vObSig = mObSig[0, :]
    mPattsT = dObSig['mPattsT']  # the sampling moments
    vPattsT = mPattsT[0, :]

    # Get the observed limited signal and saturation markers
    mObSigSatur = dObSigSatur['mObSig']      # the observed signal
    vObSigSatur = mObSigSatur[0, :]          # get the first observed signal (in fact there where only 1)
    mSaturMark = dObSigSatur['mSaturMark']   # get the saturation markers
    vSaturMark = mSaturMark[0, :]            # get the first set ot saturation markers

    # Get the observed signals with saturated sampled removed and sampling patterns with saturated samples removed
    lObSigClean = dObSigSatur['lObSigClean']
    vObSigClean = lObSigClean[0]
    lPattsTClean = dObSigSatur['lPattsTClean']
    vPattTClean = lPattsTClean[0]

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
