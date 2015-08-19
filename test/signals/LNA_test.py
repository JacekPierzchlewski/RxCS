"""
.. role:: bash(code)
    :language: bash

This is a test module for the low-noise nonlinear amplifier (LNA). |br|

It tests the LNA with a number of test cases, and analyzes
all the generated signals vs. the expected output signals. |br|

To start the test run this module directly as a script:

    :bash:`$ python randMultTest.py`

when in *rxcs/test* directory. The results are then printed to the console.
|br|

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0  | 19-AUG-2015 : * Version 1.0 released. |br|

*License*:
    BSD 2-Clause
"""
import numpy as np
import rxcs

def _LNA_test():
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
                          'Low-noise amplifier')

    # -----------------------------------------------------------------
    # Tests start here:

    # Tolerance of expected vs measured is 0.1%
    iTolerance = 0.1 * 1e-2

    # Case 1
    _TestCase1(iTolerance)

    # Case 2
    _TestCase2(iTolerance)

    # Case 3
    _TestCase3(iTolerance)


def _TestCase1(iTolerance):
    """
    This is test case function #1. |br|

    Args:
        iTolerance: maximum tolerance of a difference between an expected value
        and a real value

    Returns:
        Nothing
    """
    
    tStart = rxcs.console.module_progress('LNA test (case 1) SNR')

    # Define the input signal
    mSig = np.random.randn(1e3, 1e3)
    vCoef = np.array([3]) 
    mExp = 3 * mSig

    _checkLNA(mSig, vCoef, mExp, iTolerance)
    rxcs.console.module_progress_done(tStart)
    rxcs.console.info('case 1 OK!')


def _TestCase2(iTolerance):
    """
    This is test case function #2. |br|

    Args:
        iTolerance: maximum tolerance of a difference between an expected value
        and a real value

    Returns:
        Nothing
    """
    
    tStart = rxcs.console.module_progress('LNA test (case 2) SNR')

    # Define the input signal
    mSig = np.random.randn(1e4, 1e2)
    vCoef = np.array([3, 1]) 
    mExp = 3 * mSig + mSig**2

    _checkLNA(mSig, vCoef, mExp, iTolerance)
    rxcs.console.module_progress_done(tStart)
    rxcs.console.info('case 2 OK!')


def _TestCase3(iTolerance):
    """
    This is test case function #3. |br|

    Args:
        iTolerance: maximum tolerance of a difference between an expected value
        and a real value

    Returns:
        Nothing
    """
    
    tStart = rxcs.console.module_progress('LNA test (case 3) SNR')

    # Define the input signal
    mSig = np.random.randn(1e3, 1e3)
    vCoef = np.array([3, 1, 0.01, 10])
    mExp = 3 * mSig + mSig**2 + 0.01*mSig**3 + 10*mSig**4

    _checkLNA(mSig, vCoef, mExp, iTolerance)
    rxcs.console.module_progress_done(tStart)
    rxcs.console.info('case 3 OK!')


# =====================================================================
# =====================================================================
def _checkLNA(mSig, vCoef, mExp, iTolerance):
    """
    ENGINE OF THE TEST: Push the signals through the tested module and compare 
                        the output with the expected signal
    """

    # Put the LNA on the table
    LNA = rxcs.sig.LNA()  # Sparse vectors generator

    # Configure the LNA...
    LNA.mSig = mSig       # Input signal
    LNA.vCoef = vCoef     # Coefficients
    LNA.bMute = 1         # Switch off the output

    LNA.run()          # ... and run it!
    mSig = LNA.mSig    # take the generated signal
    
    # Compre the output with the expected signal
    mSig.shape = (mSig.size, ) 
    mExp.shape = (mExp.size, )
    iInx = 0
    for iEl in mSig:
        iElExp = mExp[iInx]
        iInx = iInx + 1
        
        if not _isequal(iEl, iElExp, iTolerance):
            raise Exception('LNA output: error!!!')


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
    _LNA_test()
