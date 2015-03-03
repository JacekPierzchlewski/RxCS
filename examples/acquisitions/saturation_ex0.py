"""
This script is an example of how to use the saturation block. |br|

In this example 1 random multitone signal is generated. The signal contains 3 random tones,
the highest possible frequency in the signal is 10 kHz. |br|

After the signal generation, the signal is pushed through a saturation block,
which limits the signal's minimum and maximum values. |br|

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

def _saturation_ex0():

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
    # Pushed the observed signal through the saturation block

    # Generate settings for the saturation block
    dAcqConf = {}
    dAcqConf['iMinAmp'] = -0.8  # Minimum amplitude
    dAcqConf['iMaxAmp'] = 0.8   # Maximum amplitude

    # Run the saturation block
    dObSig = rxcs.acq.satur.main(dAcqConf, dSig)

    # -----------------------------------------------------------------
    # Plot the results of sampling

    # Get the original signal and its time vector
    mSig = dSig['mSig']
    vSig = mSig[0, :]
    vT = dSig['vTSig']

    # Get the observed limited signal and saturation markers
    mObSig = dObSig['mObSig']  # the observed signal
    vObSig = mObSig[0, :]      # get the first observed signal (in fact there where only 1)
    mSaturMark = dObSig['mSaturMark']   # get the saturation markers
    vSaturMark = mSaturMark[0,    :]   # get the first set ot saturation markers


    hFig1 = plt.figure(1)
    # Plot the original signal and the saturated signal
    hSubPlot1 = hFig1.add_subplot(211)
    hSubPlot1.grid(True)
    hSubPlot1.set_title('Signals in the time domain')
    hSubPlot1.plot(vT, vSig, 'b-', label='original signal')
    hSubPlot1.plot(vT, vObSig, 'r-', label='signal after the saturation block')
    hSubPlot1.legend()

    hSubPlot2 = hFig1.add_subplot(212)
    hSubPlot2.set_title('Saturation markers in the time domain')
    hSubPlot2.plot(vT, vSaturMark, 'g-')
    hSubPlot2.set_xlabel('Time')
    hSubPlot2.set_ylim(-1.2, 1.2)

    # -----------------------------------------------------------------
    plt.show(block=True)



# =====================================================================
# Trigger when start as a script
# =====================================================================
if __name__ == '__main__':
    _saturation_ex0()
