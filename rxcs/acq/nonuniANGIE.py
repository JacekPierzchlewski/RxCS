from __future__ import division
import sys
import math
import time
import rxcs
import numpy as np


def main(dAcqConf,dSig):

    # =================================================================
    # Check the configuration dictionary and get the configuration from it
    # =================================================================

    # nPatts    -  the number of patterns to be generated
    # bMute     -  mute the conole output flag
    # tS        -  time of the signals to be sampled
    # tGrid     -  sampling grid period
    # fSamp     -  the average sampling frequency
    # iSigma    -  sigma parameter
    # tMin      -  minimum time betweeen sampling points
    # tMax      -  maximum time between sampling points
    (nPatts
     bMute,
     tS,
     fGrid,
     fSamp,
     iSigma,
     tMin,
     tMax) = _getConf(dAcqConf, dSig)

    # =================================================================
    # Get the signals to be sampled and their representation samp. freq.
    # =================================================================

    # mSigs     -  the signals to be sampled
    # fR        -  signals representation sampling frequency
    (mSigs
     fR) = _getSigs(dSig)


# =================================================================
# Check the configuration dictionary and get the configuration from it
# =================================================================
def _getConf(dAcqConf, dSig):

    # -----------------------------------------------------------------
    # Get the number of patterns to be generated

    # Get the number of signals from the dictionary with signals
    if not 'nSigs' in dSig:
        strError = ('Dictionary with signals to be sampled does not contain ')
        strError = strError + ('information about the number of signals')
        raise NameError(strErr)
    else:
        nSigs = dSig['nSigs']

    # Get the number of patterns from the configuraion
    if not 'nPatts' in dAcqConf:
        nPatts = nSigs
    else:
        nPatts = dAcqConf['nPatts']

    # Check if the number of patterns to be generated given in the
    # configuration is equal to the number of signals given in the dictionary
    # with signals to be sampled
    if nSigs != nPatts:
        strError = ('The number of patterns to be generated given in  ')
        strError = strError + ('the configuration differs from the number of ')
        strError = strError + ('signals in the input dictionary with signals')
        raise ValueError(strErr)

    # -----------------------------------------------------------------
    # Get the mute flag
    if not 'bMute' in dAcqConf:
        bMute = 0
    else:
        bMute = dAcqConf['bMute']

    # -----------------------------------------------------------------
    # Get the time of the sampling patterns

    # Get the time of signals from the dictionary with signals
    if not 'tS' in dSig:
        strError = ('Dictionary with signals to be sampled does not contain ')
        strError = strError + ('information about the time of the signals')
        raise NameError(strErr)
    else:
        tS = dSig['tS']

    # Get the time of patterns from the configuration
    if not 'tTau' in dAcqConf:
        tTau = tS
    else:
        tTau = dAcqConf['tTau']

    # Check if the time of patterns is equal to the time of signals to be
    $ sampled


# =================================================================
# Get the signals to be sampled and their representation samp. freq.
# =================================================================
def _getSigs(dSig):


