
from __future__ import division
import rxcs
import numpy as np
import matplotlib.pyplot as plt


def _samp_RMSG_ANGIE_ex0():

    # -----------------------------------------------------------------
    # Generate settings for the generator

    # Start the dictionary with signal generator configuration
    dSigConf = {}

    # Signal generator type: random multitone signal
    dSigConf['strSigType'] = "RandMult"

    # Time of the signal is 1 ms
    dSigConf['tS'] = 1e-3

    # The signal representation sampling frequency is 1 MHz
    dSigConf['fR'] = 1e6

    # The highest possible frequency in the signal is 10 kHz
    dSigConf['fMax'] = 10e3

    # The signal spectrum resolution is 1 kHz
    dSigConf['fRes'] = 1e3

    # - - - - - - - - - - - - - - - -

    # The number of additional tones
    dSigConf['nTones'] = 1

    # - - - - - - - - - - - - - - - -

    # The power of the signal
    dSigConf['iP'] = 1

    # The noise added to the signal
    dSigConf['iSNR'] = 5

    # - - - - - - - - - - - - - - - -

    # The number of signals to be generated
    dSigConf['nSigPack'] = 1

    # -----------------------------------------------------------------
    # Generate settings for the sampler

    # Start the dictionary with signal acquisition configuration
    dAcqConf = {}

    # The number of patterns
    dAcqConf['nPatts'] = 1

    # The time
    dAcqConf['tTau'] = 1e-3

    # The sampling grid period
    dAcqConf['Tg'] = 1e-6

    # The average sampling frequency
    dAcqConf['fSamp'] = 0.5e6

    # The minimum distance between sampling points
    dAcqConf['tMin'] = 1e-6

    # The maximum distance between sampling points
    dAcqConf['tMax'] = 1e-6

    # -----------------------------------------------------------------
    # Run the multtone signal generator and the sampler
    dSig = rxcs.sig.sigRandMult.main(dSigConf)   # the generator
    rxcs.acq.nonuniANGIE.main(dAcqConf, dSig)    # the sampler



# =====================================================================
# Trigger when start as a script
# =====================================================================
if __name__ == '__main__':
    _samp_RMSG_ANGIE_ex0()
