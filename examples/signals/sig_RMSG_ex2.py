"""
This script is an example of how to use the Random Multitone Signal
Generator module. |br|

In this example 1 random multitone signal is generated. |br|

Time of the signal is 10 us, the signal representation sampling frequency is
5 MHz. The highest possible frequency of a tone in the signal is 2 MHz,
the signal spectrum resolution is 100 kHz. |br|

There are 3 completely random tones in the signal. |br|

The power of the signal is not regulated. |br|

The noise is not added to the signal. |br|

After the generation, spectrum fo the signal is analyzed with an FFT
and ploted.

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    0.1  | 15-MAY-2014 : * Initial version. |br|
    0.2  | 21-MAY-2014 : * Docstrings added and PEP8 adjustments. |br|
    1.0  | 21-MAY-2014 : * Version 1.0 released. |br|
    1.1  | 22-MAY-2014 : * Specified frequencies removed, 3 fully random tones
                           in the signal. |br|

*License*:
    BSD 2-Clause
"""
from __future__ import division
import rxcs
import numpy as np
import matplotlib.pyplot as plt


def _sig_RMSG_ex2():

    # -----------------------------------------------------------------
    # Generate settings for the generator

    # Start the dictionary with signal generator configuration
    dSigConf = {}

    # Signal generator type: random multitone signal
    dSigConf['strSigType'] = "RandMult"

    # Time of the signal is 10 us
    dSigConf['tS'] = 10e-6

    # The signal representation sampling frequency is 5 MHz
    dSigConf['fR'] = 5e6

    # The highest possible frequency in the signal is 2 MHz
    dSigConf['fMax'] = 2e6

    # The signal spectrum resolution is 100 kHz
    dSigConf['fRes'] = 100e3

    # - - - - - - - - - - - - - - - -

    # The number of additional tones
    dSigConf['nTones'] = 3

    # Amplitude and phase parameters of additional tones:

    # Amplitude
    dSigConf['iMinAmp'] = 0.2  # Minimum amplitude
    dSigConf['iGraAmp'] = 0.1  # Gradation of amplitude
    dSigConf['iMaxAmp'] = 0.4  # Maximum amplitude

    # Phase:
    dSigConf['iMinPhs'] = 0  # Minimum phase of additional tones
    dSigConf['iGraPhs'] = 1  # Gradation of phase of additional tones
    dSigConf['iMaxPhs'] = 90  # Maximum phase of additional tones

    # - - - - - - - - - - - - - - - -

    # The number of signals to be generated
    dSigConf['nSigPack'] = 1

    # -----------------------------------------------------------------
    # Run the multtone signal generator
    dSig = rxcs.sig.sigRandMult.main(dSigConf)

    # Get the generated signal
    mSig = dSig['mSig']
    vSig = mSig[0, :]

    # Analyze the spectrum of the signal
    vFFT = np.fft.fft(vSig)

    # Get the size of the spectrum
    iS = vFFT.size

    # Get the amplitudes of tones
    vFFTa = 2*np.abs(vFFT[np.arange(iS/2).astype(int)])/iS

    # Create a vector with frequencies of the signal spectrum
    fFFTR = dSig['fFFTR']  # Signal FFT frequency resolution
    vF = fFFTR * np.arange(iS/2)

    # -----------------------------------------------------------------
    # Plot half of the spectrum
    hFig1 = plt.figure(1)
    hSubPlot1 = hFig1.add_subplot(111)
    hSubPlot1.grid(True)
    hSubPlot1.set_title('Spectrum of a random multitone signal')
    hSubPlot1.set_xlabel('Frequency [Hz]')
    (markerline, stemlines, baseline) = hSubPlot1.stem(vF, vFFTa,
                                                       linefmt='b-',
                                                       markerfmt='bo',
                                                       basefmt='r-')
    hSubPlot1.set_xlim(-100e3, 2.5e6)
    hSubPlot1.set_ylim(-0.1, 1.1)
    plt.setp(stemlines, color='b', linewidth=2.0)
    plt.setp(markerline, color='b', markersize=10.0)
    plt.show(block=True)


# =====================================================================
# Trigger when start as a script
# =====================================================================
if __name__ == '__main__':
    _sig_RMSG_ex2()
