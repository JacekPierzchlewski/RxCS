"""
This a L1-optimization signal reconstruction module. |br|

This module uses Iterative Reweighted Least Squares method as L1 solver. |br|

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0  | 22-JAN-2014 : * Version 1.0 released. |br|

*License*:
    BSD 2-Clause
"""

from __future__ import division
import rxcs
import numpy as np

def main(dCSConf):
    """
    This the main function of the reconstruction and the only one which should
    be accessed by a user. |br|

    An input dictionary, which is a sole argument to the function
    contains all the settings and data given to the module. |br|

    The function returns a matrix with found signal coefficients. |br|

    Please go to the *examples* directory for examples on how to use the
    module. |br|

    Fields in the input dictionary:

    - a. **bMute** (*float*): 'mute the console outpu' flag

    - b. **m3Theta** (*2D or 3D matrix*): matrix with Theta matrices

    - c. **iMaxIter** (*float*): the maximum numbr of iterations

    - d. **mObSig** (*matrix*): matrix with observed signals

    - c. **iConv** (*float*): the convergence parameter

    - e. **bComplex** (*float*): 'complex data' flag
    
    THETA MATRICES:
    The optimization module 'rxcs.cs.irlsL1' is designed to work with
    multiple observed signals, so that many signals can be reconstructed
    with one module call.

    Therefore, by default the input matrix with Theta matrices is a 3D matrix,
    so that many Theta matrices may be given to the module (one page of the
    'm3Theta' matrix = one Theta matrix).

    If there is a need to reconstruct only 1 signal, then the input
    Theta matrix may be 2D.


    OBSERVATION SIGNALS:
    Similarly, the observed signals are given as a 2D matrix (one column -
    one observed signal). If there is a need to reconstruct only 1 signal
    then the field 'mObSig' in the input dictionary may be a simple vector
    with the observed signal.

    Always the number of columns in the mObSig matrix must equal the number
    of pages in the m3Theta matrix.


    COMPLEX OPTIMIZATION FLAG:
    If the 'bComplex' is set, then the module converts the complex
    optimization problem into a real problem. This flag may not exists in
    the dictionary, by default it is cleared.

    Warning: the module does not support reconstruction of complex signals!
             Therefore the conversion to real problem is done with assumption
             that the complex part of the reconstructed signal is 0.


    OUTPUT MATRIX WITH SIGNAL COEFFICIENS:
    The found signal coefficients are given as a 2D matrix, where one column
    corresponds to a one vector with found signal coefficients.

    The number of columns in the output matrix equalts the number of columns
    in the input matrix with observed signals.

    Args:
        dCSConf (dictionary): dictionary with configuration for the module

    Returns:
        mCoef (matrix): matrix with found signal coefficients.

    """

    # Check if the configuration for the reconstruction make sense
    _checkConf(dCSConf)
    
    # Print the configuration to the console
    tStart = _printConf(dCSConf)
    
    # Signal reconstruction is here
    mCoef = _recon(dCSConf)
    
    # Print an info that the signal reconstruction is done! (if needed)
    if not np.isnan(tStart):   # <-tStart is nan = console output is off
        rxcs.console.module_progress_done(tStart)

    # Return the matrix with signal coefficients
    return mCoef
    
    
# =================================================================
# Check the configuration dict. and get the configuration from it
# =================================================================
def _getData(dCSConf):
    """
    This function checks if all the needed configuration fields are in
    the configuration dictionary and gets these configuration fields.

    Args:
        dCSConf (dictionary): dictionary with configuration for the module

    Returns:
        bMute (float):      mute the conole output flag
        m3Theta (matrix):   the Theta matrices
        mObSig (matrix):    matrix with the observed signals
        bComplex (float):   complex optinmization flag
        iMaxIter (int):     maximum number of IRLS iterations
        iConv (int):        convergence parameter
    """

    # -----------------------------------------------------------------
    # Get the mute parameter
    if not 'bMute' in dCSConf:
        bMute = 0
    else:
        bMute = dCSConf['bMute']

    # -----------------------------------------------------------------
    # Get the Theta matrices
    if not 'm3Theta' in dCSConf:
        strError = ('The Theta matrices (m3Theta) are missing ')
        strError = strError + ('in the input dictionary')
        raise NameError(strError)
    else:
        m3Theta = dCSConf['m3Theta']

    # -----------------------------------------------------------------
    # Get the matrix with the observed signals
    if not 'mObSig' in dCSConf:
        strError = ('The observed signals (mObSig) are missing')
        strError = strError + (' in the input dictionary')
        raise NameError(strError)
    else:
        mObSig = dCSConf['mObSig']

    # -----------------------------------------------------------------
    # Get the 'only real optimization' flag
    if not 'bComplex' in dCSConf:
        bComplex = 0
    else:
        bComplex = dCSConf['bComplex']

    # -----------------------------------------------------------------
    # Get maximum number of iterations
    if not 'iMaxIter' in dCSConf:
        iMaxIter = 100
    else:
        iMaxIter = dCSConf['iMaxIter']

    # -----------------------------------------------------------------
    # Get convergence parameter
    if not 'iConv' in dCSConf:
        iConv = 0.001
    else:
        iConv = dCSConf['iConv']

    # -----------------------------------------------------------------
    # Check if the matrix with observed signals is a numpy vector.
    # If it is a numpy vector (vector - array with one dimension),
    # make it a 2D matrix (2D matrix - array with 2 dimensions).
    mObSig = _make2Dmatrix(mObSig)

    # -----------------------------------------------------------------
    # Check if the Theta matrix is 2D.
    # If it is, then make it a 3D with one page
    m3Theta = _make3Dmatrix(m3Theta, bComplex)

    return (bMute,
            m3Theta,
            mObSig,
            bComplex,
            iMaxIter,
            iConv)


# =================================================================
# Check if the configuration for the reconstruction make sense
# =================================================================
def _checkConf(dCSConf):
    """
    This function checks the configuration of this reconstruction module.

    Args:
        dCSConf (dictionary): CS reconstruction configuration dictionary

    Returns:
        nothing

    """

    # Get configuration data
    (_, m3Theta, mObSig, bComplex, iMaxIter, iConv) = _getData(dCSConf)

    # -----------------------------------------------------------------
    # Check it the number of the observed signals is equal to the number
    # of the Theta matrices
    _checkNObs(m3Theta, mObSig)

    # -----------------------------------------------------------------
    # Check it the number of rows in the Theta matrices is equal to the
    # size of the observed signals
    _checkThetaRows(m3Theta, mObSig)

    # -----------------------------------------------------------------
    # Check if the number of iterations is an integer and is higher than 0
    if not isinstance(iMaxIter, int):
        strError = ('The number of iterations (iMaxIter) must be an integer')
        raise TypeError(strError)

    if (iMaxIter <= 0):
        strError = ('The number of iterations (iMaxIter) must be higher than 0')
        raise ValueError(strError)

    # -----------------------------------------------------------------
    # Check if convergence parameter is higher then 0
    if (iConv < 0):
        strError = ('The convergence parameter must be higher than 0')
        raise ValueError(strError)

    return


# =================================================================
# Make a one column 2D matrix from 1D vector, if needed
# =================================================================
def _make2Dmatrix(mObSig):
    """
    This function checks if the matrix with observation signals
    is a 1D numpy vecotr.
    If it is a 1D numpy matrix, then the function makes it a 2D matrix with
    one column.

    If the input matrix is a 2D matrix, then the function returns it
    as it is.

    Args:
        mObSig (matrix): Corrected matrix with observation signals

    Returns:
        mObSig (matrix): Corrected matrix with observation signals
    """

    if len(mObSig.shape) == 1:
        nRows = mObSig.size
        mObSig_ = mObSig.copy()
        mObSig = np.zeros((nRows,1))
        mObSig[:,0] = mObSig_

    return mObSig


# =================================================================
# Make a one page 3D matrix from 2D matrix, if needed
# =================================================================
def _make3Dmatrix(m3Theta, bComplex):
    """
    This function checks if the m3Theta matrix is a 2D numpy matrix.
    If it is a 2D matrix, then the function makes it a 3D matrix with
    one page,

    If the input matrix is a 3D matrix, then the function returns it
    as it is.

    Args:
        m3Theta (matrix): The Theta matrix
        bComplex (float): Compelx data flag

    Returns:
        m3Theta (matrix): The Theta matrix
    """

    if len(m3Theta.shape) == 2:
        (nRows , nCols) = m3Theta.shape
        m3Theta_ = m3Theta.copy()
        m3Theta = np.zeros((1, nRows , nCols))
        if bComplex == 1:
            m3Theta = m3Theta + 1j*np.zeros((1, nRows ,nCols))
        m3Theta[0, :, :] = m3Theta_

    return m3Theta


# =================================================================
# Check if the number of observed signals is equal to the number
# of Theta matrices
# =================================================================
def _checkNObs(m3Theta, mObSig):
    """
    This function checks if the number of observed signals equals
    the number of Theta matrices.

    The number of Theta matrices is the number of pages in the 3D matrix
    'm3Theta'.

    The number of observed signals is equal to the number of columns in
    the 'mObSig' matrix.

    Args:
        m3Theta (3D matrix): 3D matrix with Theta matrices
        mObSig (matrix): matrix with observed signals

    Returns:
        nothing
    """

    # Get the number of the observed signals
    (_ , nObSig) = mObSig.shape

    # Get the number of Theta matrices
    (nTheta , _, _) = m3Theta.shape

    # -----------------------------------------------------------------

    # Main check starts here
    if nObSig != nTheta:
        strError = ('The number of the observed signals is not equal to the')
        strError = strError + (' number of the Theta matrices')
        raise ValueError(strError)

    return


# =================================================================
# Check it the number of rows in the Theta matrices is equal to the
# size of the observed signals
# =================================================================
def _checkThetaRows(m3Theta, mObSig):
    """
    This function checks if the number of rows in the Theta matrices
    equals the size of the observed signals.

    Args:
        m3Theta (3D matrix): 3D matrix with Theta matrices
        mObSig (matrix): matrix with observed signals

    Returns:
        nothing
    """

    # Get the number of rows in the theta matrix
    (_, nRows, _) = m3Theta.shape

    # Get the size of the observed signals
    (nObSiz, _) = mObSig.shape

    # -----------------------------------------------------------------

    # Main check starts here
    if nRows != nObSiz:
        strError = ('The number of rows in the Theta matrices is not equal ')
        strError = strError + ('to the size of the observed signals')
        raise ValueError(strError)

    return

# =================================================================
# Print the configuration of the module to the console
# =================================================================
def _printConf(dCSConf):
    """
    This function prints module parameters to the console,
    if only the 'bMute' flag is not set.

    Args:
        dCSConf (dictionary): CS reconstruction configuration dictionary

    Returns:
        tStart (time): time stamp of reconstruction start
    """

    # -----------------------------------------------------------------
    # Get the configuration parameters
    #
    # bMute    -  mute the conole output flag
    # mObSig   -  matrix with the observed signals
    # iMaxIter -  the max numbr of iterations
    # iCOnv    -  convergence parameter
    #
    (bMute, _, mObSig, _, iMaxIter, iConv) = _getData(dCSConf)

    #----------------------------------------------------------------------
    # Print the configuration if the 'mute' flag is not set
    if bMute == 0:

        # Print out the header of the sampler
        strStage = 'Signals reconstruction'
        strModule = 'L1 optimization (Iterative Reweighted Least Squares)'
        rxcs.console.progress(strStage, strModule)

        # - - - - - - - - - - - - - - - - - - -
        # The number of signals to be reconstructed
        (_, nPatts) = mObSig.shape
        rxcs.console.bullet_param('the number of signals to be reconstructed',
                                  nPatts, '-', '')

        # The max number of iterations H
        rxcs.console.bullet_param('the max number of iterations p. signal',
                                  iMaxIter, '-', '')

        # The convergence parameter
        rxcs.console.bullet_param('the convergence parameter',
                                  iConv, ' ', '')

        # - - - - - - - - - - - - - - - - - - -
        # Information about the computations start
        strStartMessage = ('signals reconstruction starts!!!')
        tStart = rxcs.console.module_progress(strStartMessage)

    #----------------------------------------------------------------------
    else:   # <- the output was muted
        tStart = np.nan

    #----------------------------------------------------------------------
    return tStart

# =================================================================
# Make real-only Theta matrices, if it is needed
# =================================================================
def _makeRealProblem(m3Theta):
    """
    This function makes a real only Theta matrix from a complex
    Theta matrix.

    The output matrix has twice as many columns as the input matrix.

    This function is used only if the optimization problem
    is complex and must be transformed to a real problem.


    Let's assume that the input complex Theta matrix looks as follows:

    |  r1c1    r1c2    r1c3  |
    |  r2c1    r2c2    r2c3  |
    |  r3c1    r3c2    r3c3  |
    |  r4c1    r4c2    r4c3  |
    |  r5c1    r5c2    r5c3  |


    Then the real output matrix is:

    |  re(r1c1)   re(r1c2)   re(r1c3)   im(r1c1)   im(r1c2)   im(r1c3)  |
    |  re(r2c1)   re(r2c2)   re(r2c3)   im(r2c1)   im(r2c2)   im(r2c3)  |
    |  re(r3c1)   re(r3c2)   re(r3c3)   im(r3c1)   im(r3c2)   im(r3c3)  |
    |  re(r4c1)   re(r4c2)   re(r4c3)   im(r4c1)   im(r4c2)   im(r4c3)  |
    |  re(r5c1)   re(r5c2)   re(r5c3)   im(r5c1)   im(r5c2)   im(r5c3)  |


    Args:
        m3Theta (matrix): The Theta matrix with complex values

    Returns:
        m3ThetaR (matrix): The Theta matrix with a real only values
    """

    # Get the size of the 3d matrix with Theta matricess
    (nTheta, nRows, nCols) = m3Theta.shape

    # Creatwe the real-only Theta matrix
    m3ThetaR = np.zeros((nTheta, nRows, 2*nCols))
    m3ThetaR[:, :, np.arange(nCols)] = m3Theta.real
    m3ThetaR[:, :, np.arange(nCols, 2*nCols)] = m3Theta.imag

    return m3ThetaR


# =================================================================
# Make complex output vectors, if it is needed
# =================================================================
def _makeComplexOutput(mCoeff):
    """
    This function constructs a complex output matrix with the found
    signal coefficients,

    This function is used only if the optimization problem
    is complex and was transformed to a real problem.

    The number of rows in the output matrix equals half the number of
    rows in the input matrix.

    Let's assume that the input real matrix looks as follows:

    |  r1c1    r1c2    r1c3  |
    |  r2c1    r2c2    r2c3  |
    |  r3c1    r3c2    r3c3  |
    |  r4c1    r4c2    r4c3  |


    Then the complex output matrix is:

    |  r1c1 + j*r3c1    r1c2 + j*r3c2    r1c3 + j*r3c3  |
    |  r2c1 + j*r4c1    r2c2 + j*r4c2    r2c3 + j*r4c3  |


    Args:
        mCoeff (matrix): The real matrix with found signal coefficients

    Returns:
        mCoeffC (matrix): The complex matrix with found signal coefficients
    """

    # Get the size of the matrix with coefficients
    (nSiz, nSigs) = mCoeff.shape

    # Get the real and complex parts of the output matrix and construct the
    # output matrix
    mCoeffR = mCoeff[np.arange(int(nSiz/2)), :]
    mCoeffI = mCoeff[np.arange(int(nSiz/2), nSiz), :]
    mCoeffC = mCoeffR - 1j*mCoeffI
    return mCoeffC


# =================================================================
# Main function of the signal reconstruction
# =================================================================
def _recon(dCSConf):
    """
    This function reconstructs the signals based on the data given
    in the input dictionary.

    Args:
        dCSConf (dictionary): dictionary with configuration for the module

    Returns:
        mCoeff (matrix): matrix with signal coefficients
    """

    # Get configuration data
    (_, m3Theta, mObSig, bComplex, iMaxIter, iConv) = _getData(dCSConf)

    # Get the number of the observed signals
    (_ , nObSig) = mObSig.shape

    # If the optimization problems are complex, make them real
    if bComplex == 1:
        m3Theta = _makeRealProblem(m3Theta)

    # Get the number of columns in the Theta matrix,
    (_ , _, nCols) = m3Theta.shape

    # Allocate the output matrix with signal coefficients
    mCoeff = np.zeros((nCols, nObSig))

    # -----------------------------------------------------------------
    # Loop over all the observed signals
    for inxSig in np.arange(nObSig):

        # Get the current Theta matrix
        mTheta = m3Theta[inxSig, :, :]

        # Get the current observation signal
        vObSig = mObSig[:, inxSig]

        # Run the engine: Reconstruct the signal coefficients
        (vCoef, _, _) = rxcs.auxiliary.irls.L1(mTheta, vObSig, iMaxIter, iConv)
        vCoef.shape = (vCoef.size,)
        
        # Store the signal coefficients in the output matrix
        #vCoef.shape = (vCoef.size)
        mCoeff[:, inxSig] = vCoef

    # Construct the complex output coefficients vector (if needed)
    if bComplex == 1:
        mCoeff = _makeComplexOutput(mCoeff)

    return mCoeff



