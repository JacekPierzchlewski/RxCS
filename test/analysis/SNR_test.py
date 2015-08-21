"""
.. role:: bash(code)
    :language: bash

This is the test module for the SNR evaluation of the reconstructed signal.
|br|

It tests the SNR evaluator with the number of test cases,
and analyzes the results.

In every case random multitone signals are generated with a specified
level of noise. The Random Multitone Signal Generator is used to generate
the signals. The non noisy signal from the generator is treated as the orignal
signal, the noisy signal is treated as the reconstructed signal. |br|

The following tests are performed on the results of evaluation:

- if the measured level of noise for every signal is correct?

- if the measured average level of noise is correct?

- if the measured success ratio of the reconsteruction is correct?


To start the test run this module directly as a script:

    :bash:`$ python SNR_test.py`

when in *rxcs/test/analysis* directory. 
The results are then printed to the console.
|br|

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    0.1  | 20-MAY-2014 : * Initial version. |br|
    0.2  | 21-MAY-2014 : * Success Ratio check added. |br|
    0.3  | 21-MAY-2014 : * Docstrings added. |br|
    0.4  | 21-MAY-2014 : * UUT now configured with a dicionary. |br|
    1.0  | 21-MAY-2014 : * Version 1.0 released. |br|
    2.0  | 21-AUG-2015 : * Adjusted to SNR analysis v2.0 (objectified) |br| 

*License*:
    BSD 2-Clause
"""
from __future__ import division
import numpy as np
import rxcs


# =====================================================================
# Main function of the test
# =====================================================================
def _SNR_test():
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
                          'SNR evaluation of the reconstructed signal')

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

    The function sets up the configuration dictionary for the Random Multitone
    Signal Generator and runs the engine of the test.

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

    gen.nSigs = int(1e5)  # The number of signals to be generated
    
    gen.bMute = 1   # Mute the output from the gneerator

    # -----------------------------------------------------------------
    # ENGINE OF THE TEST:
    # Generate signals with a given SNR, measure the SNR and check if
    # the measured value is correct
    _checkSNR(gen, iTolerance)

    return


# =====================================================================
# Test case 2
# =====================================================================
def _TestCase2(iTolerance):
    """
    This is test case function #2. |br|

    The function sets up the configuration dictionary for the Random Multitone
    Signal Generator and runs the engine of the test.

    Args:
        iTolerance: maximum tolerance of a difference between an expected value
        and a real value

    Returns:
        Nothing
    """

    # Put the generator on board
    gen = rxcs.sig.randMult()
    
    gen.tS = 1e-1     # Time of the signal is 100 ms
    gen.fR = 1e6      # The signal representation sampling frequency is 1 MHz
    gen.fMax = 100e3  # The highest possible frequency in the signal is 100 kHz
    gen.fRes = 1e3    # The signal spectrum resolution is 1 kHz

    gen.iSNR = 100    # Signal noise

    gen.iP = 10      # Signal power adjustments

    gen.vFrqs = np.array([1e3])   # Vector with given frequencies
    gen.vAmps = np.array([0.5])   # Vector with given amplitudes
    gen.vPhs = np.array([180])    # Vector with given phases

    # The number of random tones
    gen.nTones = 10

    # Amplitude and phase parameters of ranimd tones:
    gen.iMinAmp = 1.0   # Minimum amplitude
    gen.iGraAmp = 0.1   # Gradation of amplitude
    gen.iMaxAmp = 10.0  # Maximum amplitude

    gen.nSigs = int(1e3)  # The number of signals to be generated
    
    gen.bMute = 1   # Mute the output from the gneerator

    # -----------------------------------------------------------------
    # ENGINE OF THE TEST:
    # Generate signals with a given SNR, measure the SNR and check if
    # the measured value is correct
    _checkSNR(gen, iTolerance)

    return

# =====================================================================
# Test case 3
# =====================================================================
def _TestCase3(iTolerance):
    """
    This is test case function #3. |br|

    The function sets up the configuration dictionary for the Random Multitone
    Signal Generator and runs the engine of the test.

    Args:
        iTolerance: maximum tolerance of a difference between an expected value
        and a real value

    Returns:
        Nothing
    """

    # Put the generator on board
    gen = rxcs.sig.randMult()
    
    gen.tS = 1       # Time of the signal is 1 s
    gen.fR = 1e6     # The signal representation sampling frequency is 1 MHz
    gen.fMax = 20e3  # The highest possible frequency in the signal is 20 kHz
    gen.fRes = 1     # The signal spectrum resolution is 1 Hz

    gen.iSNR = 5   # Signal noise

    gen.vFrqs = np.array([1e3, np.nan, np.nan])   # Vector with given frequencies
    gen.vAmps = np.array([0.5, 1, 10])            # Vector with given amplitudes
    gen.vPhs = np.array([78, np.nan, np.nan])     # Vector with given phases

    # The number of random tones
    gen.nTones = 20

    # Amplitude and phase parameters of ranimd tones:
    gen.iMinAmp = 5.0   # Minimum amplitude
    gen.iGraAmp = 0.1   # Gradation of amplitude
    gen.iMaxAmp = 10.0  # Maximum amplitude

    gen.iMinPhs = 1   # Minimum phase of additional tones
    gen.iGraPhs = 1   # Gradation of phase of additional tones
    gen.iMaxPhs = 20  # Maximum phase of additional tones

    gen.nSigs = int(1e2)  # The number of signals to be generated
    
    gen.bMute = 1   # Mute the output from the gneerator

    # -----------------------------------------------------------------
    # ENGINE OF THE TEST:
    # Generate signals with a given SNR, measure the SNR and check if
    # the measured value is correct
    _checkSNR(gen, iTolerance)

    return


# =====================================================================
# Test case 4
# =====================================================================
def _TestCase4(iTolerance):
    """
    This is test case function #4. |br|

    The function sets up the configuration dictionary for the Random Multitone
    Signal Generator and runs the engine of the test.

    Args:
        iTolerance: maximum tolerance of a difference between an expected value
        and a real value

    Returns:
        Nothing
    """

    # Put the generator on board
    gen = rxcs.sig.randMult()
    
    gen.tS = 1e-6    # Time of the signal is 1 us
    gen.fR = 1e9     # The signal representation sampling frequency is 1 GHz
    gen.fMax = 50e6  # The highest possible frequency in the signal is 50 MHz
    gen.fRes = 1e6   # The signal spectrum resolution is 1 MHz

    gen.iSNR = 45   # Signal noise

    gen.iP = 0.1      # Signal power adjustments

    gen.vFrqs = np.array([10e6, 20e6, 30e6, 40e6])   # Vector with given frequencies
    gen.vAmps = np.array([1.0, 1, 10, 20])   # Vector with given amplitudes
    gen.vPhs = np.array([78, 10, -50, -40])  # Vector with given phases

    # The number of random tones
    gen.nTones = 10

    # Amplitude and phase parameters of ranimd tones:
    gen.iMinAmp = 0.1  # Minimum amplitude
    gen.iGraAmp = 0.01  # Gradation of amplitude
    gen.iMaxAmp = 10.0  # Maximum amplitude

    gen.iMinPhs = -45   # Minimum phase of additional tones
    gen.iGraPhs = 1     # Gradation of phase of additional tones
    gen.iMaxPhs = 45    # Maximum phase of additional tones

    gen.nSigs = int(1e4)  # The number of signals to be generated
    
    gen.bMute = 1   # Mute the output from the gneerator

    # -----------------------------------------------------------------
    # ENGINE OF THE TEST:
    # Generate signals with a given SNR, measure the SNR and check if
    # the measured value is correct
    _checkSNR(gen, iTolerance)

    return


# =====================================================================
# Test case 5
# =====================================================================
def _TestCase5(iTolerance):
    """
    This is test case function #5. |br|

    The function sets up the configuration dictionary for the Random Multitone
    Signal Generator and runs the engine of the test.

    Args:
        iTolerance: maximum tolerance of a difference between an expected value
        and a real value

    Returns:
        Nothing
    """

    # Put the generator on board
    gen = rxcs.sig.randMult()
    
    gen.tS = 1e-6    # Time of the signal is 1 us
    gen.fR = 1e9     # The signal representation sampling frequency is 1 GHz
    gen.fMax = 50e6  # The highest possible frequency in the signal is 50 MHz
    gen.fRes = 1e6   # The signal spectrum resolution is 1 MHz

    gen.iSNR = 12   # Signal noise

    # The number of random tones
    gen.nTones = 10

    # Amplitude and phase parameters of ranimd tones:
    gen.iMinAmp = 0.1   # Minimum amplitude
    gen.iGraAmp = 0.01  # Gradation of amplitude
    gen.iMaxAmp = 10.0  # Maximum amplitude

    gen.iMinPhs = -45   # Minimum phase of additional tones
    gen.iGraPhs = 1     # Gradation of phase of additional tones
    gen.iMaxPhs = 45    # Maximum phase of additional tones

    gen.nSigs = int(1e4)  # The number of signals to be generated
    
    gen.bMute = 1   # Mute the output from the gneerator

    # -----------------------------------------------------------------
    # ENGINE OF THE TEST:
    # Generate signals with a given SNR, measure the SNR and check if
    # the measured value is correct
    _checkSNR(gen, iTolerance)

    return


# =====================================================================
# ENGINE OF THE TEST: Generate signals with a given SNR, measure the SNR and
#                     check it
# =====================================================================
def _checkSNR(gen, iTolerance):
    """
    This is the engine of the test.

    The function runs the signal generator, measure the SNR using the tested
    SNR evaluation and tests the measured SNR values for every signal and
    the average level of SNR. Is also checks the reported Success Ratio.

    Args:
        gen:  The Random Multitone Signal Generator
        iTolerance (float): maximum tolerance of a difference between an
                            expected value and a real value
    Returns:
        nothing

    """
    # Succcess ratio if SNR > 20 [db]
    iSNRSuccess = 20

    # -----------------------------------------------------------------
    # Run the multtone signal generator
    tStart = \
        rxcs.console.module_progress('signals generation')
    gen.run()
    rxcs.console.progress_done(tStart)

    # -----------------------------------------------------------------
    # Run the SNR evaluation
    analysisSNR = rxcs.ana.SNR()

    analysisSNR.mSigRef = gen.mSigNN        # Nonnoisy signal from the generator is a a reference signal 
    analysisSNR.mSig = gen.mSig             # Generated signal is a signal under test  
    analysisSNR.iSNRSuccess = iSNRSuccess
    analysisSNR.bMute = 1
    tStart = rxcs.console.module_progress('SNR computation')
    analysisSNR.run()
    rxcs.console.progress_doneNL(tStart)

    # -----------------------------------------------------------------
    # Check the measured SNR vs the reported orignal SNR

    # Get the number of signals
    nSigPack = gen.nSigs

    # Get the vector with measured SNR values
    vSNR = analysisSNR.vSNR

    # Check the vector with measured SNR values
    for inxSig in np.arange(nSigPack):
        iSNR_meas = vSNR[inxSig]
        if not _isequal(gen.iSNR, iSNR_meas, iTolerance):
            raise Exception('measured SNR: error!!!')

    # Check the average SNR
    iSNR_avg = analysisSNR.iSNR
    if not _isequal(gen.iSNR, iSNR_avg, iTolerance):
        raise Exception('measured average SNR: error!!!')

    # -----------------------------------------------------------------
    # Check the success ratio

    # The expected success ratio
    if gen.iSNR >= iSNRSuccess:
        iSR_expected = 1
    else:
        iSR_expected = 0

    # Check the expected success ratio
    iSR = analysisSNR.iSR  # Measured success ratio
    if not _isequal(iSR_expected, iSR, iTolerance):
        raise Exception('measured SNR success ratio: error!!!')

    # -----------------------------------------------------------------
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

    if (abs(iX - iY) <= np.abs(iMargin)):
        return 1
    else:
        return 0


# =====================================================================
# Trigger when start as a script
# =====================================================================
if __name__ == '__main__':
    _SNR_test()
