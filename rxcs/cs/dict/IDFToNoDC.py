from __future__ import division
import time
import rxcs
import numpy as np


def main(dCSConf):

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
    # Generate the IDFT dictionary matrix
    # =================================================================
    (mDict, vF, vT) = _generateIDFToNoDC(dCSConf)

    # =================================================================
    # Generate the output dictionary
    # =================================================================
    dDict = _generateOutput(dCSConf, mDict, vF, vT)

    # =================================================================
    # Signal sampling is done!
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
        dCSConf (dictionary)

    Returns:
        tStart (time )

    """

    # -----------------------------------------------------------------
    # Check and get the configuration from the configuration dictionary

    # bMute     -  mute the conole output flag
    # tS        -  time length covered by the dictionary
    # tStart    -  optional time shift
    # fR        -  signal representation sampling frequency
    # fDelta    -  frequency distance between tones
    # nTones    -  the number of tones
    (bMute, tS, tStart, fR, fDelta, nTones) = _getConf(dCSConf)

    # -----------------------------------------------------------------
    # Compute the parameters of the dictionary

    # Tg           - the signal representation period
    # tStart_real  - signal time start represented by the dictionary
    # tS_real      - correct signal time length represented by the dict.
    # tEnd         - signal time end represented by the dictionary
    # nSamp        - the number of signal samples represented by the dict.
    # fLow         - the negative frequency limit of the dictionary
    # fHigh        - the positive frequency limit of the dictionary
    (Tg,
     tStart_real, tS_real, tEnd, nSamp,
     fLow, fHigh) = _computeParam(dCSConf)

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
# Print the time parameters of the dictionary
# =================================================================
def _printConfT(Tg, tS, tStart, tStart_real, tS_real, tEnd, nSamp):

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

    rxcs.console.bullet_param('the number of tones in the dictionary',
                              nTones, '-', '')

    rxcs.console.param('frequency separation between the tones',
                              fDelta, '-', 'Hz')

    rxcs.console.param('max frequency of a tone in the dictionary',
                              fHigh, '-', 'Hz')

    #----------------------------------------------------------------------
    return


# =================================================================
# Check the highest frequency represented by the dictionary vs.
# the signal representation sampling frequency
# =================================================================
def _checkNyquist(fR, fHigh):

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
# Check the configuration dict. and get the configuration from it
# =================================================================
def _getConf(dCSConf):

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
            fDelta,    # frequency distance between tones
            nTones)    # the number of tones


# =================================================================
# Compute the parameters of the dictionary
# =================================================================
def _computeParam(dCSConf):

    # -----------------------------------------------------------------
    # Check and get the configuration from the configuration dictionary

    # tS        -  time length covered by the dictionary
    # tStart    -  optional time shift
    # fR        -  signal representation sampling frequency
    # fDelta    -  frequency distance between tones
    # nTones    -  the number of tones
    (_, tS, tStart, fR, fDelta, nTones) = _getConf(dCSConf)

    # -----------------------------------------------------------------
    # Compute the time parameters of the dictionary
    (Tg, tStart_real, tS_real, tEnd, nSamp) = _computeParamT(tS, fR, tStart)

    # -----------------------------------------------------------------
    # Compute the negative and positive frequency limits of the dictionary
    (fLow, fHigh) = _computeParamF(fDelta, nTones)

    # -----------------------------------------------------------------
    return (Tg,           # the signal representation period
            tStart_real,  # signal time start represented by the dictionary
            tS_real,      # correct signal time length represented by the dict.
            tEnd,         # signal time end represented by the dictionary
            nSamp,        # the numb. of signal samples represented by the dict.
            fLow,         # the negative frequency limit of the dictionary
            fHigh)        # the positive frequency limit of the dictionary


# =================================================================
# Compute the parameters of the dictionary
# =================================================================
def _computeParamT(tS, fR, tS_shift):

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
# Compute the negative and positive frequency limits of the dict.
# =================================================================
def _computeParamF(fDelta, nTones):

    # The negative frequency limit of the dictionary
    fLow = -fDelta * nTones

    # The positive frequency limit of the dictionary
    fHigh = fDelta * nTones

    # -------------------------------------------------------------
    return (fLow, fHigh)


# =================================================================
# Check if the configuration parameters make sense
# =================================================================
def _checkConf(dCSConf):

    # -----------------------------------------------------------------
    # Check the given configuration

    # tS        -  time length covered by the dictionary
    # fR        -  signal representation sampling frequency
    # fDelta    -  frequency separation between tones
    # nTones    -  the number of tones
    (_, tS, _, fR, fDelta, nTones) = _getConf(dCSConf)

    if not tS > 0:
        strErr = ('The time covered by the dictionary (tS) ')
        strErr = strErr + ('must be higher than zero')
        raise ValueError(strErr)

    if not fR > 0:
        strErr = ('The signal representation sampling frequency (fR) ')
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
    (_, _, tS_real, _, _, _, _) = _computeParam(dCSConf)

    if not tS_real > 0:
        strErr = ('The time covered by the dictionary ')
        strErr = strErr + ('must be higher than zero')
        raise ValueError(strErr)

    return


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
# ENGINE: generate the matrix with dictionary
# =================================================================
def _generateIDFToNoDC(dCSConf):

    # -----------------------------------------------------------------
    # Check and get the configuration from the configuration dictionary

    # fDelta    -  frequency distance between tones
    # nTones    -  the number of tones
    (_, _, _, _, fDelta, nTones) = _getConf(dCSConf)

    # Tg           - the signal representation period
    # tStart_real  - signal time start represented by the dictionary
    # nSamp        - the number of signal samples represented by the dict.
    (Tg, tStart_real, _, _, nSamp, _, _) = _computeParam(dCSConf)

    # -----------------------------------------------------------------
    # Generate the time vector
    vT =  Tg * np.arange(nSamp) + tStart_real
    vT.shape = (1,vT.size)

    # -----------------------------------------------------------------
    # Generate the frequency vector
    vF_pos = np.arange(1,nTones+1)
    vF_neg = -1 * np.arange(1,nTones+1)
    vF_neg.sort()
    vF = fDelta * np.concatenate( (vF_pos, vF_neg) )
    vF.shape = (vF.size, 1)

    # -----------------------------------------------------------------
    # Generate the Dictionary matrix
    d = (1j*2*np.pi)   # d coefficient
    mDict = 0.5*np.e**np.dot(vF,(d*vT) )

    # -----------------------------------------------------------------
    vF.shape = (vF.size, )
    vT.shape = (vT.size, )
    return (mDict, vF, vT)


# =================================================================
# Generate the output dictionary
# =================================================================
def _generateOutput(dCSConf, mDict, vF, vT):

    # -----------------------------------------------------------------
    # Get the frequency configuration from the configuration dictionary

    # fDelta    -  frequency separation between tones
    # nTones    -  the number of tones
    (_, _, _, _, fDelta, nTones) = _getConf(dCSConf)

    # -----------------------------------------------------------------
    # Compute the parameters of the dictionary

    # Tg           - the signal representation period
    # tStart_real  - signal time start represented by the dictionary
    # tS_real      - correct signal time length represented by the dict.
    # tEnd         - signal time end represented by the dictionary
    # nSamp        - the number of signal samples represented by the dict.
    # fLow         - the negative frequency limit of the dictionary
    # fHigh        - the positive frequency limit of the dictionary
    (Tg,
     tStart_real, tS_real, tEnd, nSamp,
     fLow, fHigh) = _computeParam(dCSConf)

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

    dDict['fDelta'] = fDelta   # <- frequency separation between tones

    dDict['nTones'] = nTones   # <- the number of tones in the dictionary

    dDict['fLow'] = fLow   # <- the negative frequency limit of the dictionary

    dDict['fHigh'] = fHigh   # <- the positive frequency limit of the
                             #    dict,

    # -----------------------------------------------------------------
    return dDict
