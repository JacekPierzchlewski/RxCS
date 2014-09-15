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
    1.0  | 12-SEP-2014 : * Initial version. |br|

*License*:
    BSD 2-Clause
"""

from __future__ import division
import time
import rxcs
import os.path
import cPickle
import numpy as np


def main(dAcqConf):
    """
    This the main function of the sampler. |br|

    Args:
        dAcqConf (dictionary): dictionary with configuration for the sampler


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
    tStart = _printConf(dConf)

    # - - - - - - - - - - - - - - - - - - -

    ## Check the configuration
    _checkConf(dAcqConf, dConf)

    ## - - - - - - - - - - - - - - - - - - -

    ## =================================================================
    ## Get and process the sampling patterns
    ## =================================================================
    (mPatts, mPattsRep, mPattsT, vPattInx) = _get_patterns(dAcqConf, dConf)

    ## =================================================================
    ## Generate the observation matrices
    ## =================================================================
    m3Phi = _generObser(mPattsRep, dConf)

    ## =================================================================
    ## Generate the output dictionary
    ## =================================================================
    dObMat = _generateOutput(dConf,
                             mPatts, mPattsRep, mPattsT, vPattInx,
                             m3Phi)

    ## =================================================================
    ## Signal sampling is done!
    ## =================================================================
    if not np.isnan(tStart):   # <-tStart is nan = console output is off
        rxcs.console.module_progress_done(tStart)
    return dObMat


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
        dConf (dictionary): dictionary with processed settings for the sampler

            bMute (float):      mute the conole output flag
            bFile (float):      patterns from file flag (1-from file,
                                                         0-from an argument given as
                                                         a dictionary)

            strFile (string):   name of the file with patterns (if bFile == 1,
                                                                otherwise an empty
                                                                string)

            dPatts  (dict):     dictionary with sampling patterns

            iA    (float):      index of the first pattern to be used
                                (if not given in the configuration, then = 0)

            iB    (float):      index of the last pattern to be used
                                (if not given in the configuration, then = np.inf)

            vPattInx (vector):  given indices of patterns to be used

            Tg (float):         sampling period of an observation matrix

            tS (float):         time of the observation matrix

            nObMat (int):       the number of observation matrices

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
    # Take the given indices of the sampling patterns
    if not 'vPattInx' in dAcqConf:
        vPattInx = np.array([])
    else:
        vPattInx = dAcqConf['vPattInx']
        vPattInx = vPattInx.astype(int)
        vPattInx = vPattInx.reshape(vPattInx.size)

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
    # Take the sampling period of an observation matrix
    if not 'Tg' in dAcqConf:
        strError = ('The sampling period of observation matrices (Tg) ')
        strError = strError + ('is not given in the configuration')
        raise NameError(strError)
    else:
        TgOb = dAcqConf['Tg']

    # -----------------------------------------------------------------
    # Take the time of the observation matrix
    if not 'tS' in dAcqConf:
        strError = ('The time of observation matrices (tS) ')
        strError = strError + ('is not given in the configuration')
        raise NameError(strError)
    else:
        tSOb = dAcqConf['tS']

    # -----------------------------------------------------------------
    # Take the number of observation matrices
    if (not 'nObMat' in dAcqConf) and (not 'vPattInx' in dAcqConf):
        strError = ('The number of observation matrices (nObMat) ')
        strError = strError + ('is not given in the configuration')
        raise NameError(strError)
    elif 'nObMat' in dAcqConf:
        nObMat = dAcqConf['nObMat']
    else:
        nObMat = vPattInx.size

    # -----------------------------------------------------------------
    # Create the configuration dictionary
    dConf = {}
    dConf['bMute'] = bMute         # mute the conole output flag
    dConf['bFile'] = bFile         # patterns from file flag
    dConf['strFile'] = strFile     # name of the file with patterns
    dConf['dPatts'] = dPatts       # dictionary with sampling patterns
    dConf['iA'] = iA               # index of the first pattern to be used
    dConf['iB'] = iB               # index of the last pattern to be used
    dConf['vPattInx'] = vPattInx   # given indices of patterns to be used
    dConf['TgOb'] = TgOb           # the sampling period of an observation matrix
    dConf['tSOb'] = tSOb           # the time of the observation matrix
    dConf['nObMat'] = nObMat       # the number of observation matrices to be generated

    # -----------------------------------------------------------------
    return (dConf)


# =================================================================
# Print the configuration to the console
# =================================================================
def _printConf(dConf):
    """
    This function prints the configuration of the sampler to the console.

    Args:
        dSig (dictionary): dictionary with the signals to be sampled
        dConf (dictionary): dictionary with processed settings for the sampler

    Returns:
        tStart (float): time stamp of the beginning of sampling
    """

    # -----------------------------------------------------------------
    # Get the configuration fields from the configuration dictionary
    bMute = dConf['bMute']          # mute the conole output flag
    bFile = dConf['bFile']          # patterns from file flag
    strFile = dConf['strFile']      # name of the file with patterns
    dPatts = dConf['dPatts']        # dictionary with sampling patterns
    iA = dConf['iA']                # index of the first pattern to be used
    iB = dConf['iB']                # index of the last pattern to be used
    vPattInx = dConf['vPattInx']    # given indices of patterns to be used
    TgOb = dConf['TgOb']            # the sampling period of an observation matrix
    tSOb = dConf['tSOb']            # the time of the observation matrix
    nObMat = dConf['nObMat']        # the number of observation matrices

    # -----------------------------------------------------------------
    # Get the parameters of the sampling patterns
    # nPatts    -  the number of patterns
    # Tg        -  patterns sampling grid
    # tS_r      -  the time of sampling patterns
    (nPatts,
     Tg,
     tS_r) = _getPatternsParam(dPatts)

   #----------------------------------------------------------------------
    # Print the configuration if the 'mute' flag is not set
    if bMute == 0:

        # Print out the header of the sampler
        rxcs.console.progress('Signal sampling', 'Nonuniform sampler (Exter) - DUMMY')

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
        # Given indices of patterns to be used
        if vPattInx.size > 0:
            rxcs.console.info('User gave indices of patterns to be used')

        # - - - - - - - - - - - - - - - - - - -
        # First/last Indices of patterns to be used
        else:
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
        rxcs.console.param('The sampling period of an observation matrix',
                            TgOb,'-','s')
        strInfo = ('One sampling grid period equals %d ') % int((Tg/TgOb))
        strInfo = strInfo + ('sampling periods of an observation matrix')
        rxcs.console.info(strInfo)

        # - - - - - - - - - - - - - - - - - - -

        # The number of observation matrices
        rxcs.console.bullet_param('The number of observation matrices to be generated',
                                  nObMat,'-','')
        rxcs.console.param('The time of the observation matrices', tSOb, '-', 's')

        # - - - - - - - - - - - - - - - - - - -
        # Information about the computations start
        tStart = rxcs.console.module_progress('signal sampler (dummy) starts!!!')

    #----------------------------------------------------------------------
    else:   # <- the output was muted, no time stamp of the start is required
        tStart = np.nan

    #----------------------------------------------------------------------
    return tStart


# =================================================================
# Check if the configuration for the sampler makes sense
# =================================================================
def _checkConf(dAcqConf, dConf):
    """
    This function checks if the configuration given to the sampler
    is correct.

    Args:
        dAcqConf (dictionary): dictionary with configuration for the sampler
        dConf (dictionary): dictionary with processed settings for the sampler

    Returns:
        nothing
    """

    # -----------------------------------------------------------------
    # Get the configuration fields from the configuration dictionary
    dPatts = dConf['dPatts']        # dictionary with sampling patterns
    iA = dConf['iA']                # index of the first pattern to be used
    iB = dConf['iB']                # index of the last pattern to be used
    vPattInx = dConf['vPattInx']    # given indices of patterns to be used
    TgOb = dConf['TgOb']            # the sampling period of an observation matrix
    tSOb = dConf['tSOb']            # the time of the observation matrix
    nObMat = dConf['nObMat']        # the number of observation matrices

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
    # Check if the time of patterns is equal to the time of observation
    # matrices to be generated
    if (np.abs(tS_r - tSOb)/tS_r) > 1e-9:
        print('\n\n%.21f \n\n') % (tSOb - tS_r)
        strError = ('The real time of patterns is different than the time ')
        strError = strError + ('of observation matrix to be generated')
        raise ValueError(strError)

    # -----------------------------------------------------------------
    # Check if the observation matrix sampling period is compatible
    # with the sampling period
    if np.round((Tg /TgOb) != (Tg / TgOb)):
        strError = ('The sampling grid period of patterns is incompatible with')
        strError = strError + (' the observation matrix sampling period')
        raise ValueError(strError)

    # -----------------------------------------------------------------
    # Check indices given by user
    if vPattInx.size > 0:
        if vPattInx.size != nObMat:
            strError = ('The number of indices given in \'vPattInx\' must equal ')
            strError = strError + ('the number of observation matrices to be generated')
            raise ValueError(strError)

        if vPattInx.min() < 1:
            strError = ('Indices given in \'vPattInx\' must be higher then 1!')
            raise ValueError(strError)

        if vPattInx.max() > nPatts:
            strError = ('Indices given in \'vPattInx\' must not be higher then the number of ')
            strError = strError + ('patterns!')
            raise ValueError(strError)

    # Check first/last indices given by user
    else:
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
    """
    This function reads the file with sampling patterns.

    Args:
        strFile (string):  name of the file (together with a path)

    Returns:
        dPatts (dictionary):  dictionary with sampling patterns and their parameters
    """

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
# Get the parameters of the sampling patterns
# =================================================================
def _getPatternsParam(dPatts):
    """
    This function get the parameters from the dictionary with sampling patterns

    Args:
        dPatts (dictionary):  dictionary with sampling patterns and their parameters

    Returns:
        nPatts (int): the number of patterns
        Tg (float): patterns sampling grid
        tS_r (float): the time of sampling patterns
    """

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
def _get_patterns(dAcqConf, dConf):
    """
    Chhose and process the patterns from the source of sampling patterns.

    Args:
        dAcqConf (dictionary): dictionary with configuration for the sampler
        dConf (dictionary): dictionary with processed settings for the sampler

    Returns:
        mPatts (matrix):     matrix with sampling pattens (one pattern p signal)
        mPattsRep (matrix):  matrix with sampling pattens expressed in signals representation
                             sampling points (one pattern p signal)

        mPattsT (matrix):    matrix with time moments of sampling
        vPattInx (matrix):   vector with indices of chosen sampling patterns
    """

    # -----------------------------------------------------------------
    # Get the configuration fields from the configuration dictionary
    bMute = dConf['bMute']        # mute the conole output flag
    bFile = dConf['bFile']        # patterns from file flag
    strFile = dConf['strFile']    # name of the file with patterns
    dPatts = dConf['dPatts']      # dictionary with sampling patterns
    iA = dConf['iA']              # index of the first pattern to be used
    iB = dConf['iB']              # index of the last pattern to be used
    vPattInx = dConf['vPattInx']  # given indices of patterns to be used
    TgOb = dConf['TgOb']          # the sampling period of an observation matrix
    tSOb = dConf['tSOb']          # the time of the observation matrix
    nObMat = dConf['nObMat']      # the number of observation matrices to be generated

    # -----------------------------------------------------------------
    # Get the parameters of the sampling patterns
    # nPatts    -  the number of patterns
    # Tg        -  patterns sampling grid
    (nPatts,
     Tg,
     _) = _getPatternsParam(dPatts)

    # --------------------------------------------------------------
    # Take or generate a random index of a sampling pattern for every signal to
    # be sampled
    if vPattInx.size == 0:
        if iA > 0:
            vPattInx = np.random.randint(iA, iB+1, nObMat)
        else:
            vPattInx = np.random.randint(0, nPatts, nObMat)   # <- Take all the patterns

    # Take a pattern for every signal
    mPatts = dPatts['mPatternsGrid'][vPattInx - 1, :]

    # --------------------------------------------------------------
    # Recalculate the patterns to the signal representation frequency

    # Compute the number of signal representation points which equals
    # one grid point
    iGridvsRep = int(np.round((Tg / TgOb)))
    mPattsRep = iGridvsRep * mPatts

    # --------------------------------------------------------------
    # Recalculate the indices of sampling points to the time moments of sampling
    # Get the time vector of the original signal (if it is given)
    vTSig = TgOb*np.arange(int(np.round(tSOb / TgOb)))

    mPattsT = np.nan*np.ones(mPattsRep.shape)

    for inxPat in np.arange(nObMat):  # <- loop over all the observation matrices

        # Take the pattern and clear it (remove -1)
        vPatt = mPattsRep[inxPat,:]
        vPatt = vPatt[vPatt >= 0]
        nSampPts = vPatt.size   # The number of sampling points in a pattern

        # Take the time sampling points
        mPattsT[inxPat,np.arange(nSampPts)] = vTSig[vPatt-1]

    # --------------------------------------------------------------

    return (mPatts, mPattsRep, mPattsT, vPattInx)


# =================================================================
# Generate the observation matrix
# =================================================================
def _generObser(mPattsRep, dConf):
    """
    This function generates the observation matrices.

    Args:
        mPattsRep (matrix): the sampling patterns (signal rep. sampling points)
        dConf (dictionary): dictionary with processed settings for the sampler

    Returns:
        m3Phi (3D matrix): observation matrices
    """

    TgOb = dConf['TgOb']          # the sampling period of an observation matrix
    tSOb = dConf['tSOb']          # the time of the observation matrix

    # Calculate the number of representation samples in the signals
    nSmp = int(round(tSOb / TgOb))

    # Calculate the number of patterns and the number of sampling points in patterns
    (nPatts, nSamp) = mPattsRep.shape

    # -----------------------------------------------------------------
    # Allocate the observation matrices
    m3Phi = np.zeros((nPatts, nSamp, nSmp))

    # Generate the observation matrices
    for inxPat in np.arange(nPatts):  # <- loop over all observation matrices

        # Get the current pattern
        vPatt = mPattsRep[inxPat, :]
        vPatt = vPatt[vPatt >= 0]

        # Generate the current observation matrix
        inxRow = 0
        for inxCol in vPatt:    # <- loop over all samling points in pattern
            m3Phi[inxPat, inxRow, inxCol-1] = 1
            inxRow = inxRow + 1

    # -----------------------------------------------------------------

    return m3Phi

# =================================================================
# Generate the output dictionary
# =================================================================
def _generateOutput(dConf, mPatts, mPattsRep, mPattsT, vPattInx, m3Phi):
    """
    This function generates the output dictionary.

    Args:
        dConf (dictionary): dictionary with processed settings for the sampler

        mPatts (matrix): the sampling patterns (grid indices)
        mPattsRep (matrix): the sampling patterns (signal rep. sampling points)
        mPattsT (matrix): the sampling patterns (time moments)
        vPattInx (vector): the vector with indices of chosen sampling patterns

        m3Phi (3D matrix): observation matrices

    Returns:
        dObMat (dictionary): the observed matrix and paramters
    """

    # -----------------------------------------------------------------
    # Get the parameters of the sampling patterns
    # Tg        -  patterns sampling grid
    # tS_r      -  the time of sampling patterns
    (_,
     Tg,
     tS_r) = _getPatternsParam(dConf['dPatts'])

    # -----------------------------------------------------------------
    # Initialize the output dictionary
    dObMat = {}

    # - - - - - - - - - - - - - - - - - -

    dObMat['mPatts'] = mPatts         # The sampling patterns (grid indices)

    dObMat['mPattsT'] = mPattsT       # The sampling patterns (time moments)

    dObMat['mPattsRep'] = mPattsRep   # The sampling patterns (signal
                                      # representation sampling points)

    dObMat['vPattInx'] = vPattInx     # The vector with indices of chosen sampling patterns

    # - - - - - - - - - - - - - - - - - -

    dObMat['m3Phi'] = m3Phi           # The observation matrices

    # - - - - - - - - - - - - - - - - - -

    dObMat['Tg'] = Tg           # The patterns sampling grid

    dObMat['tS_r'] = tS_r       # The time of sampling patterns

    # - - - - - - - - - - - - - - - - - -

    return dObMat
