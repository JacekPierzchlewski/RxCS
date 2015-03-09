"""
This a nonuniform sampler with additive random sampling (ARS) sampling scheme. |br|

The modules samples the given signals nonuniformly. |br|
The sampling aptterns are generated using ARS scheme.

The used ARS patterns generator is described further in
"Generation and Analysis of Constrained Random Sampling Patterns",
available in arXiv: http://arxiv.org/abs/1409.1002

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0  | 29-JAN-2015 : * Initial version. |br|
    1.1  | 9-MAR-2015 :  * Observation matrices are grouped in a list, not is a 3D Numpy array |br|

*License*:
    BSD 2-Clause
"""

from __future__ import division
import math
import rxcs
import numpy as np


def main(dAcqConf, dSig):
    """
    This the main function of the sampler. |br|

    Fields in the configuration dictionary (dAcqConf):

    - a. **bMute** (*int*): mute the console output from the generator
                            NOT REQUIRED, default = 0

    - b. **nPatts** (*int*): the number of patterns to be generateds
                             NOT REQUIRED, if not given equal to the number of signals to be sampled

    - c. **tTau** (*float*): time of patterns
                             NOT REQUIRED, if not given equal to the time of signals to be sampled

    - d. **Tg** (*float*): paterns sampling grid

    - e. **fSamp** (*float*): requested sampling frequency

    - f. **iSigma** (*float*): variance of Gaussian random process used by the pattern generator
                               NOT REQUIRED, default = 1


    Required fields in the dictionary with signals to be sampled (dSig):

    - a. **mSig** (*numpy array 2D*): 2D array with signals, one signal p. row

    - b. **fR** (*float*): signals representation sampling frequency

    - c. **tS** (*float*): time of signals


    Fields in the output dictionary (dObSig):

    WARNING: Due to different number of sampling points in patterns generated with ARS scheme,
             the matrices mObSig, mPatts, mPattsT and mPattsRep may contain NaN entries, which
             should be ignored.

    - a. **mObSig** (*numpy array 2D*): 2D array with observed signals, one signal p. row

    - b. **mPatts** (*numpy array 2D*): 2D array with sampling patterns, represented as indices of sampling grid points
                                        one signal pattern p. row

    - c. **mPattsT** (*numpy array 2D*): 2D array with sampling patterns, represented as time moments
                                         one signal pattern p. row

    - d. **mPattsRep** (*numpy array 2D*): 2D array with sampling patterns, represented as indices of signal representation points
                                           one signal pattern p. row

    - e. **lPhi** (*list*): list with observation matrices

    - f. **Tg** (*float*): the grid period of sampling patterns

    - g. **nK_g** (*int*): the number of grid points in a sampling pattern

    - h. **tTau_real** (*float*): the real time of sampling patterns

    - i. **nK_s** (*int*): the expected number of sampling points in a pattern

    - j. **f_s** (*float*): the expected average sampling frequency

    - k. **nT** (*int*): the expected average sampling period (represented as the number sampling grid points)

    - l. **tT_s** (*float*): the expected average sampling period

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
    # Generate the observation matrices
    # =================================================================
    lPhi = _generObser(mPattsRep, dAcqConf, dSig)

    # =================================================================
    # Generate the output dictionary
    # =================================================================
    dObSig = _generateOutput(dAcqConf, dSig,
                             mObSig,
                             mPatts, mPattsRep, mPattsT,
                             lPhi)

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
    # Check and get the configuration from the configuration dictionary

    # bMute     -  mute the conole output flag
    # tTau      -  time of sampling patterns
    # Tg        -  sampling grid period
    # fSamp     -  the average sampling frequency
    # iSigma    -  sigma parameter
    (_,
     bMute,
     tTau,
     Tg,
     fSamp,
     iSigma) = _getConf(dAcqConf)

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
    (nPatts,
     nK_g,
     tHatTau,
     nHatKdag_s,
     fHatdag_s,
     _,
     tHatT_s) = _computeRealParam(dAcqConf, dSig)

    # -----------------------------------------------------------------
    # Compute the number of signal representation points which equals
    # one grid point
    iGridvsRep = int(np.round((Tg * fR)))

    #----------------------------------------------------------------------
    # Print the configuration if the 'mute' flag is not set
    if bMute == 0:

        # Print out the header of the sampler
        rxcs.console.progress('Signal sampling', 'Nonuniform sampler (ARS)')

        # - - - - - - - - - - - - - - - - - - -
        # The number of signals to be sampled
        rxcs.console.bullet_param('the number of signals to be sampled',
                                  nPatts, '-', '')

        # - - - - - - - - - - - - - - - - - - -
        # Print the time of patterns
        rxcs.console.bullet_param('patterns time', tHatTau, '-', 'seconds')
        if not np.isnan(tTau) and tHatTau != tTau:
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

        rxcs.console.param('the expected number of sampling points',
                           nHatKdag_s, '-', '')

        rxcs.console.param('the expected average samp. period',
                           tHatT_s, '-', 'seconds')

        # - - - - - - - - - - - - - - - - - - -
        # The sigma parameter
        rxcs.console.bullet_param('the sigma parameter', iSigma, ' ', '')

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
    # Get the grid period from the sampler configuration dictionary

    # Tg        -  sampling grid period
    (_,
     _,
     _,
     Tg,
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
    (nPatts,
     nK_g,
     tTau_real,
     nK_s,
     _,
     nT,
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
    if (tTau_real - tS) > tS/1e12:
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
    # Get the average sampling frequencyparamet
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
    return (nPatts,    # the number of patterns to be generated
            bMute,     # mute the conole output flag
            tTau,      # the time of sampling patterns
            Tg,        # the sampling grid period
            fSamp,     # the average sampling frequency
            iSigma)    # the sigma parameter


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
    """

    # Get the configuration from the configuration dictionary

    # nPatts    -  the number of patterns
    # tTau      -  time of sampling patterns
    # Tg        -  sampling grid period
    # fSamp     -  the average sampling frequency
    (nPatts,
     _,
     tTau,
     Tg,
     fSamp,
     _) = _getConf(dAcqConf)

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

    # -----------------------------------------------------------------
    return (nPatts,      # the number of patterns
            nK_g,        # the number of grid points in the sampling pattern
            tTau_real,   # the real time of sampling patterns
            nK_s,        # the expected number of sampling points in a pattern
            f_s,         # the expected average sampling frequency
            nT,          # the expected average sampling period (as grid pts)
            tT_s)        # the expected average sampling period


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
     iSigma) = _getConf(dAcqConf)

    # -----------------------------------------------------------------
    # Get the representation sampling frequency of signals to be sampled
    (mSig, _, fR, _) = _getSigs(dSig)
    (_, nSamps) = mSig.shape          # Get the number of samples in signals

    # -----------------------------------------------------------------
    # Compute the real parameters of the sampling patterns

    # nPatts      -  the number of patterns to be generated
    # nK_g        -  the number of grid points in the sampling pattern
    # tTau_real   -  the real time of sampling patterns
    # nK_s        -  the expected number of sampling points in a pattern
    # nT          -  the expected average sampling period (as grid pts)
    (nPatts,
     nK_g,
     tTau_real,
     nK_s,
     _,
     nT,
     _) = _computeRealParam(dAcqConf, dSig)

    # --------------------------------------------------------------
    # Generate all the needed sampling patterns
    mPatts = np.ones((nPatts, nK_s), dtype='float64')   # Allocate the matrix for all the sampling patterns
    iSMaxPatt = 0   # Reset the max size of a pattern

    for inxP in np.arange(nPatts):   #<- loop over all patterns

        # ------------------------------------------
        # Generate a vector with a sampling pattern
        vPattern = _ars_engine(nK_s, nT, nK_g, iSigma)

        # --------------------------------------------------------------
        # Adjust the sampling pattern or a matrix with patterns
        (iS_v,) = vPattern.shape             # Get the size of the generated pattern
        iSMaxPatt = max((iS_v, iSMaxPatt))   # Update the max size of a pattern
        (iR_m, iC_m) = mPatts.shape          # Get the number of rows and columns in the matrix with patterns

        # Check the inequalities between matrix with vectors and the current vector with a pattern
        if iS_v < iC_m:     # <- the size of a generated pattern is lower than the
                            #    number of columns in the storage matrix

            iEmpty = iC_m - iS_v  # Calculate the size of empty space in the pattern

            vPatch = np.nan*np.ones(iEmpty)   # Update the pattern (fill up the empty spaces with a patch of -1)
            vPattern = np.hstack((vPattern, vPatch))   #

        elif iS_v > iC_m:   # <- the size of a generated pattern is higher than the number of columns in the storage matrix

            iEmpty = iS_v - iC_m   # The size of empty space in the storage matrix
            mPatch = np.nan*np.ones(iR_m, iEmpty)   # Update the storage matrix
            mPatts = np.hstack((mPatts, mPatch))
        # --------------------------------------------------------------

        mPatts[inxP, :] = vPattern  # Store the generated pattern

    vInx = range(0, iSMaxPatt)    # Clip the matrix with patterns
    mPatts = mPatts[:, vInx]      # ^

    # The patterns engine generates patterns in range  <1 ; N>, where
    # N is the number of possible positions of a sampling points.
    # Because Numpy indexes arrays from 0, the patterns should be represented
    # in range from <0 ; N-1>
    mPatts = mPatts - 1

    # --------------------------------------------------------------
    # Recalculate the patterns to the signal representation frequency

    # Compute the number of signal representation points which equals
    # one grid point
    iGridvsRep = int(np.round((Tg * fR)))
    mPattsRep = iGridvsRep * mPatts

    # --------------------------------------------------------------
    # Recalculate the patterns to the time moments

    # Get the time vector of the original signal (if it is given)
    # and the first sample
    if 'vTSig' in dSig:
        vTSig = dSig['vTSig']
    else:
        vTSig = (1 / fR) * np.arange(int(np.round(tTau_real*fR)))

    vTSig = np.hstack((vTSig, np.nan))

    # Generate matrix with patterns where NaN is change to inxex of NaN in vTSig
    mPattsRep_ = mPattsRep.copy()
    (iTPoints, ) = vTSig.shape                        # Get the number of points in the time vector
    mPattsRep_[np.isnan(mPattsRep)] = iTPoints - 1    # Change nan into pointer to nan

    # Generate patterns as time moments
    mPattsT = vTSig[mPattsRep_.astype(int)]

    # --------------------------------------------------------------
    return (mPatts, mPattsRep, mPattsT)



# =================================================================
# ARS engine
# =================================================================
def _ars_engine(nK_s, nT, K_g, sigma):

    # -----------------------------------------------------------------
    # Allocate the vector for the sampling points
    vPattern = np.nan*np.zeros(2*nK_s)

    # Reset the index of a correct sampling time point
    hatk = 0

    # Reset the current index of the grid
    n_hatk = 0

    # -----------------------------------------------------------------
    # Draw all time points
    for unused in range(1, nK_s+1):

        # Draw the current time point
        x_k = np.random.randn()
        nstar_hatk = \
            round(n_hatk + nT + np.sqrt(sigma) * x_k * nT)

        # Store the time point in the vector,
        # if it is somewhere in the sampling time due
        # and was not drawn yet
        if nstar_hatk > 0 and nstar_hatk <= K_g:

            # Store the time point
            n_hatk = nstar_hatk
            vPattern[hatk] = n_hatk
            hatk = hatk + 1

        # Check if the whole vector vPattern was
        # already filled up. If so, make it longer
        nSiz = vPattern.size
        if hatk == nSiz:
            vExtraSpace = np.nan*np.zeros(nK_s)
            vPattern = np.hstack((vPattern, vExtraSpace))

    # -----------------------------------------------------------------
    # Clear the pattern
    vPattern = vPattern[np.equal(np.isnan(vPattern), False)]

    # -----------------------------------------------------------------
    # Remove repeated moments
    vPattern = np.unique(vPattern)

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
    mSig_ = np.hstack((mSig, np.nan*np.zeros((nSigs,1))))   # Add nan to the end of signals

    # Generate matrix with patterns where NaN is changed to index of NaN in mSig_
    mPattsRep_ = mPattsRep.copy()
    (_, nSamps) = mSig.shape   # Get the number of samples in the signals
    mPattsRep_[np.isnan(mPattsRep)] = nSamps         # Change nan into pointer to nan

    mObSig = (mSig_[np.arange(nSigs), mPattsRep_.T.astype(int)]).T  # Generate correct observation signals
    # -----------------------------------------------------------------

    return mObSig


# =================================================================
# Generate the observation matrix
# =================================================================
def _generObser(mPattsRep, dAcqConf, dSig):
    """
    This function generates the observation matrices.

    Args:
        mPattsRep (matrix): the sampling patterns (signal rep. sampling points)
        dAcqConf (dictionary): dictionary with configuration for the sampler
        dSig (dictionary): dictionary with the signals to be sampled

    Returns:
        lPhi (list): list with observation matrices
    """

    (_, nMaxSamp) = mPattsRep.shape   # Get the maximum number of samples in all the sampling patterns

    # -----------------------------------------------------------------
    # Get the representation sampling frequency of signals to be sampled
    # and the time of signals to be sampled
    (_, _, fR, tS) = _getSigs(dSig)

    # Calculate the number of representation samples in the signals
    nSmp = int(round(tS * fR))

    # -----------------------------------------------------------------
    # Compute the real parameters of the sampling patterns

    # nPatts      -  the number of patterns to be generated
    (nPatts,
     _,
     _,
     _,
     _,
     _,
     _) = _computeRealParam(dAcqConf, dSig)

    # -----------------------------------------------------------------
    lPhi = []    # Start the list with the observation matrices

    # Generate the observation matrices
    for inxPat in np.arange(nPatts):  # <- loop over all observation matrices

        # Get the current pattern
        vPatts = mPattsRep[inxPat, :]
        vPatts = vPatts[np.invert(np.isnan(vPatts))]   # Clean the pattern
        nPatSiz  = vPatts.size          # Size of the pattern

        # Generate the observation matrix for the current sampling pattern
        mPhi = np.zeros((nPatSiz, nSmp))  # Allocat the observation matrix
        inxRow = 0                        # Reset index of a row
        for inxCol in vPatts:   # <- loop over all sampling points in a pattern
            mPhi[inxRow, int(inxCol)] = 1
            inxRow = inxRow + 1
        lPhi.append(mPhi.copy())   # Add the matrix to the list

    # -----------------------------------------------------------------
    return lPhi


# =================================================================
# Generate the output dictionary
# =================================================================
def _generateOutput(dAcqConf, dSig, mObSig, mPatts, mPattsRep, mPattsT, lPhi):
    """
    This function generates the output dictionary.

    Args:
        dAcqConf (dictionary): dictionary with configuration for the sampler
        dSig (dictionary): dictionary with the signals to be sampled
        mObSig (matrix):  the observed signals
        mPatts (matrix): the sampling patterns (grid indices)
        mPattsRep (matrix): the sampling patterns (signal rep. sampling points)
        mPattsT (matrix): the sampling patterns (time moments)
        lPhi (list): list with observation matrices

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
     _) = _getConf(dAcqConf)

    # -----------------------------------------------------------------
    # Compute the real parameters of the sampling patterns

    # nK_g        -  the number of grid points in a sampling pattern
    # tTau_real   -  the real time of sampling patterns
    # nK_s        -  the expected number of sampling points in a pattern
    # f_s         -  the expected average sampling frequency
    # nT          -  the expected average sampling period (as grid pts)
    # tT_s        -  the expected average sampling period
    (_,
     nK_g,
     tTau_real,
     nK_s,
     f_s,
     nT,
     tT_s) = _computeRealParam(dAcqConf, dSig)

    # -----------------------------------------------------------------
    # Initialize the output dictionary
    dObSig = {}

    # - - - - - - - - - - - - - - - - - -

    dObSig['mObSig'] = mObSig   # The observed signals

    # - - - - - - - - - - - - - - - - - -

    dObSig['mPatts'] = mPatts         # The sampling patterns (grid indices)

    dObSig['mPattsT'] = mPattsT       # The sampling patterns (time moments)

    dObSig['mPattsRep'] = mPattsRep   # The sampling patterns (signal
                                      # representation sampling points)

    # - - - - - - - - - - - - - - - - - -

    dObSig['lPhi'] = lPhi           # The observation matrices

    # - - - - - - - - - - - - - - - - - -

    dObSig['Tg'] = Tg       # The grid period

    dObSig['nK_g'] = nK_g   # The number of grid points in a sampling pattern

    dObSig['tTau_real'] = tTau_real   # The real time of sampling patterns

    # - - - - - - - - - - - - - - - - - -

    dObSig['nK_s'] = nK_s  # The expected number of sampling points in a pattern

    dObSig['f_s'] = f_s    # The expected average sampling frequency

    dObSig['nT'] = nT      # The expected average sampling period (as grid pts)

    dObSig['tT_s'] = tT_s  # The expected average sampling period

    # - - - - - - - - - - - - - - - - - -

    return dObSig
