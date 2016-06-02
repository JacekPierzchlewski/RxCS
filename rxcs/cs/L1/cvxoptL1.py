"""
This a L1-optimization signal reconstruction module. |br|

This module uses cvxopt software as L1 solver. |br|

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

Therefore, the Theta matrices should be grouped in a list,
so that many Theta matrices may be given to the module (one element of the
'lTheta' list = one Theta matrix).



OBSERVATION SIGNALS:
Similarly, the observed signals are given as a list with 1D Numpy arrays
(one list element  - one observed signal).

Always the number of elements in the list with observed signals must equal
the number Theta matrices.


COMPLEX OPTIMIZATION FLAG:
If the 'bComplex' is set, then the module converts the complex
optimization problem into a real problem. This flag may not be given,
by default it is cleared.

Warning: the module does not support reconstruction of complex signals!
         Therefore the conversion to real problem is done with assumption
         that the complex part of the reconstructed signal is 0.


OUTPUT MATRIX WITH SIGNAL COEFFICIENS:
The found signal coefficients are given as a list with 1D Numpy arrays,
where one element of a list corresponds to a one array with found
signal coefficients.

The number of elements in the output list equals the number of elements
in the input list with observed signals.

------------------------------------------------------------------------------

*Examples*:
    Please go to the *examples/reconstruction* directory for examples on how to
    use the L1 reconstruction module. |br|

*Settings*:
    Parameters of the L1 reconstruction module are described below.

    Take a look on '__parametersDefine' function for more info on the
    parameters.

    Parameters of the L1 reconstruction module are attributes of the class
    which must/can be set before the generator is run.

    Required parameters:

    - a. **lObserved** (*list*): list with the observed signals

    - b. **lTheta** (*list*): list with Theta matrices

    - c. **iK** (*float*): the 'k' parameter from  the equation above


    Optional parameters:

    - d, **bComplex** (*float*):   'complex' problem flag, should be switched
                                   if Theta matrices are complex [default = 0]

    - e. **bMute** (*int*):    mute the console output from the sampler [default = 0]


*Output*:
    Description of the L1 reconstruction module output is below.
    This is the list of attributes of the class which are available
    after calling the 'run' method:

    - a. **lCoeff** (*list*):  list with the reconstructed signal coefficients,
                               one element of the list is a 1D Numpy array with
                               coefficients for one signal

*License*:
    GNU GPL v3
    WARNING: Ths module has a different license (GNU GPL v3) than most of the
             RxCS code (BSD 2-clause)!

Copyright (C) <2014-2015>  Jacek Pierzchlewski
              Based on a file copyyrighted by:
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
    0.1    | 11-JUN-2014 : * Initial version. |br|
    0.2    | 12-JUN-2014 : * Docstrings added. |br|
    1.0    | 12-JUN-2014 : * Version 1.0 released. |br|
    2.0    | 21-AUG-2015 : * Version 2,0 (objectified version) released. |br|
    2.0r1  | 25-AUG-2015 : * Improvements in code comments and in headers |br|
    2.0r2  | 03-JUN-2016 : * A bug in reconstruction of multisignals is fixed |br|

"""
from __future__ import division
import rxcs
import numpy as np
from cvxopt import matrix, mul, div, sqrt
from cvxopt import blas, lapack, solvers


# =================================================================
# L1 solver object
# =================================================================
class cvxoptL1(rxcs._RxCSobject):

    def __init__(self, *args):
        rxcs._RxCSobject.__init__(self)    # Make it a RxCS object

        # Name of group of RxCS modules and module name
        self.strRxCSgroup = 'Reconstruction'
        self.strModuleName = 'L1 basis pursuit (regularized regression) [cvxopt]'

        self.__inputSignals()      # Define the input signals
        self.__parametersDefine()  # Define the parameters

    # Define parameters
    def __inputSignals(self):

        # Observed signals
        self.paramAddMan('lObserved', 'Observed signals', noprint=1)
        self.paramType('lObserved', list)            # Must be a list
        self.paramTypeEl('lObserved', (np.ndarray))  # Elements must be np.ndarray

        # Theta matrices
        self.paramAddMan('lTheta', 'Theta matrices', noprint=1)
        self.paramType('lTheta', list)            # Must be a list
        self.paramTypeEl('lTheta', (np.ndarray))  # Elements must be np.ndarray
        self.paramSizEq('lTheta', 'lObserved')    # The number of theta matrices
                                                  # must equal the number of observed
                                                  # signals
    # Define parameters
    def __parametersDefine(self):

         # 'complex data' flag
        self.paramAddOpt('bComplex', '\'complex data\' flag')
        self.paramType('bComplex', (int, float))  # Must be a number  type
        self.paramAllowed('bComplex', [0, 1])     # It can be either 1 or 0

         # k parameter
        self.paramAddMan('iK', 'k parameter')
        self.paramType('iK', (int, float))    # Must be of int type
        self.paramHE('iK', 0)
        self.paramL('iK', np.inf)

         # 'Mute the output' flag
        self.paramAddOpt('bMute', 'Mute the output', noprint=1, default=0)
        self.paramType('bMute', int)           # Must be of int type
        self.paramAllowed('bMute', [0, 1])     # It can be either 1 or 0

    # Run
    def run(self):
        self.parametersCheck()    # Check if all the needed partameters are in place and are correct
        self.parametersPrint()    # Print the values of parameters

        self.checktInputSig()     # Check if the observed signals and Theta
                                  # matrices are correct

        self.engineStartsInfo()  # Info that the engine starts
        self.__engine()          # Run the engine
        self.engineStopsInfo()   # Info that the engine ends
        return self.__dict__     # Return dictionary with the parameters

    # Check if the observed signals and Theta matrices are correct
    def checktInputSig(self):

        # Get the number of the observed signals
        nObSig = len(self.lObserved)

        # Check if the observed signals are 1 dimensional
        for inxSig in np.arange(nObSig):
            nDim = self.lObserved[inxSig].ndim
            if not (nDim == 1):
                strE = 'The observed signals must be 1-dimensional'
                strE = strE + 'Observed signal #%d has %d dimensions' % (inxSig, nDim)
                raise ValueError(strE)

        # Check if the Theta matrices are 2 dimensional and have the number
        # of rows equal to the size of corresponding observed signa;
        for inxTheta in np.arange(nObSig):
            nDim = self.lTheta[inxTheta].ndim
            if not (nDim == 2):
                strE = 'The Theta matrices must be 2-dimensional! '
                strE = strE + 'Theta matrix #%d has %d dimensions' % (inxTheta, nDim)
                raise ValueError(strE)

            (nRows, _) = self.lTheta[inxTheta].shape
            (nSize) = self.lObserved[inxTheta].shape
            if (nRows == nSize):
                strE = 'The Theta matrices must have the number of rows equal '
                strE = strE + 'to the size of corresponding observed signal! '
                strE = strE + 'Theta matrix #%d has incorrect shape!' % (inxTheta)
                raise ValueError(strE)

        return

    # Engine - reconstruct the signal coefficients
    def __engine(self):

        # Get the number of the observed signals
        nObSig = len(self.lObserved)

        # If the optimization problems are complex, make them real
        if self.bComplex == 1:
            self.lTheta = self._makeRealProblem(self.lTheta)

        # -----------------------------------------------------------------
        # Loop over all the observed signals
        self.lCoeff = []   # Start a list with signal coefficients
        for inxSig in np.arange(nObSig):

            # Run reconstruction of the current signal
            vCoeff = self._recon1sig(inxSig)

            # Store the coefficients in the list with coefficients
            self.lCoeff.append(vCoeff)

        # -----------------------------------------------------------------
        # Construct the complex output coefficients vector (if needed)
        if self.bComplex == 1:
            self.lCoeff = self._makeComplexOutput(self.lCoeff)

        # -----------------------------------------------------------------
        return

    # Reconstruct a single signal
    def _recon1sig(self, inxSig):
        """
        Args:
            inxSig (list):  Index of the signal from the list with observed signals

        Returns:
            vCoef (Numpy array 1D):  reconstructed signal coefficients

        """
        # Get the current Theta matrix and make it a cvxopt matrix
        mmTheta = matrix(self.lTheta[inxSig])

        # Get the current observed signal and make it a cxxopt matrix
        vvObSig = matrix(self.lObserved[inxSig].copy())

        # Run the engine: Reconstruct the signal coefficients
        vvCoef = _reconEngine(mmTheta, vvObSig, self.iK)

        # Make the vector with signal coefficients a Numpy array
        vCoef = np.array(vvCoef)
        vCoef.shape = (vCoef.size)

        return vCoef

    # Make real-only Theta matrices, if it is needed
    def _makeRealProblem(self, lTheta):
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
            lTheta (list): The list with theta matrices with complex values

        Returns:
            lThetaR (list): The list with theta matrices with real only values
        """

        # Get the size of the 3d matrix with Theta matricess
        nTheta = len(lTheta)                # Get the number of Theta matrices

        # Create the real-only Theta matrix
        lThetaR = []

        for inxPage in np.arange(nTheta):
            (nRows, nCols) = lTheta[inxPage].shape    # Get the number of rows/cols in the current Theta matrix
            mThetaR = np.zeros((nRows, 2*nCols))      # Construct a new empty real-only Theta matrix
            mThetaR[:, np.arange(nCols)] = lTheta[inxPage].real
            mThetaR[:, np.arange(nCols, 2*nCols)] = lTheta[inxPage].imag
            lThetaR.append(mThetaR.copy())

        return lThetaR

    # Make complex output vectors, if it is needed
    def _makeComplexOutput(self, lCoeff):
        """
        This function constructs a complex output vector with the found
        signal coefficients,

        This function is used only if the optimization problem
        is complex and was transformed to a real problem.

        Args:
            lCoeff (list): List with found real signal coefficients

        Returns:
            lCoeffC (list): List with found complex signal coefficients
        """

        # Get the size of the list with coefficients
        nSigs = len(lCoeff)

        # Start the list with complex coefficients
        lCoeffC = []

        # Loop over all signals
        for inxSignal in np.arange(nSigs):

            # Get the current vector and its size
            vCoeff = lCoeff[inxSignal]
            nSiz = vCoeff.size

            # Get the real and complex parts of the vector and construct the
            # output complex vector
            vCoeffR = vCoeff[np.arange(int(nSiz/2))]
            vCoeffI = vCoeff[np.arange(int(nSiz/2), nSiz)]
            vCoeffC = vCoeffR - 1j * vCoeffI

            # Store the current complex vector
            lCoeffC.append(vCoeffC)

        return lCoeffC

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
