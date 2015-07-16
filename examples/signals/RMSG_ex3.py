"""
This script is an example of how to use the Random Multitone Signal
Generator module. |br|

In this example 4 random multitone signal is generated. |br|

Time of the signal is 10 us, the signal representation sampling frequency is
100 MHz. The highest possible frequency of a tone in the signal is 40 MHz,
the signal spectrum resolution is 100 kHz. |br|

The signal contains 11 tones with specified frequencies.
Frequencies of the first 6 tones are specified, these frequencies are
1kHz, 2kHz, 3kHz, 4kHz, 5kHz and 6kHz.
The amplitudes of the first 6 tones are specified, all are equal to 1.
Frequencies of the next 5 tones are specified, these frequencies are
22kHz, 23kHz, 24kHz, 25kHz and 26kHz.
The amplitudes of these 5 tones are not specified,
The phases of all 11 tones are randomly chosen by the generator. |br|

There are no additional random tones in the signal. |br|

The power of the signals is adjusted to 1 W. |br|

The noise is not added to the signal. |br|

After the generation, the power of signals at different frequencies
is analyzed using the Welch's method.

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    0.1  | 15-MAY-2014 : * Initial version. |br|
    0.2  | 21-MAY-2014 : * Docstrings added and PEP8 adjustments. |br|
    1.0  | 21-MAY-2014 : * Version 1.0 released. |br|
    1.1  | 15-JUL-2015 : * Adjusted to new name of random multitone gen. |br|


*License*:
    BSD 2-Clause
"""
from __future__ import division
import rxcs
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt


def _RMSG_ex3():

    # -----------------------------------------------------------------
    # Generate settings for the generator

    # Start the dictionary with signal generator configuration
    dSigConf = {}

    # Signal generator type: random multitone signal
    dSigConf['strSigType'] = "RandMult"

    # Time of the signal is 10 us
    dSigConf['tS'] = 10e-6

    # The signal representation sampling frequency is 100 MHz
    dSigConf['fR'] = 100e6

    # The highest possible frequency in the signal is 40 MHz
    dSigConf['fMax'] = 40e6

    # The signal spectrum resolution is 100 kHz
    dSigConf['fRes'] = 100e3

    # - - - - - - - - - - - - - - - -

    # Vector with given frequencies
    dSigConf['vFrqs'] = np.array([1e6,
                                  2e6,
                                  3e6,
                                  4e6,
                                  5e6,
                                  6e6,
                                  22e6,
                                  23e6,
                                  24e6,
                                  25e6,
                                  26e6])

    # Vector with given amplitudes
    dSigConf['vAmps'] = np.array([1,
                                  1,
                                  1,
                                  1,
                                  1,
                                  1,
                                  np.nan,
                                  np.nan,
                                  np.nan,
                                  np.nan,
                                  np.nan])

    # Vector with given phases
    dSigConf['vPhs'] = np.nan*np.zeros(11)

    # - - - - - - - - - - - - - - - -

    # The power of signals
    dSigConf['iP'] = 1

    # - - - - - - - - - - - - - - - -

    # The number of additional tones
    dSigConf['nTones'] = 0

    # Amplitude and phase parameters of additional tones:

    # Amplitude
    dSigConf['iMinAmp'] = 1.0  # Minimum amplitude
    dSigConf['iGraAmp'] = 0.1  # Gradation of amplitude
    dSigConf['iMaxAmp'] = 3.0  # Maximum amplitude

    # Phase:
    dSigConf['iMinPhs'] = 0  # Minimum phase of additional tones
    dSigConf['iGraPhs'] = 1  # Gradation of phase of additional tones
    dSigConf['iMaxPhs'] = 90  # Maximum phase of additional tones

    # - - - - - - - - - - - - - - - -

    # The number of signals to be generated
    dSigConf['nSigPack'] = 4

    # -----------------------------------------------------------------
    # Run the multtone signal generator
    dSig = rxcs.sig.randMult.main(dSigConf)

    # Get the generated signals
    mSig = dSig['mSig']
    vSig1 = mSig[0, :]
    vSig2 = mSig[1, :]
    vSig3 = mSig[2, :]
    vSig4 = mSig[3, :]

    # Get the signals representation sampling frequency
    fR = dSig['fR']

    # Analyze the spectrum of the signals
    (vF, Pxx_den1) = signal.welch(vSig1, fR, nperseg=128)

    # Analyze the spectrum of the signals
    (_, Pxx_den2) = signal.welch(vSig2, fR, nperseg=128)

    # Analyze the spectrum of the signals
    (_, Pxx_den3) = signal.welch(vSig3, fR, nperseg=128)

    # Analyze the spectrum of the signals
    (_, Pxx_den4) = signal.welch(vSig4, fR, nperseg=128)

    # -----------------------------------------------------------------
    # Plot the spectrum
    hFig1 = plt.figure(1)

    # Signal 1
    hSubPlot1 = hFig1.add_subplot(221)
    hSubPlot1.grid(True)
    hSubPlot1.set_title('Spectrum of a random multitone signal #1')
    hSubPlot1.set_xlabel('Frequency [Hz]')
    hSubPlot1.plot(vF, Pxx_den1, '-')

    # Signal 2
    hSubPlot2 = hFig1.add_subplot(222)
    hSubPlot2.grid(True)
    hSubPlot2.set_title('Spectrum of a random multitone signal #2')
    hSubPlot2.set_xlabel('Frequency [Hz]')
    hSubPlot2.plot(vF, Pxx_den2, '-')

    # Signal 3
    hSubPlot2 = hFig1.add_subplot(223)
    hSubPlot2.grid(True)
    hSubPlot2.set_title('Spectrum of a random multitone signal #3')
    hSubPlot2.set_xlabel('Frequency [Hz]')
    hSubPlot2.plot(vF, Pxx_den3, '-')

    # Signal 4
    hSubPlot2 = hFig1.add_subplot(224)
    hSubPlot2.grid(True)
    hSubPlot2.set_title('Spectrum of a random multitone signal #4')
    hSubPlot2.set_xlabel('Frequency [Hz]')
    hSubPlot2.plot(vF, Pxx_den4, '-')

    plt.show(block=True)

# =====================================================================
# Trigger when start as a script
# =====================================================================
if __name__ == '__main__':
    _RMSG_ex3()
