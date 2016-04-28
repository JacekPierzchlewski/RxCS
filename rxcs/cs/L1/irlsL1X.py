from __future__ import division
import rxcs
import numpy as np
import sys


# =================================================================
# L1 solver object
# =================================================================
class irlsL1X(rxcs._RxCSobject):

    def __init__(self, *args):
        rxcs._RxCSobject.__init__(self)    # Make it a RxCS object

        # Name of group of RxCS modules and module name
        self.strRxCSgroup = 'Reconstruction'
        self.strModuleName = 'L1 basis pursuit [irls X]'

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
        self.paramType('iConvStop', (int, float))  # Must be a number
        self.paramH('iConvStop', 0)  # The convergence parameter should be higher than 0
        self.paramL('iConvStop', 1)  # and lower than 1

        # Switch on/off the L2 side reconstruction
        self.paramAddOpt('bL2', 'L2 side reconstruction', noprint=1, default=0)
        self.paramType('bL2', int)           # Must be of int type
        self.paramAllowed('bL2', [0, 1])     # It can be either 1 or 0

        # 'Mute the output' flag
        self.paramAddOpt('bMute', 'Mute the output', noprint=1, default=0)
        self.paramType('bMute', int)           # Must be of int type
        self.paramAllowed('bMute', [0, 1])     # It can be either 1 or 0

        # Energy cut coefficient
        self.paramAddOpt('iEnergyCut', 'Energy cut coefficient', noprint=1, default=1e-12)
        self.paramType('iEnergyCut', (int, float))  # Must be a number
        self.paramHE('iEnergyCut', 0)  # Must be higher or equal to zero...
        self.paramL('iEnergyCut', 1)  # ... and lower than 1

        # L2 stop criteria - after how many L2 optimisations it should be stopped
        self.paramAddOpt('nL2Stop', 'L2 stop criteria', noprint=1, default=1e-12)
        self.paramType('nL2Stop', (int, float))  # Must be a number
        self.paramH('nL2Stop', 0)  # Must be higher than zero...

        # Signal dictionaries (for analysis purposes)
        self.paramAddOpt('lDict', 'signal dictionaries (for analysis purposes)', noprint=1)
        self.paramType('lDict', list)          # Must be a list
        self.paramTypeEl('lDict', np.ndarray)  # with Numpy arrays
        self.paramSizH('lDict', 0)             # The list can not be empty

        # Indices of columns of dictionary used to reconstruct the signal  (for analysis purposes)
        self.paramAddOpt('lInxDict', 'indices of columns of dictionary (for analysis purposes)', noprint=1)
        self.paramType('lInxDict', list)          # Must be a list
        self.paramTypeEl('lInxDict', np.ndarray)  # with Numpy arrays
        self.paramSizH('lInxDict', 0)             # The list can not be empty

        # Reference signal (for analysis purposes)
        self.paramAddOpt('mSigRef', 'Reference signal', noprint=1)
        self.paramType('mSigRef', np.ndarray)         # Must be a Numpy array
        self.paramTypeEl('mSigRef', (int, float))     # Elements must be of float or int type
        self.paramNDimLE('mSigRef', 2)                # Must be a 1, or 2 dimensional matrix

        # Success threshold
        self.paramAddOpt('iSNRSuccess', 'Success threshold', noprint=1, default=15)
        self.paramType('iSNRSuccess', (int, float))   # Must be a Numpy array
        self.paramH('iSNRSuccess', -np.inf)
        self.paramL('iSNRSuccess', np.inf)


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


    def __engine(self):

        # Get the number of the observed signals
        nObSig = len(self.lObserved)
        self.nObSig = nObSig

        # If the optimization problems are complex, make them real
        if self.bComplex == 1:
            self.lTheta = self._makeRealProblem(self.lTheta)

        # -----------------------------------------------------------------
        # Loop over all the observed signals
        self.lCoeff = []   # Start a list with signal coefficients
        self.lmX = []      # List with matrix with vectors x found in every iteration
        self.lIter = []    # The number of iterations
        self.lAux = []     # Dictionaries with auxiliary data
        for inxSig in np.arange(nObSig):

            # Run reconstruction of the current signal
            (vCoef, mX, iIter, dAuxDict) = self._recon1sig(inxSig)

            # Store the coefficients in the list with coefficients
            self.lCoeff.append(vCoef)
            self.lmX.append(mX)
            self.lIter.append(iIter)
            self.lAux.append(dAuxDict)

        # -----------------------------------------------------------------
        # Construct the complex output coefficients vector (if needed)
        if self.bComplex == 1:
            self.lCoeff = self._makeComplexOutput(self.lCoeff)
        # -----------------------------------------------------------------

        # -----------------------------------------------------------------
        self._postprocessing()
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
        (vCoef, mX, iIter, dAuxDict) = self._irlsXL1(mTheta, vObSig, inxSig)
        vCoef.shape = (vCoef.size,)

        return (vCoef, mX, iIter, dAuxDict)


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


    # =====================================================================
    # Reconstruction irls
    # =====================================================================
    def _irlsXL1(self, mA, vY, inxSig):

        # Take the parameters
        iMaxIter = self.iMaxIter
        iConvStop = self.iConvStop
        iPowerCut = self.iEnergyCut
        nL2Stop = self.nL2Stop

        # -------------------------------------------------------------------------
        # ALLOCATE DATA FOR ANALYSIS PURPOSES:
        (_, nCols) = mA.shape     # Take the number of rows and columns in Theta

        mX = np.zeros((nCols, iMaxIter))    # Matrix with vectors found in every iteration
        vL2found = np.zeros(iMaxIter)       # Vectors found in L2 computations

        vXleft = np.zeros(iMaxIter)  # The number of elements of the vector over the power threshold
        mPreservedInd = np.nan*np.zeros((nCols, iMaxIter))   # Indices of preserved elements of the vector X

        mXL2 = np.zeros((nCols, iMaxIter))  # Matrix with vectors found in L2 side check
        # -------------------------------------------------------------------------

        # COMPUTATIONS START HERE:
        vX = self.solverL2(mA, vY)

        # Loop over all iterations
        strStopCond = 'Max iterations'
        for iIter in np.arange(iMaxIter):

            # Store the previous solution
            vX_prev = vX.copy()

            # Compute the next vX value
            vX = self.irlscore(vX, mA, vY)

            # Power cut
            (vInxPreserved, iLeft) = self.powercut(vX, iPowerCut, nCols)

            # Perform the side L2 optimisation, if it makes sense
            (bL2, vXL2) = self.L2recon(iLeft, vY, mA, vInxPreserved, vX, mX, iIter)
            vL2found[iIter] = bL2

            # Check convergence condition
            (bStop, strStopCond) = self.check_convergence(vX, vX_prev, vL2found, iIter, iConvStop, nL2Stop)

            # -----------------------------------------------------------------------------------------
            # Store data from the current iteration
            vX_1dim = vX.copy(); vX_1dim.shape = (nCols, ); mX[:, iIter] = vX_1dim  # The found x vector in
                                                                                    # the 'mX' matrix

            # Store the number of preserved elements of a dictionary and indices of preserved elements
            vXleft[iIter] = iLeft
            mPreservedInd[np.arange(vInxPreserved.size), iIter] = vInxPreserved

            # L2
            if bL2 == 1:
                mXL2[:, iIter] = vXL2

            # Stop, if needed
            if bStop == 1:
                break
            # -----------------------------------------------------------------------------------------


        # -------------------------------------------------
        # Take the correct output
        if strStopCond == 'Max iterations':
            vXfinal = vX
        elif strStopCond == 'IRLS conv':
            vXfinal = vX
        elif strStopCond == 'L2 conv':
            vXfinal = vXL2

        # Cut down the auxiliary matrices
        mX = mX[:, np.arange(iIter+1)]
        vL2found = vL2found[np.arange(iIter+1)]
        vXleft = vXleft[np.arange(iIter+1)]
        mPreservedInd = mPreservedInd[:, np.arange(iIter+1)]
        mXL2 = mXL2[:, np.arange(iIter+1)]

        # Generate iterations vector
        vIter = np.arange(1, iIter+2)  # Iterations vector

        # Compute SNR for all the iterations
        (vSNR, vSNRL2) = self.SNRvsIter(vIter, mX, mXL2, self.lDict, self.lInxDict, self.mSigRef, inxSig)

        # Start the output dictionary with the auxiliary data
        dAuxDict = dict()
        dAuxDict['vXfinal'] = vXfinal.T            # Final vector with signal coefficients
        dAuxDict['vX'] = vX.T                      # Vector from the main iterations
        dAuxDict['vXleft'] = vXleft
        dAuxDict['mX'] = mX                        # Vectors from all the main iterations
        dAuxDict['strStopCond'] = strStopCond      # Correct stop conditions
        iIter = iIter + 1
        dAuxDict['iIter'] = iIter
        dAuxDict['vIter'] = vIter
        dAuxDict['mPreservedInd'] = mPreservedInd
        dAuxDict['mXL2'] = mXL2
        dAuxDict['vL2found'] = vL2found
        dAuxDict['vSNR'] = vSNR
        dAuxDict['vSNRL2'] = vSNRL2

        return (vXfinal.T, mX, iIter-1, dAuxDict)


    def _postprocessing(self):

        # The average number of finished iterations
        self.iAvgIter = sum(self.lIter) / len(self.lIter)

        # The stop reasons:
        self.lReasons = []         # 0: max iterations, 1: main IRLS convergence, 2: L2 stop condition
        self.iStopMaxIter = 0      # How many time IRLS was stoped by max iterations?
        self.iStopIRLSConv = 0     # How many times IRLS was stopped by convergence of the main line?
        self.iStopL2 = 0           # How many time  IRLS was stopped by L2 stope reasons?

        # Loop over all the reconstructed signals
        for iObSig in range(self.nObSig):
            if self.lAux[iObSig]['strStopCond'] == 'Max iterations':
                self.lReasons.append(0)
                self.iStopMaxIter = self.iStopMaxIter + 1
            elif self.lAux[iObSig]['strStopCond'] == 'IRLS conv':
                self.lReasons.append(1)
                self.iStopIRLSConv = self.iStopIRLSConv + 1
            elif self.lAux[iObSig]['strStopCond'] == 'L2 conv':
                self.lReasons.append(2)
                self.iStopL2 = self.iStopL2 + 1

            # Compute the ratio
            self.iRStopMaxIter = self.iStopMaxIter / self.nObSig
            self.iRStopIRLSConv = self.iStopIRLSConv / self.nObSig
            self.iRStopL2 = self.iStopL2 / self.nObSig

        # Compute the average SNR achieved by the main line and by L2 optimization
        lSNR = []
        lSNRL2 = []
        for iObSig in range(self.nObSig):
            lSNR.append(self.lAux[iObSig]['vSNR'][-1])
            lSNRL2.append(self.lAux[iObSig]['vSNRL2'][-1])
        self.iSNRAvgMain = sum(lSNR) / len(lSNR)
        self.iSNRAvgL2 = sum(lSNRL2) / len(lSNRL2)

        # Conpute the average successful ratio
        vSNR = np.array(lSNR)
        vSNRL2 = np.array(lSNRL2)
        self.iSR = vSNR[vSNR > self.iSNRSuccess].size / vSNR.size
        self.iSRL2 = vSNRL2[vSNRL2 > self.iSNRSuccess].size / vSNRL2.size


    # Compute SNR for all the iterations
    def SNRvsIter(self, vIter, mX, mXL2, lDict, lInxDict, mSigRef, inxSig):

        vSNR = np.zeros(vIter.shape)     # Allocate vector for SNR
        vSNRL2 = np.zeros(vIter.shape)   # Allocate vector for SNR L2

        if (not self.wasParamGivenVal(lDict)) or (not self.wasParamGivenVal(mSigRef)):
            return (vSNR, vSNRL2)

        # Take a dictionary for the current signal
        if len(lDict) > 1:
            mDict = lDict[inxSig]
        else:
            mDict = lDict[0]

        # Take a reference signal for the current signal
        vSigRef = mSigRef[inxSig, :]

        # If indices of wanted coefficients were not given, the wanted
        # coefficients are all the coeffcients in the reconstructed vector
        if not self.wasParamGivenVal(lInxDict):
             (_, nCols) = mDict.shape
             vInxDict = np.arange(nCols)
        else:
            # Take the correct indices of dictionary for the current signal
            if len(lInxDict) > 1:
                vInxDict = lInxDict[inxSig]
            else:
                vInxDict = lInxDict[0]

        mDict = mDict[:, vInxDict]     # Cut down the dictionary to the
                                       # dictionary which is of interest

        analysisSNR = rxcs.ana.SNR()   # Create SNR analysis block
        analysisSNR.bMute = 1
        analysisSNR.mSigRef = vSigRef

        #--------------------------------------------------------------
        # Main IRLS - loop over all iterations

        # Loop over all the iterations
        for inxIter in vIter:

            #--------------------------------------------------------------
            # Main line:
            # Get the current coefficients and reconstruct the signal
            vX = mX[:, inxIter-1]
            vX = vX[vInxDict]
            vSigRecon = np.dot(mDict, vX).real
            vSigRecon.shape = (vSigRecon.size, )

            # Run the SNR analysis
            analysisSNR.mSig = vSigRecon
            analysisSNR.run()

            # Store SNR in the vector
            iSNR = analysisSNR.iSNR
            vSNR[inxIter-1] = iSNR

            #--------------------------------------------------------------
            # L2:

            # Get the current coefficients and reconstruct the signal
            vXL2 = mXL2[:, inxIter-1]
            vXL2 = vXL2[vInxDict]
            vSigReconL2 = np.dot(mDict, vXL2).real
            vSigReconL2.shape = (vSigReconL2.size, )

            # Run the SNR analysis
            analysisSNR.mSig = vSigReconL2.copy()
            analysisSNR.run()

            # Store SNR in the vector
            iSNR = analysisSNR.iSNR
            vSNRL2[inxIter-1] = iSNR.copy()

        #--------------------------------------------------------------
        return (vSNR, vSNRL2)


    def irlscore(self, vX, mA, vY):
        (nRows, _) = mA.shape     # Take the number of rows and columns in Theta

        # Weighted matrix
        mAWeightedX = np.ones(mA.shape)      # Allocate new matrix with weights
        for inxRow in np.arange(nRows):      # Compute the matrix with weights
            mAWeightedX[inxRow, :] = np.abs(vX) * mA[inxRow, :]

        # Compute the current x vector
        mAtemp = np.dot(mAWeightedX, mA.T)
        vX_temp = self.solverL2(mAtemp, vY)
        vX = np.dot(mAWeightedX.T, vX_temp.T).T
        return vX


    def powercut(self, vX, iPowerCut, nCols):

        vInxCols = np.arange(nCols)   # Construct an auxiliary vector with indices
                                      # of columns of the matrix A

        # ----------------------------------------------------
        # Power cut
        iXPower = np.sum(np.abs(vX) * np.abs(vX))  # Total power of the vector
        vXX = vX * vX              # The power of elements of the vector X
        vXX.shape = (vXX.size, )   # ^

        # Compute how many elements of X are below the threshold total power
        iRemoved = np.sum(vXX < iPowerCut*iXPower)

        vInxPreserved = vInxCols[vXX >= iPowerCut*iXPower]  # Indices of preserved columns
        iLeft = nCols - iRemoved

        return (vInxPreserved, iLeft)


    def L2recon(self, iLeft, vY, mA, vInxPreserved, vX, mX, iIter):

        # If L2 is switched off, then return
        if self.bL2 == 0:
            return (0, np.nan)

        # Make a decision should L2 be started and which which columns?
        (bL2, vInxPreserved) = self._startL2(iLeft, vY, mA, vInxPreserved, vX, mX, iIter)

        # Perform an L2 check
        if bL2 == 1:
            mADamaged = mA[:, vInxPreserved]            
            vXL2_ = self.solverL2(mADamaged, vY)
            (_, nCols) = mA.shape     # Take the number of rows and columns in Theta
            vXL2 = np.zeros(nCols)
            vXL2[vInxPreserved] = vXL2_
        else:
            vXL2 = np.nan
        return (bL2, vXL2)


    def _startL2(self, iLeft, vY, mA, vInxPreserved, vX, mX, iIter):

        # Make a decision to start L2 and with which columns of a dictionary
        if iLeft < vY.size:
            bL2 = 1
        else:
            bL2 = 0
        return (bL2, vInxPreserved)


    def check_convergence(self, vX, vX_prev, vL2found, iIter, iConvStop, nL2Stop):

        bStop = 0    # Clear stop flag
        strStopCond = 'Max iterations'  # Clear stop condition

        if iIter == 0:
            return (bStop, strStopCond)

        # Main IRLS convergence
        vXd = vX - vX_prev              # Compute the difference vector
        iXd_n2 = np.linalg.norm(vXd)    # Second norm of the difference vector
        iX_n2 = np.linalg.norm(vX)      # Second norm of the current x vector
        if (iXd_n2 / iX_n2 ) < iConvStop:  # Should we stop?
            bStop = 1
            strStopCond = 'IRLS conv'

        # L2 found
        if iIter >= (nL2Stop - 1):
            vInx = np.arange(iIter - nL2Stop + 1, iIter+1)

            vL2found_ = vL2found[vInx]
            if sum(vL2found_) == (nL2Stop):
                bStop = 1
                strStopCond = 'L2 conv'

        return (bStop, strStopCond)

    
    # =====================================================================
    # Solver L2
    # =====================================================================
    def solverL2(self, mA, vY):
                
        self.L2solv.mA = mA
        self.L2solv.vY = vY
        self.L2solv.bMute = 1
        self.L2solv.run()   # Find the initial vector X
        vX = self.L2solv.vX.copy() 
        return vX
