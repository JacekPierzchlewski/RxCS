"""
.. role:: bash(code)
    :language: bash

This is a test module for the Random Multitone Signal Generator. |br|

It tests the generator with a number of test cases, and analyzes
all of the generated signals. |br|

The following tests are performed on the generated signals:

- if the number of generated signals is correct?

- if the number of generated signals agree with the reported number?

- if the length (the number of samples) in signals is correct?

- if the number of tones in signals is correct?

- frequencies of tones:

    - if the reported frequencies agree with real frequencies in the spectrum?

    - if the requested frequencies are present in the real spectrum?

- amplitudes of tones:

    - if the reported amplitudes of tones agree with real amplitudes of tones?

    - if the requested amplitudes of tones agree with real amplitudes of tones?

    - if the random amplitudes are in the requested min/max amplitude limits?

- phases of tones:

    - if the reported phases of tones agree with real phases of tones?

    - if the requested phases of tones agree with real phases of tones?

    - if the random phases are in the requested min/max phases limits?

- power:

    - if the reported power of signals agree with real power?

    - if the requested power of signals agree with real power (if applicable)?

- noise:

    - if the requested noise in signals agree with real noise (if applicable)?


FFT analysis is used to get the real frequency, amplitude and phases of the
generated signals.

To start the test run this module directly as a script:

    :bash:`$ python randMultTest.py`

when in *rxcs/test* directory. The results are then printed to the console.
|br|

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    0.1  | 15-MAY-2014 : * Initial version. |br|
    0.2  | 15-MAY-2014 : * Docstrings added. |br|
    0.3  | 20-MAY-2014 : * PEP8 adjustments. |br|
    1.0  | 20-MAY-2014 : * Version 1.0 released. |br|
    1.1  | 15-JUL-2015 : * Adjusted to new name of random multitone gen. |br|  
    2.0  | 21-JUL-2015 : * Version 2.0 released (adjusted to v2.0 of the generator) |br|


*License*:
    BSD 2-Clause
"""

from __future__ import division
import numpy as np
import rxcs


# =====================================================================
# Main function of the test
# =====================================================================
def _randMult_test():
    """
    This is main function of the test.

    It runs the test case functions.
    An info that a test was passed is printed to the console if a case
    function returns.

    Args:
        None

    Returns:
        Nothing
    """

    # Print out the header of the signal generator test
    print('')
    rxcs.console.progress('Function under test',
                          'Random multitone signal generator')

    # -----------------------------------------------------------------
    # Tests start here:

    # Tolerance of expected vs measured is 0.1%
    iTolerance = 0.1 * 1e-2

    _TestCase1(iTolerance)
    rxcs.console.info('case 1 OK!')

    _TestCase2(iTolerance)
    rxcs.console.info('case 2 OK!')

    _TestCase3(iTolerance)
    rxcs.console.info('case 3 OK!')

    _TestCase4(iTolerance)
    rxcs.console.info('case 4 OK!')

    _TestCase5(iTolerance)
    rxcs.console.info('case 5 OK!')


# =====================================================================
# Test case 1
# =====================================================================
def _TestCase1(iTolerance):
    """
    This is test case function #1. |br|

    The function configures the Random Multitone Signal Generator,
    runs the generator and checks the generated signals using the
    *_checkSignals* function.


    Args:
        iTolerance: maximum tolerance of a difference between an expected value
        and a real value

    Returns:
        Nothing
    """

    # Put the generator on board
    gen = rxcs.sig.randMult()
    
    gen.tS = 1e-3   # Time of the signal is 1 ms
    gen.fR = 2e4    # The signal representation sampling frequency is 20 kHz
    gen.fMax = 8e3  # The highest possible frequency in the signal is 8 kHz
    gen.fRes = 1e3  # The signal spectrum resolution is 1 kHz

    gen.iSNR = 30   # Signal noise

    gen.iP = 2      # Signal power adjustments

    gen.vFrqs = np.array([2e3, np.nan, 4e3])   # Vector with given frequencies
    gen.vAmps = np.array([np.nan, 1, np.nan])  # Vector with given amplitudes
    gen.vPhs = np.array([np.nan, np.nan, 90])  # Vector with given phases

    # The number of random tones
    gen.nTones = 2

    # Amplitude and phase parameters of ranimd tones:
    gen.iMinAmp = 0.1  # Minimum amplitude
    gen.iGraAmp = 0.1  # Gradation of amplitude
    gen.iMaxAmp = 1.0  # Maximum amplitude

    gen.iMinPhs = 0   # Minimum phase of additional tones
    gen.iGraPhs = 2   # Gradation of phase of additional tones
    gen.iMaxPhs = 90  # Maximum phase of additional tones

    gen.nSigs = int(1e4)  # The number of signals to be generated
    
    gen.bMute = 1   # Mute the output from the gneerator

    # -----------------------------------------------------------------
    # Run the multtone signal generator
    tStart = rxcs.console.module_progress('test (case 1) signals generation')
    gen.run()
    rxcs.console.progress_doneNL(tStart)

    # -----------------------------------------------------------------
    # Check signals
    _checkSignals(gen, iTolerance)

    # -----------------------------------------------------------------

    return


# =====================================================================
# Test case 2
# =====================================================================
def _TestCase2(iTolerance):
    """
    This is test case function #2. |br|

    The function configures the Random Multitone Signal Generator,
    runs the generator and checks the generated signals using the
    *_checkSignals* function.


    Args:
        iTolerance: maximum tolerance of a difference between an expected value
        and a real value

    Returns:
        Nothing
    """

    # Put the generator on board
    gen = rxcs.sig.randMult()
    
    gen.tS = 1e-3     # Time of the signal is 1 ms
    gen.fR = 1e6      # The signal representation sampling frequency is 1 MHz
    gen.fMax = 100e3  # The highest possible frequency in the signal is 100 kHz
    gen.fRes = 1e3    # The signal spectrum resolution is 1 kHz

    gen.iSNR = 100    # Signal noise

    gen.iP = 10       # Signal power adjustments

    gen.vFrqs = np.array([1e3])   # Vector with given frequencies
    gen.vAmps = np.array([0.5])   # Vector with given amplitudes
    gen.vPhs = np.array([180])    # Vector with given phases

    # The number of random tones
    gen.nTones = 10

    # Amplitude and phase parameters of ranimd tones:
    gen.iMinAmp = 1.0   # Minimum amplitude
    gen.iGraAmp = 0.1   # Gradation of amplitude
    gen.iMaxAmp = 10.0  # Maximum amplitude

    gen.iMinPhs = -179  # Minimum phase of additional tones
    gen.iGraPhs = 1     # Gradation of phase of additional tones
    gen.iMaxPhs = 180   # Maximum phase of additional tones

    gen.nSigs = int(1e4)  # The number of signals to be generated
    
    gen.bMute = 1   # Mute the output from the gneerator

    # -----------------------------------------------------------------
    # Run the multtone signal generator
    tStart = rxcs.console.module_progress('test (case 2) signals generation')
    gen.run()
    rxcs.console.progress_doneNL(tStart)

    # -----------------------------------------------------------------
    # Check signals
    _checkSignals(gen, iTolerance)

    # -----------------------------------------------------------------

    return


# =====================================================================
# Test case 3
# =====================================================================
def _TestCase3(iTolerance):
    """
    This is test case function #3. |br|

    The function configures the Random Multitone Signal Generator,
    runs the generator and checks the generated signals using the
    *_checkSignals* function.


    Args:
        iTolerance: maximum tolerance of a difference between an expected value
        and a real value

    Returns:
        Nothing
    """

    # Put the generator on board
    gen = rxcs.sig.randMult()
    
    gen.tS = 1         # Time of the signal is 1 s
    gen.fR = 1e6       # The signal representation sampling frequency is 1 MHz
    gen.fMax = 20e3    # The highest possible frequency in the signal is 20 kHz
    gen.fRes = 1       # The signal spectrum resolution is 1 Hz

    gen.iSNR = np.inf  # Signal noise

    gen.iP = np.nan    # Signal power adjustments

    gen.vFrqs = np.array([1e3, np.nan, np.nan])   # Vector with given frequencies
    gen.vAmps = np.array([0.5, 1, 10])            # Vector with given amplitudes
    gen.vPhs = np.array([78, np.nan, np.nan])     # Vector with given phases

    # The number of random tones
    gen.nTones = 20

    # Amplitude and phase parameters of ranimd tones:
    gen.iMinAmp = 5.0   # Minimum amplitude
    gen.iGraAmp = 0.1   # Gradation of amplitude
    gen.iMaxAmp = 10.0  # Maximum amplitude

    gen.iMinPhs = 1     # Minimum phase of additional tones
    gen.iGraPhs = 1     # Gradation of phase of additional tones
    gen.iMaxPhs = 20    # Maximum phase of additional tones

    gen.nSigs = int(1e2)  # The number of signals to be generated
    
    gen.bMute = 1   # Mute the output from the generator

    # -----------------------------------------------------------------
    # Run the multtone signal generator
    tStart = rxcs.console.module_progress('test (case 3) signals generation')
    gen.run()
    rxcs.console.progress_doneNL(tStart)

    # -----------------------------------------------------------------
    # Check signals
    _checkSignals(gen, iTolerance)

    # -----------------------------------------------------------------

    return


# =====================================================================
# Test case 4
# =====================================================================
def _TestCase4(iTolerance):
    """
    This is test case function #4. |br|

    The function configures the Random Multitone Signal Generator,
    runs the generator and checks the generated signals using the
    *_checkSignals* function.


    Args:
        iTolerance: maximum tolerance of a difference between an expected value
        and a real value

    Returns:
        Nothing
    """

    # Put the generator on board
    gen = rxcs.sig.randMult()
    
    gen.tS = 1e-6     # Time of the signal is 1 us
    gen.fR = 1e9      # The signal representation sampling frequency is 1 GHz
    gen.fMax = 50e6   # The highest possible frequency in the signal is 50 MHz
    gen.fRes = 1e6    # The signal spectrum resolution is 1 MHz

    gen.iSNR = 100    # Signal noise

    gen.iP = 0.1      # Signal power adjustments

    gen.vFrqs = np.array([10e6, 20e6, 30e6, 40e6])  # Vector with given frequencies
    gen.vAmps = np.array([1.0, 1, 10, 20])          # Vector with given amplitudes
    gen.vPhs = np.array([78, 10, -50, -40])         # Vector with given phases

    # The number of random tones
    gen.nTones = 10

    # Amplitude and phase parameters of ranimd tones:
    gen.iMinAmp = 0.1    # Minimum amplitude
    gen.iGraAmp = 0.01   # Gradation of amplitude
    gen.iMaxAmp = 10.0   # Maximum amplitude

    gen.iMinPhs = -45   # Minimum phase of additional tones
    gen.iGraPhs = 1     # Gradation of phase of additional tones
    gen.iMaxPhs = 45    # Maximum phase of additional tones

    gen.nSigs = int(1e4)  # The number of signals to be generated
    
    gen.bMute = 1   # Mute the output from the generator

    # -----------------------------------------------------------------
    # Run the multtone signal generator
    tStart = rxcs.console.module_progress('test (case 4) signals generation')
    gen.run()
    rxcs.console.progress_doneNL(tStart)

    # -----------------------------------------------------------------
    # Check signals
    _checkSignals(gen, iTolerance)

    # -----------------------------------------------------------------

    return


# =====================================================================
# Test case 5
# =====================================================================
def _TestCase5(iTolerance):
    """
    This is test case function #5. |br|

    The function configures the Random Multitone Signal Generator,
    runs the generator and checks the generated signals using the
    *_checkSignals* function.


    Args:
        iTolerance: maximum tolerance of a difference between an expected value
        and a real value

    Returns:
        Nothing
    """

    # Put the generator on board
    gen = rxcs.sig.randMult()
    
    gen.tS = 1e-6     # Time of the signal is 1 us
    gen.fR = 1e9      # The signal representation sampling frequency is 1 GHz
    gen.fMax = 50e6   # The highest possible frequency in the signal is 50 MHz
    gen.fRes = 1e6    # The signal spectrum resolution is 1 MHz

    gen.iSNR = 10     # Signal noise

    gen.iP = np.nan   # Signal power adjustments

    # The number of random tones
    gen.nTones = 10

    # Amplitude and phase parameters of ranimd tones:
    gen.iMinAmp = 0.1    # Minimum amplitude
    gen.iGraAmp = 0.01   # Gradation of amplitude
    gen.iMaxAmp = 10.0   # Maximum amplitude

    gen.iMinPhs = -45  # Minimum phase of additional tones
    gen.iGraPhs = 1    # Gradation of phase of additional tones
    gen.iMaxPhs = 45   # Maximum phase of additional tones

    gen.nSigs = int(1e4)  # The number of signals to be generated
    
    gen.bMute = 1   # Mute the output from the generator

    # -----------------------------------------------------------------
    # Run the multtone signal generator
    tStart = rxcs.console.module_progress('test (case 5) signals generation')
    gen.run()
    rxcs.console.progress_doneNL(tStart)

    # -----------------------------------------------------------------
    # Check signals
    _checkSignals(gen, iTolerance)

    # -----------------------------------------------------------------

    return


# =====================================================================
# ENGINE OF THE TEST: Check the generated signals
# =====================================================================
def _checkSignals(gen, iTolerance):
    """
    This function is an engine of all the tests. |br|

    It passes the configuration dictionary and the signals dictionary into
    the test fucntions which perform particular tests.

    Args:

        gen: random multitone signal generator object |br|

        iTolerance: maximum tolerance of a difference between an expected value
        and a real value |br|

    Returns:
        Nothing
    """

    # Check the number of generated signals
    _checkNoOfSignals(gen)

    # Check the number of samples in the signal
    _checkNoOfSamples(gen)

    # Check the number of tones in the spectrum
    _checkNoOfTones(gen)

    # Check the frequencies of tones in the spectrum
    _checkFrequencies(gen)

    # Check the amplitudes of tones in the spectrum
    _checkAmplitudes(gen, iTolerance)

    # Check the phases of tones in the spectrum
    _checkPhases(gen, iTolerance)

    # Check the power of non noisy signals
    _checkPower(gen, iTolerance)

    # Check the noise of signals
    _checkNoise(gen, iTolerance)

    return


# =====================================================================
# This function tests the number of generated signals
# =====================================================================
def _checkNoOfSignals(gen):
    """
    This function tests if the number of generated signals is equal to the
    requested number of signals.

    Args:
        gen: random multitone signal generator object |br|

    Returns:
        Nothing
    """

    # Reset the ok flag
    bOk = 1

    # Get the correct number of generated signals
    nSigsCorr = gen.nSigs

    # Compute the number of generated signals
    (nSigsReal, _) = gen.mSigNN.shape

    # Check:
    if nSigsReal != nSigsCorr:
        bOk = 0

    # Report
    if bOk == 1:
        rxcs.console.note('the number of signals:                    ok!')
    else:
        raise Exception('the number of signals: error!!!')

    return


# =====================================================================
# This function tests the number of generated samples
# =====================================================================
def _checkNoOfSamples(gen):
    """
    This function tests the number of samples in the generated signals. |br|

    The function tests:

        - if the number of samples in the generated signals is correct.

        - if the number of samples in the generated signals is equal to
          the reported number.

    Args:
        gen: random multitone signal generator object |br|

    Returns:
        Nothing
    """

    # Reset the ok flag
    bOk = 1

    # Compute the correct number of samples in the signal
    nSmpCorr = int(np.round(gen.tS * gen.fR))

    # Get the reported number of samples in the signal
    nSmpRep = gen.nSmp

    # Compute the number of samples in the generated signals
    (_, nSmpReal) = gen.mSigNN.shape

    # Check:
    if nSmpReal != nSmpRep:
        bOk = 0
    if nSmpReal != nSmpCorr:
        bOk = 0

    # Report
    if bOk == 1:
        rxcs.console.note('the number of samples in the signals:     ok!')
    else:
        raise Exception('the number of samples in the signals: error!!!')

    return


# =====================================================================
# This function tests the number of tones in the spectrum
# =====================================================================
def _checkNoOfTones(gen):
    """
    This function tests the number of tones in the spectrum.

    The function tests:

        - if the number of tones in the generated signals is correct.

        - if the number of tones in the generated signals is equal to
          the reported number of tones.

    Args:
        gen: random multitone signal generator object |br|

    Returns:
        Nothing
    """

    # Reset the ok flag
    bOk = 1

    # Get the correct number of generated signals
    nSigsCorr = gen.nSigs

    # Compute the correct number of tones in the spectrum
    nTonesCorr = gen.vFrqs.size + gen.nTones

    # Compute the real number of tones in the spectrum
    vTonesReal = _computeTones(gen.mSigNN)

    # Get the reported number of tones in the spectrum
    (_, nTonesRep) = (gen.mFrqs).shape

    # Check:
    if nTonesRep != nTonesCorr:
        bOk = 0
    for inxSig in np.arange(nSigsCorr):  # Loop over all signals
        if vTonesReal[inxSig] != nTonesCorr:
            bOk = 0

    # Report
    if bOk == 1:
        rxcs.console.note('the number of tones in the spectrum:      ok!')
    else:
        raise Exception('the number of tones in the spectrum: error!!!')

    return


# =====================================================================
# This function tests the frequencies of tones in the spectrum
# =====================================================================
def _checkFrequencies(gen):
    """
    This function tests the frequencies of tones in the spectrum.

    The function tests:

        - if reported frequencies agree with real frequencies in the spectrum.

        - if the requested frequencies are present in the real spectrum.

    Args:
        gen: random multitone signal generator object |br|

    Returns:
        Nothing
    """

    # Reset the ok flag
    bOk = 1

    # Get the correct number of generated signals
    nSigsCorr = gen.nSigs

    # Compute the correct number of tones in the spectrum
    nTonesCorr = gen.vFrqs.size + gen.nTones

    # Get the reported frequencies of tones in the spectrum
    mFrqsRep = gen.mFrqs

    # Compute the real frequencies of tones in the spectrum
    mFrqsReal = _computeFreqs(gen.mSigNN, gen.fFFTR, nTonesCorr)

    # Check if reported frequencies agree with real frequencies in the spectrum
    for inxSig in np.arange(nSigsCorr):  # Loop over all signals

        # Take the vector with reported frequencies of the current signal
        # and sort it
        vFrqsRep = mFrqsRep[inxSig, :]
        vFrqsRep = np.sort(vFrqsRep)

        # Take the vector with real frequencies of the current signal
        # and sort it
        vFrqsReal = mFrqsReal[inxSig, :]
        vFrqsReal = np.sort(vFrqsReal)

        # Compare the vectors
        iErr = np.sum(vFrqsRep - vFrqsReal)
        if not _isequal(iErr, 0, 1e-12):
            bOk = 0

    # - - - - - - - - - - - - - - - - -
    # Check if requested frequencies are in the real spectrum

    # Get the vector with requested frequencies
    vFrqs = gen.vFrqs

    # Take only the specified frequencies
    vFrqs = vFrqs[np.isnan(vFrqs) == 0]

    # Count the number of specified requested frequencies
    nReqFrqs = vFrqs.size
    for inxSig in np.arange(nSigsCorr):  # Loop over all signals

        # Take the vector with real frequencies of the current signal
        # and sort it
        vFrqsReal = mFrqsReal[inxSig, :]

        # Check if all the requested frequencies are in the spectrum
        for inxFrq in np.arange(nReqFrqs):

            # Take the tone frequency
            iFrq = vFrqs[inxFrq]

            # Check if the tone is in the spectrum
            if np.sum(vFrqsReal == iFrq) != 1:
                bOk = 0

    # Report
    if bOk == 1:
        rxcs.console.note('frequencies of tones in the spectrum:     ok!')
    else:
        raise Exception('frequencies of tones in the spectrum: error!!!')

    return


# =====================================================================
# This function tests amplitudes of tones in the spectrum
# =====================================================================
def _checkAmplitudes(gen, iTolerance):
    """
    This function tests amplitudes of tones in the spectrum.

    The function tests:

        - if the reported amplitudes agree with the real amplitudes.

        - if the requested amplitudes of tones agree with real amplitudes of
          tones.

        - if the random amplitudes are in the requested min/max amplitude
          limits.

    Args:
        gen: random multitone signal generator object |br|

        iTolerance: maximum tolerance of a difference between an expected value
        and a real value |br|

    Returns:
        Nothing
    """

    # Reset the ok flag
    bOk = 1

    # Get the correct number of generated signals
    nSigsCorr = gen.nSigs

    # Compute the correct number of tones in the spectrum
    nTonesCorr = gen.vFrqs.size + gen.nTones

    # Compute the real amplitudes of tones in the spectrum
    (mFrqsReal, mAmpsReal) = _computeAmps(gen.mSigNN,
                                          gen.fFFTR, nTonesCorr)

    # Get the reported frequencies of tones in the spectrum
    mFrqsRep = gen.mFrqs

    # Get the reported amplitudes
    mAmpsRep = gen.mAmps

    # Get the power adjustment coefficients which were used on signals
    vPCoef = gen.vPCoef

    # - - - - - - - - - - - - - - - - -
    # Check if the reported amplitudes are equal to the real:

    # Check signal by signal
    for inxSig in np.arange(nSigsCorr):   # Loop over all signals

        # Get the real frequencies of the current signal
        vFrqsReal = mFrqsReal[inxSig, :]

        # Get the real amplitudes of the current signal
        vAmpsReal = mAmpsReal[inxSig, :]

        # - - - - - - - - - - - - - - - - -

        # Get the reported frequencies of the current signal
        vFrqsRep = mFrqsRep[inxSig, :]

        # Get the reported amplitudes of the current signal
        vAmpsRep = mAmpsRep[inxSig, :]

        # Sort the reported frequencies
        vFrqsInx = np.argsort(vFrqsRep)
        vFrqsRep = np.sort(vFrqsRep)

        # Sort the reported amplitudes of the current signal according to
        # sorted frequency sorting
        vAmpsRep = vAmpsRep[vFrqsInx]

        # - - - - - - - - - - - - - - - - -

        # Loop over all tones
        for inxTon in np.arange(nTonesCorr):

            # Check if the reported frequency is equal to the real
            if not _isequal(vFrqsReal[inxTon], vFrqsRep[inxTon],
                            iTolerance*vFrqsRep[inxTon]):
                bOk = 0

            # Check if the reported amplitude is equal to the real
            if not _isequal(vAmpsReal[inxTon], vAmpsRep[inxTon],
                            iTolerance*vAmpsReal[inxTon]):
                bOk = 0
        # - - - - - - - - - - - - - - - - -

    # - - - - - - - - - - - - - - - - -
    # Check if the requested amplitudes of tones agree with real
    # amplitudes of tones?:

    # Get the vector with requested frequencies
    vFrqs = gen.vFrqs

    # Get the number of requested frequencies
    nFrqs = vFrqs.size

    # Get the vector with requested amplitudes
    vAmps = gen.vAmps

    # Get the requested minimum amplitude of random amplitudes
    iMinAmp = gen.iMinAmp

    # Get the requested maximum amplitude of random amplitudes
    iMaxAmp = gen.iMaxAmp

    # Check signal by signal
    for inxSig in np.arange(nSigsCorr):   # Loop over all signals

        # Get the reported frequencies of the current signal
        vFrqsRep = mFrqsRep[inxSig, :]

        # Get the reported amplitudes of the current signal
        vAmpsRep = mAmpsRep[inxSig, :]

        # Get the power adjustment coefficient for the current signal
        iPCoef = vPCoef[inxSig]

        # Loop over all requested tones
        for inxTon in np.arange(nFrqs):

            # Get the requested frequency
            iF = vFrqs[inxTon]

            # Get the reported frequency
            iFRep = vFrqsRep[inxTon]

            # Get the requested amplitude
            iA = vAmps[inxTon]

            # Get the reported amplitude
            iARep = vAmpsRep[inxTon]

            # Offset the power adjustment
            iARep = iARep / iPCoef

            # Check if the reported frequency is equal to the requested
            if not np.isnan(iF):
                if not _isequal(iF, iFRep, iTolerance*iF):
                    bOk = 0

            # Check if the requested amplitude was given explicitely
            if not np.isnan(iA):

                # Check if the reported amplitude is equal to the requested
                if not _isequal(iA, iARep, iTolerance*iA):
                    bOk = 0

            # Check if the requested amplitude was given explicitely
            else:  # <- was not given explicitly

                # Check if the random amplitude was drawn correctly
                if iA > iMaxAmp * (1 + iTolerance) or \
                   iA < iMinAmp * (1 - iTolerance):
                        bOk = 0

    # - - - - - - - - - - - - - - - - -

    # Report
    if bOk == 1:
        rxcs.console.note('amplitudes of tones in the spectrum:      ok!')
    else:
        raise Exception('amplitudes of tones in the spectrum: error!!!')

    # -----------------------------------------------------------------

    return


# =====================================================================
# This function tests phases of tones in the spectrum
# =====================================================================
def _checkPhases(gen, iTolerance):
    """
    This function tests phases of tones in the spectrum

    The function tests:

        - if the reported phases agree with the real phases.

        - if the requested phases of tones agree with real phases of
          tones.

        - if the random phases are in the requested min/max phases
          limits.

    Args:
        gen: random multitone signal generator object |br|

        iTolerance: maximum tolerance of a difference between an expected value
        and a real value |br|

    Returns:
        Nothing
    """

    # Reset the ok flag
    bOk = 1

    # Get the correct number of generated signals
    nSigsCorr = gen.nSigs

    # Compute the correct number of tones in the spectrum
    nTonesCorr = gen.vFrqs.size + gen.nTones

    # Compute the real phases of tones in the spectrum
    (mFrqsReal, mPhsReal) = _computePhs(gen.mSigNN,
                                        gen.fFFTR, nTonesCorr)

    # Get the reported frequencies of tones in the spectrum
    mFrqsRep = gen.mFrqs

    # Get the reported phases
    mPhsRep = gen.mPhs

    # - - - - - - - - - - - - - - - - -
    # Check if the reported phases are equal to the real:

    # Check signal by signal
    for inxSig in np.arange(nSigsCorr):   # Loop over all signals

        # Get the real frequencies of the current signal
        vFrqsReal = mFrqsReal[inxSig, :]

        # Get the real phases of the current signal
        vPhsReal = mPhsReal[inxSig, :]

        # - - - - - - - - - - - - - - - - -

        # Get the reported frequencies of the current signal
        vFrqsRep = mFrqsRep[inxSig, :]

        # Get the reported phases of the current signal
        vPhsRep = mPhsRep[inxSig, :]

        # Sort the reported frequencies
        vFrqsInx = np.argsort(vFrqsRep)
        vFrqsRep = np.sort(vFrqsRep)

        # Sort the reported phases of the current signal according to
        # sorted frequency sorting
        vPhsRep = vPhsRep[vFrqsInx]

        # - - - - - - - - - - - - - - - - -

        # Loop over all tones
        for inxTon in np.arange(nTonesCorr):

            # Check if the reported frequency is equal to the real
            if not _isequal(vFrqsReal[inxTon], vFrqsRep[inxTon],
                            iTolerance*vFrqsRep[inxTon]):
                bOk = 0

            # Take the real phase and put it to the range -180 <--> +180
            iPhsReal = vPhsReal[inxTon]
            if iPhsReal <= -180:
                iPhsReal = iPhsReal + 360
            if iPhsReal > 180:
                iPhsReal = iPhsReal - 360

            # Take the reported phase and put it to the range -180 <--> +180
            iPhsRep = vPhsRep[inxTon]
            if iPhsRep <= -180:
                iPhsRep = iPhsRep + 360
            if iPhsRep > 180:
                iPhsRep = iPhsRep - 360

            # Check if the reported phases is equal to the real
            if not _isequal(iPhsReal, iPhsRep, iTolerance*iPhsRep):

                # Check the case where one value is =~ -180, other =~ +180
                if _isequal(iPhsReal, -180, iTolerance*iPhsReal):
                    iPhsReal = iPhsReal + 360
                if _isequal(iPhsRep, -180, iTolerance*iPhsRep):
                    iPhsRep = iPhsRep + 360
                if not _isequal(iPhsReal, iPhsRep, iTolerance*iPhsRep):
                    bOk = 0
        # - - - - - - - - - - - - - - - - -

    # - - - - - - - - - - - - - - - - -
    # Check if the reported phases are as requested:

    # Get the vector with requested frequencies
    vFrqs = gen.vFrqs

    # Get the number of requested frequencies
    nFrqs = vFrqs.size

    # Get the vector with requested phases
    vPhs = gen.vPhs

    # Get the requested minimum phase of random phases
    iMinPhs = gen.iMinPhs

    # Get the requested maximum phase of random phases
    iMaxPhs = gen.iMaxPhs

    # Check signal by signal
    for inxSig in np.arange(nSigsCorr):   # Loop over all signals

        # Get the reported frequencies of the current signal
        vFrqsRep = mFrqsRep[inxSig, :]

        # Get the reported phases of the current signal
        vPhsRep = mPhsRep[inxSig, :]

        # Loop over all requested tones
        for inxTon in np.arange(nFrqs):

            # Get the requested frequency
            iF = vFrqs[inxTon]

            # Get the reported frequency
            iFRep = vFrqsRep[inxTon]

            # Take the requested phase and put it to the range -180 <--> +180
            iPhs = vPhs[inxTon]
            if iPhs <= -180:
                iPhs = iPhs + 360
            if iPhs > 180:
                iPhs = iPhs - 360

            # Take the reported phase and put it to the range -180 <--> +180
            iPhsRep = vPhsRep[inxTon]
            if iPhsRep <= -180:
                iPhsRep = iPhsRep + 360
            if iPhsRep > 180:
                iPhsRep = iPhsRep - 360

            # Check if the reported frequency is equal to the requested
            if not np.isnan(iF):
                if not _isequal(iF, iFRep, iTolerance * iF):
                    bOk = 0

            # Check if the requested phase was given explicitly
            if not np.isnan(iPhs):

                # Check if the reported phase is equal to the requested
                if not _isequal(iPhs, iPhsRep, iTolerance * iPhs):

                    # Check the case where one value is =~ -180, other =~ +180
                    if _isequal(iPhs, -180, iTolerance*iPhs):
                        iPhs = iPhs + 360
                    if _isequal(iPhsRep, -180, iTolerance * iPhsRep):
                        iPhsRep = iPhsRep + 360
                    if not _isequal(iPhs, iPhsRep, iTolerance * iPhsRep):
                        bOk = 0

            # Check if the requested phase was given explicitely
            else:  # <- was not given explicitly

                # Check if the random phase was drawn correctly
                if (iPhs > iMaxPhs * (1 + iTolerance)) or \
                   (iPhs < iMinPhs * (1 - iTolerance)):
                        bOk = 0

    # - - - - - - - - - - - - - - - - -

    # Report
    if bOk == 1:
        rxcs.console.note('phases of tones in the spectrum:          ok!')
    else:
        raise Exception('phases of tones in the spectrum: error!!!')

    # -----------------------------------------------------------------

    return


# =====================================================================
# This function tests the power of signals
# =====================================================================
def _checkPower(gen, iTolerance):
    """
    This function tests the power of generated signals.

    The function tests:

        - if the reported power agree with the real power.

        - if the real power of generated signals agree with
          the requested power (if it was requested).

    Args:
        gen: random multitone signal generator object |br|

        iTolerance: maximum tolerance of a difference between an expected value
        and a real value |br|

    Returns:
        Nothing
    """

    # Reset the ok flag
    bOk = 1

    # Compute the correct number of samples in the signal
    nSmpCorr = int(np.round(gen.tS * gen.fR))

    # Get the correct number of generated signals
    nSigsCorr = gen.nSigs

    # Take the matrix with non noisy signals
    mSigNN = gen.mSigNN

    # Compute the real power of non noisy signals
    vPNN = (np.sum(mSigNN * mSigNN, axis=1) / nSmpCorr)

    # - - - - - - - - - - - - - - - - -
    # Compare the reported power of non noisy signals with the real power of
    # non noisy sygnals

    # Get the reported power of nonnoisy signals
    vPNNRep = gen.vPNN

    # Compare the reported power with the real power
    for inxSig in np.arange(nSigsCorr):       # Loop over all signal

        # Get the reported power of the current non noisy signal
        iPNNRep = vPNNRep[inxSig]

        # Get the real power of the current non noisy signal
        iPNN = vPNN[inxSig]

        # Compare the real power with the reported power
        if not _isequal(iPNN, iPNNRep, iPNNRep*iTolerance):
            bOk = 0

    # - - - - - - - - - - - - - - - - -
    # Compare the requested power of nonoisy signals with the real power of
    # non noisy sygnals

    # Get the requested power of signals
    iPCorr = gen.iP

    # Check, if the power adjustment was requested
    if not np.isnan(iPCorr) and not np.isinf(iPCorr):
        for inxSig in np.arange(nSigsCorr):       # Loop over all signals

            # Get the real power of the current non noisy signal
            iPNN = vPNN[inxSig]

            # Compare the real power with the requested power
            if not _isequal(iPNN, iPCorr, iPCorr*iTolerance):
                bOk = 0

    # - - - - - - - - - - - - - - - - -
    # Compare the reported power of noisy signals with the real power of
    # noisy sygnals

    # Take the matrix with noisy signals
    mSig = gen.mSig

    # Compute the real power of noisy signals
    vP = np.sum(mSig * mSig, axis=1) / nSmpCorr

    # Get the reported power of noisy signals
    vPRep = gen.vP

    # Compare the reported power with the real power
    for inxSig in np.arange(nSigsCorr):       # Loop over all signals

        # Get the real power of the current noisy signal
        iP = vP[inxSig]

        # Get the reported power of the current noisy signal
        iPRep = vPRep[inxSig]

        # Compare the real power with the reported power
        if not _isequal(iP, iPRep, iTolerance*iP):
            bOk = 0

    # Report
    if bOk == 1:
        rxcs.console.note('power of the signals:                     ok!')
    else:
        raise Exception('power of the signals: error!!!')

    # -----------------------------------------------------------------

    return


# =====================================================================
# This function tests the noise in signals
# =====================================================================
def _checkNoise(gen, iTolerance):
    """
    This function tests the noise in the generated signals.

    The function tests:

        - if the real level of noise in  generated signals agree with the
          requested level of nosie (if it was requested).

    Args:
        gen: random multitone signal generator object |br|

        iTolerance: maximum tolerance of a difference between an expected value
        and a real value |br|

    Returns:
        Nothing
    """

    # Reset the ok flag
    bOk = 1

    # Compute the correct number of samples in the signal
    nSmpCorr = int(np.round(gen.tS * gen.fR))

    # Get the correct number of generated signals
    nSigsCorr = gen.nSigs

    # Get the requested noise in the signals
    iSNR = gen.iSNR

    # Take the matrix with non noisy signals
    mSigNN = gen.mSigNN

    # Take the matrix with noisy signals
    mSig = gen.mSig

    # Get the vector with the power of non noisy signals
    vPNN = gen.vPNN

    if not np.isnan(iSNR) and not np.isinf(iSNR):

        # Compute the noise in the signals
        mNoise = mSigNN - mSig

        # Compute the correct power of noise
        vPnCorr = vPNN / (10**(iSNR/10))

        # Compute the real power of noises
        vPn = np.sum(mNoise * mNoise, axis=1) / nSmpCorr

        # Compare the real power of noise with the requested power of noise
        for inxSig in np.arange(nSigsCorr):       # Loop over all noise signals

            # Get the current power of noise
            iPn = vPn[inxSig]

            # Get the correct power of noise
            iPnCorr = vPnCorr[inxSig]

            # Compare the real power of noise with the requested power of noise
            if not _isequal(iPn, iPnCorr, iPnCorr * iTolerance):
                bOk = 0

        # Report
        if bOk == 1:
            rxcs.console.note('level of noise in the signals:            ok!')
        else:
            raise Exception('level of noise in the signals: error!!!')

    else:
        # Report
        strMessage = 'level of noise in the signals:            not tested!'
        rxcs.console.note(strMessage)
    # -----------------------------------------------------------------

    return bOk


# =====================================================================
# This function counts the number of tones in the spectrum
# =====================================================================
def _computeTones(mSig):
    """
    This function counts the number of tones in the spectrum of signals.

    It analyzes every signal with FFT and returns the number of
    positive tones with an amplitude higher than 1e-4.

    Args:
        mSig:  matrix with generated signals (one signal in a row)

    Returns:
        vTones: vector with the number of tones in the spectrum
    """

    # Perform the fft of all the signals
    mFFT = np.fft.fftn(mSig, axes=[1])

    # Compute the amplitudes of tones
    mFFTA = np.abs(mFFT)
    mFFTA[mFFTA < 1e-4] = 0     # Clear the matrix

    # Compute the number of tones
    mFFTA[mFFTA >= 1e-4] = 1
    vNTones = np.sum((mFFTA), 1)
    vNTones = (vNTones / 2).astype(int)

    # Return the vector with the number of tones
    return vNTones


# =====================================================================
# This function computes real frequencies of tones in the spectrum
# =====================================================================
def _computeFreqs(mSig, fFFTR, nTones):
    """
    This function computes real frequencies of tones in the spectrum of
    signals.

    It analyzes every signal with FFT and returns the frequencies of
    positive tones with an amplitude higher than 1e-4.

    Args:
        mSig:  matrix with generated signals (one signal in a row) |br|
        fFFTR: FFT frequency resolution |br|
        nTones: the number of tones in every signal |br|

    Returns:
        mFrqsReal:   matrix with frequencies of tones in the signal
    """

    # Get the number of signals
    (nSigs, _) = mSig.shape

    # Perform the fft of all the signals
    mFFT = np.fft.fftn(mSig, axes=[1])

    # Get the number elements in the IFFT spectrum
    (_, nIFFT) = mFFT.shape

    # Take only half of the IFFT spectrum
    mFFT = mFFT[:, np.arange(nIFFT / 2).astype(int)]

    # Get the number elements in the half of the IFFT spectrum
    (_, nIFFT) = mFFT.shape

    # Create a vector with frequencies of tones in the IFFT spectrum
    vFrqs = fFFTR*np.arange((nIFFT))

    # Compute the amplitudes of tones
    mFFTA = np.abs(mFFT)
    mFFTA[mFFTA < 1e-4] = 0     # Clear the matrix

    # Denote the present tones with 1
    mFFTA[mFFTA >= 1e-4] = 1

    # Allocate the matrix for frequencies of tones
    mFrqsReal = np.zeros((nSigs, nTones))

    # Compute the real frequencies
    for inxSig in np.arange(nSigs):
        mFrqsReal[inxSig, :] = vFrqs[mFFTA[inxSig, :] == 1]

    # Return the matrix with frequencies
    return mFrqsReal


# =====================================================================
# This function computes real amplitudes of tones in the spectrum
# =====================================================================
def _computeAmps(mSig, fFFTR, nTones):
    """
    This function computes real amplitudes of tones in the spectrum of
    signals.

    It analyzes every signal with FFT and returns the amplitudes of
    positive tones with an amplitude higher than 1e-4.

    Args:
        mSig:  matrix with generated signals (one signal in a row) |br|
        fFFTR: FFT frequency resolution |br|
        nTones: the number of tones in every signal |br|

    Returns:
        mFrqsReal: matrix with frequencies of tones in the signal |br|
        mAmpsReal: matrix with amplitudes of tones in the signal |br|
    """

    # Get the number of signals
    (nSigs, _) = mSig.shape

    # Get the number of samples in the IFFT spectrum
    (_, nIFFT) = mSig.shape

    # Perform the fft of all the signals
    mFFT = np.fft.fftn(mSig, axes=[1])*2/nIFFT

    # Take only half of the IFFT spectrum
    mFFT = mFFT[:, np.arange(nIFFT / 2).astype(int)]

    # Get the number elements in the half of the IFFT spectrum
    (_, nIFFT) = mFFT.shape

    # Create a vector with frequencies of tones in the IFFT spectrum
    vFrqs = fFFTR*np.arange((nIFFT))

    # Compute the amplitudes of tones
    mFFTA = np.abs(mFFT)
    mFFTA[mFFTA < 1e-4] = 0     # Clear the matrix

    # Denote the present tones with 1
    mFFTA_ = mFFTA.copy()
    mFFTA_[mFFTA > 1e-4] = 1

    # Allocate the matrix for frequencies of tones
    mFrqsReal = np.zeros((nSigs, nTones))

    # Allocate the matrix for amplitudes of tones
    mAmpsReal = np.zeros((nSigs, nTones))

    # Compute the real frequencies
    for inxSig in np.arange(nSigs):

        # Take only these tones, which have an amplitude higher than 1e-4
        mFrqsReal[inxSig, :] = vFrqs[mFFTA_[inxSig, :] == 1]

        # Get amplitudes of the frequencies
        mAmpsReal[inxSig, :] = mFFTA[inxSig, mFFTA_[inxSig, :] == 1]

    # Return the matrices with frequncies and amplitudes
    return (mFrqsReal, mAmpsReal)


# =====================================================================
# This function computes real phases of tones in the spectrum
# =====================================================================
def _computePhs(mSig, fFFTR, nTones):
    """
    This function computes real phases of tones in the spectrum of
    signals.

    It analyzes every signal with FFT and returns the phases of
    positive tones with an amplitude higher than 1e-4.

    Args:
        mSig:  matrix with generated signals (one signal in a row) |br|
        fFFTR: FFT frequency resolution |br|
        nTones: the number of tones in every signal |br|

    Returns:
        mFrqsReal: matrix with frequencies of tones in the signal |br|
        mPhsReal: matrix with phases of tones in the signal |br|
    """

    # Get the number of signals
    (nSigs, _) = mSig.shape

    # Get the number of samples in the IFFT spectrum
    (_, nIFFT) = mSig.shape

    # Perform the fft of all the signals
    mFFT = np.fft.fftn(mSig, axes=[1])*2/nIFFT
    mFFT[np.abs(mFFT) < 1e-4] = 0

    # Take only half of the IFFT spectrum
    mFFT = mFFT[:, np.arange(nIFFT / 2).astype(int)]

    # Get the number elements in the half of the IFFT spectrum
    (_, nIFFT) = mFFT.shape

    # Create a vector with frequencies of tones in the IFFT spectrum
    vFrqs = fFFTR*np.arange((nIFFT))

    # Compute the amplitudes of tones
    mFFTA = np.abs(mFFT)
    mFFTA[mFFTA < 1e-4] = 0     # Clear the matrix

    # Compute the phases of tones
    mFFTP = np.angle(mFFT)
    mFFTP[np.abs(mFFTP) < 1e-4] = 0    # Clear the matrix

    # Denote the present tones with 1
    mFFTA[mFFTA > 0] = 1

    # Allocate the matrix for frequencies of tones
    mFrqsReal = np.zeros((nSigs, nTones))

    # Allocate the matrix for phases of tones
    mPhsReal = np.zeros((nSigs, nTones))

    # Compute the real frequencies
    for inxSig in np.arange(nSigs):

        # Take only these tones, which have an amplitude higher than 1e-4
        mFrqsReal[inxSig, :] = vFrqs[mFFTA[inxSig, :] == 1]

        # Get phases of the frequencies
        pi = np.pi
        mPhsReal[inxSig, :] = mFFTP[inxSig, mFFTA[inxSig, :] == 1] * 180 / pi

    # Return the matrices with frequncies and amplitudes
    return (mFrqsReal, mPhsReal)


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

    if (abs(iX - iY) <= np.abs(iMargin)):
        return 1
    else:
        return 0


# =====================================================================
# Trigger when start as a script
# =====================================================================
if __name__ == '__main__':
    _randMult_test()
