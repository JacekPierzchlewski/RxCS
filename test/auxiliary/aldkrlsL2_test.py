"""
.. role:: bash(code)
    :language: bash

This is the test module for the L2 solver which uses Kernel Recursive
Least Squares Method. |br|

The solver finds x which minimizes ||y - Ax||_2 for a given A and y.
In every case a number of problems as the above are randomly generated.
This script tests if the found vector x is correct with a given tolerance. |br|

To start the test run this module directly as a script:

    :bash:`$ python aldkrlsL2_test.py`

when in *rxcs/test* directory. The results are then printed to the console.
|br|

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0  |  2-DEC-2014 : * Initial version. |br|
    2.0  | 31-AUG-2015 : * Adjusted to v2.0 of the aldkrlsL2 solver. |br|


*License*:
    BSD 2-Clause
"""
from __future__ import division
import numpy as np
import rxcs


def _aldkrlsL2_test():

    # Print out the header of the signal generator test
    print('')
    rxcs.console.progress('Function under test',
                          'L2 solver which uses Kernel Recursive Least Squares Method')

    # -----------------------------------------------------------------
    # Tests start here:
    _testCase1()                       # Test case 1
    _testCase2()                       # Test case 2
    _testCase3()                       # Test case 3


# =====================================================================
# Test case # 1
# =====================================================================
def _testCase1():

    iM = 10
    iN = 6
    nTests = 1e4

    # Run the multtone signal generator
    tStart = rxcs.console.module_progress('test (case 1): ')
    _testEngine(iM, iN, nTests)
    rxcs.console.module_progress_done(tStart)
    rxcs.console.info('case 1 OK!')

# =====================================================================
# Test case # 2
# =====================================================================
def _testCase2():

    iM = 100
    iN = 50
    nTests = 1e4

    # Run the multtone signal generator
    tStart = rxcs.console.module_progress('test (case 2): ')
    _testEngine(iM, iN, nTests)
    rxcs.console.module_progress_done(tStart)
    rxcs.console.info('case 2 OK!')

# =====================================================================
# Test case # 3
# =====================================================================
def _testCase3():

    iM = 20
    iN = 11
    nTests = 1e4

    # Run the multtone signal generator
    tStart = rxcs.console.module_progress('test (case 3): ')
    _testEngine(iM, iN, nTests)
    rxcs.console.module_progress_done(tStart)
    rxcs.console.info('case 3 OK!')

# =====================================================================
# Engine of the test
# =====================================================================
def _testEngine(iM, iN, nTests):

    # Allocate the unit under test
    aldkrlsL2 = rxcs.auxiliary.aldkrlsL2()

    for inxTest in np.arange(nTests):

        if (iM < iN):
            raise Exception('The system cannot be underdefined')

        # Construct the vectors
        mA = np.random.randint(-10, 10, (iM, iN))
        vX = np.random.randint(-10,10,(iN, 1))
        vY = mA.dot(vX)
        vY.shape = (vY.size, )

        aldkrlsL2.mA = mA
        aldkrlsL2.vY = vY
        aldkrlsL2.bMute = 1
        aldkrlsL2.run()              # Find the vector X using KRLS with linear kernel
        vX_KRLS = aldkrlsL2.vX_KRLS

        iErr = np.linalg.norm(np.abs(vX_KRLS - vX.T),2)   # Find the error
        if (iErr > 1e-1):
            print(mA)
            print(vY)
            print(vX_KRLS)
            print(vX.T)

            strMsg = ('aldkr test: error for iM: %d,  iN: %d (iErr = %.12f)!!!') % (iM, iN, iErr)
            raise Exception(strMsg)


# =====================================================================
# Trigger when start as a script
# =====================================================================
if __name__ == '__main__':
    _aldkrlsL2_test()
