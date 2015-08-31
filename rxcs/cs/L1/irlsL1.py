"""
This a L1-optimization signal reconstruction module. |br|

This module uses Iterative Reweighted Least Squares method as L1 solver. |br|


   The optimization scheme is:

   min( |x|_1  )   subject to.
                                 |Ax - y|_2^2


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


    Optional parameters:

    - c, **iMaxIter** (*int*):   the maximum number of iterations [default = 100]

    - d, **iConvStop** (*float*):  convergence stop parameter  [default = 0.001]

    - e, **bComplex** (*float*):   'complex' problem flag, should be switched 
                                   if Theta matrices are complex [default = 0]

    - f. **bMute** (*int*):    mute the console output from the sampler [default = 0]


*Output*:
    Description of the L1 reconstruction module output is below. 
    This is the list of attributes of the class which are available 
    after calling the 'run' method:

    - a. **lCoeff** (*list*):  list with the reconstructed signal coefficients,
                               one element of the list is a 1D Numpy array with 
                               coefficients for one signal

    - b. **lIter** (*list*):   list with the number of irls iterations spend on
                               every reconstructed signals

    - c. **lmX** (*list*):     list with matrices with reconstructed signal 
                               coefficients in every iteration for every 
                               reconstructed signal
    
------------------------------------------------------------------------------

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0    | 22-JAN-2014 : * Version 1.0 released. |br|
    2.0    | 31-AUG-2015 : * Version 2,0 (objectified version) released. |br|

*License*:
    BSD 2-Clause
"""

from __future__ import division
import rxcs
import numpy as np


# =================================================================
# L1 solver object
# =================================================================
class irlsL1(rxcs._RxCSobject):

    def __init__(self, *args):
        rxcs._RxCSobject.__init__(self)    # Make it a RxCS object 
        
        # Name of group of RxCS modules and module name
        self.strRxCSgroup = 'Reconstruction'  
        self.strModuleName = 'L1 basis pursuit [irls]'

        self.__inputSignals()      # Define the input signals
        self.__parametersDefine()  # Define the parameters
        
        # Start L2 solver object
        self.L2solv = rxcs.auxiliary.aldkrlsL2()


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
                                                  # must equal the number of 
                                                  # observed signals
    # Define parameters
    def __parametersDefine(self):

        # 'complex data' flag
        self.paramAddOpt('bComplex', '\'complex data\' flag')
        self.paramType('bComplex', (int, float))  # Must be a number  type
        self.paramAllowed('bComplex', [0, 1])     # It can be either 1 or 0

        # the maximum number of iterations
        self.paramAddOpt('iMaxIter', 'The maximum number of iterations', default=100)
        self.paramType('iMaxIter', (int))       # Must be an integer number
        self.paramH('iMaxIter', 0)              # It must be higher than 0

        # convergence parameter
        self.paramAddOpt('iConvStop', 'Convergence stop parameter', default=0.001)
        self.paramType('iConvStop', (int, float))  # Must be a number  type
        self.paramH('iConvStop', 0)  # The convergence parameter should be higher than 0
        self.paramL('iConvStop', 1)  # and lower than 1 

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
        # of rows equal to the size of corresponding observed signal
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
        self.lmX = []      # List with matrix with vectors x found in every iteration
        self.lIter = []    # The number of iterations      
        for inxSig in np.arange(nObSig):

            # Run reconstruction of the current signal
            (vCoef, mX, iIter) = self._recon1sig(inxSig)                    
                        
            # Store the coefficients in the list with coefficients
            self.lCoeff.append(vCoef)
            self.lmX.append(mX)
            self.lIter.append(iIter)

        # -----------------------------------------------------------------
        # Construct the complex output coefficients vector (if needed)
        if self.bComplex == 1:
            self.lCoeff = self._makeComplexOutput(self.lCoeff)
        # -----------------------------------------------------------------        
        return

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


    # Reconstruct a single signal
    def _recon1sig(self, inxSig):
        """
        Args:
            inxSig (list):  Index of the signal from the list with observed signals
    
        Returns:
            vCoef (Numpy array 1D):  reconstructed signal coefficients    
        """

        # Get the current Theta matrix
        mTheta = self.lTheta[inxSig]

        # Get the current observed signal
        vObSig = self.lObserved[inxSig]

        # Run the engine: Reconstruct the signal coefficients
        (vCoef, mX, iIter) = self.L1(mTheta, vObSig, self.iMaxIter, self.iConvStop)
        vCoef.shape = (vCoef.size,)

        return (vCoef, mX, iIter)        


    def L1(self, mA, vY, iMaxIter, iConvStop):
        """
         This function looks for an optimum solution Ax = y, minimizing the
         L_1 norm ||x||_1, using Iterative Reweighted Least Squares algortihm.

         It used an L2 minimizer implemented using Kernel Recursive Least Squares
         algorithm with linear kernel.

         An example irls_ex0.py in examples/auxiliary shows how to use this function.

        Args:
            mA  (numpy array):    matrix A   (look desc. above)
            vY  (numpy array):    vector y   (look desc. above)
            iMaxIter (number):    the max number of iterations
            iConvStop (number):   convergence parameter

        Returns:
            vX  (numpy array):    found vector x (look desc. above)
            mX   (numpy array)    matrix with vectors x found in every iteration
            iIter (number):       the number of iterations
        """

        (nRows, nCols) = mA.shape             # Take the number of rows and columns in Theta
        mX = np.zeros((nCols, iMaxIter+1))    # Allocate a matrix for storing the found vectors from every iteration

        # Compute the initial solution and store it in mX
        self.L2solv.mA = mA
        self.L2solv.vY = vY
        self.L2solv.bMute = 1
        self.L2solv.run()   # Find the initial vector X
        vX = self.L2solv.vX.copy()        
        mX[:, 0] = vX
          
        # Loop over all iterations      
        for iIter in np.arange(iMaxIter):
    
            mAWeightedX = np.ones(mA.shape)      # Allocate new matrix with weights
            for inxRow in np.arange(nRows):      # Compute the matrix with weights      
                mAWeightedX[inxRow, :] = np.abs(vX) * mA[inxRow, :]

            vX_prev = vX.copy() # Store the previous solution

            # Compute the current x vector

            self.L2solv.mA = np.dot(mAWeightedX, mA.T)
            self.L2solv.vY = vY
            self.L2solv.run()                 # Find the current vector X
            vX_temp = self.L2solv.vX.copy()        
            
            vX = np.dot(mAWeightedX.T, vX_temp.T).T
            
            # Stopre the found x vector in the 'mX' matrix
            vX_1dim = vX.copy(); vX_1dim.shape = (nCols,)
            mX[:, iIter+1] = vX_1dim

            # Check convergence condition
            vXd = vX - vX_prev              # Compute the difference vector 
            iXd_n2 = np.linalg.norm(vXd)    # Second norm of the difference vector
            iX_n2 = np.linalg.norm(vX)      # Second norm of the current x vector
            if (iXd_n2 / iX_n2 ) < iConvStop:  # Should we stop?
                break
     
        return (vX.T, mX, iIter)


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
