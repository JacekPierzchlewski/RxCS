"""
This module generates Inverse Discrete Hartley Transform. |br|


*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0  | 13-JAN-2015 : * Initial version. |br|

*License*:
    BSD 2-Clause

"""
from __future__ import division
import rxcs
import numpy as np


def main(dCSConf):
    """
    Main function of the module.

    Args:
        dCSConf (dictionary): Dictionary with configuration for the module

    Returns:
        mDict (time) : Time stamp of the module start
        dDict (dictionary):  Dictionary with auxiliary data for the module

    """
    # =================================================================
    # Check the configuration and print it to the console
    # =================================================================

    # Print the configuration to the console
    tStart = _printConf(dCSConf)

    # - - - - - - - - - - - - - - - - - - -

    # Check if the configuration for the dictionary make sense
    _checkConf(dCSConf)

    # - - - - - - - - - - - - - - - - - - -

    # =================================================================
    # Generate the IDHT dictionary matrix
    # =================================================================
    (mDict, vF, vT) = _generateIDHT(dCSConf)

    # =================================================================
    # Generate the output dictionary
    # =================================================================
    dDict = _generateOutput(dCSConf, mDict, vF, vT)

    # =================================================================
    # Dictionary generation is done!
    # =================================================================
    if not np.isnan(tStart):   # <-tStart is nan = console output is off
        rxcs.console.module_progress_done(tStart)

    return (mDict, dDict)


# =================================================================
# Print the configuration to the console
# =================================================================
def _printConf(dCSConf):
    """
    This function prints all the parameters of the dicitonary to the console,
    if only the bMute flag is not set.

    Args:
        dCSConf (dictionary): Dictionary with configuration for the module

    Returns:
        tStart (time) : Time stamp of the module start

    """

    # -----------------------------------------------------------------
    # Check and get the configuration from the configuration dictionary

    # bMute     -  mute the conole output flag
    # tS        -  time length covered by the dictionary
    # tStart    -  optional time shift
    # fR        -  signal representation sampling frequency
    # fDelta    -  frequency distance between tones
    # nTones    -  the number of tones
    (bMute, tS, tStart, fR, _, fDelta, nTones) = _getConf(dCSConf)

    # -----------------------------------------------------------------
    # Compute the parameters of the dictionary

    # Tg           - the signal representation period
    # tStart_real  - signal time start represented by the dictionary
    # tS_real      - correct signal time length represented by the dict.
    # tEnd         - signal time end represented by the dictionary
    # nSamp        - the number of signal samples represented by the dict.
    # fHigh        - the high frequency limit of the dictionary
    (Tg,
     tStart_real, tS_real, tEnd, nSamp, fHigh) = _computeParam(dCSConf)


    #----------------------------------------------------------------------
    # Print the configuration if the 'mute' flag is not set
    if bMute == 0:

        # Print out the header of the dictionary matrix generator
        rxcs.console.progress('Signal dictionary', 'IDFT')

        # - - - - - - - - - - - - - - - - - - -

        # Print the time parameters
        _printConfT(Tg, tS, tStart, tStart_real, tS_real, tEnd, nSamp)

        # Print the frequency parameters
        _printConfF(fDelta, nTones, fHigh)

        # Check for Nyquist and print a warning if needed
        _checkNyquist(fR, fHigh)

        # - - - - - - - - - - - - - - - - - - -
        # Information about the computations start
        tStart = rxcs.console.module_progress('dict. generation starts!!!')

    #----------------------------------------------------------------------
    else:   # <- the output was muted, no time stamp of the start is required
        tStart = np.nan

    #----------------------------------------------------------------------
    return tStart


# =================================================================
# Get data from the configuration dictionary and check it
# =================================================================
def _getConf(dCSConf):
    """
    This function gets module settings from the configuration dictionary
    and checks if all the needed settings are in place.

    Args:
        dCSConf (dictionary): Dictionary with configuration for the module

    Returns:
        bMute   (flag)     mute the conole output flag
        tS      (number)   time length covered by the dictionary
        tStart  (number)   optional time shift
        fR      (number)   signal representation sampling frequency
        fFirst  (number)   first frequency in the spectrum
        fDelta  (number)   frequency distance between tones
        nTones  (number)   the number of tones
    """

    # -----------------------------------------------------------------
    # Get the mute flag
    if not 'bMute' in dCSConf:
        bMute = 0
    else:
        bMute = dCSConf['bMute']

    # -----------------------------------------------------------------
    # Get the time length covered by the dictionary
    if not 'tS' in dCSConf:
        strError = ('The time covered by the dictionary (tS) ')
        strError = strError + ('is not given in the configuration')
        raise NameError(strError)
    else:
        tS = dCSConf['tS']

    # -----------------------------------------------------------------
    # Get the optional time shift
    if not 'tStart' in dCSConf:
        tStart = 0
    else:
        tStart = dCSConf['tStart']

    # -----------------------------------------------------------------
    # Get the signal representation sampling frequency
    if not 'fR' in dCSConf:
        strError = ('The signal representation sampling frequency (fR) ')
        strError = strError + ('is not given in the configuration')
        raise NameError(strError)
    else:
        fR = dCSConf['fR']

    # -----------------------------------------------------------------
    # Get the frequency separation between tones
    if not 'fDelta' in dCSConf:
        strError = ('The frequency separation between tones (fDelta) ')
        strError = strError + ('is not given in the configuration')
        raise NameError(strError)
    else:
        fDelta = dCSConf['fDelta']

    # -----------------------------------------------------------------
    # Get the first frequency in the spectrum
    if not 'fFirst' in dCSConf:
        fFirst = fDelta
    else:
        fFirst = dCSConf['fFirst']

    # -----------------------------------------------------------------
    # Get the number of tones
    if not 'nTones' in dCSConf:
        strError = ('The number of tones (nTones) is not given ')
        strError = strError + ('is not given in the configuration')
        raise NameError(strError)
    else:
        nTones = dCSConf['nTones']

    # -----------------------------------------------------------------
    return (bMute,     # mute the conole output flag
            tS,        # time length covered by the dictionary
            tStart,    # optional time shift
            fR,        # signal representation sampling frequency
            fFirst,    # first frequency in the spectrum
            fDelta,    # frequency distance between tones
            nTones)    # the number of tones


# =================================================================
# Compute the parameters of the dictionary
# =================================================================
def _computeParam(dCSConf):
    """
    This function computes the parameters of the dictionary based on the
    given settings.

    Args:
        dCSConf (dictionary): Dictionary with configuration for the module

    Returns:
        Tg           (number)  the signal representation period
        tStart_real  (number)  the signal representation period
        tS_real      (number)  correct signal time length represented by the dict.
        tEnd         (number)  signal time end represented by the dictionary
        nSamp        (number)  the numb. of signal samples represented by the dict.
        fHigh        (number)  the high frequency limit of the dictionary
    """

    # -----------------------------------------------------------------
    # Check and get the configuration from the configuration dictionary

    # tS        -  time length covered by the dictionary
    # tStart    -  optional time shift
    # fR        -  signal representation sampling frequency
    # fFirst    -  first frequency in the spectrum
    # fDelta    -  frequency distance between tones
    # nTones    -  the number of tones
    (_, tS, tStart, fR, fFirst, fDelta, nTones) = _getConf(dCSConf)

    # -----------------------------------------------------------------
    # Compute the time parameters of the dictionary
    (Tg, tStart_real, tS_real, tEnd, nSamp) = _computeParamT(tS, fR, tStart)

    # Compute the frequency parameters of the dictionary
    (fHigh) = _computeParamF(fFirst, fDelta, nTones)

    # -----------------------------------------------------------------
    return (Tg,           # the signal representation period
            tStart_real,  # the signal representation period
            tS_real,      # correct signal time length represented by the dict.
            tEnd,         # signal time end represented by the dictionary
            nSamp,        # the numb. of signal samples represented by the dict.
            fHigh)        # the high frequency limit of the dictionary

# =================================================================
# Compute the parameters of the dictionary
# =================================================================
def _computeParamT(tS, fR, tS_shift):
    """
    This function computes the time parameters of the dictionary based on the
    given settings.
    """

    # Compute the signal representation period
    Tg = 1/fR

    # Signal time start represented by the dictionary
    tStart_real = np.round(tS_shift / Tg)*Tg

    # The number of signal samples represented by the dictionary
    nSamp = int(np.round(tS / Tg))

    # Correct ssignal time length represented by the dictionary
    tS_real = nSamp * Tg

    # Signal time end represented by the dictionary
    tEnd = tStart_real + tS_real

    # -----------------------------------------------------------------
    return (Tg, tStart_real, tS_real, tEnd, nSamp)


# =================================================================
# Compute the frequency limit of the dict.
# =================================================================
def _computeParamF(fFirst, fDelta, nTones):
    """
    This function computes the frequency limit of the dictionary based
    on the given settings.
    """

    # The positive low frequency limit of the dictionary
    fFirstHigh = np.floor(fFirst/fDelta) * fDelta

    # The positive high frequency limit of the dictionary
    fHigh = fFirstHigh + fDelta * (nTones - 1)

    # -------------------------------------------------------------
    return (fHigh)


# =================================================================
# Print the time parameters of the dictionary
# =================================================================
def _printConfT(Tg, tS, tStart, tStart_real, tS_real, tEnd, nSamp):
    """
    This function prints the time parameters of the dictionary
    """

    # Signal time length represented by the dictionary
    rxcs.console.bullet_param('Signal time length represented by the dict',
                              tS_real, '-', 'seconds')

    if not _isequal(tS_real, tS, 1e-12*tS_real):
        rxcs.console.param('the requested signal time length',
                            tS, '-', 'seconds')

    #----------------------------------------------------------------------
    # The time start and the time end, if time start different than zero

    if (tStart_real != 0) or (tStart != 0):

        rxcs.console.param('the time start represented by the dictionary',
                        tStart_real, '-', 'seconds')

        if not _isequal(tStart, tStart_real, 1e-6*tStart):
            rxcs.console.param('requested time start',
                        tStart, '-', 'seconds')

        rxcs.console.param('the time end represented by the dictionary',
                        tEnd, '-', 'seconds')

    #----------------------------------------------------------------------
    # The signal representation sampling frequency and period
    rxcs.console.bullet_param('the signal representation sampling frequency',
                              1/Tg, '-', 'Hz')
    rxcs.console.param('the signal representation sampling period',
                              Tg, '-', 'seconds')
    rxcs.console.param('the number of signal samples',
                              nSamp, '-', 'samples')

    #----------------------------------------------------------------------
    return


# =================================================================
# Print the frequency parameters of the dictionary
# =================================================================
def _printConfF(fDelta, nTones, fHigh):
    """
    This function prints the frequency parameters of the dictionary
    """

    rxcs.console.param('the number of tones in the dictionary',
                              nTones, '-', '')

    rxcs.console.param('frequency separation between the tones',
                              fDelta, '-', 'Hz')

    rxcs.console.param('the highest frequency in the spectrum is',
                              fHigh, '-', 'Hz')

    #----------------------------------------------------------------------
    return


# =================================================================
# Check the highest frequency represented by the dictionary vs.
# the signal representation sampling frequency
# =================================================================
def _checkNyquist(fR, fHigh):
    """
    This function checks if the signal representation sampling frequency
    is high enough to represent the highest tone frequency in the dictionary
    according to the Nyquist principle.
    """

    #----------------------------------------------------------------------
    # Check the highest frequency represented by the dictionary vs.
    # the signal representation sampling frequency
    if not fR > 2*fHigh:
        strWarn = ('The signal representation frequency is too small ')
        strWarn = strWarn + ('to represent max frequency in the dictionary')
        rxcs.console.warning(strWarn)

    #----------------------------------------------------------------------
    return


# =================================================================
# Check if the configuration parameters make sense
# =================================================================
def _checkConf(dCSConf):
    """
    This function checks if the module settings given in the dictionary
    make sense.
    """

    # -----------------------------------------------------------------
    # Check the given configuration

    # tS        -  time length covered by the dictionary
    # fR        -  signal representation sampling frequency
    # fFirst    -  first frequency in the spectrum
    # fDelta    -  frequency separation between tones
    # nTones    -  the number of tones
    (_, tS, _, fR, fFirst, fDelta, nTones) = _getConf(dCSConf)

    if not tS > 0:
        strErr = ('The time covered by the dictionary (tS) ')
        strErr = strErr + ('must be higher than zero')
        raise ValueError(strErr)

    if not fR > 0:
        strErr = ('The signal representation sampling frequency (fR) ')
        strErr = strErr + ('must be higher than zero')
        raise ValueError(strErr)

    if not fFirst > 0:
        strErr = ('The first frequency in the spectrum (fFirst) ')
        strErr = strErr + ('must be higher than zero')
        raise ValueError(strErr)

    if not fDelta > 0:
        strErr = ('The frequency separation between tones (fDelta) ')
        strErr = strErr + ('must be higher than zero')
        raise ValueError(strErr)

    if not nTones > 0:
        strErr = ('The number of tones (nTones) ')
        strErr = strErr + ('must be higher than zero')
        raise ValueError(strErr)

    # -----------------------------------------------------------------
    # Check the signal time covered by the dictionary after correction

    # tS_real      - correct signal time length represented by the dict.
    (_, _, tS_real, _, _, _ ) = _computeParam(dCSConf)

    if not tS_real > 0:
        strErr = ('The time covered by the dictionary ')
        strErr = strErr + ('must be higher than zero')
        raise ValueError(strErr)

    return


# =================================================================
# ENGINE: generate the matrix with IDHT dictionary
# =================================================================
def _generateIDHT(dCSConf):
    """
    This function is the core of the dictionary generation.
    """
    # -----------------------------------------------------------------
    # Check and get the configuration from the configuration dictionary

    # fFirst    -  first frequency in the spectrum
    # fDelta    -  frequency distance between tones
    # nTones    -  the number of tones
    (_, _, _, _, fFirst, fDelta, nTones) = _getConf(dCSConf)

    # Tg           - the signal representation period
    # tStart_real  - signal time start represented by the dictionary
    # nSamp        - the number of signal samples represented by the dict.

    (Tg, tStart_real, _, _, nSamp, _) = _computeParam(dCSConf)

    # -----------------------------------------------------------------
    # Generate the time vector
    vT =  Tg * np.arange(nSamp) + tStart_real
    vT.shape = (1,vT.size)                     # Make a 2D horizontal vector

    # -----------------------------------------------------------------
    # Generate the frequency vector
    vF = np.arange(fFirst, fFirst+(fDelta*nTones), fDelta)
    vF.shape = (vF.size, 1)                    # Make it a 2D vertical vector

    # -----------------------------------------------------------------
    # Generate the Dictionary matrix
    mFT = np.dot(vF,vT)
    mFT = 2*np.pi*mFT                 # Frequency / time matrix
    mCos = np.cos(mFT)                # Cosine part of the matrix
    mSin = np.sin(mFT)                # Sinus part of the matrrix
    mDict = np.vstack((mCos,mSin))    # IDHT matrix

    # -----------------------------------------------------------------
    # -----------------------------------------------------------------
    vF.shape = (vF.size, )
    vT.shape = (vT.size, )

    return (mDict, vF, vT)

# =====================================================================
# This function compares two values.
# The function allows for a very small error margin
# =====================================================================
def _isequal(iX, iY, iMargin):
    """
    This function checks if a difference between two values is in the
    given allowed margin.

    Args:
        iX: the first value |br|
        iY: the second value |br|
        iMargin: the allowed margin |br|

    Returns:
        1: if the difference between the given values does not exceed the
           given margin |br|
        0: if the difference between the given values does exceed the
           given margin |br|
    """

    if iX < 1e-12:  # <- very small values will create problems due to
                    #    floating point representation problems
        return 1

    if (abs(iX - iY) <= np.abs(iMargin)):
        return 1
    else:
        return 0


# =================================================================
# Generate the output dictionary
# =================================================================
def _generateOutput(dCSConf, mDict, vF, vT):
    """
    This function generates auxiliary dictionary with all the paramters
    of a generated IDHT matrix. This dictionary is returned by the main
    function as a second argument.

    """

    # -----------------------------------------------------------------
    # Get the frequency configuration from the configuration dictionary

    # fFirst    -  first frequency in the spectrum
    # fDelta    -  frequency separation between tones
    # nTones    -  the number of tones
    (_, _, _, _, fFirst, fDelta, nTones) = _getConf(dCSConf)

    # -----------------------------------------------------------------
    # Compute the parameters of the dictionary

    # Tg           - the signal representation period
    # tStart_real  - signal time start represented by the dictionary
    # tS_real      - correct signal time length represented by the dict.
    # tEnd         - signal time end represented by the dictionary
    # nSamp        - the number of signal samples represented by the dict.
    # fHigh        - the high frequency limit of the dictionary
    (Tg,
     tStart_real, tS_real, tEnd, nSamp, fHigh) = _computeParam(dCSConf)

    # -----------------------------------------------------------------
    # Initialize the output dictionary
    dDict = {}

    # - - - - - - - - - - - - - - - - - -

    dDict['mDict'] = mDict   # <- matrix with the dictionary

    dDict['vF'] = vF   # <- vector with frequencies represented by the dict.

    dDict['vT'] = vT   # <- vector with time samples represented by the dict.

    # - - - - - - - - - - - - - - - - - -

    dDict['Tg'] = Tg   # <- the signal representation period

    dDict['tS_real'] = tS_real   # <- correct signal time length represented
                                 # by the dictionary

    dDict['tStart_real'] = tStart_real   # <- signal time start represented by
                                         # the dictionary

    dDict['tEnd'] = tEnd   # <- signal time end represented by the dictionary

    dDict['nSamp'] = nSamp   # <- the number of signal samples represented by
                             # the dictionary

    # - - - - - - - - - - - - - - - - - -

    dDict['fFirst'] = fFirst   # <- first frequency in the spectrum

    dDict['fDelta'] = fDelta   # <- frequency separation between tones

    dDict['nTones'] = nTones   # <- the number of tones in the dictionary

    dDict['fHigh'] = fHigh     # <- the high frequency limit of the dict,

    # -----------------------------------------------------------------
    return dDict
