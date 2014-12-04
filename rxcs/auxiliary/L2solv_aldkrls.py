"""
Module contains a solver which finds x which minimizes ||y - Ax||_2 for a given A and y.
The solver uses Kernel Recurive Least Squares algorithm with linear kenrel. |br|

Take a look on  'L2solve_aldkrls_ex0.py' in 'examples/auxiliary' directory for examples of using the module.

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0  | 2-DEC-2014 : * Initial version. |br|
    1.2  | 4-DEC-2014 : * KRLS with linear kernel in integrated into the module. |br|


*License*:
    BSD 2-Clause

"""

from __future__ import division
import numpy as np

# =====================================================================
# For a given A and y, find x which minimizes ||y - Ax||_2
# =====================================================================
def main(mA, vY):
    """
    Main function of the module. The function finds x which minimizes ||y - Ax||_2 for a given A and y |br|

    Args:
        mA (numpy array): Matrix A from the above equation

        vY (numpy array): Vector y from the above equation

    Returns:
        vX (numpy array): Vector x which solves the above problem

    """

    dAldKRLS = _krls_init()  # Construct a 'aldKRLSL' object

    (iR, _) = mA.shape                     # Get the number of rows in the matrix A

    # Training loop (loop over all rows in the matrix A)
    for i in np.arange(iR):
        dAldKRLS = _krls_train(dAldKRLS , mA[i,:], vY[i])

    vX_KRLS = _krls_evaluate(dAldKRLS)
    return vX_KRLS


def _krls_init(iALDth=1e-4, iMaxDict=1e3):
    """
    Function initializes krls dictionary. |br|

    Args:
        iALDth (float): ALD threshold [default= 1e-4]

        iMaxDict (int): Max size of the dictionary [default = 1e3]

    Returns:
        dAldKRLS (dictionary):  Python dictionary which contains all the data of the current KRLS algorithm.

        Fields in the output dictionary:

            - a. **iALDth** (*int*):   ALD threshold

            - b. **iMaxDt** (*float*):  Max size of the dictionary

            - c. **bInit** (*int*):  Initialization flag = 1. This flag is cleared with a first call to the 'train' function.
    """

    dAldKRLS = {}           # Initialize dictionary with data for aldkrls algorithm

    # Store all the parameters in the dictionary
    dAldKRLS['iALDth'] = iALDth;         # ALD threshold
    dAldKRLS['iMaxDt'] = iMaxDict;       # Maximum size of the dictionary

    dAldKRLS['bInit'] = 0      # Clear 'Initialization done' flag

    return dAldKRLS


def _krls_train(dAldKRLS, vX, vY):
    """
    Function trains the current krls algorithm. |br|

    Args:
        dAldKRLS (dictionary):  Python dictionary which contains all the data of the current KRLS algorithm.
                                Must be initialized by the *init* function from this module.

        vX (numpy array):       X training data. It should be 2D or 1D numpy array.
        vY (numpy array):       Y trainig data.

    Returns:

        dAldKRLS (dictionary):  Python dictionary which contains all the data of the current KRLS algorithm.

        Fields in the output dictionary:

            - a. **iALDth** (*int*):   ALD threshold

            - b. **iMaxDt** (*float*):  Max size of the dictionary

            - c. **bInit** (*int*):  Initialization flag = 0. This flag is cleared with a first call to the 'train' function.

            - d. **mKinv** (*numpy array*):  Kernel matrix

            - e. **vAlpha** (*numpy array*): Alpha vector

            - f. **mP** (*numpy array*): 'P' matrix

            - g. **mDict** (*numpy array*): Dictionary matrix
    """

    bInit = dAldKRLS['bInit']  # Get the initialization flag

    if (bInit == 0):
        # Initialize training:

        iKtt = (np.dot(vX,vX.T))
        dAldKRLS['mKinv'] = np.array([[1/iKtt]])
        dAldKRLS['vAlpha'] = np.array([vY/iKtt])
        dAldKRLS['mP'] = np.array([[1]])
        dAldKRLS['mDict'] = np.array([vX])

        dAldKRLS['bInit'] = 1      # Set 'Initialization done' flag

    else:
        # Training:

        if vX.ndim == 1:             # Change the shape of the input vector, if needed
            vX = np.array([vX])

        # Get the needed data from the dictionary with data
        mDict = dAldKRLS['mDict']
        vAlpha = dAldKRLS['vAlpha']
        mKinv = dAldKRLS['mKinv']
        iALDth = dAldKRLS['iALDth']        # ALD threshold
        iMaxDict = dAldKRLS['iMaxDt']      # Maximum size of the dictionary
        mP = dAldKRLS['mP']

        vK = np.dot(np.vstack((mDict, vX)), vX.T)
        vKt = vK[np.arange(0, vK.size-1)]
        iKtt = float(vK[vK.size-1])
        vAT = np.dot(mKinv, vKt)                   # AT vector

        iDelta = iKtt - float(np.dot(vKt.T, vAT))     # Delta value (integer)

        (iRowsDict, _) = mDict.shape                  # The number of rows in the dictionary


        if ((iDelta > iALDth) and (iRowsDict < iMaxDict)):  # expand, if delta is higher than
                                                            # ALD threshold, and there is a
                                                            # place size of the dictionary

            mDict = np.vstack((mDict, vX))
            mKinv = (1/iDelta)*np.vstack((np.hstack(((iDelta * mKinv + np.dot(vAT, vAT.T)), -vAT)), np.hstack((-vAT.T, np.array([[1]])))))

            (iRowsP, _) = mP.shape
            vZ = np.zeros((iRowsP, 1))

            mP = np.vstack((np.hstack((mP, vZ)), np.hstack((vZ.T, np.array([[1]])))))

            iOde = 1/iDelta * (vY - np.dot(vKt.T,vAlpha) )
            vAlpha = np.vstack(( (vAlpha - np.dot(vAT,iOde)), iOde))


        else: # only update alpha

            vQ = np.dot(mP,vAT) / (1 + np.dot(np.dot(vAT.T,mP),vAT))
            mP = mP - np.dot(vQ, (np.dot(vAT.T,mP)))
            vAlpha = vAlpha + mKinv.dot(vQ).dot(vY - (vKt.T).dot(vAlpha))

        # Store the data in the dictionary
        dAldKRLS['mDict'] = mDict
        dAldKRLS['vAlpha'] = vAlpha
        dAldKRLS['mKinv'] = mKinv
        dAldKRLS['mP'] = mP

    return dAldKRLS


def _krls_evaluate(dAldKRLS):
    """
    Function evaluates the current krls algorithm. |br|

    Args:
        dAldKRLS (dictionary):  Python dictionary which contains all the data of the current KRLS algorithm.

    Returns:

        vX (numpy array): x = alpha * dictionary, where 'alpha' and 'dictionary' are outcomes of the
                          training of the KRLS algporithm stored in the dAldKRLS dictionary

    """

    # Get the needed data from the dictionary with data
    mDict = dAldKRLS['mDict']
    vAlpha = dAldKRLS['vAlpha']

    (iRowsDict, _) = mDict.shape # Get the number of rows from the dictionary
    if iRowsDict > 0:
        vX = np.dot(vAlpha.T, mDict)
    else:
        vX = np.zeros((iRowsDict,1))

    return vX
