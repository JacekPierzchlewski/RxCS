from __future__ import division
import rxcs
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

def _sig_RMSG_ex3():

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
                                  26e6,
                                  ])

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
                                  np.nan,
                                  ])

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
    dSig = rxcs.sig.sigRandMult.main(dSigConf)

    # Get the generated signals
    mSig = dSig['mSig']
    vSig1 = mSig[0,:]
    vSig2 = mSig[1,:]
    vSig3 = mSig[2,:]
    vSig4 = mSig[3,:]

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
    _sig_RMSG_ex3()
