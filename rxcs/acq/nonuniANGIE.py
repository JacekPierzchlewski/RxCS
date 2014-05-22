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

    # nSigs     -  the number of signals to be sampled
    # bMute     -  mute the conole output flag
    # tS        -  time of the signals to be sampled
    # tGrid     -  sampling grid period
    # fSamp     -  the average sampling frequency
    # iSigma    -  sigma parameter
    # tMin      -  minimum time betweeen sampling points
    # tMax      -  maximum time between sampling points
    (nSigs
     bMute,
     tS,
     fGrid,
     fSamp,
     iSigma,
     tMin,
     tMax) = _getConf(dAcqConf,dSig)


    # =================================================================
    # Get the signals to be sampled and their representation sampling frequency
    # =================================================================

    # nSigs     -  the number of signals to be sampled
    # bMute     -  mute the conole output flag
    # tS        -  time of the signals to be sampled
    # tGrid     -  sampling grid period
    # fSamp     -  the average sampling frequency
    # iSigma    -  sigma parameter
    # tMin      -  minimum time betweeen sampling points
    # tMax      -  maximum time between sampling points
    (nSigs
     bMute,
     tS,
     fGrid,
     fSamp,
     iSigma,
     tMin,
     tMax) = _getSigs(dSig)

def _getConf()

