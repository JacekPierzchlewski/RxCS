"""
This a Random Multitone Signal Generator module. |br|

It is able to generate *N* multitone random signals according to settings
given by a user. |br|
An input dictionary, which is a sole argument to the *main*
function contains all the settings given to the generator.

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    0.1  | 15-MAY-2014 : * Initial version. |br|
    0.2  | 16-MAY-2014 : * Docstrings added. |br|
    0.3  | 19-MAY-2014 : * The main func. divided into smaller functions. |br|
    0.4  | 20-MAY-2014 : * Errors are served by 'raise'. |br|
    0.5  | 20-MAY-2014 : * Docstrings are added to the internal functions. |br|
    0.5r1| 20-MAY-2014 : * Order of the internal functions was changed. |br|
    1.0  | 20-MAY-2014 : * Version 1.0 released. |br|
    1.0r1| 21-MAY-2014 : * Error in progress printing is fixed. |br|
    1.0r2| 21-MAY-2014 : * Error in default random amplitude is fixed. |br|
    1.0r3| 21-MAY-2014 : * Error in progress printing (if muted) is fixed. |br|

*License*:
    BSD 2-Clause
"""

from __future__ import division
import numpy as np
import sys
import rxcs
from sys import stdout


def main(dSigConf):
    """
    This the main function of the generator and the only one which should be
    accessed by a user. |br|

    An input dictionary, which is a sole argument to the function
    function contains all the settings given to the generator. |br|

    The function returns a dictionary with generated signals and their
    parameters. |br|

    Please go to the *examples* directory for examples on how to use the
    generator. |br|

    Fields in the configuration dictionary:

    - a. **bMute** (*int*): mute the console output from the generator

    - b. **tS** (*float*): time of a signals

    - c. **fR** (*float*): signals representation frequency

    - d. **iSNR** (*float*): level of noise in signals [dB] (SNR)

    - e. **iP** (*float*): requested power of signals

    - f. **fMax** (*float*): maximum frequency present in signals

    - g. **fRes** (*float*): tones frequency resolution

    - h. **vFrqs** (*vector*): vector with requested frequencies of tones

    - i. **vAmps** (*vector*): vector with requested amplitudes of tones

    - j. **vPhs** (*vector*): vector with requested phases of tones

    - k. **iMinAmp** (*float*): min amplitude of a tone present in a signal

    - l. **iGraAmp** (*float*): gradation of a random amplitude of a tone

    - m. **iMaxAmp** (*float*): max amplitude of a tone present in a signal

    - n. **iMinPhs** (*float*): min allowed phase of a tone present in a signal

    - o. **iGraPhs** (*float*): gradation of a random phase of a tone

    - p. **iMaxPhs** (*float*): max allowed phase of a tone present in a signal

    - q. **nSigPack** (*float*): the number of signals to be generated


    Fields in the output dictionary:

    - a. **mSig** (*int*): Matrix with output signals

    - b. **mSigNN** (*float*): Matrix with nonnoisy output signals

    - c. **nSigs** (*float*): The number of generated signals

    - d. **fR** (*float*): Signal representation sampling frequency

    - e. **tS** (*float*): The time of the signals [s]

    - f. **nSmp** (*float*): The number of samples in the signals

    - g. **vTSig** (*float*): The time vector for the generated signals

    - h. **iSNR** (*vector*): Signal 2 noise ratio

    - i. **iP** (*vector*): Requested power of the signals

    - j. **vP** (*vector*): Power of the signals

    - k. **vPNN** (*vector*): Power of the non noisy signals

    - l. **vPCoef** (*vector*): Power adjustment coefficients

    - m. **mFrqs** (*matrix*): Frequencies of tones in the signals

    - n. **mAmps** (*matrix*): Amplitudes of tones in the signals

    - o. **mPhs** (*matrix*): Phases of tones in the signals

    - p. **mAmPh** (*matrix*): Complex matrix with amplitudes/phases of tones

    - q. **fFFTR** (*float*): Signal FFT frequency resolution


    Args:
        dSigConf (dictionary): dictionary with configuration for the generator

    Returns:
        dSig (dictionary): dictionary with generated signals and their
        parameters

    """

    # The name of the function (for error purposes)
    strFunc = 'sigRandMult.main'

    # =================================================================
    # Check the configuration dictionary and get the configuration from it
    # =================================================================

    # nSigs     -  the number of signals
    # bMute     -  mute the conole output flag
    # tS        -  time of the signal
    # fR        -  signal representation sampling frequency
    # iSNR      -  signal-to-noise-ratio
    # iP        -  power of the signal
    # fMax      -  maximum frequency
    # fRes      -  signal resolution frequency
    # vFrqs     -  vector with specified freqs
    # vAmps     -  vector with amplitudes of specified freqs
    # vPhs      -  vector with phases of specified freqs
    # nTones    -  the number of additional tones
    # iMinAmp   -  minimum amplitude of random tones
    # iGraAmp   -  gradation of amplitude of random tones
    # iMaxAmp   -  maximum amplitude of random tones
    # iMinPhs   -  minimum phase of random tones
    # iGraPhs   -  gradation of phase of random tones
    # iMaxPhs   -  maximum phase of random tones
    (nSigs,
     bMute,
     tS,
     fR,
     iSNR,
     iP,
     fMax,
     fRes,
     vFrqs,
     vAmps,
     vPhs,
     nTones,
     iMinAmp,
     iGraAmp,
     iMaxAmp,
     iMinPhs,
     iGraPhs,
     iMaxPhs) = _getConf(dSigConf)

    # - - - - - - - - - - - - - - - - - - -

    # Check the configuration
    _checkConf(dSigConf)

    # - - - - - - - - - - - - - - - - - - -

    # Print the configuration and signal parameters to the console
    tStart = _printParam(dSigConf)

    # =================================================================
    # Signal generation starts here
    # =================================================================

    # Draw frequencies of the signals
    mFrqsInx = _drawFreq(vFrqs, nTones, fMax, nSigs, fRes)

    # Draw amplitudes of the signals
    mAmps = _drawAmps(vAmps, nTones, nSigs, iMinAmp, iGraAmp, iMaxAmp)

    # Draw phases of the signals
    mPhs = _drawPhases(vPhs, nTones, nSigs, iMinPhs, iGraPhs, iMaxPhs)

    # - - - - - - - - - - - - - - - - - - -

    # Generate the signals by IFFT
    (mSig, mAmPh, mFrqs, fFFTR) = _genSigs(mFrqsInx, mAmps, mPhs,
                                           nSigs, tS, fR, fRes)

    # - - - - - - - - - - - - - - - - - - -

    # Adjust the signal power
    (mSig, vP, vPCoef, mAmps, mAmPh) = _adjPower(mSig, iP, mAmps, mAmPh)

    # Add the AWGN noise to the signals
    (mSigNN, vPNN, mSig, vP) = _addNoise(mSig, vP, iSNR)

    # =================================================================
    # Generate the output dictionary
    # =================================================================

    # Start the output dictionary
    dSig = {}

    # - - - - - - - - - - - - - - - - - - -
    dSig['mSig'] = mSig       # Matrix with output signals
    dSig['mSigNN'] = mSigNN   # Matrix with nonnoisy output signals

    dSig['nSigs'] = nSigs     # The number of generated signals

    # - - - - - - - - - - - - - - - - - - -

    dSig['fR'] = fR                 # Signal representation sampling frequency
    dSig['tS'] = tS                 # The time of the signals [s]
    (_, nSmp) = mSig.shape          # The number of samples in the signals
    dSig['nSmp'] = nSmp

    # Generate the time vector for the signal and add it to the output dict.
    vTSig = np.arange(1, nSmp+1) / fR
    dSig['vTSig'] = vTSig

    # - - - - - - - - - - - - - - - - - - -

    dSig['iSNR'] = iSNR     # Signal 2 noise ratio

    # - - - - - - - - - - - - - - - - - - -

    dSig['iP'] = iP           # Requested power of the signals
    dSig['vP'] = vP           # Power of the signals
    dSig['vPNN'] = vPNN       # Power of the non noisy signals
    dSig['vPCoef'] = vPCoef   # Power adjustment coefficients

    # - - - - - - - - - - - - - - - - - - -

    dSig['mFrqs'] = mFrqs     # Frequencies of tones in the signals
    dSig['mAmps'] = mAmps     # Amplitudes of tones in the signals
    dSig['mPhs'] = mPhs       # Phases of tones in the signals

    dSig['mAmPh'] = mAmPh     # Amp/Phases tones complex vector

    dSig['fFFTR'] = fFFTR     # Signal FFT frequency resolution

    # =================================================================
    # Signal generation is done!
    # =================================================================
    if bMute == 0:
        rxcs.console.module_progress_done(tStart)

    return dSig


# ====================================================================
# Check the configuration dictionary and get the configuration from it
# ====================================================================
def _getConf(dSigConf):
    """
    This function checks if all the needed configuration fields are in
    the configuration dictionary and gets these configuration fields.

    Args:
        dSigConf (dictionary): dictionary with configuration for the generator

    Returns:
        nSigs (float):     the number of signals
        bMute (float):     mute the conole output flag
        tS (float):        time of the signal
        fR (float):        signal representation sampling frequency
        iSNR (float):      signal-to-noise-ratio
        iP (float):        power of the signal
        fMax (float):      maximum frequency
        fRes (float):      signal resolution frequency
        vFrqs (vector):    vector with specified freqs
        vAmps (vector):    vector with amplitudes of specified freqs
        vPhs (vector):     vector with phases of specified freqs
        nTones (float):    the number of additional tones
        iMinAmp (float):   minimum amplitude of random tones
        iGraAmp (float):   gradation of amplitude of random tones
        iMaxAmp (float):   maximum amplitude of random tones
        iMinPhs (float):   minimum phase of random tones
        iGraPhs (float):   gradation of phase of random tones
        iMaxPhs (float):   maximum phase of random tones
    """

    # -----------------------------------------------------------------
    # Get the number of signals to be generated
    nSigs = int(round(dSigConf['nSigPack']))

    # -----------------------------------------------------------------
    # Mute the output parameters:
    if not 'bMute' in dSigConf:
        bMute = 0
    else:
        bMute = dSigConf['bMute']

    # -----------------------------------------------------------------
    # Signal time parameters:

    # The time of a signal [s]
    # If not given, it is an error
    strErr = ('The time of the signal [s] (tS) ')
    strErr = strErr + ('is not given in the configuration!')
    if not 'tS' in dSigConf:
        raise NameError(strErr)
    tS = dSigConf['tS']

    # The signal representation sampling freuqency [Hz]
    # If not given, it is an error
    strErr = ('The signal representation sampling freuqency [Hz] (fR) ')
    strErr = strErr + ('is not given in the configuration!')
    if not 'fR' in dSigConf:
        raise NameError(strErr)
    fR = dSigConf['fR']

    # -----------------------------------------------------------------
    # Signal noise
    if 'iSNR' in dSigConf:
        iSNR = dSigConf['iSNR']
    else:
        iSNR = np.inf

    # -----------------------------------------------------------------
    # Get the requested power of signals
    if 'iP' in dSigConf:
        iP = dSigConf['iP']
    else:
        iP = np.nan

    # -----------------------------------------------------------------
    # Signal spectrum parameters

    # The highest possible frequency in the signal [Hz]
    # If not given, it is an error
    strErr = ('The highest possible frequency in the signal [Hz] (fMax) ')
    strErr = strErr + ('is not given in the configuration!')
    if not 'fMax' in dSigConf:
        raise NameError(strErr)
    fMax = dSigConf['fMax']

    # Signal spectrum resolution [Hz]
    # If not given, it is an error
    strErr = ('Signal spectrum resolution [Hz] (fRes) ')
    strErr = strErr + ('is not given in the configuration!')
    if not 'fRes' in dSigConf:
        raise NameError(strErr)
    fRes = dSigConf['fRes']

    # -----------------------------------------------------------------
    # Get the vectors with signal cosine tones content

    # Get the vector with given frequencies of signal cosine tones content
    # (if this vector exists)
    if 'vFrqs' in dSigConf:
        vFrqs = dSigConf['vFrqs']
    else:
        vFrqs = np.zeros(0)

    # -----------------------------------------------------------------
    # Get the vector with given amplitudes of signal cosine tones content
    # (if this vector exists)
    if 'vAmps' in dSigConf:
        vAmps = dSigConf['vAmps']
    else:
        vAmps = np.zeros(0)

    # -----------------------------------------------------------------
    # Get the vector with given phases of signal cosine tones content
    # (if this vector exists)
    if 'vPhs' in dSigConf:
        vPhs = dSigConf['vPhs']
    else:
        vPhs = np.zeros(0)

    # -----------------------------------------------------------------
    # Get the number of additional tones
    # (if the number exists)
    if 'nTones' in dSigConf:
        nTones = int(round(dSigConf['nTones']))
    else:
        nTones = 0

    # -----------------------------------------------------------------
    # Get the boundaries for amplitudes

    # Amplitude min value
    if 'iMinAmp' in dSigConf:
        iMinAmp = dSigConf['iMinAmp']
    else:
        iMinAmp = 0

    # Amplitude gradation
    if 'iGraAmp' in dSigConf:
        iGraAmp = dSigConf['iGraAmp']
    else:
        iGraAmp = 0.1

    # Amplitude max value
    if 'iMaxAmp' in dSigConf:
        iMaxAmp = dSigConf['iMaxAmp']
    else:
        iMaxAmp = 1

    # -----------------------------------------------------------------
    # Get the boundaries for phases

    # Phase min value
    if 'iMinPhs' in dSigConf:
        iMinPhs = dSigConf['iMinPhs']
    else:
        iMinPhs = 0

    # Phase gradation
    if 'iGraPhs' in dSigConf:
        iGraPhs = dSigConf['iGraPhs']
    else:
        iGraPhs = 0.1

    # Phase max value
    if 'iMaxPhs' in dSigConf:
        iMaxPhs = dSigConf['iMaxPhs']
    else:
        iMaxPhs = 0

    # -----------------------------------------------------------------
    return (nSigs,            # the number of signals
            bMute,            # mute the conole output flag
            tS,               # time of the signal
            fR,               # signal representation sampling frequency
            iSNR,             # signal-to-noise-ratio
            iP,               # power of the signal
            fMax,             # maximum frequency
            fRes,             # signal resolution frequency
            vFrqs,            # vector with specified freqs
            vAmps,            # vector with amplitudes of specified freqs
            vPhs,             # vector with phases of specified freqs
            nTones,           # the number of additional tones
            iMinAmp,          # minimum amplitude of random tones
            iGraAmp,          # gradation of amplitude of random tones
            iMaxAmp,          # maximum amplitude of random tones
            iMinPhs,          # minimum phase of random tones
            iGraPhs,          # gradation of phase of random tones
            iMaxPhs)          # maximum phase of random tones


# =================================================================
# Check the configuration
# =================================================================
def _checkConf(dSigConf):
    """
    This function checks the configuration of the generator.

    Args:
        dSigConf (dictionary): dictionary with configuration for the generator

    Returns:
        nothing

    """

    # =================================================================
    # Get the configuration from the configuration dictionary

    # nSigs     -  the number of signals
    # bMute     -  mute the conole output flag
    # tS        -  time of the signal
    # fR        -  signal representation sampling frequency
    # iSNR      -  signal-to-noise-ratio
    # iP        -  power of the signal
    # fMax      -  maximum frequency
    # fRes      -  signal resolution frequency
    # vFrqs     -  vector with specified freqs
    # vAmps     -  vector with amplitudes of specified freqs
    # vPhs      -  vector with phases of specified freqs
    # nTones    -  the number of additional tones
    # iMinAmp   -  minimum amplitude of random tones
    # iGraAmp   -  gradation of amplitude of random tones
    # iMaxAmp   -  maximum amplitude of random tones
    # iMinPhs   -  minimum phase of random tones
    # iGraPhs   -  gradation of phase of random tones
    # iMaxPhs   -  maximum phase of random tones
    (nSigs,
     bMute,
     tS,
     fR,
     iSNR,
     iP,
     fMax,
     fRes,
     vFrqs,
     vAmps,
     vPhs,
     nTones,
     iMinAmp,
     iGraAmp,
     iMaxAmp,
     iMinPhs,
     iGraPhs,
     iMaxPhs) = _getConf(dSigConf)

    #----------------------------------------------------------------------
    # Check the Nyquist vs. highest possible frequency
    strErr = 'The representation sampling frequency is to low!'
    if fR <= 2*fMax:
        raise ValueError(strErr)

    #----------------------------------------------------------------------
    # Check the highest possible frequency in the signal vs spectrum
    # resolution
    strErr = 'The highest possible frequency in the signal is not a multiple '
    strErr = strErr + 'of the signal spectrum resolution'
    if (round(fMax/fRes) - fMax/fRes) > 1e-15:
        raise ValueError(strErr)

    #----------------------------------------------------------------------
    # Check if there is a space for all the frequencies requested in
    # the signal
    nFG = vFrqs.size   # the number of given frequencies
    nSpectTones = int(fMax/fRes)  # number of tones in max possible spectrum
    nSigTones = nFG + nTones  # the total number of tones

    strErr = 'The signal spectrum consists of %d tones. ' % (nSpectTones)
    strErr = strErr + 'I can not put there %d [vFrqs] + %d [nTones] tones' \
        % (nFG, nTones)
    if nSpectTones < nSigTones:
        raise ValueError(strErr)

    #----------------------------------------------------------------------
    # Check the vector with given frequencies

    # Check the vector with given frequencies, if it is longer then 0
    if nFG > 0:

        # Create the vector with given and specified frequencies (not np.nan)
        vFrqs_ = vFrqs[np.isnan(vFrqs) == 0]

        # 1. resolution:
        if np.abs(np.sum(np.round(vFrqs_/fRes) - (vFrqs_/fRes))) > 1e-15:
            strErr = ('A frequency given in the vFrqs vector is ')
            strErr = strErr + ('incoherent with the resolution of signal ')
            strErr = strErr + ('spectrum!\n')
            raise ValueError(strErr)

        # Correct possible representation errors in the vector with frequencies
        vFrqs = np.round(vFrqs/fRes)*fRes

        # 2. max frequency:
        if max(vFrqs) > fMax:
            strErr = ('The highest frequency in vFrqs vector is higher than ')
            strErr = strErr + ('the highest possible in the signal spectrum!')
            raise ValueError(strErr)

        # 3. Repeated frequency
        # Check if there is any frequency repeated in the
        # vector with given frequencies (vFrqs)
        # (only if the vector is longer than 1)
        if nFG > 1:
            vFrqsUnique = np.unique(vFrqs)

            if (vFrqsUnique.size != vFrqs.size):
                strErr = ('There are frequencies repeated in ')
                strErr = strErr + ('the vFrqs vector!')
                raise ValueError(strErr)

        # 4. All the frequencies higher than 0
        for inxFreq in np.arange(vFrqs.size):
            if vFrqs[inxFreq] <= 0:
                strErr = ('Frequencies in the vFrqs must be higher than 0!')
                raise ValueError(strErr)

    # Check the vector with given frequencies is equal to
    # the vector with given amplitudes
    # and the vector with given phases
    nAG = vAmps.size   # Calculate the number of given amplitudes
    nPG = vPhs.size    # Calculate the number of given phases

    if not ((nFG == nAG) and (nFG == nPG)):
        strErr = ('Size of the vector with given frequencies (vFrqs) must ')
        strErr = strErr + ('be equal to size of the vectors vAmps and vPhs')
        raise ValueError(strErr)

    #----------------------------------------------------------------------
    # Check the vector with given amplitudes

    # Check the vector with given amplitudes, if it is longer then 0
    if nAG > 0:

        # 1. All the amplitudes higher than 0
        for inxAmps in np.arange(vAmps.size):
            if vAmps[inxAmps] <= 0:
                strErr = ('Amplitudes in the vAmps must be higher than 0!')
                raise ValueError(strErr)

    #----------------------------------------------------------------------
    # Check the vector with given phases, if it is longer then 0
    if nPG > 0:

        # 1. All the phases must be higher than -180 and lower than 180
        for inxPhs in np.arange(vPhs.size):
            if vPhs[inxPhs] <= -180:
                strErr = ('Phases in the vPhs must be higher than -180!')
                raise ValueError(strErr)
            if vPhs[inxPhs] > 180:
                strErr = ('Phases in the vPhs must be lower than 180!')
                raise ValueError(strErr)

    #----------------------------------------------------------------------
    # The number of additional tones can not be lower than 0
    if (nTones < 0):

        strErr = ('The number of additional tones can not be lower')
        strErr = strErr + (' than 0')
        raise ValueError(strErr)

    #----------------------------------------------------------------------
    # Check if the given amplitudes boundaries make sense

    # 1. min amplitude vs. max amplitude
    if iMinAmp > iMaxAmp:
        strErr = ('Minimum possible amplitude can not be greater ')
        strErr = strErr + ('than the maximum possible amplitude!')
        raise ValueError(strErr)

    # 2. amplitude gradation
    if iGraAmp <= 0:
        strErr = ('Amplitude gradation must be higher than zero!')
        raise ValueError(strErr)

    # 3. Min amplitude and max amplitude must be higher than 0
    if iMinAmp < 0:
        strErr = ('Minimum amplitude must be higher than zero!')
        raise ValueError(strErr)
    if iMaxAmp < 0:
        strErr = ('Maximum amplitude must be higher than zero!')
        raise ValueError(strErr)

    #----------------------------------------------------------------------
    # Check if the given phase boundaries make sense

    # 1. min phase vs. max phase
    if iMinPhs > iMaxPhs:
        strErr = ('Minimum possible phase can not be greater than ')
        strErr = strErr + ('the maximum possible phase!')
        raise ValueError(strErr)

    # 2. phase gradation
    if iGraPhs <= 0:
        strErr = ('Phase gradation must be higher than zero!')
        raise ValueError(strErr)

    # 3. Min phase and max phase must be higher than -180 and lower than + 180
    if iMinPhs <= -180:
        strErr = ('Minimum phase must be higher than -180!')
        raise ValueError(strErr)
    if iMinPhs > 180:
        strErr = ('Minimum phase must be lower than 180!')
        raise ValueError(strErr)
    if iMaxPhs <= -180:
        strErr = ('Maximum phase must be higher than -180!')
        raise ValueError(strErr)
    if iMaxPhs > 180:
        strErr = ('Maximum phase must be lower than 180!')
        raise ValueError(strErr)

    #----------------------------------------------------------------------
    # Check the number of signals to be generated
    if (nSigs < 1):
        strErr = ('The number of signals to be generated must ')
        strErr = strErr + ('be higher than one!')
        raise ValueError(strErr)

    #----------------------------------------------------------------------
    # Check if there is a frequency leackage
    nSmp = int(round(tS*fR))  # Calculate the number of samples in the signals
    fFFTR = fR/nSmp    # Calculate the FFT frequency resolution

    if abs(round(fRes/fFFTR) - fRes/fFFTR) > 0:
        strErr = ('Frequency leackage! Signal spectrum resolution can not be ')
        strErr = strErr + ('represented with the current signal parameters!')
        raise ValueError(strErr)

    #----------------------------------------------------------------------
    return


# =================================================================
# # Print the configuration and signal parameters to the console
# =================================================================
def _printParam(dSigConf):
    """
    This function prints the generator configuration and the signal parameters
    to the console, if the 'bMute' flag on the configuration is cleared.

    Args:
        dSigConf (dictionary): dictionary with configuration for the generator

    Returns:
        tStart (float): time stamp of starting the generator

    """

    #----------------------------------------------------------------------
    # Get the configuration from the configuration dictionary

    # nSigs     -  the number of signals
    # bMute     -  mute the conole output flag
    # tS        -  time of the signal
    # fR        -  signal representation sampling frequency
    # iSNR      -  signal-to-noise-ratio
    # iP        -  power of the signal
    # fMax      -  maximum frequency
    # fRes      -  signal resolution frequency
    # vFrqs     -  vector with specified freqs
    # vAmps     -  vector with amplitudes of specified freqs
    # vPhs      -  vector with phases of specified freqs
    # nTones    -  the number of additional tones
    # iMinAmp   -  minimum amplitude of random tones
    # iGraAmp   -  gradation of amplitude of random tones
    # iMaxAmp   -  maximum amplitude of random tones
    # iMinPhs   -  minimum phase of random tones
    # iGraPhs   -  gradation of phase of random tones
    # iMaxPhs   -  maximum phase of random tones
    (nSigs,
     bMute,
     tS,
     fR,
     iSNR,
     iP,
     fMax,
     fRes,
     vFrqs,
     vAmps,
     vPhs,
     nTones,
     iMinAmp,
     iGraAmp,
     iMaxAmp,
     iMinPhs,
     iGraPhs,
     iMaxPhs) = _getConf(dSigConf)

    #----------------------------------------------------------------------
    # Print the configuration if the 'mute' flag is not set
    if bMute == 0:

        # Print out the header of the signal generator
        tStart = rxcs.console.progress('Signal generator', 'Random multitone')

        # - - - - - - - - - - - - - - - - - - -
        # Time parameters

        # Calculate the number of samples
        nSmp = int(round(tS*fR))

        rxcs.console.bullet_param('signal time', tS, '-m', 'seconds')
        rxcs.console.param('representation sampling frequency',
                           fR, '-M', 'MHz')
        rxcs.console.param('the number of samples', nSmp, '-', 'samples')

        # - - - - - - - - - - - - - - - - - - -
        # Frequency parameters

        # Calculate the number of given frequencies
        nFG = vFrqs.size

        # Calculate the total number of tones
        nSigTones = nFG + nTones

        # The number of tones in the maximum possible signal spectrum
        nSpectTones = int(fMax/fRes)

        # Calculate the signal sparsity
        iSpar = 1 - nSigTones / nSpectTones

        rxcs.console.bullet_param('the highest possible freq. in the signal',
                                  fMax, '-k', 'Hz')
        rxcs.console.param('signal spectrum resolution', fRes, 'k', 'Hz')
        rxcs.console.param('the number of tones in the max possible spectrum',
                           nSpectTones, '-', '')

        rxcs.console.param('the total number of tones in the signal',
                           nSigTones, '-', '')
        rxcs.console.param('the signal sparsity',
                           iSpar, ' ', '')

        rxcs.console.bullet_param('the number of given frequencies',
                                  nFG, '-', '')

        rxcs.console.bullet_param('the number of additional tones',
                                  nTones, '-', '')

        # - - - - - - - - - - - - - - - - - - -
        # Random amplitudes and phases
        rxcs.console.param('minimum amplitude', iMinAmp, ' ', '')
        rxcs.console.param('amplitude gradation', iGraAmp, ' ', '')
        rxcs.console.param('maximum amplitude', iMaxAmp, ' ', '')

        rxcs.console.param('minimum phase', iMinPhs, ' ', '')
        rxcs.console.param('amplitude phase', iGraPhs, ' ', '')
        rxcs.console.param('maximum phase', iMaxPhs, ' ', '')

        # - - - - - - - - - - - - - - - - - - -
        # Noise
        if np.isinf(iSNR) or np.isnan(iSNR):
            rxcs.console.bullet_info('noise',
                                     'not added to the signal (SNR=inf)')
        else:
            rxcs.console.bullet_param('noise (SNR)', iSNR, '-', 'dB')

        # - - - - - - - - - - - - - - - - - - -
        # Signal power
        if np.isinf(iP) or np.isnan(iP):
            rxcs.console.bullet_info('signal power', 'not adjusted')
        else:
            rxcs.console.bullet_param('signal power', iP, '-', 'W')

        # - - - - - - - - - - - - - - - - - - -
        # The number of signals
        rxcs.console.bullet_param('the number of signals to be generated',
                                  nSigs, '-', 'signals')

        # - - - - - - - - - - - - - - - - - - -
        # Information about the computations start
        tStart = rxcs.console.module_progress('signal generation starts!!!')

    #----------------------------------------------------------------------
    else:   # <- the output was muted
        tStart = np.nan

    #----------------------------------------------------------------------
    return tStart


# =================================================================
# Draw frequencies of the signals
# =================================================================
def _drawFreq(vFrqs, nTones, fMax, nSigs, fRes):
    """
    This function draws frequencies of tones for all the signals
    according to the rules specified by users,

    Args:
        vFrqs (vector):  vector with specified frequencies
        nTones (int):    the number of additional tones
        fMax (int):      the max allowed frequency in the signal spectrum
        nSigs (int):     the number of signals to be generated
        fRes (int):      signal spectrum resolution
                         (distance between the tones in the spectrum)

    Returns:
        mFrqsInx (matrix):  matrix with frequencies of tones for all
                            the signals (one row - one signal)
                            The frequencies are represented as indices of
                            frequencies from the allowed signal spectrum.

    """

    # The number of tones in the maximum possible signal spectrum
    nSpectTones = int(fMax/fRes)

    #----------------------------------------------------------------------
    # Recalculate frequencies to indices of tones in the spectrum

    # Recalculate the vector with frequencies from frequency to index
    # of a frequency in the spectrum
    vFrqsInx = (vFrqs / fRes)

    # Create a vector with GIVEN (not nan) indices of frequencies in the
    # vFrqs vector
    vFrqsInx_ = (vFrqsInx[np.isnan(vFrqsInx) == 0]).astype(int)

    #----------------------------------------------------------------------
    # Create the vector with indices of avaialble frequencies in the spectrum

    # Create a vector with inidces of all the tones in the spectrum
    vSpecInx = np.arange(1, nSpectTones + 1)

    # Boolean vector which indicates if the frequency is free
    vFreqIsFree = np.ones(nSpectTones).astype(bool)
    vFreqIsFree[vFrqsInx_ - 1] = 0

    # Create the vector with indices of available frequencies
    vAvailFreqsInx = vSpecInx[vFreqIsFree]

    #----------------------------------------------------------------------
    # Construct a vector with indices of frequencies for all the needed signals

    # Add unknown frequencies of the additional tones to the vFrqsInx vector
    vFrqsInx = np.concatenate((vFrqsInx, np.nan*np.zeros(nTones)))

    # Calculate the number of missing frequencies in the vector with
    # frequencies
    iMissF = len(vFrqsInx) - len(vFrqsInx_)

    # Construct a matrix with indices of frequencies for all the needed signals
    mFrqsInx = np.tile(vFrqsInx, (nSigs, 1))

    #----------------------------------------------------------------------
    # Draw the frequencies
    for inxSig in np.arange(nSigs):

        # Permute all the indices of frequencies in the spectrum
        vPermutedFreqsInx = ((np.random.permutation(vAvailFreqsInx)).T)

        # From the permuted indices of frequencices take as many
        # as it is missing
        vTakenFreqsInx = vPermutedFreqsInx[np.arange(iMissF)]

        # Put the taken indices of frequencies to the matrix with frequency
        # indices for all the signals
        mFrqsInx[inxSig, np.isnan(mFrqsInx[inxSig, :])] = vTakenFreqsInx

    return mFrqsInx


# =================================================================
# Draw amplitudes of the signals
# =================================================================
def _drawAmps(vAmps, nTones, nSigs, iMinAmp, iGraAmp, iMaxAmp):
    """
    This function draws amplitudes of tones for all the signals
    according to the rules specified by users,

    Args:
        vAmps (vector):  vector with specified amplitudes of tones in signals
        nTones (int):    the number of additional tones
        nSigs (int):     the number of signals to be generated
        iMinAmp (int):   min amplitude of a random tone present in a signal
        iGraAmp (int):   gradation of a amplitude of a random tone
        iMaxAmp (int):   max amplitude of a random tone present in a signal

    Returns:
        mAmps (matrix):  matrix with amplitudes of tones for all
                         the signals (one row - one signal)

    """

    # Add unknown amplitudes of the additional tones to the vAmps vector
    vAmps = np.concatenate((vAmps, np.nan*np.zeros(nTones)))

    # Compute the number of missing amplitudes for every signal
    iMissA = (vAmps[np.isnan(vAmps)]).size

    #----------------------------------------------------------------------

    # Compute the number of possible amplitude values
    nAmpVal = np.floor((iMaxAmp - iMinAmp) / iGraAmp) + 1

    #----------------------------------------------------------------------

    # Draw the missing amplitudes for all the signals
    vDrawAmps = \
        iMinAmp + iGraAmp*(np.random.randint(0, nAmpVal, (nSigs*iMissA)))

    # Construct a matrix with amplitudes of tones for all the needed signals
    mAmps = np.tile(vAmps, (nSigs, 1))

    # Put the draw amplitudes to the matrix with amplitudes of tones for
    # all the needed signals
    mAmps[np.isnan(mAmps)] = vDrawAmps

    return mAmps


# =================================================================
# Draw phases of the signals
# =================================================================
def _drawPhases(vPhs, nTones, nSigs, iMinPhs, iGraPhs, iMaxPhs):
    """
    This function draws phases of tones for all the signals
    according to the rules specified by users,

    Args:
        vPhs (vector):   vector with specified phases of tones in signals
        nTones (int):    the number of additional tones
        nSigs (int):     the number of signals to be generated
        iMinPhs (int):   min phase of a random tone present in a signal
        iGraPhs (int):   gradation of a phase of a random tone
        iMaxPhs (int):   max phase of a random tone present in a signal

    Returns:
        mPhs (matrix):   matrix with phases of tones for all
                         the signals (one row - one signal)

    """

    # Add unknown phases of the additional tones to the vAmps vector
    vPhs = np.concatenate((vPhs, np.nan*np.zeros(nTones)))

    # Compute the number of missing phases for every signal
    iMissP = (vPhs[np.isnan(vPhs)]).size

    #----------------------------------------------------------------------

    # Compute the number of possible phase values
    nPhsVal = np.floor((iMaxPhs - iMinPhs)/iGraPhs) + 1

    #----------------------------------------------------------------------

    # Draw the missing phases for all the signals
    vDrawPhs = \
        iMinPhs + iGraPhs*(np.random.randint(0, nPhsVal, (nSigs*iMissP)))

    # Construct a matrix with phases of tones for all the needed signals
    mPhs = np.tile(vPhs, (nSigs, 1))

    # Put the draw phases to the matrix with phases of tones for
    # all the needed signals
    mPhs[np.isnan(mPhs)] = vDrawPhs

    return mPhs


# =================================================================
# Generate the signals by IFFT
# =================================================================
def _genSigs(mFrqsInx, mAmps, mPhs, nSigs, tS, fR, fRes):
    """
    This function generate the multitone signals using the IFFT algorithm.

    Args:
        mFrqsInx (matrix):  matrix with freqs of tones for all the signals
                            (as indices of tones in the allowed spectrum)
        mAmps (matrix):     matrix with amplitudes of tones for all the signals
        mPhs (matrix):      matrix with phases of tones for all the signals
        nSigs (float):      the number of signals
        tS (float):         time of the signals
        fR (float):         signal representation sampling frequency
        fRes (float):       signal spectrum resolution
                            (distance between the tones in the spectrum)

    Returns:
        mSig (matrix):   matrix with signals (one row - one signal)
        mAmPh (float):   complex matrix with amplitudes/phases of tones
        mFrqs (matrix):  matrix with freqs of tones for all the signals
        fFFTR (float):   signal FFT frequency resolution
    """

    # Calculate the number of samples in the signals
    nSmp = int(round(tS*fR))

    # Calculate the FFT frequency resolution
    fFFTR = fR/nSmp

    #----------------------------------------------------------------------

    # Adjust the amplitudes value to the number of points
    mAmpsAdj = mAmps * nSmp/2

    # Change phases into radians
    mPhsRad = mPhs*np.pi/180

    # Generate a one complex matrix for all the signals and its conjugated copy
    mAmPh = mAmpsAdj*np.cos(mPhsRad) + 1j*mAmpsAdj*np.sin(mPhsRad)
    mAmPh_conj = np.conjugate(mAmPh)

    #----------------------------------------------------------------------
    # Put the complex matrix with amplitudes and phases of tones into
    # one matrix dedicated for IFFT

    # Recalculate the matrix with indices of frequencies in the spectrum
    # to real frequencies
    mFrqs = mFrqsInx*fRes

    # Recalculate the matrix with indices of frequencies in the spectrum
    # to indices of frequencies in the IFFT transform
    mIFFTFrqsInx = np.around(mFrqs/fFFTR).astype(int)

    # Allocate the vector for the ifft coefficients for all the signals
    # (one signal in one row)
    mIFFT = np.zeros((nSigs, nSmp)) + 1j*np.zeros((nSigs, nSmp))

    # Put the complex vector with tones values into the IFFT matrix
    for inxSig in np.arange(nSigs):

        # IFFT indices of tones for the current signal
        vInx = mIFFTFrqsInx[inxSig, :]

        # Put the tones for the current signal
        mIFFT[inxSig, vInx] = mAmPh[inxSig, :]

        # IFFT indices of conjugate tones for the current signal
        vInxConj = (nSmp - mIFFTFrqsInx[inxSig, :]).astype(int)

        # Put the conjugate tones for the current signal
        mIFFT[inxSig, vInxConj] = mAmPh_conj[inxSig, :]

    #----------------------------------------------------------------------
    # Generate the signals (perform the IFFT)
    mSig = np.fft.ifftn(mIFFT, axes=[1]).real

    return (mSig, mAmPh, mFrqs, fFFTR)


# =================================================================
# Adjust the signal power
# =================================================================
def _adjPower(mSig, iP, mAmps, mAmPh):
    """
    This function adjustes powers of the generated signals.
    If the requested power of the signals is equal to NaN or inf, then
    the signals are not adjusted.

    Args:
        mSig (matrix):   matrix with signals (one row - one signal)
        iP (float):      requested power of the signals
        mAmps (matrix):  matrix with amplitudes of tones in the signals
        mAmPh (matrix):  complex matrix with amplitudes/phases of tones

    Returns:
        mSig (matrix):   matrix with noisy signals
        vP (vector):     vector with powers of noisy signals
        vPCoef (vector): vector with coefficients which adjsuted the signals
        mAmps (matrix):  matrix with adjusted amplitudes of tones
        mAmPh (matrix):  complex matrix with adjusted amplitudes/phases
    """

    # Get the number of signals and the size of signals (the number of samples)
    (nSigs, nSmp) = mSig.shape

    # Measure the power of the signals
    vP = (np.sum(mSig * mSig, axis=1) / nSmp).reshape(nSigs, 1)

    # Adjust the signal power, if needed
    if not np.isnan(iP) or np.isinf(iP):

        # Compute power adjustments coefficients for the noise signals
        vPCoef = np.sqrt(iP / vP)

        # Adjust the signal power
        mPCoef = np.tile(vPCoef, (1, nSmp))
        mSig = mSig * mPCoef

        # Adjust the reported amplitudes of tones
        (_, nAmps) = mAmps.shape
        mPCoef = np.tile(vPCoef, (1, nAmps))
        mAmps = mAmps * mPCoef
        mAmPh = mAmPh * mPCoef

        # Measure the power of the adjusted signals
        vP = np.sum(mSig*mSig, axis=1) / nSmp

    else:
        # Power adjustment coefficients are equal to 1 (no adjustment)
        vPCoef = np.ones((nSigs, 1))

    return (mSig, vP, vPCoef, mAmps, mAmPh)


# =================================================================
# Add the AWGN noise to the signals
# =================================================================
def _addNoise(mSig, vP, iSNR):
    """
    This function adds noise to the generated signals.
    If the requested level of noise is equal to NaN or inf,
    then no noise is added.


    Args:
        mSig (matrix):   matrix with signals (one row - one signal)
        vP (vector):     vector with powers of signals
        iSNR (float):    wanted level of noise in the signals

    Returns:
        mSigNN (matrix): matrix with non noisy signals
        vPNN (vector):   vector with powers of non noisy signals
        mSig (matrix):   matrix with noisy signals
        vP (vector):     vector with powers of noisy signals
    """

    # Backup the non noisy signals
    mSigNN = mSig.copy()      # Matrix with signals
    vPNN = vP.copy()          # Power of non noisy signals

    # Add the noise, if needed
    if not (np.isnan(iSNR) or np.isinf(iSNR)):

        # Get the number of signals and the size of signals
        # (the number of samples)
        (nSigs, nSmp) = mSig.shape

        # Generate the noise
        mNoise = np.random.randn(nSigs, nSmp)

        # Measure the current powers of the noise signals
        vNoisePReal = (np.sum(mNoise*mNoise, axis=1) / nSmp).reshape(nSigs, 1)

        # Compute the requested noise power for every signal
        vNoiseP = (vP / (10**(iSNR/10))).reshape(nSigs, 1)

        # Compute power adjustments coefficients for the noise signals
        vPNoiseCoef = np.sqrt(vNoiseP / vNoisePReal)

        # Adjust the noise power
        mPNoiseCoef = np.tile(vPNoiseCoef, (1, nSmp))
        mNoise = mPNoiseCoef * mNoise

        # Add the noise to the signals
        mSig = mSig + mNoise

        # Measure the power of the signals
        vP = np.sum(mSig * mSig, axis=1) / nSmp

    return (mSigNN, vPNN, mSig, vP)
