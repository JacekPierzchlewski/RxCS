from __future__ import division
import rxcs
import numpy as np
from cvxopt import matrix, mul, div, sqrt
from cvxopt import blas, lapack, solvers


def main(dCSConf):

    # =================================================================
    # Check the configuration and print it to the console
    # =================================================================

    # Print the configuration to the console
    tStart = _printConf(dCSConf)

    # - - - - - - - - - - - - - - - - - - -

    # =================================================================
    # Signal reconstruction starts here
    # =================================================================
    mCoef = _recon(dCSConf)

    # =================================================================
    # Signal reconstruction is done!
    # =================================================================
    if not np.isnan(tStart):   # <-tStart is nan = console output is off
        rxcs.console.module_progress_done(tStart)

    return mCoef

# =================================================================
# Check the configuration dict. and get the configuration from it
# =================================================================
def _printConf(dCSConf):

    # bMute    -  mute the conole output flag
    # iK       -  the K parameter
    # mObSig   -  matrix with the observed signals
    (bMute,
     iK,
     _,
     mObSig,
     _) = _getData(dCSConf)

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
        bComplex (float)   complex flag

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
# Check it the number of the observed signals is equal to the number
# of the Theta matrices
# =================================================================
def _checkNObs(m3Theta, mObSig):

    # Get the number of the observed signals
    (_ , nObSig) = mObSig.shape

    # Check if the Theta matrix is truly 3D, or just a 2D
    if len(m3Theta.shape) == 2:
        # It is just a 2D matrix
        nTheta = 1
    else:
        # Get the number of Theta matrices
        (_ , _, nTheta) = m3Theta.shape

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

    # Get the number of rowss
    # check if the Theta matrix is truly 3D, or just a 2D
    if len(m3Theta.shape) == 2:
        (nRows , _) = m3Theta.shape
    else:
        (nRows , _, _) = m3Theta.shape

    # Get the size of the observed signals
    (nObSiz , _) = mObSig.shape

    # -----------------------------------------------------------------

    # Main check starts here
    if nRows != nObSiz:
        strError = ('The number of rows in the Theta matrices is not equal ')
        strError = strError + ('to the size of the observed signals')
        raise ValueError(strError)

    return


# =================================================================
# Signal reconstruction
# =================================================================
def _recon(dCSConf):

    # -----------------------------------------------------------------
    # Get the input data
    # iK       -  the K parameter
    # m3Theta  -  3D matrix with the Theta matrices
    # mObSig   -  matrix with the observed signals
    (_,
     iK,
     m3Theta,
     mObSig,
     bComplex) = _getData(dCSConf)

    # Get the number of the observed signals
    (_ , nObSig) = mObSig.shape

    # Check if the Theta matrix is 2D, if it is, then make it a 3D with one
    # page
    if len(m3Theta.shape) == 2:
        (nRows , nCols) = m3Theta.shape
        m3Theta_ = m3Theta.copy()
        m3Theta = np.zeros((1, nRows , nCols))+1j*np.zeros((1, nRows , nCols))
        m3Theta[0, :, :] = m3Theta_

    # If the optimization problems are complex, make them real
    if bComplex:
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
        vvCoef = _reconEngine(mmTheta, vvObSig, iK, 1)

        # Store the signal coefficients in the output matrix
        vCoef = np.array(vvCoef)
        vCoef.shape = (vCoef.size)
        mCoeff[:, inxSig] = vCoef

    # Construct the complex output coefficients vector (if needed)
    if bComplex:
        mCoeff = _makeComplexOutput(mCoeff)

    # -----------------------------------------------------------------
    return mCoeff


# =================================================================
# Make real-only Theta matrices, if it is needed
# =================================================================
def _makeRealProblem(m3Theta):

    # Get the size of the 3d matrix with Theta matricess
    (nTheta, nRows, nCols) = m3Theta.shape

    # Creatwe the real-only Theta matrix
    m3ThetaR = np.zeros((nTheta, nRows, 2*nCols))
    m3ThetaR[:, :, np.arange(nCols)] = m3Theta.real
    m3ThetaR[:, :, np.arange(nCols, 2*nCols)] = m3Theta.imag

    return m3ThetaR

# =================================================================
# Make complex output vector, if it is needed
# =================================================================
def _makeComplexOutput(mCoeff):

    # Get the size of the matrix with coefficients
    (nSiz, nSigs) = mCoeff.shape

    # Get the real and complex parts of the output matrix and construct the
    # output matrix
    mCoeffR = mCoeff[np.arange(int(nSiz/2)), :]
    mCoeffC = mCoeff[np.arange(int(nSiz/2), nSiz), :]
    mCoeff = mCoeffR - 1j*mCoeffC
    return mCoeff


# =================================================================
# ENGINE OF THE RECONSTRUCTION: basis pursuit problem
# =================================================================
def _reconEngine(mmTheta_, vvSig_, iK, bSilence):
    """
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
        vvSig_ (cvxopt vector):   vector with observed signal
        iK (float):  k parameter

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
    if bSilence == 1:
        solvers.options['show_progress'] = False

    # --------------------------------------------------------------------

    #
    # Q = -2.0 * A' * y
    vvQ = matrix(float(iK), (2*iC,1))

    blas.gemv(mmTh, vvSig_, vvQ, alpha = -2.0, trans = 'T')

    mmH = matrix(0.0, (2*iC,1))
    vvCoef = solvers.coneqp(P, vvQ, G, mmH, kktsolver = Fkkt)['x'][:iC]

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
