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
    # tTau      -  time of sampling patterns
    # Tg        -  sampling grid period
    # fSamp     -  the average sampling frequency
    # iSigma    -  sigma parameter
    # tMin      -  minimum time betweeen sampling points
    # tMax      -  maximum time between sampling points
    (nPatts,
     bMute,
     tTau,
     Tg,
     fSamp,
     iSigma,
     tMin,
     tMax) = _getConf(dAcqConf, dSig)

    # - - - - - - - - - - - - - - - - - - -

    # Get the signals to be sampled and get their representation sampling
    # frequency and time
    # mSigs     -  the signals to be sampled
    # fR        -  signals representation sampling frequency
    # tS        -  time  of signals
    (mSig, fR, tS) = _getSigs(dSig)

    # - - - - - - - - - - - - - - - - - - -

    # Print the configuration to the console
    tStart = _printConf(dAcqConf, dSig)

    # - - - - - - - - - - - - - - - - - - -

    # Check if the configuration for the sampler make sense
    _checkConf(dAcqConf, dSig)

    # - - - - - - - - - - - - - - - - - - -

    # =================================================================
    # Generate the sampling patterns
    # =================================================================


    # =================================================================
    # Sample the signals
    # =================================================================


    # =================================================================
    # Generate the output dictionary
    # =================================================================

    # =================================================================
    # Signal sampling is done!
    # =================================================================
    if bMute == 0:
        rxcs.console.module_progress_done(tStart)


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
        raise NameError(strError)
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
        raise ValueError(strError)

    # -----------------------------------------------------------------
    # Get the mute flag
    if not 'bMute' in dAcqConf:
        bMute = 0
    else:
        bMute = dAcqConf['bMute']

    # -----------------------------------------------------------------
    # Get the time of sampling patterns

    # Get the time of signals from the dictionary with signals
    if not 'tS' in dSig:
        strError = ('Dictionary with signals to be sampled does not contain ')
        strError = strError + ('information about the time of the signals')
        raise NameError(strError)
    else:
        tS = dSig['tS']

    # Get the time of patterns from the configuration
    if not 'tTau' in dAcqConf:
        tTau = tS
    else:
        tTau = dAcqConf['tTau']

    # The time of patterns must be higher than zero
    if not tTau > 0:
        strError = ('The time of patterns must be higher than zero')
        raise ValueError(strError)

    # -----------------------------------------------------------------
    # Get the sampling grid period
    if not 'Tg' in dAcqConf:
        strError = ('The sampling grid period (Tg) is not given in the ')
        strError = strError + ('configuration')
        raise NameError(strError)
    else:
        Tg = dAcqConf['Tg']

    # The sampling grid period must be higher than zero
    if not Tg > 0:
        strError = ('The sampling grid period must be higher than zero')
        raise ValueError(strError)

    # -----------------------------------------------------------------
    # Get the average sampling frequency
    if not 'fSamp' in dAcqConf:
        strError = ('The average sampling frequency (fSamp) is not given in ')
        strError = strError + ('the configuration')
        raise NameError(strError)
    else:
        fSamp = dAcqConf['fSamp']

    # The average sampling frequency must be higher than zero
    if not fSamp > 0:
        strError = ('The average sampling frequency must be higher than zero')
        raise ValueError(strError)

    # -----------------------------------------------------------------
    # Get the sigma parameter
    if not 'iSigma' in dAcqConf:
        iSigma = 1
    else:
        iSigma = dAcqConf['iSigma']

    # The sigma parameter must be higher than zero
    if not iSigma > 0:
        strError = ('The sigma parameter must be higher than zero')
        raise ValueError(strError)

    # -----------------------------------------------------------------
    # Get the minimum distance between sampling points
    if not 'tMin' in dAcqConf:
        tMin = np.nan
    else:
        tMin = dAcqConf['tMin']

    # The minimum distance between sampling points must be higher than zero
    if not tMin > 0:
        strError = ('The min. distance between sampling points must be ')
        strError = strError + ('higher than zero')
        raise ValueError(strError)

    # -----------------------------------------------------------------
    # Get the maximum distance between sampling points
    if not 'tMax' in dAcqConf:
        tMax = np.nan
    else:
        tMax = dAcqConf['tMax']

    # The maximum distance between sampling points must be higher than zero
    if not tMax > 0:
        strError = ('The max distance between sampling points must be ')
        strError = strError + ('higher than zero')
        raise ValueError(strError)

    # -----------------------------------------------------------------
    return (nPatts,    # the number of patterns to be generated
            bMute,     # mute the conole output flag
            tTau,      # the time of sampling patterns
            Tg,        # the sampling grid period
            fSamp,     # the average sampling frequency
            iSigma,    # the sigma parameter
            tMin,      # minimum time between sampling patterns
            tMax)      # maximum time between sampling patterns


# =================================================================
# Get the signals to be sampled and their representation samp. freq.
# =================================================================
def _getSigs(dSig):

    # -----------------------------------------------------------------
    # Get the signals to be sampled
    if not 'mSig' in dSig:
        strError = ('Dictionary with signals to be sampled does not contain ')
        strError = strError + ('signals')
        raise NameError(strError)
    else:
        mSig = dSig['mSig']

    # -----------------------------------------------------------------
    # Get the signals representation sampling frequency
    if not 'fR' in dSig:
        strError = ('Dictionary with signals to be sampled does not contain')
        strError = strError + ('signals representation sampling frequency')
        raise NameError(strError)
    else:
        fR = dSig['fR']

    # -----------------------------------------------------------------
    # Get the signals time
    if not 'tS' in dSig:
        strError = ('Dictionary with signals to be sampled does not contain')
        strError = strError + ('signals time')
        raise NameError(strError)
    else:
        tS = dSig['tS']

    # -----------------------------------------------------------------
    return (mSig,   # the signals to be sampled
            fR,     # the signals representation sampling frequency
            tS)     # the signals time


# =================================================================
# Check if the configuration for the sampler make sense
# =================================================================
def _checkConf(dAcqConf, dSig):

    # -----------------------------------------------------------------
    # Get the configuration

    # nPatts    -  the number of patterns to be generated
    # bMute     -  mute the conole output flag
    # tTau      -  time of sampling patterns
    # Tg        -  sampling grid period
    # fSamp     -  the average sampling frequency
    # iSigma    -  sigma parameter
    # tMin      -  minimum time between sampling points
    # tMax      -  maximum time between sampling points
    (nPatts,
     bMute,
     tTau,
     Tg,
     fSamp,
     iSigma,
     tMin,
     tMax) = _getConf(dAcqConf, dSig)

    # -----------------------------------------------------------------
    # Get the representation sampling frequency of signals to be sampled
    # and the time of the signals
    (_, fR, tS) = _getSigs(dSig)

    # -----------------------------------------------------------------
    # Compute the real parameters of the sampling patterns

    # nK_g        -  the number of grid points in the sampling period
    # tHatTau     -  the real time of sampling patterns
    # nHatKdag_s  -  the expected number of sampling points in a pattern
    # fHatdag_s,  -  the expected average sampling frequency
    # nHatdag_s,  -  the expected average sampling period (as grid pts)
    # tHatT_s,    -  the expected average sampling period
    # nK_min      -  min t between the samp pts as the number of grid pts
    # nK_max      -  max t between the samp pts as the number of grid pts
    # tHatMin,    -  the real minimum time between sampling points
    # tHatMax)    -  the real maximum time between sampling points
    (nK_g,
     tHatTau,
     nHatKdag_s,
     fHatdag_s,
     nHatdag_s,
     tHatT_s,
     nK_min,
     nK_max,
     tHatMin,
     tHatMax) = _computeRealParam(dAcqConf, dSig)

    # -----------------------------------------------------------------
    # Check if the real time of patterns is higher than 0
    if not tHatTau > 0:
        strError = ('Real time of patterns must be higher than zero')
        raise ValueError(strError)

    # -----------------------------------------------------------------
    # Check if the number of grid points in patterns is higher than 0
    if not nK_g > 0:
        strError = ('Real number of grid points in patterns must be higher ')
        strError = strError + ('than zero')
        raise ValueError(strError)

    # -----------------------------------------------------------------
    # Check if the expected number of sampling points is higher than 0
    if not nHatKdag_s > 0:
        strError = ('The expected number of sampling points in patterns ')
        strError = strError + ('must be higher than zero')
        raise ValueError(strError)

    # -----------------------------------------------------------------
    # Check if the time of patterns is equal to the time of signals to be
    # sampled
    if tHatTau != tS:
        strError = ('The real time of patterns is different than the time ')
        strError = strError + ('of signals to be sampled')
        raise ValueError(strError)

    # -----------------------------------------------------------------
    # Check if the expected number of sampling points is lower or equal
    # to the number of grid points
    if not nK_g >= nHatKdag_s:
        strError = ('The real number of grid points in patterns must be ')
        strError = strError + ('higher or equal to the number of expected ')
        strError = strError + ('sampling points')
        raise ValueError(strError)

    # -----------------------------------------------------------------
    # Check if the minimum time between the sampling points is lower or
    # equal to the average sampling period
    if not nHatdag_s >= nK_min:
        strError = ('The minimum time between the sampling points must be ')
        strError = strError + ('lower or equal to the expected average ')
        strError = strError + ('sampling period ')
        raise ValueError(strError)

    # -----------------------------------------------------------------
    # Check if the maximum time between the sampling points is higher or
    # equal to the average sampling period
    if not nK_max >= nHatdag_s:
        strError = ('The maximum time between the sampling points must be ')
        strError = strError + ('higher or equal to the expected average ')
        strError = strError + ('sampling period ')
        raise ValueError(strError)

    # -----------------------------------------------------------------
    # Check if the signal representation sampling frequency is compatible
    # with the sampling period
    if np.round(Tg * fR) != (Tg * fR):
        strError = ('The chosen sampling grid period is incompatible with ')
        strError = strError + ('the signals representation sampling ')
        strError = strError + ('frequency')
        raise ValueError(strError)

    # -----------------------------------------------------------------
    return


# =================================================================
# Compute the real parameters of the sampling patterns
# =================================================================
def _computeRealParam(dAcqConf, dSig):

    # Get the configuration

    # nPatts    -  the number of patterns to be generated
    # bMute     -  mute the conole output flag
    # tTau      -  time of sampling patterns
    # Tg        -  sampling grid period
    # fSamp     -  the average sampling frequency
    # iSigma    -  sigma parameter
    # tMin      -  minimum time betweeen sampling points
    # tMax      -  maximum time between sampling points
    (nPatts,
     bMute,
     tTau,
     Tg,
     fSamp,
     iSigma,
     tMin,
     tMax) = _getConf(dAcqConf, dSig)

    # Calculate the number of grid points in the sampling period
    nK_g = math.floor(tTau / Tg)

    # Calculate the real time of sampling patterns
    tHatTau = nK_g * Tg

    # Calculate the expected number of sampling points in a pattern
    nHatKdag_s = int(round(tHatTau * fSamp))

    # Calculate the expected average sampling frequency
    fHatdag_s = nHatKdag_s / tHatTau

    # Calculate the expected average sampling period
    tHatT_s = 1 / fHatdag_s

    # Calculate the expected average sampling period and recalculate it to
    # the grid
    nHatdag_s = int(math.ceil(1 / (fHatdag_s * Tg)))

    # Minimum time between the sampling points as the number of grid:
    if np.isnan(tMin):
        nK_min = 1
    else:
        nK_min = int(math.ceil(tMin / Tg))
    tHatMin = nK_min * Tg   # The real minimum time between sampling points

    # Maximum time between the sampling points as the number of grid:
    if np.isnan(tMax):
        nK_max = np.inf
    else:
        nK_max = int(math.floor(tMax/Tg))
    tHatMax = nK_max * Tg   # The real maximum time between sampling points

    # -----------------------------------------------------------------
    return (nK_g,        # the number of grid points in the sampling period
            tHatTau,     # the real time of sampling patterns
            nHatKdag_s,  # the expected number of sampling points in a pattern
            fHatdag_s,   # the expected average sampling frequency
            nHatdag_s,   # the expected average sampling period (as grid pts)
            tHatT_s,     # the expected average sampling period
            nK_min,      # min t between the samp pts as the number of grid pts
            nK_max,      # max t between the samp pts as the number of grid pts
            tHatMin,     # the real minimum time between sampling points
            tHatMax)     # the real maximum time between sampling points


# =================================================================
# Print the configuration to the console
# =================================================================
def _printConf(dAcqConf, dSig):

    # -----------------------------------------------------------------
    # Get the configuration

    # nPatts    -  the number of patterns to be generated
    # bMute     -  mute the conole output flag
    # tTau      -  time of sampling patterns
    # Tg        -  sampling grid period
    # fSamp     -  the average sampling frequency
    # iSigma    -  sigma parameter
    # tMin      -  minimum time betweeen sampling points
    # tMax      -  maximum time between sampling points
    (nPatts,
     bMute,
     tTau,
     Tg,
     fSamp,
     iSigma,
     tMin,
     tMax) = _getConf(dAcqConf, dSig)

    # -----------------------------------------------------------------
    # Get the representation sampling frequency of signals to be sampled
    # and the time of the signals
    (_, fR, tS) = _getSigs(dSig)

    # -----------------------------------------------------------------
    # Compute the real parameters of the sampling patterns

    # nK_g        -  the number of grid points in the sampling period
    # tHatTau     -  the real time of sampling patterns
    # nHatKdag_s  -  the expected number of sampling points in a pattern
    # fHatdag_s,  -  the expected average sampling frequency
    # nHatdag_s,  -  the expected average sampling period (as grid pts)
    # tHatT_s,    -  the expected average sampling period
    # nK_min      -  min t between the samp pts as the number of grid pts
    # nK_max      -  max t between the samp pts as the number of grid pts
    # tHatMin     -  the real minimum time between sampling points
    # tHatMax     -  the real maximum time between sampling points
    (nK_g,
     tHatTau,
     nHatKdag_s,
     fHatdag_s,
     nHatdag_s,
     tHatT_s,
     nK_min,
     nK_max,
     tHatMin,
     tHatMax) = _computeRealParam(dAcqConf, dSig)

    #----------------------------------------------------------------------
    # Print the configuration if the 'mute' flag is not set
    if bMute == 0:

        # Print out the header of the signal generator
        rxcs.console.progress('Signal sampling', 'Nonuniform sampler (ANGIE)')

        # - - - - - - - - - - - - - - - - - - -
        # Print the time of patterns
        rxcs.console.bullet_param('patterns time', tHatTau, '-', 'seconds')
        if tHatTau != tTau:
            rxcs.console.param('requested patterns time', tTau, '-', 'seconds')

        # - - - - - - - - - - - - - - - - - - -
        # Print the grid period
        rxcs.console.bullet_param('grid period', Tg, '-', 'seconds')
        rxcs.console.param('the number of grid points', nK_g, '-', '')

        # - - - - - - - - - - - - - - - - - - -
        # The expected average sampling frequency
        rxcs.console.bullet_param('the expected average samp. freq',
                                  fHatdag_s, '-', 'Hz')
        if fHatdag_s != fSamp:
            rxcs.console.param('requested average samp. freq.',
                               fSamp, '-', 'Hz')

        rxcs.console.param('the number of sampling points',
                           nHatKdag_s, '-', '')

        rxcs.console.param('the expected average samp. period',
                           tHatT_s, '-', 'seconds')

        # - - - - - - - - - - - - - - - - - - -
        # The minimum time between sampling points
        if not np.isnan(tMin):
            rxcs.console.bullet_param('the min time between sampling points',
                                      tHatMin, '-', 'seconds')
            rxcs.console.param('which corresponds to',
                               nK_min, '-', 'grid points')
            if tMin != tHatMin:
                rxcs.console.param('the requested min time',
                                   tMin, '-', 'seconds')

        # - - - - - - - - - - - - - - - - - - -
        # The maximum time between sampling points
        if not np.isnan(tMax):
            rxcs.console.bullet_param('the max time between sampling points',
                                      tHatMax, '-', 'seconds')
            rxcs.console.param('which corresponds to ',
                               nK_max, '-', 'grid points')
            if tMax != tHatMax:
                rxcs.console.param('the requested max time',
                                   tMax, '-', 'seconds')

        # - - - - - - - - - - - - - - - - - - -
        # Information about the computations start
        tStart = rxcs.console.module_progress('signal sampling starts!!!')

    #----------------------------------------------------------------------
    else:   # <- the output was muted
        tStart = np.nan

    #----------------------------------------------------------------------
    return tStart






