"""
This a nonuniform sampler with externally acquired sampling scheme. |br|

The modules samples the given signals nonuniformly. |br|
The sampling patterns are taken from a file with sampling patterns
or from a dictionary given to the sampler. In particular the sampling
pattern may be uniform.

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    0.1  | 1-SEP-2014 : * Initial version. |br|

*License*:
    BSD 2-Clause
"""

from __future__ import division
import sys
import math
import time
import rxcs
import os.path
import cPickle
import numpy as np


def main(dAcqConf, dSig):
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

    # Read the configuration of the sampler
    (dConf) = _getConf(dAcqConf)

    # - - - - - - - - - - - - - - - - - - -

    # Print the configuration
    tStart = _printConf(dSig, dConf)

    # - - - - - - - - - - - - - - - - - - -

    # Check the configuration
    _checkConf(dAcqConf, dSig, dConf)

    # - - - - - - - - - - - - - - - - - - -

    # =================================================================
    # Get and process the sampling patterns
    # =================================================================
    (mPatts, mPattsRep, mPattsT) = _take_patterns(dAcqConf, dSig, dConf)

    # =================================================================
    # Sample the signals
    # =================================================================
    #mObSig = _sample(dConf, dSig)

    # =================================================================
    # Generate the observation matrices
    # =================================================================
    #m3Phi = _generObser(mPattsRep, dAcqConf, dSig)

    # =================================================================
    # Generate the output dictionary
    # =================================================================
    #dObSig = _generateOutput(dAcqConf, dSig,
                             #mObSig,
                             #mPatts, mPattsRep, mPattsT,
                             #m3Phi)

    # =================================================================
    # Signal sampling is done!
    # =================================================================
    if not np.isnan(tStart):   # <-tStart is nan = console output is off
        rxcs.console.module_progress_done(tStart)

    #return dObSig
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
        bMute (float):     mute the conole output flag
        bFile (float):     patterns from file flag (1-from file,
                                                    0-from an argument given as
                                                      a dictionary)

        strFile (string):  name of the file with patterns (if bFile == 1,
                                                           otherwise an empty
                                                           string)

        dPatts  (dict):    dictionary with sampling patterns

        iA    (float):     index of the first pattern to be used
                           (if not given in the configuration, then = 0)

        iB    (float):     index of the last pattern to be used
                           (if not given in the configuration, then = np.inf)

    """

    # -----------------------------------------------------------------
    # Get the mute flag
    if not 'bMute' in dAcqConf:
        bMute = 0
    else:
        bMute = dAcqConf['bMute']

    # -----------------------------------------------------------------
    # Check if the sampling patterns were given as a dicitonary, or should be
    # taken form a separate file
    if not 'dPatts' in dAcqConf:
        strError = ('Dictionary with a source of sampling patterns (dPatts) ')
        strError = strError + ('is not given in the configuration')
        raise NameError(strError)

    else:
        dPatts = dAcqConf['dPatts']

    # Read the file with sampling patterns if needed and mark the ]
    # dFile flag as needed
    if type(dPatts) == str:
        bFile = 1
        strFile = dPatts
        dPatts = _readFile(strFile)

    elif type(dPatts) == dict:
        bFile = 0
        strFile = ''

    else:
        strError = ('Source of sampling patterns (dPatts) must be either ')
        strError = strError + ('a string or a dictionary')
        raise NameError(strError)

    # -----------------------------------------------------------------
    # Take the indices of first and last sampling pattens to be used
    if not 'iA' in dAcqConf:
        iA = 0
    else:
        iA = dAcqConf['iA']

    if not 'iB' in dAcqConf:
        iB = np.inf
    else:
        iB = dAcqConf['iB']

    # -----------------------------------------------------------------
    # Create the configuration dictionary
    dConf = {}
    dConf['bMute'] = bMute       # mute the conole output flag
    dConf['bFile'] = bFile       # patterns from file flag
    dConf['strFile'] = strFile   # name of the file with patterns
    dConf['dPatts'] = dPatts     # dictionary with sampling patterns
    dConf['iA'] = iA             # index of the first pattern to be used
    dConf['iB'] = iB             # index of the last pattern to be used

    # -----------------------------------------------------------------
    return (dConf)


# =================================================================
# Print the configuration to the console
# =================================================================
def _printConf(dSig, dConf):
    """
    This function prints the configuration of the sampler to the console.

    Args:
        dAcqConf (dictionary): dictionary with configuration for the sampler
        dSig (dictionary): dictionary with the signals to be sampled

    Returns:
        tStart (float): time stamp of the beginning of sampling
    """

    # -----------------------------------------------------------------
    # Get the configuration fields from the configuration dictionary
    bMute = dConf['bMute']       # mute the conole output flag
    bFile = dConf['bFile']       # patterns from file flag
    strFile = dConf['strFile']   # name of the file with patterns
    dPatts = dConf['dPatts']     # dictionary with sampling patterns
    iA = dConf['iA']             # index of the first pattern to be used
    iB = dConf['iB']             # index of the last pattern to be used

    # -----------------------------------------------------------------
    # Get the parameters of the sampling patterns
    # nPatts    -  the number of patterns
    # Tg        -  patterns sampling grid
    # tS_r      -  the time of sampling patterns
    (nPatts,
     Tg,
     tS_r) = _getPatternsParam(dPatts)

    # -----------------------------------------------------------------
    # Get the representation sampling frequency of signals to be sampled,
    # the number of signals and the time of the signals
    (_, nSigs, fR, tS) = _getSigs(dSig)

   #----------------------------------------------------------------------
    # Print the configuration if the 'mute' flag is not set
    if bMute == 0:

        # Print out the header of the sampler
        rxcs.console.progress('Signal sampling', 'Nonuniform sampler (Exter)')

        # - - - - - - - - - - - - - - - - - - -
        # Source of the sampling patterns
        if bFile == 1:
            strSource = ('external file > %s <') % (strFile)
        else:
            strSource = ('dictionary given as an argument')

        rxcs.console.bullet_info('Source of the patterns:',strSource)

        # - - - - - - - - - - - - - - - - - - -
        # The number of sampling patterns avaialable
        rxcs.console.param('The number of patterns avaialble:',
                           nPatts,
                           '-',
                           'patterns')

        # - - - - - - - - - - - - - - - - - - -
        # Indices of patterns to be used
        if iA == 0:
            rxcs.console.info('All the available patterns will be used')
        else:
            rxcs.console.bullet_param('Index of the first pattern to be used',
                                      iA,' ','')

            if np.isinf(iB):
                rxcs.console.param('The number of pattern to be used',
                                          nPatts-iA + 1,'-','patterns')
            else:
                rxcs.console.param('Index of the last pattern to be used',
                                          iB,' ','')

                rxcs.console.param('The number of pattern to be used',
                                          iB-iA + 1,'-','patterns')

        # - - - - - - - - - - - - - - - - - - -

        # Time
        rxcs.console.bullet_param('The time of the sampling pattern',
                                  tS_r,'-','s')

        # - - - - - - - - - - - - - - - - - - -

        # Grid
        rxcs.console.bullet_param('Sampling grid of the pattern',
                                  Tg,'-','s')
        rxcs.console.param('Signal representation period',
                           1/fR,'-','s')
        strInfo = ('One sampling grid period equals %d ') % int((Tg/(1/fR)))
        strInfo = strInfo + ('signal represention periods')
        rxcs.console.info(strInfo)

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
def _checkConf(dAcqConf, dSig, dConf):
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
    # Get the representation sampling frequency of signals to be sampled,
    # the number of signals and the time of the signals
    (_, nSigs, fR, tS) = _getSigs(dSig)

    # -----------------------------------------------------------------
    # Get the configuration fields from the configuration dictionary
    bMute = dConf['bMute']       # mute the conole output flag
    bFile = dConf['bFile']       # patterns from file flag
    strFile = dConf['strFile']   # name of the file with patterns
    dPatts = dConf['dPatts']     # dictionary with sampling patterns
    iA = dConf['iA']             # index of the first pattern to be used
    iB = dConf['iB']             # index of the last pattern to be used

    # -----------------------------------------------------------------
    # Get the parameters of the sampling patterns
    # nPatts    -  the number of patterns
    # Tg        -  patterns sampling grid
    # tS_r      -  the time of sampling patterns
    (nPatts,
     Tg,
     tS_r) = _getPatternsParam(dPatts)

    # -----------------------------------------------------------------
    # Check if the real time of patterns is higher than 0
    if not tS_r > 0:
        strError = ('Real time of patterns must be higher than zero')
        raise ValueError(strError)

    # -----------------------------------------------------------------
    # Check if the time of patterns is equal to the time of signals to be
    # sampled
    if tS_r != tS:
        strError = ('The real time of patterns is different than the time ')
        strError = strError + ('of signals to be sampled')
        raise ValueError(strError)

    # -----------------------------------------------------------------
    # Check if the signal representation sampling frequency is compatible
    # with the sampling period
    if np.round(Tg * fR) != (Tg * fR):
        strError = ('The sampling grid period of pattern is incompatible with')
        strError = strError + (' the signals representation sampling ')
        strError = strError + ('frequency')
        raise ValueError(strError)

    # -----------------------------------------------------------------
    # Check indices of the first and last patterns to be used
    if not (iA >= 0):
        strError = ('Index of the first pattern to be used (iA) must be')
        strError = strError + (' higher than zero')
        raise ValueError(strError)

    if not (iB >= iA):
        strError = ('Index of the last pattern to be used (iB) must be')
        strError = strError + (' higher or equal to the index of the first')
        strError = strError + (' pattern to be used (iA)')
        raise ValueError(strError)

    if not (nPatts >= iA):
        strError = ('Index of the first pattern to be used (iA) must be')
        strError = strError + ('lower or equal to the number of patterns')
        raise ValueError(strError)

    if not np.isinf(iB) and (iA > 0):
        if not (nPatts >= iB):
            strError = ('Index of the last pattern to be used (iB) must be ')
            strError = strError + ('lower or equal to the number of patterns')
            raise ValueError(strError)

    # -----------------------------------------------------------------


    return


# =================================================================
# Read the file with sampling patterns
# =================================================================
def _readFile(strFile):

    # Check fi the file exists
    if os.path.isfile(strFile) == False:
        strError = ('File >%s< with patterns do not exist!') % (strfile)
        raise RuntimeError(strError)

    # Open the file with sampling patterns
    file = open(strFile,'rb')

    # Unpickle the file
    dPatts = cPickle.load(file)

    # Check if the file contains a dictionary
    if not (type(dPatts) == dict):
        strError = ('File >%s< does not contain patterns!') % (strfile)
        raise RuntimeError(strError)

    # Return the file with sampling patterns
    return dPatts


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
# Get the parameters of the sampling patterns
# =================================================================
def _getPatternsParam(dPatts):

    # -----------------------------------------------------------------
    # Get the number of patterns
    if not 'mPatternsGrid' in dPatts:
        strError = ('Dictionary with patterns does not contain')
        strError = strError + ('the matrix with pattern (mPatternsGrid)')
        raise NameError(strError)
    else:
        (nPatts, _) = dPatts['mPatternsGrid'].shape

    # -----------------------------------------------------------------
    # Get the pattens time
    if not 'tS_r' in dPatts:
        strError = ('Dictionary with patterns does not contain')
        strError = strError + ('the time of sampling patterns (tS_r)')
        raise NameError(strError)
    else:
        tS_r = dPatts['tS_r']

    # -----------------------------------------------------------------
    # Get the pattens sampling grid
    if not 'Tg' in dPatts:
        strError = ('Dictionary with patterns does not contain')
        strError = strError + ('the pattens sampling grid  (Tg)')
        raise NameError(strError)
    else:
        Tg = dPatts['Tg']

    # -----------------------------------------------------------------

    return (nPatts,   # the number of patterns
            Tg,       # patterns sampling grid
            tS_r)     # the time of sampling patterns


# =================================================================
# Get and process the sampling patterns
# =================================================================
def _take_patterns(dAcqConf, dSig, dConf):

    # -----------------------------------------------------------------
    # Get the representation sampling frequency of signals to be sampled,
    # the number of signals and the time of the signals
    (_, nSigs, fR, tS) = _getSigs(dSig)

    # -----------------------------------------------------------------
    # Get the configuration fields from the configuration dictionary
    bMute = dConf['bMute']       # mute the conole output flag
    bFile = dConf['bFile']       # patterns from file flag
    strFile = dConf['strFile']   # name of the file with patterns
    dPatts = dConf['dPatts']     # dictionary with sampling patterns
    iA = dConf['iA']             # index of the first pattern to be used
    iB = dConf['iB']             # index of the last pattern to be used

    # -----------------------------------------------------------------
    # Get the parameters of the sampling patterns
    # nPatts    -  the number of patterns
    # Tg        -  patterns sampling grid
    # tS_r      -  the time of sampling patterns
    (nPatts,
     Tg,
     tS_r) = _getPatternsParam(dPatts)


    # --------------------------------------------------------------
    # Generate a random index of a sampling patterns for every signal to
    # be sampled
    vPattInx = np.random.randint(iA-1, iB, nSigs)

    # Take a pattern for every signal
    mPatts = dPatts['mPatternsGrid'][vPattInx, :]


    # --------------------------------------------------------------
    # Recalculate the patterns to the signal representation frequency

    # Compute the number of signal representation points which equals
    # one grid point
    iGridvsRep = int(np.round((Tg * fR)))

    # Get the time vector of the original signal (if it is given)
    # and the first sample
    if 'vTSig' in dSig:
        vTSig = dSig['vTSig']
    else:
        vTSig = np.arange(int(np.round(tTau_real*fR)))
    iT1 = vTSig[0]

    if iT1 == 0:  # <- If the time stamp of the first sample is zero,
                  #    then the sampler should count the grid indices from zero.
                  #    By default the grid indices counts from 1, so there is
                  #    a need to decrease the gird indices by 1
        mPatts = mPatts - 1
        mPattsRep = iGridvsRep * mPatts
    else:
        mPattsRep = iGridvsRep * mPatts
        mPattsRep = mPattsRep - 1

    # --------------------------------------------------------------
    # Recalculate the patterns to the time moments
    mPattsT = vTSig[mPattsRep]

    # --------------------------------------------------------------

    return (mPatts, mPattsRep, mPattsT)


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
    mObSig = (mSig[np.arange(nSigs), mPattsRep.T]).T

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
        m3Phi (3D matrix): observation matrices
    """

    # -----------------------------------------------------------------
    # Get the representation sampling frequency of signals to be sampled
    # and the time of signals to be sampled
    (_, _, fR, tS) = _getSigs(dSig)

    # Calculate the number of representation samples in the signals
    nSmp = int(round(tS * fR))

    # -----------------------------------------------------------------
    # Compute the real parameters of the sampling patterns

    # nPatts      -  the number of patterns to be generated
    # nK_s        -  the expected number of sampling points in a pattern
    (nPatts,
     _,
     _,
     nK_s,
     _,
     _,
     _,
     _,
     _,
     _,
     _) = _computeRealParam(dAcqConf, dSig)

    # -----------------------------------------------------------------

    # Allocate the observation matrices
    m3Phi = np.zeros((nPatts, nK_s, nSmp))

    # Generate the observation matrices
    for inxPat in np.arange(nPatts):  # <- loop over all observation matrices

        # Get the current pattern
        vPatts = mPattsRep[inxPat, :]

        # Generate the current observation matrix
        inxRow = 0
        for inxCol in vPatts:    # <- loop over all samling points in pattern
            m3Phi[inxPat, inxRow, inxCol] = 1
            inxRow = inxRow + 1

    # -----------------------------------------------------------------

    return m3Phi

# =================================================================
# Generate the output dictionary
# =================================================================
def _generateOutput(dAcqConf, dSig, mObSig, mPatts, mPattsRep, mPattsT, m3Phi):
    """
    This function generates the output dictionary.

    Args:
        dAcqConf (dictionary): dictionary with configuration for the sampler
        dSig (dictionary): dictionary with the signals to be sampled
        mObSig (matrix):  the observed signals
        mPatts (matrix): the sampling patterns (grid indices)
        mPattsRep (matrix): the sampling patterns (signal rep. sampling points)
        mPattsT (matrix): the sampling patterns (time moments)
        m3Phi (3D matrix): observation matrices

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

    dObSig['mObSig'] = mObSig   # The observed signals

    # - - - - - - - - - - - - - - - - - -

    dObSig['mPatts'] = mPatts         # The sampling patterns (grid indices)

    dObSig['mPattsT'] = mPattsT       # The sampling patterns (time moments)

    dObSig['mPattsRep'] = mPattsRep   # The sampling patterns (signal
                                      # representation sampling points)

    # - - - - - - - - - - - - - - - - - -

    dObSig['m3Phi'] = m3Phi           # The observation matrices

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
