"""
This a nonuniform sampler with ANGIE scheme. |br|

The modules samples the given signals nonuniformly. |br|
THe sampling aptterns are generated using ANGIE scheme.

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    0.1  | 26-MAY-2014 : * Initial version. |br|
    0.2  | 27-MAY-2014 : * Docstrings added. |br|

*License*:
    BSD 2-Clause
"""

from __future__ import division
import sys
import math
import time
import rxcs
import numpy as np


def main(dAcqConf,dSig):
    """
    This the main function of the sampler. |br|

    Args:
        dAcqConf (dictionary): dictionary with configuration for the sampler
        dSig (dictionary): dictionary with the signals to be sampled


    Returns:
        dObSig (dictionary): the observed signals and paramters of sampling
    """

    # =================================================================
    # Check the configuration and print it to the console
    # =================================================================

    # Print the configuration to the console
    tStart = _printConf(dAcqConf, dSig)

    # - - - - - - - - - - - - - - - - - - -

    # Check if the configuration for the sampler make sense
    _checkConf(dAcqConf, dSig)

    # - - - - - - - - - - - - - - - - - - -

    # =================================================================
    # Generate the sampling patterns
    # =================================================================
    (mPatts, mPattsRep, mPattsT) = _generate_patterns(dAcqConf, dSig)

    # =================================================================
    # Sample the signals
    # =================================================================
    mObSig = _sample(mPattsRep, dSig)

    # =================================================================
    # Generate the output dictionary
    # =================================================================
    dObSig = _generateOutput(dAcqConf, dSig,
                             mObSig,
                             mPatts, mPattsRep, mPattsT)

    # =================================================================
    # Signal sampling is done!
    # =================================================================
    if not np.isnan(tStart):   # <-tStart is nan = console output is off
        rxcs.console.module_progress_done(tStart)

    return dObSig


# =================================================================
# Print the configuration to the console
# =================================================================
def _printConf(dAcqConf, dSig):
    """
    This function prints the configuration of the sampler to the console.

    Args:
        dAcqConf (dictionary): dictionary with configuration for the sampler
        dSig (dictionary): dictionary with the signals to be sampled

    Returns:
        tStart (float): time stamp of the beginning of sampling
    """

    # -----------------------------------------------------------------
    # Check and get the configuration from the configuration directory

    # bMute     -  mute the conole output flag
    # tTau      -  time of sampling patterns
    # Tg        -  sampling grid period
    # fSamp     -  the average sampling frequency
    # iSigma    -  sigma parameter
    # tMin      -  minimum time betweeen sampling points
    # tMax      -  maximum time between sampling points
    (_,
     bMute,
     tTau,
     Tg,
     fSamp,
     iSigma,
     tMin,
     tMax) = _getConf(dAcqConf)

    # -----------------------------------------------------------------
    # Get the representation sampling frequency of signals to be sampled
    (_, _, fR, _) = _getSigs(dSig)

    # -----------------------------------------------------------------
    # Compute the real parameters of the sampling patterns

    # nPatts      -  the number of patterns to be generated
    # nK_g        -  the number of grid points in the sampling pattern
    # tHatTau     -  the real time of sampling patterns
    # nHatKdag_s  -  the expected number of sampling points in a pattern
    # fHatdag_s,  -  the expected average sampling frequency
    # tHatT_s,    -  the expected average sampling period
    # nK_min      -  min t between the samp pts as the number of grid pts
    # nK_max      -  max t between the samp pts as the number of grid pts
    # tHatMin     -  the real minimum time between sampling points
    # tHatMax     -  the real maximum time between sampling points
    (nPatts,
     nK_g,
     tHatTau,
     nHatKdag_s,
     fHatdag_s,
     _,
     tHatT_s,
     nK_min,
     nK_max,
     tHatMin,
     tHatMax) = _computeRealParam(dAcqConf, dSig)

    # -----------------------------------------------------------------
    # Compute the number of signal representation points which equals
    # one grid point
    iGridvsRep = int(np.round((Tg * fR)))

    #----------------------------------------------------------------------
    # Print the configuration if the 'mute' flag is not set
    if bMute == 0:

        # Print out the header of the signal generator
        rxcs.console.progress('Signal sampling', 'Nonuniform sampler (ANGIE)')

        # - - - - - - - - - - - - - - - - - - -
        # The number of signals to be sampled
        rxcs.console.bullet_param('the number of signals to be sampled',
                                  nPatts, '-', '')

        # - - - - - - - - - - - - - - - - - - -
        # Print the time of patterns
        rxcs.console.bullet_param('patterns time', tHatTau, '-', 'seconds')
        if tHatTau != tTau:
            rxcs.console.param('requested patterns time', tTau, '-', 'seconds')

        # - - - - - - - - - - - - - - - - - - -
        # Print the grid period
        rxcs.console.bullet_param('grid period', Tg, '-', 'seconds')
        rxcs.console.param('the number of grid points', nK_g, '-', '')

        rxcs.console.param('the signal representation period', 1/fR, '-', '')
        rxcs.console.param('one grid points is',
                           iGridvsRep, '-', 'signal samples')

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
        # The sigma parameter
        rxcs.console.bullet_param('the sigma parameter', iSigma, ' ', '')

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
    else:   # <- the output was muted, no time stamp of the start is required
        tStart = np.nan

    #----------------------------------------------------------------------
    return tStart


# =================================================================
# Check if the configuration for the sampler make sense
# =================================================================
def _checkConf(dAcqConf, dSig):
    """
    This function checks if the configuration given to the sampler
    is correct.

    Args:
        dAcqConf (dictionary): dictionary with configuration for the sampler
        dSig (dictionary): dictionary with the signals to be sampled

    Returns:
        nothing
    """

    # -----------------------------------------------------------------
    # Get the grid period from the sampler configuration directory

    # Tg        -  sampling grid period
    (_,
     _,
     _,
     Tg,
     _,
     _,
     _,
     _) = _getConf(dAcqConf)

    # -----------------------------------------------------------------
    # Get the representation sampling frequency of signals to be sampled
    # and the time of the signals
    (_, nSigs, fR, tS) = _getSigs(dSig)

    # -----------------------------------------------------------------
    # Compute the real parameters of the sampling patterns

    # nPatts      -  the number of patterns to be generated
    # nK_g        -  the number of grid points in the sampling pattern
    # tTau_real   -  the real time of sampling patterns
    # nK_s        -  the expected number of sampling points in a pattern
    # nT,         -  the expected average sampling period (as grid pts)
    # nK_min      -  min t between the samp pts as the number of grid pts
    # nK_max      -  max t between the samp pts as the number of grid pts
    (nPatts,
     nK_g,
     tTau_real,
     nK_s,
     _,
     nT,
     _,
     nK_min,
     nK_max,
     _,
     _) = _computeRealParam(dAcqConf, dSig)

    # -----------------------------------------------------------------
    # Check if the number of patterns to be generated is equal to the
    # number of signals to be sampled
    if nPatts != nSigs:
        strError = ('The number of sampling patterns is different than ')
        strError = strError + ('the number of signals to be sampled')
        raise ValueError(strError)

    # -----------------------------------------------------------------
    # Check if the real time of patterns is higher than 0
    if not tTau_real > 0:
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
    if not nK_s > 0:
        strError = ('The expected number of sampling points in patterns ')
        strError = strError + ('must be higher than zero')
        raise ValueError(strError)

    # -----------------------------------------------------------------
    # Check if the time of patterns is equal to the time of signals to be
    # sampled
    if tTau_real != tS:
        strError = ('The real time of patterns is different than the time ')
        strError = strError + ('of signals to be sampled')
        raise ValueError(strError)

    # -----------------------------------------------------------------
    # Check if the expected number of sampling points is lower or equal
    # to the number of grid points
    if not nK_g >= nK_s:
        strError = ('The real number of grid points in patterns must be ')
        strError = strError + ('higher or equal to the number of expected ')
        strError = strError + ('sampling points')
        raise ValueError(strError)

    # -----------------------------------------------------------------
    # Check if the minimum time between the sampling points is lower or
    # equal to the average sampling period
    if not nT >= nK_min:
        strError = ('The minimum time between the sampling points must be ')
        strError = strError + ('lower or equal to the expected average ')
        strError = strError + ('sampling period ')
        raise ValueError(strError)

    # -----------------------------------------------------------------
    # Check if the maximum time between the sampling points is higher or
    # equal to the average sampling period
    if not nK_max >= nT:
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
# Check the configuration dict. and get the configuration from it
# =================================================================
def _getConf(dAcqConf):
    """
    This function checks if all the needed configuration fields are in
    the configuration dictionary and gets these configuration fields.

    Args:
        dAcqConf (dictionary): dictionary with configuration for the sampler

    Returns:
        nPatts (float):    the number of patterns to be generated
        bMute (float):     mute the conole output flag
        tTau (float):      the time of sampling patterns
        Tg (float):        the sampling grid period
        fSamp (float):     the average sampling frequency
        iSigma (float):    the sigma parameter
        tMin (float):      minimum time between sampling patterns
        tMax (float):      maximum time between sampling patterns
    """
    # -----------------------------------------------------------------
    # Get the number of patterns to be generated

    # Get the number of patterns from the configuraion
    if not 'nPatts' in dAcqConf:
        nPatts = np.nan
    else:
        nPatts = dAcqConf['nPatts']

    if not np.isnan(nPatts) and not nPatts > 0:
        strError = ('The number of patterns must be higher than zero')
        raise ValueError(strError)

    # -----------------------------------------------------------------
    # Get the mute flag
    if not 'bMute' in dAcqConf:
        bMute = 0
    else:
        bMute = dAcqConf['bMute']

    # -----------------------------------------------------------------
    # Get the time of patterns from the configuration
    if not 'tTau' in dAcqConf:
        tTau = np.nan
    else:
        tTau = dAcqConf['tTau']

    # The time of patterns must be higher than zero
    if not np.isnan(tTau) and not tTau > 0:
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
    # (if it was given)
    if not np.isnan(tMin) and not tMin > 0:
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
    # (if it was given)
    if not np.isnan(tMax) and not tMax > 0:
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
# Check the dictionary with signals to be sampled.
# Get the signals to be sampled and their parameters.
# =================================================================
def _getSigs(dSig):
    """
    This function checks if the dictionary with signals to be sampled
    contains all the needed fields. Then the function gets these fields.

    Args:
        dSig (dictionary): dictionary with the signals to be sampled

    Returns:
        mSig (matrix):  the matrix with signals to be sampled
        nSigs (float):  the number of signals to be sampled
        fR (float):     the signals representation sampling frequency
        tS (float):     time of the signals
    """

    # -----------------------------------------------------------------
    # Get the signals to be sampled and the number of signals to be sampled
    if not 'mSig' in dSig:
        strError = ('Dictionary with signals to be sampled does not contain ')
        strError = strError + ('signals')
        raise NameError(strError)
    else:
        mSig = dSig['mSig']
    (nSigs, _) = mSig.shape

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
            nSigs,  # the number of signals to be sampled
            fR,     # the signals representation sampling frequency
            tS)     # the signals time


# =================================================================
# Compute the real parameters of the sampling patterns
# =================================================================
def _computeRealParam(dAcqConf, dSig):
    """
    This function computes the 'real' (corrected) parameters of sampling.

    Args:
        dAcqConf (dictionary): dictionary with configuration for the sampler
        dSig (dictionary): dictionary with the signals to be sampled

    Returns:
        nPatts (float):    the number of patterns
        nK_g (float):      the number of grid points in the sampling pattern
        tTau_real (float): the real time of sampling patterns
        nK_s (float):      the expected number of sampling points in a pattern
        f_s (float):       the expected average sampling frequency
        nT (float):        the expected average sampling period (as grid pts)
        tT_s (float):      the expected average sampling period
        nK_min (float):    min t between the samp pts as the number of grid pts
        nK_max (float):    max t between the samp pts as the number of grid pts
        tMin_real (float): the real minimum time between sampling points
        tMax_real (float): the real maximum time between sampling points
    """

    # Get the configuration from the configuration directory

    # nPatts    -  the number of patterns
    # tTau      -  time of sampling patterns
    # Tg        -  sampling grid period
    # fSamp     -  the average sampling frequency
    # tMin      -  minimum time between sampling points
    # tMax      -  maximum time between sampling points
    (nPatts,
     _,
     tTau,
     Tg,
     fSamp,
     _,
     tMin,
     tMax) = _getConf(dAcqConf)

    # Get the number of signals from the dictionary with signals if the number
    # of patterns was not given in the sampler configuration dictionary
    if np.isnan(nPatts):
        if not 'nSigs' in dSig:
            strError = ('Dictionary with signals to be sampled does not ')
            strError = strError + ('contain information about the number of')
            strError = strError + ('signals')
            raise NameError(strError)
        else:
            nPatts = dSig['nSigs']

    # Get the time of signals from the dictionary with signals if the time
    # of patterns was not given in the sampler configuration dictionary
    if np.isnan(tTau):
        if not 'tS' in dSig:
            strError = ('Dictionary with signals to be sampled does not ')
            strError = strError + ('contain information about the time of ')
            strError = strError + ('the signals')
            raise NameError(strError)
        else:
            tTau = dSig['tS']

    # Calculate the number of grid points in the sampling period
    nK_g = math.floor(tTau / Tg)

    # Calculate the real time of sampling patterns
    tTau_real = nK_g * Tg

    # Calculate the expected number of sampling points in a pattern
    nK_s = int(round(tTau_real * fSamp))

    # Calculate the expected average sampling frequency
    f_s = nK_s / tTau_real

    # Calculate the expected average sampling period
    tT_s = 1 / f_s

    # Calculate the expected average sampling period and recalculate it to
    # the grid
    nT = int(math.ceil(1 / (f_s * Tg)))

    # Minimum time between the sampling points as the number of grid:
    if np.isnan(tMin):
        nK_min = 1
    else:
        nK_min = int(math.ceil(tMin / Tg))
    tMin_real = nK_min * Tg   # The real minimum time between sampling points

    # Maximum time between the sampling points as the number of grid:
    if np.isnan(tMax):
        nK_max = np.inf
    else:
        nK_max = int(math.floor(tMax/Tg))
    tMax_real = nK_max * Tg   # The real maximum time between sampling points

    # -----------------------------------------------------------------
    return (nPatts,      # the number of patterns
            nK_g,        # the number of grid points in the sampling pattern
            tTau_real,   # the real time of sampling patterns
            nK_s,        # the expected number of sampling points in a pattern
            f_s,         # the expected average sampling frequency
            nT,          # the expected average sampling period (as grid pts)
            tT_s,        # the expected average sampling period
            nK_min,      # min t between the samp pts as the number of grid pts
            nK_max,      # max t between the samp pts as the number of grid pts
            tMin_real,   # the real minimum time between sampling points
            tMax_real)   # the real maximum time between sampling points


# =================================================================
# Generate the patterns
# =================================================================
def _generate_patterns(dAcqConf, dSig):
    """
    This function generates the required number of sampling patterns.

    Args:
        dAcqConf (dictionary): dictionary with configuration for the sampler
        dSig (dictionary): dictionary with the signals to be sampled

    Returns:
        mPatts (matrix): the sampling patterns (grid indices)
        mPattsRep (matrix): the sampling patterns (signal rep. sampling points)
        mPattsT (matrix): the sampling patterns (time moments)
    """

    # -----------------------------------------------------------------
    # Get the configuration from the configuration dictionary

    # Tg        -  the sampling grid period
    # iSigma    -  sigma parameter
    (_,
     _,
     _,
     Tg,
     _,
     iSigma,
     _,
     _) = _getConf(dAcqConf)

    # -----------------------------------------------------------------
    # Get the representation sampling frequency of signals to be sampled
    (_, _, fR, _) = _getSigs(dSig)

    # -----------------------------------------------------------------
    # Compute the real parameters of the sampling patterns

    # nPatts      -  the number of patterns to be generated
    # nK_g        -  the number of grid points in the sampling pattern
    # nK_s        -  the expected number of sampling points in a pattern
    # nK_min      -  min t between the samp pts as the number of grid pts
    # nK_max      -  max t between the samp pts as the number of grid pts
    (nPatts,
     nK_g,
     _,
     nK_s,
     _,
     _,
     _,
     nK_min,
     nK_max,
     _,
     _) = _computeRealParam(dAcqConf, dSig)

    # --------------------------------------------------------------
    # Allocate the matrix for all the sampling patterns
    mPatts = np.ones((nPatts, nK_s), dtype='int64')

    # Generate all the needed sampling patterns
    for inxP in np.arange(nPatts):

        # ------------------------------------------
        # Generate a vector with a sampling pattern
        vPattern = _angie_engine(nK_s, nK_g, nK_min, nK_max, iSigma)
        # ------------------------------------------

        # Store the generated pattern
        mPatts[inxP, :] = vPattern

    # --------------------------------------------------------------
    # Recalculate the patterns to the signal representation frequency

    # Compute the number of signal representation points which equals
    # one grid point
    iGridvsRep = int(np.round((Tg * fR)))

    # Recalculate the sampling patterns from grid to signal representation
    # points
    if iGridvsRep != 1:
        mPattsRep = iGridvsRep * mPatts
    else:
        mPattsRep = mPatts.copy()
    mPattsRep = mPattsRep - 1

    # --------------------------------------------------------------
    # Recalculate the patterns to the time moments
    mPattsT = Tg * mPatts

    # --------------------------------------------------------------
    return (mPatts, mPattsRep, mPattsT)


# =================================================================
# ANGIE engine
# =================================================================
def _angie_engine(nK_s, K_g, K_min, K_max, sigma):
    """
    This function is the engine of ANGIE sampling generator.
    It generates one sampling pattern.

    Args:
        nK_s (float):  the number of sampling points in a pattern
        K_g (float):   the number of grid points in a pattern
        K_min (float): minimum distance between sampling points
        K_max (float): maximum distance between sampling points
        sigma (float): the sigma parameter

    Returns:
        vPattern (vector): vector with the sampling pattern
    """

    # Allocate the vector for the sampling points
    vPattern = np.nan*np.zeros(nK_s)

    # Reset the current sampling moment
    nk = 0

    # -----------------------------------------------------------------
    # Reset the minimum and maximum limits:

    # Reset the minimum the minimum limit
    nminus_k = 1

    # Reset the maximum limit
    nplus_k = K_g - K_min*(nK_s-1)

    # -----------------------------------------------------------------
    # Draw all the points
    for k in range(nK_s):    # <- Loop over all the expected points

        # -------------------------------------------------------------
        # The number of sampling points left
        nLeft = nK_s - k

        # -------------------------------------------------------------
        # Calculate the expected position of the sample:

        # Calculate the average sampling period for the rest of sampling
        # points (in the grid indices)
        nddag_k = round((K_g - nk) / (nLeft + 1))

        # Calculate the expected position (in the grid indices)
        Enk = nk + nddag_k

        # -------------------------------------------------------------
        # Distances between the expected position and the limits

        # Calculate distance to the minimum limit
        ndminus_k = abs(Enk - nminus_k)

        # Calculate distance to the maximum limit
        ndplus_k = nplus_k - Enk

        # Get the correct distance
        nd_k = min(ndminus_k, ndplus_k)

        # -------------------------------------------------------------
        # Draw the sampling point:

        # -------------------------------------------------------------
        # Soft start, if enabled
        # -------------------------------------------------------------
        # First sampling point is different, if soft start is enabled
        if k == 0:

            # Draw the sampling moment (uniformly)
            nk = math.ceil(np.random.rand()*nddag_k)
        # -------------------------------------------------------------
        # -------------------------------------------------------------

        else:
            # Draw Gaussian
            xk = np.random.randn()

            # Draw the sampling point
            nk = Enk + math.sqrt(sigma)*xk*nd_k
            nk = round(nk)

        # -------------------------------------------------------------
        # Check limits
        if nk < nminus_k:
            nk = nminus_k

        elif nk > nplus_k:
            nk = nplus_k

        # -------------------------------------------------------------
        # Store the drawn sampling point
        vPattern[k] = nk

        # -------------------------------------------------------------
        # Calculate the minimum and maximum limits:

        # Move the minimum limit forward (by the minimum distance)
        nminus_k = nk + K_min

        # Move the maximum limit forward
        nplus_k = K_g - K_min*(nLeft-2)

        nplus_k = min(nplus_k, nk + K_max)  # <- Add maximum limit (this line
                                            #    can be removed if there is no
                                            #    need for maximum limit)
                                            #
    # -----------------------------------------------------------------
    return vPattern


# =================================================================
# Sample the signals using the generated patterns
# =================================================================
def _sample(mPattsRep, dSig):
    """
    This function samples signals using the previously generated
    sampling patterns.

    Args:
        mPattsRep (matrix): the sampling patterns (signal rep. sampling points)
        dSig (dictionary): dictionary with the signals to be sampled

    Returns:
        mObSig (matrix):  the observed signals
    """

    # -----------------------------------------------------------------
    # Get the signals to be sampled and the number of signals to be sampled
    (mSig, nSigs, _, _) = _getSigs(dSig)

    # -----------------------------------------------------------------

    # Sample the signals
    mObSig = (mSig[np.arange(nSigs),mPattsRep.T]).T

    # -----------------------------------------------------------------
    return mObSig


# =================================================================
# Generate the output dictionary
# =================================================================
def _generateOutput(dAcqConf, dSig, mObSig, mPatts, mPattsRep, mPattsT):
    """
    This function generates the output dictionary.

    Args:
        dAcqConf (dictionary): dictionary with configuration for the sampler
        dSig (dictionary): dictionary with the signals to be sampled
        mObSig (matrix):  the observed signals
        mPatts (matrix): the sampling patterns (grid indices)
        mPattsRep (matrix): the sampling patterns (signal rep. sampling points)
        mPattsT (matrix): the sampling patterns (time moments)

    Returns:
        dObSig (dictionary): the observed signals and paramters of sampling
    """

    # -----------------------------------------------------------------
    # Get the sampling grid period from the configuration dictionary
    (_,
     _,
     _,
     Tg,
     _,
     _,
     _,
     _) = _getConf(dAcqConf)

    # -----------------------------------------------------------------
    # Compute the real parameters of the sampling patterns

    # nK_g        -  the number of grid points in a sampling pattern
    # tTau_real   -  the real time of sampling patterns
    # nK_s        -  the expected number of sampling points in a pattern
    # f_s         -  the expected average sampling frequency
    # nT          -  the expected average sampling period (as grid pts)
    # tT_s        -  the expected average sampling period
    # nK_min      -  min t between the samp pts as the number of grid pts
    # nK_max      -  max t between the samp pts as the number of grid pts
    # tMin_real   -  the real minimum time between sampling points
    # tMax_real   -  the real maximum time between sampling points
    (_,
     nK_g,
     tTau_real,
     nK_s,
     f_s,
     nT,
     tT_s,
     nK_min,
     nK_max,
     tMin_real,
     tMax_real) = _computeRealParam(dAcqConf, dSig)

    # -----------------------------------------------------------------
    # Initialize the output dictionary
    dObSig = {}

    # - - - - - - - - - - - - - - - - - -

    dObSig['mObSig'] = mObSig   # The observed signal

    # - - - - - - - - - - - - - - - - - -

    dObSig['mPatts'] = mPatts         # The sampling patterns (grid indices)

    dObSig['mPattsT'] = mPattsT       # The sampling patterns (time moments)

    dObSig['mPattsRep'] = mPattsRep   # The sampling patterns (signal
                                      # representation sampling points)

    # - - - - - - - - - - - - - - - - - -

    dObSig['Tg'] = Tg       # The grid period

    dObSig['nK_g'] = nK_g   # The number of grid points in a sampling pattern

    dObSig['tTau_real'] = tTau_real   # The real time of sampling patterns

    # - - - - - - - - - - - - - - - - - -

    dObSig['nK_s'] = nK_s   # The number of sampling points in a pattern

    dObSig['f_s'] = f_s   # The expected average sampling frequency

    dObSig['nT'] = nT     # The expected average sampling period (as grid pts)

    dObSig['tT_s'] = tT_s  # The expected average sampling period

    # - - - - - - - - - - - - - - - - - -

    dObSig['nK_min'] = nK_min   # Min t between the samp pts
                                # (as the number of grid pts)

    dObSig['nK_max'] = nK_max   # Max t between the samp pts
                                # (as the number of grid pts)

    dObSig['tMin_real'] = tMin_real   # The real minimum time between sampling
                                      # points

    dObSig['tMax_real'] = tMax_real   # The real maximum time between sampling
                                      # points

    # - - - - - - - - - - - - - - - - - -

    return dObSig
