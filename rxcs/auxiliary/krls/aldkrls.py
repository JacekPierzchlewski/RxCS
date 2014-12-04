"""
This module contains implementation of Kernel Recurive Least Squares algorithm with
Approximate Linear Dependency criterion. |br|

Take a look on  'aldkrls_ex0.py'  in  'examples/auxiliary'  for examples of using the module.

*Authors*:

This implementation is based on Matlab implementation in 'Kafbox' by Steven Van Vaerenbergh.

    2012 - 2014 Steven Van Vaerenbergh (Matlab version: http://sourceforge.net/projects/kafbox/)
    2014        Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0  | 3-DEC-2014 : * Initial version. |br|

*License*:
    BSD 2-Clause

"""

from __future__ import division
import numpy as np
import kernel

def init(strKernel, iKernelPar=1, iALDth=1e-4, iMaxDict=1e3):
    """
    Function initializes krls dictionary. |br|

    Args:

        strKernel (string): Type of the kernel

        iKernelPar (float): Kernel parameter [default = 1]

        iALDth (float): ALD threshold [default = 1e-4]

        iMaxDict (int): Max size of the dictionary [default = 1e3]


    Returns:
        dAldKRLS (dictionary):  Python dictionary which contains all the data of the current KRLS algorithm.

        Fields in the output dictionary:

            - a. **iALDth** (*int*):   ALD threshold

            - b. **iMaxDt** (*float*):  Max size of the dictionary

            - c. **strKernel** (*string*):  Type of the kernel

            - d. **iKernelPar** (*float*):  Kernel parameter

            - e. **bInit** (*int*):  Initialization flag = 1. This flag is cleared with a first call to the 'train' function.
    """

    dAldKRLS = {}           # Initialize dictionary with data for aldkrls algorithm

    # Store all the parameters in the dictionary
    dAldKRLS['iALDth'] = iALDth;         # ALD threshold
    dAldKRLS['iMaxDt'] = iMaxDict;       # Maximum size of the dictionary
    dAldKRLS['strKernel'] = strKernel    # Type of the kernel
    dAldKRLS['iKernelPar'] = iKernelPar  # Kernel parameter
    dAldKRLS['bInit'] = 0      # Clear 'Initialization done' flag

    return dAldKRLS


def train(dAldKRLS, vX, vY):
    """
    Function trains the current krls algorithm. |br|

    Args:
        dAldKRLS (dictionary):  Python dictionary which contains all the data of the current KRLS algorithm.
                                Must be initialized by the *init* function from this module.

        vX (numpy array):       X training data. It should be 2D or 1D numpy array or an integer.
        vY (numpy array):       Y trainig data. It should be 2D or 1D numpy array or an integer.

    Returns:

        dAldKRLS (dictionary):  Python dictionary which contains all the data of the current KRLS algorithm.

        Fields in the output dictionary:

            - a. **iALDth** (*int*):   ALD threshold

            - b. **iMaxDt** (*float*):  Max size of the dictionary

            - c. **strKernel** (*string*):  Type of the kernel

            - d. **iKernelPar** (*float*):  Kernel parameter

            - e. **bInit** (*int*):  Initialization flag = 0. This flag is cleared with a first call to the 'train' function.

            - f. **mKinv** (*numpy array*):  Kernel matrix

            - g. **vAlpha** (*numpy array*): Alpha vector

            - h. **mP** (*numpy array*): 'P' matrix

            - i. **mDict** (*numpy array*): Dictionary matrix
    """

    # -------------------------------------------------------------------
    # Check the input data
    #
    # Check if vX is a number? If so, make it a 1x1 numpy array
    if type(vX) is not np.ndarray:
        vX = np.array([[vX]])
    # Check if vX is a 1-dim np array? If so, make it a 2-dim numpy array
    elif vX.ndim == 1:
        vX = np.array([vX])
    elif vX.ndim == 2:
        pass
    else:
        strErr = ('vX must be 1dim or 2dim numpy array or an integer')
        raise ValueError(strErr)

    # Check if vY is a number? If so, make it a 1x1 numpy array
    if type(vY) is not np.ndarray:
        vY = np.array([[vY]])
    # Check if vY is a 1-dim np array? If so, make it a 2-dim numpy array
    elif vY.ndim == 1:
        vY = np.array([vY])
    elif vY.ndim == 2:
        pass
    else:
        strErr = ('vY must be 1dim or 2dim numpy array or an integer')
        raise ValueError(strErr)
    # -------------------------------------------------------------------


    bInit = dAldKRLS['bInit']  # Get the initialization flag
    if (bInit == 0):
        # Initialize training:

        # Get the needed data
        strKernel = dAldKRLS['strKernel']    # Type of the kernel
        iKernelPar = dAldKRLS['iKernelPar']  # Kernel parameter

        vK = kernel.main(vX, vX.T, strKernel, iKernelPar)
        vKt = vK[np.arange(0, vK.size-1)]
        iKtt = float(vK[vK.size-1])

        # Store all the parameters in the dictionary
        dAldKRLS['mKinv'] = 1/iKtt
        dAldKRLS['vAlpha'] = vY/iKtt
        dAldKRLS['mP'] = np.array([[1]])
        dAldKRLS['mDict'] = vX

        dAldKRLS['bInit'] = 1      # Set 'Initialization done' flag

    else:
        # Training:

        # Get the needed data from the dictionary with data
        strKernel = dAldKRLS['strKernel']     # Type of the kernel
        iKernelPar = dAldKRLS['iKernelPar']   # Kernel parameter

        mDict = dAldKRLS['mDict']
        vAlpha = dAldKRLS['vAlpha']
        mKinv = dAldKRLS['mKinv']
        iALDth = dAldKRLS['iALDth']          # ALD threshold
        iMaxDict = dAldKRLS['iMaxDt']        # Maximum size of the dictionary
        mP = dAldKRLS['mP']

        # Computations start here
        vK = kernel.main(np.vstack((mDict, vX)), vX.T, strKernel, iKernelPar)
        vKt = vK[np.arange(0, vK.size-1)]
        iKtt = float(vK[vK.size-1])
        vAT = np.dot(mKinv, vKt)                   # AT vector

        iDelta = iKtt - float(np.dot(vKt.T, vAT))     # Delta value (integer)

        if mDict.ndim == 2:
            (iRowsDict, _) = mDict.shape                  # The number of rows in the dictionary
        else:
            (iRowsDict, ) = mDict.shape                   # The number of rows in the dictionary

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


def evaluate(dAldKRLS, vX):
    """
    Function evaluates the current krls algorithm. |br|

    Args:
        dAldKRLS (dictionary):  Python dictionary which contains all the data of the current KRLS algorithm.
        vX (numpy array or integer):  Evaluation argument

    Returns:

        vY (numpy array): x = alpha * dictionary, where 'alpha' and 'dictionary' are outcomes of the
                          training of the KRLS algporithm stored in the dAldKRLS dictionary

    """

    # -------------------------------------------------------------------
    # Check the input data
    #
    # Check if vX is a number? If so, make a 1x1 numpy array
    if type(vX) is not np.ndarray:
        vX = np.array([[vX]])
    # Check if vX is a 1-dim np array? If so, make is a 2-dim numpy array
    elif vX.ndim == 1:
        vX = np.array([vX]).T
    elif vX.ndim == 2:
        pass
    else:
        strErr = ('Input vector must be 1dim or 2dim numpy array or an integer')
        raise ValueError(strErr)

    # -------------------------------------------------------------------

    # Get the needed data from the dictionary with data
    strKernel = dAldKRLS['strKernel']    # Type of the kernel
    iKernelPar = dAldKRLS['iKernelPar']  # Kernel parameter
    mDict = dAldKRLS['mDict']
    vAlpha = dAldKRLS['vAlpha']

    if mDict.ndim == 2:
        (iRowsDict, _) = mDict.shape                  # The number of rows in the dictionary
    else:
        (iRowsDict, ) = mDict.shape                   # The number of rows in the dictionary

    if iRowsDict > 0:
        vK = kernel.main(mDict, vX, strKernel, iKernelPar)
        vY = np.dot(vK.T, vAlpha)
    else:
        vY = np.zeros((iRowsDict,1))

    return vY
