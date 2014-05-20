"""
This script is an example of how to use the Random Multitone Signal
Generator module. |br|

In this example 1 random multitone signal is generated. |br|

Time of the signal is 1 ms, the signal representation sampling frequency is
100 kHz. The highest possible frequency of a tone in the signal is 20 kHz,
the signal spectrum resolution is 1 kHz. |br|

The signal contains 3 tones with specified frequencies (2000 Hz, 3000Hz and
4000 Hz). The amplitudes of these tones are 1, 2 and 3 respectively. The
phases of these tones are randomly chosen by the generator. |br|
The above is given in the 3 fields in the generator configuration dictionary:

    dSigConf['vFrqs'] = np.array([2e3, 3e3, 4e3]) |br|

    dSigConf['vAmps'] = np.array([1, 2, 3]) |br|

    dSigConf['vPhs'] = np.array([np.nan, np.nan, np.nan]) |br|

Additonally, there are 3 completely random tones in the signal. |br|

The power of the signal is not regulated. |br|

The noise is not added to the signal. |br|

After the generation, spectrum fo the signal is analyzed with an FFT
and ploted.

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    0.1  | 15-MAY-2014 : * Initial version. |br|
    0.2  | 20-MAY-2014 : * Docstrings added and PEP8 adjustments. |br|
    1.0  | 20-MAY-2014 : * Version 1.0 released. |br|

*License*:
    BSD 2-Clause
"""
from __future__ import division
import rxcs
import numpy as np
import matplotlib.pyplot as plt


def _sig_RMSG_ex1():

    # -----------------------------------------------------------------
    # Generate settings for the generator

    # Start the dictionary with signal generator configuration
    dSigConf = {}

    # Signal generator type: random multitone signal
    dSigConf['strSigType'] = "RandMult"

    # Time of the signal is 1 ms
    dSigConf['tS'] = 1e-3

    # The signal representation sampling frequency is 100 kHz
    dSigConf['fR'] = 1e5

    # The highest possible frequency in the signal is 20 kHz
    dSigConf['fMax'] = 40e3

    # The signal spectrum resolution is 1 kHz
    dSigConf['fRes'] = 1e3

    # - - - - - - - - - - - - - - - -

    # Vector with given frequencies
    dSigConf['vFrqs'] = np.array([2e3, 3e3, 4e3])

    # Vector with given amplitudes
    dSigConf['vAmps'] = np.array([1, 2, 3])

    # Vector with given phases
    dSigConf['vPhs'] = np.array([np.nan, np.nan, np.nan])

    # - - - - - - - - - - - - - - - -

    # The number of additional tones
    dSigConf['nTones'] = 3

    # Amplitude and phase parameters of additional tones:

    # Amplitude
    dSigConf['iMinAmp'] = 0.1  # Minimum amplitude
    dSigConf['iGraAmp'] = 0.1  # Gradation of amplitude
    dSigConf['iMaxAmp'] = 1.0  # Maximum amplitude

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
    hSubPlot1.set_xlim(-1*1e3, 51*1e3)
    hSubPlot1.set_ylim(-0.1, 3.1)
    plt.setp(stemlines, color='b', linewidth=2.0)
    plt.setp(markerline, color='b', markersize=10.0)
    plt.show(block=True)


# =====================================================================
# Trigger when start as a script
# =====================================================================
if __name__ == '__main__':
    _sig_RMSG_ex1()
