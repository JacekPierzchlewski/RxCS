"""
This is a saturation block. |br|

The modules saturates the given signal. |br|

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0  | 03-MAR-2015 : * Initial version. |br|
    2.0  | 17-AUG-2015 : * Objectified version (2.0) |br|


*License*:
    BSD 2-Clause
"""
from __future__ import division
import rxcs
import numpy as np

class satur(rxcs._RxCSobject):

    def __init__(self, *args):
        rxcs._RxCSobject.__init__(self)    # Make it a RxCS object 
        
        self.strRxCSgroup = 'Acquisition'       # Name of group of RxCS modules
        self.strModuleName = 'saturation'       # Module name        

        self.__inputSignals()          # Define input signals
        self.__parametersDefine()      # Define the parameters
        self.__inputOptSignals()       # Define optional input signals

        # If there are arguments given when the object was created, then run the engine  
        if len(args) > 0:
            self.run(*args)


    # Input signals
    def __inputSignals(self):

        # 1d/2d array with input signals, one signal p. row
        self.paramAddMan('mSig', 'Input signals', noprint=1)
        self.paramType('mSig', np.ndarray)
        self.paramTypeEl('mSig', (int, float))
        self.paramNDimLE('mSig', 2)

    # Define parameters
    def __parametersDefine(self):

        # The minimum allowed amplitude of a signal
        self.paramAddMan('iMinAmp', 'The minimum allowed amplitude of a signal')
        self.paramType('iMinAmp', (int, float))   # Must be of int or float type

        # The maximum allowed amplitude of a signal
        self.paramAddMan('iMaxAmp', 'The maximum allowed amplitude of a signal')
        self.paramType('iMaxAmp', (int, float))   # Must be of int or float type
        self.paramH('iMaxAmp', 'iMinAmp')         # The maximum allowed amplitude must be higher than the minimum amplitude

        # 'Mute the output' flag
        self.paramAddOpt('bMute', 'Mute the output', noprint=1, default=0)
        self.paramType('bMute', int)           # Must be of int type
        self.paramAllowed('bMute',[0, 1])      # It can be either 1 or 0

    # Define optional input signals
    def __inputOptSignals(self):

        # Signal time vector
        self.paramAddOpt('vT', 'Signal time vector', noprint=1, default=np.empty(0))
        self.paramType('vT', np.ndarray)      # Must be a Numpy array
        self.paramTypeEl('vT', (int, float))  # Elements must be of float or int type 
        self.paramNDimEq('vT', 1)             # Must be a 1 dimensional vector

        # Sampling patterns (grid indices)
        self.paramAddOpt('mPatts', 'Sampling patterns', noprint=1, default=np.empty((0, 0)))
        self.paramType('mPatts', np.ndarray)      # Must be a Numpy array
        self.paramTypeEl('mPatts', (int, float))  # Elements must be of float or int type 

        # Sampling patterns (signal rep. sampling points)
        self.paramAddOpt('mPattsRep', 'Sampling patterns  (signal rep. sampling points)', noprint=1, default=np.empty((0, 0)))
        self.paramType('mPattsRep', np.ndarray)      # Must be a Numpy array
        self.paramTypeEl('mPattsRep', (int, float))  # Elements must be of float or int type 
        self.paramNDimEq('mPattsRep', 2)             # Must be a 2 dimensional matrix

        # Sampling patterns (time moments)
        self.paramAddOpt('mPattsT', 'Sampling patterns  (time moments)', noprint=1, default=np.empty((0, 0)))
        self.paramType('mPattsT', np.ndarray)      # Must be a Numpy array
        self.paramTypeEl('mPattsT', (int, float))  # Elements must be of float or int type 
        self.paramNDimEq('mPattsT', 2)             # Must be a 2 dimensional matrix

        # Observation matrices
        self.paramAddOpt('lPhi', 'Observation matrices', noprint=1, default=[])
        self.paramType('lPhi', list)            # Must be a list
        self.paramTypeEl('lPhi', np.ndarray)    # Elements of this list must be Numpy arrays

    # Run
    def run(self, *args):

        self.parametersProcess(*args)  # Get parameters given directly to 'run' function
        self.parametersCheck()         # Check if all the needed partameters are in place and are correct
        self.parametersPrint()         # Print the values of parameters
        
        self.engineStartsInfo()  # Info that the engine starts
        self.__engine()          # Run the engine
        self.engineStopsInfo()   # Info that the engine ends
        return self.__dict__     # Return dictionary with the parameters

    # Engine
    def __engine(self):

        self.mSig = self._make2DSignals(self.mSig) 
        
        # Saturate signals
        (self.mSaturMark, self.nSatMin, self.nSatMax, self.mObSig) = self._saturateSignals(self.mSig, self.iMinAmp, self.iMaxAmp)

        # Generate 'clean' observed signals
        self.lObSigClean = self._cleanObSignals(self.mSig, self.mSaturMark)
        self.lvTClean = self._cleanvT(self.vT, self.mSaturMark)

        # Generate 'clean' sampling patterns, with saturated samples removed
        self.lPattsClean = self._cleanPattern(self.mPatts, self.mSaturMark)
        self.lPattsTClean = self._cleanPattern(self.mPattsT, self.mSaturMark)
        self.lPattsRepClean = self._cleanPattern(self.mPattsRep, self.mSaturMark)

        # Clean observation matrices
        self.lPhiClean = self._cleanObserMat(self.lPhi, self.mSaturMark)        
        
        # Print results of saturation
        self._printResults(self.mSig, self.nSatMin, self.nSatMax)
        return

    def _make2DSignals(self, mSig):
        # Make the matrix with signals 2 dim, if it is 1 dim
        if mSig.ndim == 1:
            mSig = mSig.copy()            
            mSig.shape = (1, mSig.size)
        return mSig
        
    def _saturateSignals(self, mSig, iMinAmp, iMaxAmp):
    
        # -----------------------------------------------------------------
        # Saturation markers
        mSaturMark = np.zeros(mSig.shape)      # Create an array with saturation markers
        mSaturMark[mSig < iMinAmp] = -1     # Samples saturated because of too low value
        mSaturMark[mSig > iMaxAmp] = 1      # Samples saturated because of too high value
    
        nSatMin = mSaturMark[mSaturMark == -1].size   # The total number of saturated samples because of too low value
        nSatMax = mSaturMark[mSaturMark == 1].size    # The total number of saturated samples because of too high value

        # -----------------------------------------------------------------
        # Generate the observed saturated signals
        mObSig = mSig.copy()
        mObSig[mSaturMark == -1] = self.iMinAmp
        mObSig[mSaturMark == 1] = self.iMaxAmp
        
        return (mSaturMark, nSatMin, nSatMax, mObSig)
        
    def _cleanObSignals(self, mObSig, mSaturMark):
        """
            Generate the observed limited signals with saturated signals removed
        """

        (nSigs, _) = mObSig.shape        # Get the number of observed signals 
        lObSigClean = []
        for inxSig in np.arange(nSigs):
            vObSig = mObSig[inxSig, :].copy()          # Get the current observed signal
            vSaturMark = mSaturMark[inxSig, :]         # Get the current saturation marks
            vObSigClean = vObSig[vSaturMark == 0]      # Clean the current observed signal
            lObSigClean.append(vObSigClean)            # Add the current clean observed signal into the list
        return lObSigClean

    def _cleanvT(self, vT, mSaturMark):
        (nSigs, _) = mSaturMark.shape        # Get the number of observed signals 
        lvTClean = []

        # If vT was not given, return from the function doing nothing         
        if vT.size == 0:
            return lvTClean
            
        for inxSig in np.arange(nSigs):
            vT = self.vT.copy()          # Copy the time vector for the 
            vSaturMark = mSaturMark[inxSig, :]   # Get the current saturation marks
            vTClean = vT[vSaturMark == 0]        # Clean the current time vector
            lvTClean.append(vTClean)          # Add the current clean time vector into the list

        return lvTClean

    def _cleanPattern(self, mPatterns, mSaturMark):

        # -----------------------------------------------------------------
        # Patterns (as grid indices):
        lPattsClean = []
        if mPatterns.size > 0:
            mPatterns_ = mPatterns.copy()                         # Create a working copy of an array with patterns
            mPatterns_ = mPatterns_.astype('float')               # Type of patterns must be float to include NaNs 
            (nPatts, _) = mPatterns_.shape                        # Get the number of patterns
            mPatterns_[np.invert(mSaturMark == 0)] = np.nan       # Mark the saturated samples with NaN 
            for inxPat in np.arange(nPatts):                      # Loop over all patterns    
                vPatt = mPatterns_[inxPat, :]
                vPatt = vPatt[np.invert(np.isnan(vPatt))]         # Remove all the NaN elements from the smapling pattern
                lPattsClean.append(vPatt)                         # Add a new pattern with removed saturated patterns to the output list
        return lPattsClean

    def _cleanObserMat(self, lPhi, mSaturMark):

        lPhiClean = []                            
        for inxObMat in np.arange(len(lPhi)):         # Loop over all observation matrices
            mPhi = lPhi[inxObMat]                     # Get the current original observation matrix...
            (nRows, nCols) = mPhi.shape               # ...and its shape
                          
            vSaturMark = mSaturMark[inxObMat, :]       # Get the saturation markers for the current signal
            nNSSamp = vSaturMark[vSaturMark==0].size   # Get the number of non-saturated samples

            # Generate the clean observation matrix for the current pattern
            mPhiClean = np.zeros((nNSSamp, nCols))   # Allocate the current observation matrix
            inxRowClean = 0                           # Reset the index of the row in the clean observation matrix            
            for inxRow in np.range(nRows):            # Loop over all rows in the original observation matrix
                if vSaturMark[inxRow] == 0:                       
                    # Propagate a row from the observation matrix into the clean observation matrix,
                    # if the sample which correspond to this row was not saturated
                    mPhiClean[inxRowClean, :] = mPhi[inxRow, :]    
                    inxRowClean = inxRowClean + 1                    
                                    
            lPhiClean.append(mPhiClean)   # Store the generated clean observation matrix in the list
        
        return lPhiClean

    # =================================================================
    # Print some statistical info about the results
    # =================================================================
    def _printResults(self, mSig, nSatMin, nSatMax):
        """
        This function generates the observation matrices.
    
        Args:
            nSigs (int):        the number of signals in the input dictioanry
            nSamps (int):       the total number of signal representation sampling points in all the signals
            nSatMin (float):    the total number of saturated samples because of too low value
            nSatMax (float):    the total number of saturated samples because of too high value
    
        Returns:  none
        """

        (nSigs, nSamps) = mSig.shape  # Get the number of signals and the number of samples in one signal
 
        print('')        
        rxcs.console.bullet_param('The total number of signals is', nSigs, '-', '')
        rxcs.console.param('The number of samples in one signal is', nSamps, '-', 'samples')
        rxcs.console.param('The total number of samples is', nSamps*nSigs, '-', 'samples')
    
        rxcs.console.bullet_param('The total number of saturated samples', nSatMin+nSatMax, '-', 'samples')
        rxcs.console.param('which is',(nSatMin+nSatMax)/(nSamps*nSigs)*100, ' ', '%')
    
        rxcs.console.param('The total number of saturated samples because of too low value', nSatMin, '-', 'samples')
        rxcs.console.param('which is',nSatMin/(nSamps*nSigs)*100, ' ', '%')
    
        rxcs.console.param('The total number of saturated samples because of too high value', nSatMax, '-', 'samples')
        rxcs.console.param('which is',nSatMax/(nSamps*nSigs)*100, ' ', '%')
        return

