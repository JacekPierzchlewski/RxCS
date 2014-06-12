"""
This a L1-optimization signal reconstruction module. |br|

Copyright (C) <2014>  Jacek Pierzchlewski
              <2014>  Martin S. Andersen, Joachim Dahl, and Lieven Vandenberghe

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

*Authors*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

    This module is based on the example of basis pursuit by
    Martin S. Andersen, Joachim Dahl, and Lieven Vandenberghe.

    The example can be found here:
    http://cvxopt.org/examples/book/basispursuit.html

*Version*:
    0.1  | 11-JUN-2014 : * Initial version. |br|
    0.2  | 12-JUN-2014 : * Docstrings added. |br|
    1.0  | 12-JUN-2014 : * Version 1.0 released. |br|

*License*:
    GNU GPL v3
    WARNING: Ths module has a different license (GNU GPL v3) than most of the
             RxCS code (BSD 2-clause)!
"""
from __future__ import division
import rxcs
import numpy as np
from cvxopt import matrix, mul, div, sqrt
from cvxopt import blas, lapack, solvers


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

    - c. **iK** (*float*): k parameter

    - d. **mObSig** (*matrix*): matrix with observed signals

    - e. **bComplex** (*float*): 'complex data' flag


    The optimization scheme is:

       min(  |Ax - y|_2^2  +  k * |x|_1  )
                              ^
                              |
                              |
                       the 'k' parameter


    THETA MATRICES:
    The optimization module 'rxcs.cs.cvxoptL1' is designed to work with
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
    # iK       -  the K parameter
    # mObSig   -  matrix with the observed signals
    (bMute, iK,_, mObSig, _) = _getData(dCSConf)

    #----------------------------------------------------------------------
    # Print the configuration if the 'mute' flag is not set
    if bMute == 0:

        # Print out the header of the sampler
        strStage = 'Signals reconstruction'
        strModule = 'L1 optimization (regularized regression) [cvxopt]'
        rxcs.console.progress(strStage, strModule)

        # - - - - - - - - - - - - - - - - - - -
        # The number of signals to be reconstructed
        (_, nPatts) = mObSig.shape
        rxcs.console.bullet_param('the number of signals to be reconstructed',
                                  nPatts, '-', '')

        # The K parameter
        rxcs.console.bullet_param('the K parameter',
                                  iK, ' ', '')

        # - - - - - - - - - - - - - - - - - - -
        # Information about the computations start
        strStartMessage = ('signals reconstruction starts!!!')
        tStart = rxcs.console.module_progress(strStartMessage)

    #----------------------------------------------------------------------
    return tStart


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
        bMute (float):     mute the conole output flag
        iK (float):        the K parameter
        m3Theta (matrix)   the Theta matrices
        mObSig (matrix)    matrix with the observed signals
        bComplex (float)   complex optinmization flag

    """

    # -----------------------------------------------------------------
    # Get the mute parameter
    if not 'bMute' in dCSConf:
        bMute = 0
    else:
        bMute = dCSConf['bMute']

    # -----------------------------------------------------------------
    # Get the K parameter
    if not 'iK' in dCSConf:
        strError = ('The K parameter (iK) is not given in the configuration')
        raise NameError(strError)
    else:
        iK = dCSConf['iK']

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
    # Check if the matrix with observed signals is a numpy vector.
    # If it is a numpy vector (vector - array with one dimension),
    # make it a 2D matrix (2D matrix - array with 2 dimensions).
    mObSig = _make2Dmatrix(mObSig)

    # -----------------------------------------------------------------
    # Check if the Theta matrix is 2D.
    # If it is, then make it a 3D with one page
    m3Theta = _make3Dmatrix(m3Theta, bComplex)

    # -----------------------------------------------------------------
    # Check it the number of the observed signals is equal to the number
    # of the Theta matrices
    _checkNObs(m3Theta, mObSig)

    # -----------------------------------------------------------------
    # Check it the number of rows in the Theta matrices is equal to the
    # size of the observed signals
    _checkThetaRows(m3Theta, mObSig)

    # -----------------------------------------------------------------
    return (bMute,     # mute the conole output flag
            iK,        # K parameter
            m3Theta,   # Theta matrices
            mObSig,    # Observed signals
            bComplex)  # The complex optimization flag


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
# Main functio of the signal reconstruction
# =================================================================
def _recon(dCSConf):
    """
    This function reconstructs the signals based on the data given
    in the input dictionary.

    Args:
        dCSConf (dictionary): dictionary with configuration for the module

    Returns:
        mCoeff (matrix):
    """

    # -----------------------------------------------------------------
    # Get the input data
    # iK       -  the K parameter
    # m3Theta  -  3D matrix with the Theta matrices
    # mObSig   -  matrix with the observed signals
    # bComplex -  complex optmization flag
    (_,
     iK,
     m3Theta,
     mObSig,
     bComplex) = _getData(dCSConf)

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

        # Get the current Theta matrix and make a cvxopt matrix
        mmTheta = matrix(m3Theta[inxSig, :, :])

        # Get the current observation signal
        vvObSig = matrix(mObSig[:, inxSig])

        # Run the engine: Reconstruct the signal coefficients
        vvCoef = _reconEngine(mmTheta, vvObSig, iK)

        # Store the signal coefficients in the output matrix
        vCoef = np.array(vvCoef)
        vCoef.shape = (vCoef.size)
        mCoeff[:, inxSig] = vCoef

    # Construct the complex output coefficients vector (if needed)
    if bComplex == 1:
        mCoeff = _makeComplexOutput(mCoeff)

    # -----------------------------------------------------------------
    return mCoeff





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
# ENGINE OF THE RECONSTRUCTION: basis pursuit problem
# =================================================================
def _reconEngine(mmTheta_, vvSig_, iK):
    """
    This is the engine of the reconstruction.

    Basis pursuit problem:

       minimize    ||A*x - y||_2^2 + k * ||x||_1

    where:
         1. A - Theta matrix
            A = B * C:
                   B - observation matirx
                   C - dictionary matrix

         2. y - observed signal
         3. x - vector with coefficients we are looking for
         4. k - noise wage coefficient

    ----------------------------------------------------------------------

    The engine of this reconstruction is based on the fact that a problem:

        minimize    ||A*x - y||_2^2 + ||x||_1

    can be translated to:

        minimize    x'*A'*A*x - 2.0*y'*A*x + 1'*u
        subject to  -u <= x <= u

    variables x (n),  u (n).

    ----------------------------------------------------------------------

    Args:
        mTheta_ (cvxopt matrix):  Theta matrix
        vvSig_ (cvxopt vector):   vector with an observed signal
        iK (float):               k parameter

    Returns:
        vvCoef (cvxopt vector):   vector with found coefficients

    NOTE: 'cvxopt vector' is nothing but a 'cvxopt matrix' of a size (N x 1)
    """

    # --------------------------------------------------------------------
    # Get the input Theta matrix and make it global
    global mmTh
    mmTh = mmTheta_

    # --------------------------------------------------------------------
    # Get the size of the Theta matrix
    global iR       # The number of rows
    global iC       # The number of columns
    iR, iC = mmTh.size

    # --------------------------------------------------------------------
    # Silence the outoput from the cvxopt
    solvers.options['show_progress'] = False

    # --------------------------------------------------------------------

    # Q = -2.0 * A' * y
    vvQ = matrix(float(iK), (2*iC,1))
    blas.gemv(mmTh, vvSig_, vvQ, alpha = -2.0, trans = 'T')

    # Run the solver
    mmH = matrix(0.0, (2*iC,1))
    vvCoef = solvers.coneqp(P, vvQ, G, mmH, kktsolver = Fkkt)['x'][:iC]

    # --------------------------------------------------------------------
    # Return the vecto with coefficients
    return vvCoef


# =====================================================================
# 'P' function
# =====================================================================
def P(u, vvV, alpha = 1.0, beta = 0.0):
    """
    Function and gradient evaluation of

          v := alpha * 2*A'*A * u + beta * v
    """
    # Allocate R
    vvR = matrix(0.0, (iR, 1))

    # R = A * u
    blas.gemv(mmTh, u, vvR)

    # v = 2 * A' * R
    blas.gemv(mmTh, vvR, vvV, alpha = 2.0*alpha, beta = beta, trans = 'T')


# =====================================================================
# 'Q' function
# =====================================================================
def G(u, vvV, alpha = 1.0, beta = 0.0, trans = 'N'):
    """
          v := alpha*[I, -I; -I, -I] * u + beta * v  (trans = 'N' or 'T')
    """
    blas.scal(beta, vvV)
    blas.axpy(u, vvV, n = iC, alpha = alpha)
    blas.axpy(u, vvV, n = iC, alpha = -alpha, offsetx = iC)
    blas.axpy(u, vvV, n = iC, alpha = -alpha, offsety = iC)
    blas.axpy(u, vvV, n = iC, alpha = -alpha, offsetx = iC, offsety = iC)


# =====================================================================
# Custom solver
# =====================================================================
def Fkkt(W):
    """
        Custom solver:

          v := alpha * 2*A'*A * u + beta * v
    """

    global mmS
    mmS = matrix(0.0, (iR,iR))

    global vvV
    vvV = matrix(0.0, (iR,1))

    # Factor
    #
    #     S = A*D^-1*A' + I
    #
    # where D = 2*D1*D2*(D1+D2)^-1, D1 = d[:n]**2, D2 = d[n:]**2.
    mmAsc = matrix(0.0, (iR,iC))

    d1, d2 = W['di'][:iC]**2, W['di'][iC:]**2

    # ds is square root of diagonal of D
    ds = sqrt(2.0) * div( mul( W['di'][:iC], W['di'][iC:]), sqrt(d1+d2) )
    d3 =  div(d2 - d1, d1 + d2)

    # Asc = A*diag(d)^-1/2
    blas.copy(mmTh, mmAsc)
    for k in range(iR):
        blas.tbsv(ds, mmAsc, n=iC, k=0, ldA=1, incx=iR, offsetx=k)

    # S = I + A * D^-1 * A'
    blas.syrk(mmAsc, mmS)
    mmS[::iR+1] += 1.0
    lapack.potrf(mmS)

    def g(x, y, z):

        x[:iC] = 0.5 * ( x[:iC] - mul(d3, x[iC:]) + \
                mul(d1, z[:iC] + mul(d3, z[:iC])) - \
                mul(d2, z[iC:] - mul(d3, z[iC:])) )
        x[:iC] = div( x[:iC], ds)

        # Solve
        #
        #     S * v = 0.5 * A * D^-1 * ( bx[:n]
        #             - (D2-D1)*(D1+D2)^-1 * bx[n:]
        #             + D1 * ( I + (D2-D1)*(D1+D2)^-1 ) * bz[:n]
        #             - D2 * ( I - (D2-D1)*(D1+D2)^-1 ) * bz[n:] )

        blas.gemv(mmAsc, x, vvV)
        lapack.potrs(mmS, vvV)

        # x[:n] = D^-1 * ( rhs - A'*v ).
        blas.gemv(mmAsc, vvV, x, alpha=-1.0, beta=1.0, trans='T')
        x[:iC] = div(x[:iC], ds)

        # x[n:] = (D1+D2)^-1 * ( bx[n:] - D1*bz[:n]  - D2*bz[n:] )
        #         - (D2-D1)*(D1+D2)^-1 * x[:n]
        x[iC:] = div( x[iC:] - mul(d1, z[:iC]) - mul(d2, z[iC:]), d1+d2 )\
                - mul( d3, x[:iC] )

        # z[:n] = D1^1/2 * (  x[:n] - x[n:] - bz[:n] )
        # z[n:] = D2^1/2 * ( -x[:n] - x[n:] - bz[n:] ).
        z[:iC] = mul( W['di'][:iC],  x[:iC] - x[iC:] - z[:iC] )
        z[iC:] = mul( W['di'][iC:], -x[:iC] - x[iC:] - z[iC:] )

    return g
