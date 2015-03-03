"""
This is a saturation block. |br|

The modules saturates the given signal. |br|

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0  | 03-MAR-2015 : * Initial version. |br|

*License*:
    BSD 2-Clause
"""
from __future__ import division
import rxcs
import numpy as np
import sys

def main(dAcqConf, dSig):
    """
    This the main function of the saturation block. |br|

    Fields in the configuration dictionary (dAcqConf):

    - a. **bMute** (*int*): mute the console output from the module
                            NOT REQUIRED, default = 0

    - b. **iMinAmp** (*float*): minimum allowed value of the signal

    - c. **iMaxAmp** (*float*): maximum allowed value of the signal


    Required fields in the dictionary with signals to be sampled (dSig):

    - a. **mSig** or **mObSig** (*numpy array 2D*): 2D array with signals, one signal p. row

    Fields in the dictionary with signals to be sampled (dSig) which will be processed if exist:

    - b. **mPatts** (*numpy array 2D*):       array with sampling patterns as sampling grid indices

    - c. **mPattsT** (*numpy array 2D*):      array with sampling patterns as time moments

    - d. **mPattsRep** (*numpy array 2D*):    array with sampling patterns as signal rep. points

    - e. **m3Phi** (*numpy array 3D*):        observation matrices


    Fields in the output dictionary (dObSig):

    - a. **mObSig** (*numpy array 2D*): 2D array with observed signals, one signal p. row

    - b. **lObSigClean** (*list*): list with the observed limited signals with saturated signals removed

    - c. **mSaturMark** (*numpy array 2D*): 2D array with sampling patterns, represented as time moments

    - d. **nSamps** (*float*): the total number of samples in all the signals

    - e. **nSatMin** (*float*): the total number of saturated samples because of too low value

    - f. **nSatMax** (*float*): the total number of saturated samples because of too high value

    - g. **lPattsClean** (*list*): list with modified sampling patterns, represented as indices of sampling grid points
                                   (only if list with sampling patterns represented as indices of sampling grid points
                                    was present in the input dictionary)

    - h. **lPattsTClean** (*list*): list with modified sampling patterns, represented as time moments
                                   (only if list with sampling patterns represented as indices of sampling grid points
                                    was present in the input dictionary)

    - i. **lPattsRepClean** (*list*): list with modified sampling patterns, represented as indices of signal representation points
                                   (only if list with sampling patterns represented as indices of sampling grid points
                                    was present in the input dictionary)

    - j. **lPhi** (*list*): list with observation matrices
                            (only if list with observation matrices was present in the input dictionary)
    """

    # =================================================================
    # Check the configuration and print it to the console
    # =================================================================

    # Print the configuration to the console
    tStart = _printConf(dAcqConf)

    # Check if the configuration for the saturation block make sense
    _checkConf(dAcqConf)

    # =================================================================
    # Engine of the saturation block (signal limitation) runs here
    # =================================================================
    (mObSig, lObSigClean, mSaturMark,
     nSigs, nSamps, nSatMin, nSatMax,
     lPattsClean, lPattsTClean, lPattsRepClean, lPhi) = _engine(dAcqConf, dSig)

    _printResults(nSigs, nSamps, nSatMin, nSatMax)  # Print some statistical info about the results

    # =================================================================
    # Generate the output dictionary
    # =================================================================
    dObSig = _generateOutput(mObSig, lObSigClean, mSaturMark,
                             nSamps, nSatMin, nSatMax,
                             lPattsClean, lPattsTClean, lPattsRepClean, lPhi)

    if not np.isnan(tStart):   # <-tStart is nan = console output is off
        rxcs.console.module_progress_done(tStart)

    return dObSig


# =================================================================
# Print the configuration to the console
# =================================================================
def _printConf(dAcqConf):
    """
    This function prints the configuration of the saturation module to the console.

    Args:
        dAcqConf (dictionary): dictionary with configuration for the saturation block

    Returns:
        tStart (float): time stamp of the beginning of sampling
    """

    # -----------------------------------------------------------------
    # Check and get the configuration from the configuration dictionary

    # bMute     -  mute the conole output flag
    # iMinAmp   -  minimum amplitude
    # iMaxAmp   -  maximum amplitude
    (bMute,
     iMinAmp,
     iMaxAmp) = _getConf(dAcqConf)

    #----------------------------------------------------------------------
    # Print the configuration if the 'mute' flag is not set
    if bMute == 0:

        # Print out the header of the sampler
        rxcs.console.progress('Signal acquisition', 'Saturation block')

        # - - - - - - - - - - - - - - - - - - -
        # Print the allowed signals amplitudes
        rxcs.console.bullet_param('Minimum allowed signals amplitude', iMinAmp, ' ', '')
        rxcs.console.param('Maximum allowed signals amplitude', iMaxAmp, ' ', '')

        # - - - - - - - - - - - - - - - - - - -
        # Information about the computations start
        tStart = rxcs.console.module_progress('saturation block starts!!!')

    #----------------------------------------------------------------------
    else:   # <- the output was muted, no time stamp of the start is required
        tStart = np.nan

    #----------------------------------------------------------------------
    return tStart


# =================================================================
# Check if the configuration for the saturation module make sense
# =================================================================
def _checkConf(dAcqConf):
    """
    This function checks if the configuration given to the saturation module
    is correct.

    Args:
        dAcqConf (dictionary): dictionary with configuration for the saturation block

    Returns:
        nothing
    """
    # -----------------------------------------------------------------
    # Check and get the configuration from the configuration dictionary

    # bMute     -  mute the conole output flag
    # iMinAmp   -  minimum amplitude
    # iMaxAmp   -  maximum amplitude
    (bMute,
     iMinAmp,
     iMaxAmp) = _getConf(dAcqConf)

    # -----------------------------------------------------------------
    # Check if the maximum amplitude is higher than the minimum amplitude
    if not (iMinAmp < iMaxAmp):
        strError = ('The maximum amplitude must be higher than the minimum amplitude')
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
        dAcqConf (dictionary): dictionary with configuration for the saturation block

    Returns:
        bMute (float):      mute the output flag
        iMinAmp (float):    minimum amplitude of a signal
        iMaxAmp (float):    maximum amplitude of a signal
    """

    # -----------------------------------------------------------------
    # Get the mute flag
    if not 'bMute' in dAcqConf:
        bMute = 0
    else:
        bMute = dAcqConf['bMute']

    # -----------------------------------------------------------------
    # Get the minimum allowed amplitude of a signal
    if not 'iMinAmp' in dAcqConf:
        strError = ('The minimum allowed amplitude of a signal (iMinAmp) is not given in ')
        strError = strError + ('the configuration')
        raise NameError(strError)
    else:
        iMinAmp = dAcqConf['iMinAmp']

    # -----------------------------------------------------------------
    # Get the maximum amplitude of a signal
    if not 'iMaxAmp' in dAcqConf:
        strError = ('The maximum allowed amplitude of a signal (iMaxAmp) is not given in ')
        strError = strError + ('the configuration')
        raise NameError(strError)
    else:
        iMaxAmp = dAcqConf['iMaxAmp']

    # -----------------------------------------------------------------
    return (bMute,       # mute the conole output flag
            iMinAmp,     # minimum amplitude of a signal
            iMaxAmp)     # maximum amplitude of a signal


# =================================================================
# Check the dictionary with signals to be sampled.
# Get the signals to be sampled and their parameters.
# =================================================================
def _getSigs(dSig):
    """
    This function checks if the dictionary with signals to be sampled
    contains all the needed fields. Then the function gets these fields.

    Args:
        dSig (dictionary): dictionary with the input signals to be limited

    Returns:
        mSig (array):   an array with the input signals to be limited
        nSigs (float):  the number of the input signals
        nSamps (float): the number of samples in ONE signal
        mPatts (numpy array 2D):       array with sampling patterns as sampling grid indices
                                       (if present in the input dictionary, otherwise mPatts = int(0))

        mPattsT (numpy array 2D):      array with sampling patterns as time moments
                                       (if present in the input dictionary, otherwise mPattsT = int(0))

        mPattsRep (numpy array 2D):    array with sampling patterns as signal rep. points
                                       (if present in the input dictionary, otherwise mPattsRep = int(0))

        m3Phi (numpy array 3D):        observation matrices
                                       (if present in the input dictionary,  otherwise m3Phi = int(0))
    """

    # -----------------------------------------------------------------
    # Get the signals to be sampled and the number of signals to be sampled
    if (not 'mSig' in dSig) and (not 'mObSig' in dSig):
        strError = ('Dictionary with signals to be sampled does not contain ')
        strError = strError + ('signals (neither \'mObSig\' nor \'mSig\' field is present in the dictionary)')
        raise NameError(strError)
    elif ('mSig' in dSig):
        mSig = dSig['mSig']
    else:
        mSig = dSig['mObSig']
    (nSigs, nSamps) = mSig.shape

    # -----------------------------------------------------------------
    # Get the sampling patterns (if exists)
    mPatts = int(0)
    if ('mPatts' in dSig):
        mPatts = dSig['mPatts']

    mPattsT = int(0)
    if ('mPattsT' in dSig):
        mPattsT = dSig['mPattsT']

    mPattsRep = int(0)
    if ('mPattsRep' in dSig):
        mPattsRep = dSig['mPattsRep']

    # -----------------------------------------------------------------
    # Get the observation matrices (if exists)
    m3Phi = int(0)
    if ('m3Phi' in dSig):
        m3Phi = dSig['m3Phi']

    # -----------------------------------------------------------------
    return (mSig,       # the signals to be sampled
            nSigs,      # the number of signals to be processed
            nSamps,     # the maximum number of samples in ONE signal
            mPatts,     # the sampling patterns (grid indices)
            mPattsT,    # the sampling patterns (time moments)
            mPattsRep,  # the sampling patterns (signal representation sampling points)
            m3Phi)      # the observation matrices


# =================================================================
# Engine of the saturation block
# =================================================================
def _engine(dAcqConf, dSig):
    """
    This function is the engine of the saturation block (signal limitation).

    Args:
        dAcqConf (dictionary):      dictionary with configuration for the saturation block
        dSig (dictionary):          dictionary with the input signals to be limited

    Returns:
        mObSig (array):              an array with observed limited signals
        lObSigClean (list):          list with the observed limited signals with saturated signals removed
        mSaturMark (array):          an array with saturation markers
        nSigs (float):               the numbe of input signals
        nSamps (float):              the total number of samples in all the signals
        nSatMin (float):             the total number of saturated samples because of too low value
        nSatMax (float):             the total number of saturated samples because of too high value
        lPattsClean (list):          list with modified sampling patterns, represented as indices of sampling grid points
        lPattsTClean (list):         list with modified sampling patterns, represented as time moments
        lPattsRepClean (list):       list with modified sampling patterns, represented as indices of signal representation points
        lPhi (list):                 list with observation matrices
    """

    # -----------------------------------------------------------------
    # Check and get the configuration from the configuration dictionary

    # bMute     -  mute the conole output flag
    # iMinAmp   -  minimum amplitude
    # iMaxAmp   -  maximum amplitude
    (bMute,
     iMinAmp,
     iMaxAmp) = _getConf(dAcqConf)

    # -----------------------------------------------------------------
    # Get the input signals, the sampling patterns and the observation matrices
    (mSig, nSigs, nSamps, mPatts, mPattsT, mPattsRep, m3Phi) = _getSigs(dSig)

    # -----------------------------------------------------------------
    # Saturation markers
    mSaturMark = np.zeros(mSig.shape)   # array with saturation markers
    mSaturMark[mSig < iMinAmp] = -1     # Samples saturated because of too low value
    mSaturMark[mSig > iMaxAmp] = 1      # Samples saturated because of too high value

    nSatMin = mSaturMark[mSaturMark == -1].size   # The total number of saturated samples because of too low value
    nSatMax = mSaturMark[mSaturMark == 1].size    # The total number of saturated samples because of too high value

    # -----------------------------------------------------------------
    # Generate the observed limited signals
    mObSig = mSig.copy()
    mObSig[mSaturMark == -1] = iMinAmp
    mObSig[mSaturMark == 1] = iMaxAmp

    # Generate the observed limited signals with saturated signals removed
    lObSigClean = []
    for inxSig in np.arange(nSigs):
        vSig = mObSig[inxSig, :]
        vSaturMark = mSaturMark[inxSig, :]
        vSig = vSig[vSaturMark == 0]
        lObSigClean.append(vSig)

    # -----------------------------------------------------------------
    # Process sampling patterns and observation matrices, if these were present in the input dictionary
    (lPattsClean, lPattsTClean, lPattsRepClean) = _enginePatterns(mPatts, mPattsT, mPattsRep, mSaturMark)
    lPhi = _engineObser(m3Phi, lPattsRepClean, mSaturMark)

    return (mObSig, lObSigClean, mSaturMark, nSigs, nSamps, nSatMin, nSatMax, lPattsClean, lPattsTClean, lPattsRepClean, lPhi)


def _enginePatterns(mPatts, mPattsT, mPattsRep, mSaturMark):
    """
    This function modifies sampling patterns.
    It removes sampling points in which the signal is saturated.

    Args:
        mPatts (numpy array 2D:        an array with sampling patterns, represented as indices of sampling grid points
        mPattsT (numpy array 2D):      an array with sampling patterns, represented as time moments
        mPattsRep (numpy array 2D):    an array with sampling patterns, represented as indices of signal representation points
        mSaturMark (numpy array 2D):   an array with saturation markers

        If arrays with patterns where not present in the dictionary with input signals, the first 3 arguments are integers
        equal to 0.

    Returns:
        lPattsClean (list):      a list with modified sampling patterns, represented as indices of sampling grid points
        lPattsTClean (list):     a list with modified sampling patterns, represented as time moments
        lPattsRepClean (list):   a list with modified sampling patterns, represented as indices of signal rep. points

        If arrays with patterns where not present in the dictionary with input signals, the output 3 arguments are empty
        lists.
    """
    # -----------------------------------------------------------------
    # Patterns (as grid indices):
    lPattsClean = []
    if not isinstance(mPatts, int):
        mPatts_ = mPatts.astype('float')
        (nSigs, _) = mPatts_.shape
        mPatts_[np.invert(mSaturMark == 0)] = np.nan
        for inxPat in np.arange(nSigs):
            vPatt = mPatts_[inxPat,:]
            vPatt = vPatt[np.invert(np.isnan(vPatt))]         # Remove all the NaN elements from the smapling pattern
            lPattsClean.append(vPatt)

    # -----------------------------------------------------------------
    # Patterns (as time moments):
    lPattsTClean = []
    if not isinstance(mPattsT, int):
        mPattsT_ = mPattsT.astype('float')
        (nSigs, _) = mPatts_.shape
        mPattsT_[np.invert(mSaturMark == 0)] = np.nan
        for inxPat in np.arange(nSigs):
            vPattT = mPattsT_[inxPat,:]
            vPattT = vPattT[np.invert(np.isnan(vPattT))]      # Remove all the NaN elements from the smapling pattern
            lPattsTClean.append(vPattT)

    # -----------------------------------------------------------------
    # Patterns (as indices of signal representation points):
    lPattsRepClean = []
    if not isinstance(mPattsRep, int):
        mPattsRep_ = mPattsRep.astype('float')
        (nSigs, _) = mPattsRep_.shape
        mPattsRep_[np.invert(mSaturMark == 0)] = np.nan
        for inxPat in np.arange(nSigs):
            vPattRep = mPattsRep_[inxPat,:]
            vPattRep = vPattRep[np.invert(np.isnan(vPattRep))]  # Remove all the NaN elements from the smapling pattern
            lPattsRepClean.append(vPattRep)

    # -----------------------------------------------------------------
    return (lPattsClean, lPattsTClean, lPattsRepClean)


def _engineObser(m3Phi, lPattsRepClean, mSaturMark):
    """
    This function generates the observation matrices.

    Args:
        m3Phi (numpy array 3D):         observation matrices from the dictionary with the input signals
        lPattsRepClean (list):          a list with modified sampling patterns, represented as indices of signal rep. points
        mSaturMark (numpy array 2D):    an array with saturation markers

    Returns:
        lPhi (list):        a list with observation matrices
    """

    lPhi = []
    # Do not create an observation matrices, if there was no in the input dictionary
    if not isinstance(m3Phi, int):
        (nSigs, _, nSamps) = m3Phi.shape
        for inxPat in np.arange(nSigs):               # Loop over all patterns (signals)
            vPatts = lPattsRepClean[inxPat]           # Get the current pattern

            # Generate the observation matrix for the current pattern
            mPhi = np.zeros((vPatts.size, nSamps))    # Allocate the current observation matrix
            inxRow = 0                                # Reset index of the row
            for inxCol in vPatts:                     # Loop over all sampling points
                mPhi[inxRow, int(inxCol)] = 1
                inxRow = inxRow + 1

            lPhi.append(mPhi)   # Store the genenrated observation matrix in the list
    return (lPhi)


# =================================================================
# Print some statistical info about the results
# =================================================================
def _printResults(nSigs, nSamps, nSatMin, nSatMax):
    """
    This function generates the observation matrices.

    Args:
        nSigs (int):        the number of signals in the input dictioanry
        nSamps (int):       the total number of signal representation sampling points in all the signals
        nSatMin (float):    the total number of saturated samples because of too low value
        nSatMax (float):    the total number of saturated samples because of too high value

    Returns:  none
    """

    print('')
    rxcs.console.bullet_param('The total number of signals is', nSigs, '-', '')
    rxcs.console.param('The number of samples in one signal is', nSamps, '-', 'samples')
    rxcs.console.param('The total number of samples is', nSamps*nSigs, '-', 'samples')

    rxcs.console.bullet_param('The total number of saturated samples', nSatMin+nSatMax, '-', 'samples')
    rxcs.console.param('which is',(nSatMin+nSatMax)/(nSamps*nSigs)*100, ' ', '%')

    rxcs.console.param('The total number of saturated samples because of too low value', nSatMin, '-', 'samples')
    rxcs.console.param('which is',nSatMin/(nSamps*nSigs)*100, ' ', '%')

    rxcs.console.param('The total number of saturated samples because of too high value', nSatMax, '-', 'samples')
    rxcs.console.param('which is',nSatMax/(nSamps*nSigs)*100, ' ', '%')

    sys.stdout.write('\n                                          ...')
    return


# =================================================================
# Generate the output dictionary
# =================================================================
def _generateOutput(mObSig, lObSigClean, mSaturMark, nSamps, nSatMin, nSatMax, lPattsClean, lPattsTClean, lPattsRepClean, lPhi):
    """
    This function generates the output dictionary.

    Args:
        mObSig (array):             an array with the observed limited signals
        lObSigClean (list):         list with the observed limited signals with saturated signals removed
        mSaturMark (array):         an array with saturation markers
        nSamps (float):             the total number of samples in all the signals
        nSatMin (float):            the total number of saturated samples because of too low value
        nSatMax (float):            the total number of saturated samples because of too high value
        lPattsClean (list):         list with modified sampling patterns, represented as indices of sampling grid points
        lPattsTClean (list):        list with modified sampling patterns, represented as time moments
        lPattsRepClean (list):      list with modified sampling patterns, represented as indices of signal representation points
        lPhi (list):                list with observation matrices

    Returns:
        dObSig (dictionary): dictionary with the observed signals and additional data
    """

    dObSig = {}

    dObSig['mObSig'] = mObSig             # an array with the observed limited signals
    dObSig['lObSigClean'] = lObSigClean   # list with the observed limited signals with saturated signals removed
    dObSig['mSaturMark'] = mSaturMark     # an array with saturation markers

    dObSig['nSamps'] = nSamps             # the total number of samples in all the signals
    dObSig['nSatMin'] = nSatMin           # the total number of saturated samples because of too low value
    dObSig['nSatMax'] = nSatMax           # the total number of saturated samples because of too high value

    # ---------------------------------------------------------------
    if (len(lPattsClean) > 0):
        dObSig['lPattsClean'] = lPattsClean         # list with modified sampling patterns,
                                                    # represented as indices of sampling grid points
    if (len(lPattsTClean) > 0):
        dObSig['lPattsTClean'] = lPattsTClean       # list with modified sampling patterns,
                                                    # represented as time moments
    if (len(lPattsRepClean) > 0):
        dObSig['lPattsRepClean'] = lPattsRepClean    # list with modified sampling patterns,
                                                     # represented as indices of signal representation points
    # ---------------------------------------------------------------
    if not isinstance(lPhi, int):
        dObSig['lPhi'] = lPhi       # list with observation matrices

    return dObSig
