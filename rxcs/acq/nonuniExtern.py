"""
This a nonuniform sampler with externally acquired sampling patterns. |br|

The module samples the given signals (**mSig**) if the signals are given.
Otherwise, the module runs in 'dummy mode' - only observation matrices are 
created. |br|

The sampling patterns are taken from a Numpy array with sampling 
patterns (**mPatterns**). |br|

Parameter **vPattInx** defines which random sampling pattern will be applied
on every signal.

The number of elements in **vPattInx** must be equal to the number of signals 
in **mSig** array.

Example:  **vPattInx** = [3, 0] means that a sampling pattern form the row 
          with index 3 (4th row) will be applied on the first signal, 
          and a sampling pattern from the row with index 0 (1st row ) will 
          be applied on the second signal.

If **vPattInx** is not given, than a random sampling pattern from **mPatterns** 
is applied on every signal.  |br|


*Examples*:
    Please go to the *examples/acquisitions* directory for examples on how to 
    use the sampler. |br|

*Settings*:
    Parameters of the sampler are described below.

    Take a look on '__parametersDefine' function for more info on the 
    parameters.

    Parameters of the sampler are attributes of the class which must/can
    be set before the sampler is run.

    Required parameters:

    - a. **tS** (*float*): time of input signals

    - b. **fR** (*float*): input signals' representation sampling frequency

    - c. **mPatterns** (*Numpy array 2D*): Numpy array 2D with pattern

    - d. **Tg** (*float*): patterns sampling grid


    Optional parameters:

    - e. **mSig** (*Numpy array 2D*): Input signals
                                      [default = not given]
                                      If input signals are not given, then
                                      the sampler becomes a 'dummy' sampler - 
                                      it only creates observation matrices.

    - f. **vPattInx** (*Numpy array 1D*):  Indices of sampling patterns 
                                           applied on signals.
                                           It must have the same lenght as  
                                           the mumber of input signals.
                                           [default = not given]

    - g. **bMute** (*int*):    mute the console output from the sampler 
                               [default = 0]


*Output*:
    Description of the sampler output is below. 
    This is the list of attributes of the sampler class which are available 
    after calling the 'run' method:

    Observed signals:
    - a. **mObSig** (*Numpy array 2D*): Observed sampled signals
                                       [only if **mSig** was given]

    Sampling patterns:
    - b. **mPatts** (*Numpy array 2D*): Sampling patterns (as grid indices)

    - c. **mPattsRep** (*Numpy array 2D*):  Sampling patterns 
                                            (as signal representaion points)

    - d. **mPattsT** (*Numpy array 2D*):   Sampling patterns
                                           (as time moments)

    - e **vPattInx** (*Numpy array 1D*):   Indices of sampling patterns used
                                           on signals.

    Observation matrices:                         
    - f. **lPhi** (list)   List with observation matrices.
                           One matrix p. signal.


*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    0.1  | 1-SEP-2014 : * Initial version. |br|
    1.0  | 12-SEP-2014 : * Version 1.0 is ready. |br|
    2.0  | 19-AUG-2015 : * Version 2.0 is ready. |br|

*License*:
    BSD 2-Clause
"""

from __future__ import division
import rxcs
import numpy as np


class nonuniExtern(rxcs._RxCSobject):

    def __init__(self):
        rxcs._RxCSobject.__init__(self)    # Make it a RxCS object 
        
        self.strRxCSgroup = 'Acquisition'         # Name of group of RxCS modules
        self.strModuleName = 'External sampler'   # Module name

        self.__inputSignals()          # Define input signals
        self.__parametersDefine()      # Define the parameters

    # Input signals
    def __inputSignals(self):

        # Time of input signals
        self.paramAddMan('tS', 'Time of input signals', unit='s')
        self.paramType('tS', (int, float))
        self.paramH('tS', 0)
        self.paramL('tS', np.inf)

        # Input signals representation sampling frequency
        self.paramAddMan('fR', 'Input signals representation sampling frequency', unit='Hz')
        self.paramType('fR', (int, float))
        self.paramH('fR', 0)
        self.paramL('fR', np.inf)

        #  Array with input signals, one signal p. row
        self.paramAddOpt('mSig', 'Input signals', noprint=1)
        self.paramType('mSig', np.ndarray)
        self.paramTypeEl('mSig', (int, float))
        self.paramNDimLE('mSig', 2)

    # Define parameters
    def __parametersDefine(self):

        # Matrix with sampling patterns
        self.paramAddMan('mPatterns', 'Sampling patterns', noprint=1)
        self.paramType('mPatterns', np.ndarray)
        self.paramTypeEl('mPatterns', (int))
        self.paramNDimEq('mPatterns', 2)
        self.paramDimH('mPatterns',0, 'rows')  # There must be at least one sampling pattern
        self.paramH('mPatterns', 0)   # Patterns must not containt zeroes

        # Grid period of a sampling pattern
        self.paramAddMan('Tg', 'Grid period of sampling patterns')
        self.paramType('Tg', (int, float))
        self.paramH('Tg', 0)
        self.paramL('Tg', np.inf)

        # Vector with indices of sampling patterns which should be used
        self.paramAddOpt('vPattInx', 'Vector with indices of sampling patterns which should be used', noprint=1)
        self.paramType('vPattInx', np.ndarray)
        self.paramTypeEl('vPattInx', int)
        self.paramNDimEq('vPattInx', 1)
        self.paramDimEq('vPattInx', 'mSig', 0, 'rows')   # The number of indices must equal the number of signals in mSig
        self.paramHE('vPattInx', 0)                      # All the indices must be higher or equal to 0

        # 'Mute the output' flag
        self.paramAddOpt('bMute', 'Mute the output', noprint=1, default=0)
        self.paramType('bMute', int)            # Must be of int type
        self.paramAllowed('bMute', [0, 1])      # It can be either 1 or 0

    # Run
    def run(self):
        
        self.parametersCheck()         # Check if all the needed partameters are in place and are correct
        self.parametersPrint()         # Print the values of parameters

        self.engineStartsInfo()   # Info that the engine starts
        self.__engine()           # Run the engine
        self.engineStopsInfo()    # Info that the engine ends
        return self.__dict__      # Return dictionary with the parameters

    def __engine(self):

        # Make the array with signals a 2 dimensional array, if it was given
        if self.wasParamGivenVal(self.mSig):
            self.mSig = self.makeArray2Dim(self.mSig)

        # Check configuration of sampling
        self._checkSampPatts(self.Tg, self.fR, self.tS, self.mPatterns, self.vPattInx)

        # Sample the signals
        (self.mObSig, self.mPattsRep, self.mPattsT, self.vPattInx) = self._sampleSignals(self.Tg, self.fR, self.tS, self.mPatterns, self.mSig, self.vPattInx)

        # Generate the observation matrices
        self.lPhi = self._generObser(self.fR, self.tS, self.mPattsRep, self.mSig, self.vPattInx)
        return        

    def _checkSampPatts(self, Tg, fR, tS, mPatterns, vPattInx):
        """
        This function checks the parameters of sampling patterns given to the sampler.

        Args:
            Tg:           [number]           Sampling gird period
            fR:           [number]           Signal representation sampling frequency 
            tS:           [number]           Signal time
            mPatterns:    [Numpy array 2D]   Sampling patterns
            vPattInx:     [Numpy array 1D]   Indices of sampling patterns which should be used
    
        Returns:
            none
        """

        # -----------------------------------------------------------------
        # Check if the signal representation sampling frequency is compatible
        # with the sampling period
        if np.abs(np.round(Tg * fR) - (Tg * fR)) > (1e-9*(Tg * fR)):
            strError = ('The sampling grid period of pattern is incompatible with')
            strError = strError + (' the signals representation sampling ')
            strError = strError + ('frequency')
            raise ValueError(strError)

        # -----------------------------------------------------------------
        # Check if the sampling patterns are not sampling outside the time
        # of signals
        tMax = np.max(mPatterns) * Tg 
        if tMax > tS:
            strError = ('Patterns contain sampling points which sample outside the time range of signals!')
            raise ValueError(strError)

        # -----------------------------------------------------------------
        # Check if the indices od samplin patterns which should be used are 
        # not higher than the number of sampling patterns
        if self.wasParamGivenVal(vPattInx):
            (nPatts, _) = mPatterns.shape   # Get the number of given sampling patterns
            if vPattInx[vPattInx > (nPatts - 1)].size > 0:
                strError = ('The vector with indices of sampling patterns contain indices which are higher than the number of patterns!')
                raise ValueError(strError)
            
        return

    # Sample the signals
    def _sampleSignals(self, Tg, fR, tS, mPatterns, mSig, vPattInx):
        """
        This function samples signals using the previously generated
        sampling patterns.
    
        Args:
            Tg:           [number]           Sampling gird period
            fR:           [number]           Signal representation sampling frequency 
            tS:           [number]           Signal time
            mPatterns:    [Numpy array 2D]   Sampling patterns
            mSig:         [Numpy array 2D]   Signals to be sampled
            vPattInx:     [Numpy array 1D]   Indices of sampling patterns which should be used
            
        Returns:
            mObSig:       [Numpy array 2D]   Observed signals
            mPattsRep:    [Numpy array 2D]   Sampling patterns as indices of signal representation sampling points
            mPattsT:      [Numpy array 2D]   Sampling patterns as time moments 
            vPattInx:     [Numpy array 1D]   Indices of sampling patterns which were used           
        """

        # Compute the patterns as signals representation grid 
        mPattsRep = mPatterns * np.round(Tg * fR)
        mPattsRep = mPattsRep.astype(int)

        # Recalculate the patterns to the time moments
        vTSig = (1 / fR) * np.arange(int(np.round(tS * fR)))   # The time vector of the input signal
        mPattsRep_ = mPattsRep.copy()                    
        (iTPoints, ) = vTSig.shape                        # Get the number of points in the time vector
        mPattsRep_[np.isnan(mPattsRep)] = iTPoints - 1    # Change nan into pointer to nan          
        mPattsT = vTSig[mPattsRep]

        # Get the number of signals
        if self.wasParamGivenVal(mSig):
            (nSigs, _) = mSig.shape               
        else: 
            nSigs = 0

        # Get the number of given sampling patterns and the maximum size of a pattern
        (nPatts, iMaxPat) = mPatterns.shape   

        # Construct a vector with indices for sampling patterns,
        # if such a vector was not yet given
        if not self.wasParamGivenVal(vPattInx):
            vPattInx = np.random.randint(0, nPatts, nSigs)

        mObSig = np.nan * np.zeros((nSigs, iMaxPat))  # Allocate an array for the observed signals

        # Loop over all the signals
        for inxSig in range(nSigs):
             vPatt = mPattsRep[vPattInx[inxSig], :]      # Take the current pattern   
             vPatt = vPatt[np.invert(np.isnan(vPatt))]   # Clean the pattern
             vObSig = mSig[inxSig, vPatt]                # Create the current observed signal

             # Store the observed signal in the array for the observed signals
             mObSig[inxSig, np.arange(vObSig.size)] = vObSig
            
        return (mObSig, mPattsRep, mPattsT, vPattInx)

    # Generate the observation matrices    
    def _generObser(self, fR, tS, mPattsRep, mSig, vPattInx):
        """
        This function generates the observation matrices.
    
        Args:
            fR:           [number]           Signal representation sampling frequency 
            tS:           [number]           Signal time
            mPattsRep:    [Numpy array 2D]   Sampling patterns as indices of signal representation sampling points
            mSig:         [Numpy array 2D]   Signals to be sampled
            vPattInx:     [Numpy array 1D]   Indices of sampling patterns which were used

        Returns:
            lPhi:     [list]    List with observation matrices for all the signals
        """

        # Get the number of signals
        if self.wasParamGivenVal(mSig):
            (nSigs, _) = mSig.shape
        else:
            nSigs = 0

        # Compute the number of representation sampling points in the input signals
        nSmp = int(np.round(fR * tS)) 

        # Get the number of sampling patterns
        (nPatt, _) = mPattsRep.shape

        # Start the list with the observation matrices
        lPhi = []    

        # Generate the observation matrices for every signal, if the signals were given
        if nSigs > 0:
            for inxSig in np.arange(nSigs):  # <- loop over all signals
                vPatt = mPattsRep[vPattInx[inxSig], :]     # Take the current pattern   
                mPhi = self._gener1Obser(vPatt, nSmp)      # Create an observation matrix for the current pattern
                lPhi.append(mPhi.copy())                   # Add the matrix to the list

        # Generate the observation matrices for every pattern (dummy sampler), if the signals were not given
        if nSigs == 0:
            for inxSamp in np.arange(nPatt):  # <- loop over all sampling patterns
                vPatt = mPattsRep[inxSamp, :]              # Take the current pattern   
                mPhi = self._gener1Obser(vPatt, nSmp)      # Create an observation matrix for the current pattern
                lPhi.append(mPhi.copy())                   # Add the matrix to the list

        return lPhi

    # Generate the observation matrix for the current sampling pattern
    def _gener1Obser(self, vPatt, nSmp):
        """
        This function generates a single observation matrix for a sampling pattern.
    
        Args:
            vPatt:   [Numpy array 1D]   Sampling pattern (as indices of signals' representaion sampling points)
            nSmp:    [number]           The number of signal representation sampling points

        Returns:
            mPhi:    [Numpy array 2D]   The generated observation matrix
        """
        vPatt = vPatt[np.invert(np.isnan(vPatt))]  # Clean the pattern
        nPatSiz  = vPatt.size  # Get the size of the pattern

        mPhi = np.zeros((nPatSiz, nSmp))   # Allocate the observation matrix
        inxRow = 0                         # Reset index of a row
        for inxCol in vPatt:   # <- loop over all sampling points in a pattern
            mPhi[inxRow, int(inxCol)] = 1
            inxRow = inxRow + 1
        return mPhi

