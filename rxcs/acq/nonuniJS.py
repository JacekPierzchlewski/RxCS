"""
This a nonuniform sampler with jittered sampling (JS) sampling scheme. |br|

The modules samples the given signals nonuniformly. |br|
The sampling aptterns are generated using JS scheme.

The used JS patterns generator is described further in
"Generation and Analysis of Constrained Random Sampling Patterns",
available in arXiv: http://arxiv.org/abs/1409.1002

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

    - a. **mSig** (*Numpy array 2D*): Input signals

    - b. **tS** (*float*): time of input signals

    - d. **fR** (*float*): input signals' representation sampling frequency

    - d. **Tg** (*float*): patterns sampling grid

    - e. **fSamp** (*float*): the requested average sampling frequency of the sampling patterns


    Optional parameters:

    - f. **iSigma** (*float*):  variance of Gaussian random process [default = 1]

    - g. **bMute** (*int*):    mute the console output from the sampler [default = 0]


*Output*:
    Description of the sampler output is below. 
    This is the list of attributes of the sampler class which are available 
    after calling the 'run' method:

    Observed signals:
    - a. **mObSig** (*Numpy array 2D*): Observed sampled signals
    
    Sampling patterns:
    - b. **mPatts** (*Numpy array 2D*): Sampling patterns (as grid indices)

    - c. **mPattsRep** (*Numpy array 2D*):  Sampling patterns (as signal representaion points) 
                                            
    - d. **mPattsT** (*Numpy array 2D*):   Sampling patterns (as time moments)
                                           
    
    Observation matrices:                         
    - e. **lPhi** (list)   List with observation matrices.
                           One matrix p. signal.


    Additional parameters of sampling patterns:    
    - f. **nK_g**  (*int*): the number of grid points in the sampling pattern
    
    - g. **tTau_real** (*float*):   the real time of sampling patterns
    
    - h. **nK_s** (*int*):   the expected number of sampling points in a pattern     
    
    - i. **f_s** (*float*):  the expected average sampling frequency
    
    - j. **nT** (*int*):   the expected average sampling period (as grid pts)
    
    - k  **tT_s**. (*float*):   the expected average sampling period

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0    | 29-JAN-2015 :  * Initial version. |br|
    1.1    | 9-MAR-2015  :  * Observation matrices are grouped in a list, not in a 3D Numpy array |br|
    2.0    | 14-AUG-2015 :  * Objectified version (2.0) |br|
    2.0r1  | 18-AUG-2015 :  * Adjusted to RxCSObject v1.0 |br|


*License*:
    BSD 2-Clause
"""

from __future__ import division
import math
import rxcs
import numpy as np


class nonuniJS(rxcs._RxCSobject):

    def __init__(self, *args):
        rxcs._RxCSobject.__init__(self)    # Make it a RxCS object 
        
        self.strRxCSgroup = 'Acquisition'       # Name of group of RxCS modules
        self.strModuleName = 'JS sampler'       # Module name

        self.__inputSignals()          # Define input signals
        self.__parametersDefine()      # Define the parameters


    # Input signals
    def __inputSignals(self):

        # 1d/2d array with input signals, one signal p. row
        self.paramAddMan('mSig', 'Input signals')
        self.paramType('mSig', np.ndarray)
        self.paramTypeEl('mSig', (int, float))
        self.paramNDimLE('mSig', 2)

        # Input signals representation sampling frequency
        self.paramAddMan('fR', 'Input signals representation sampling frequency', unit='Hz')
        self.paramType('fR', (int, float))
        self.paramH('fR', 0)
        self.paramL('fR', np.inf)

        # Time of input signals
        self.paramAddMan('tS', 'Time of input signals', unit='s')
        self.paramType('tS', (int, float))
        self.paramH('tS', 0)
        self.paramL('fR', np.inf)


    # Define parameters
    def __parametersDefine(self):

        # Patterns sampling grid
        self.paramAddMan('Tg', 'Patterns sampling grid', unit='s')
        self.paramType('Tg', (int, float))   # Must be of int or float type
        self.paramH('Tg', 0)                 # Patterns sampling grid must be higher than zero
        self.paramL('Tg', np.inf)            # ...and lower than infinity
        
        # Requested sampling frequency
        self.paramAddMan('fSamp', 'Requested sampling frequency', unit='Hz')
        self.paramType('fSamp', (int, float))   # Must be of int or float type
        self.paramH('fSamp', 0)                 # Requested sampling frequency must be higher than zero
        self.paramL('fSamp', np.inf)            # ...and lower than infinity

        # Variance of Gaussian random process used by the pattern generator
        self.paramAddOpt('iSigma', 'Variance of Gaussian random process', default=1)
        self.paramType('iSigma', (int, float))   # Must be of int or float type
        self.paramH('iSigma', 0)                 # Variance must be higher than zero
        self.paramL('iSigma', np.inf)            # ...and lower than infinity

        # 'Mute the output' flag
        self.paramAddOpt('bMute', 'Mute the output', noprint=1, default=0)
        self.paramType('bMute', int)           # Must be of int type
        self.paramAllowed('bMute',[0, 1])      # It can be either 1 or 0


    # Run
    def run(self):

        self.parametersCheck()         # Check if all the needed partameters are in place and are correct
        self.parametersPrint()         # Print the values of parameters
        
        self.engineStartsInfo()  # Info that the engine starts
        self.__engine()          # Run the engine
        self.engineStopsInfo()   # Info that the engine ends
        return self.__dict__     # Return dictionary with the parameters


    # Engine of the function
    def __engine(self):

        self._computeParam()    # Compute parameters of sampling
        self._checkConf()       # Check configuration of sampling

        self._generatePatterns()     # Generate the sampling patterns   
        self._sampleSignals()        # Sample the signals
        self._generObser()           # Generate the observation matrices
        return


    # Compute parameters
    def _computeParam(self):
        """
        This function computes parameters of sampling.

        Args:
            none
    
        Returns:
            none

            List of variables added by function to the object:

            nK_g (float):      the number of grid points in the sampling pattern
            tTau_real (float): the real time of sampling patterns
            nK_s (float):      the expected number of sampling points in a pattern
            f_s (float):       the expected average sampling frequency
            nT (float):        the expected average sampling period (as grid pts)
            tT_s (float):      the expected average sampling period
        """

        # Calculate the number of grid points in the sampling period
        nK_g = math.floor(self.tS / self.Tg)

        # Calculate the real time of sampling patterns
        tTau_real = nK_g * self.Tg

        # Calculate the expected number of sampling points in a pattern
        nK_s = int(round(tTau_real * self.fSamp))

        # Calculate the expected average sampling frequency
        f_s = nK_s / tTau_real
    
        # Calculate the expected average sampling period
        tT_s = 1 / f_s
    
        # Calculate the expected average sampling period and recalculate it to
        # the grid
        nT = int(math.ceil(1 / (f_s * self.Tg)))

        self.nK_g = nK_g              # the number of grid points in the sampling pattern
        self.tTau_real = tTau_real    # the real time of sampling patterns
        self.nK_s = nK_s              # the expected number of sampling points in a pattern
        self.f_s = f_s                # the expected average sampling frequency  
        self.nT = nT                  # the expected average sampling period (as grid pts)
        self.tT_s = tT_s              # the expected average sampling period
        return


    def _checkConf(self):
        """
        This function checks configuration of sampling

        Args:
            none
    
        Returns:
            none
        """

        # -----------------------------------------------------------------
        # Check if the number of grid points in patterns is higher than 0
        if not self.nK_g > 0:
            strError = ('Real number of grid points in patterns must be higher ')
            strError = strError + ('than zero')
            raise ValueError(strError)
    
        # -----------------------------------------------------------------
        # Check if the real time of patterns is higher than 0
        if not self.tTau_real > 0:
            strError = ('Real time of patterns must be higher than zero')
            raise ValueError(strError)
        
        # -----------------------------------------------------------------
        # Check if the expected number of sampling points is higher than 0
        if not self.nK_s > 0:
            strError = ('The expected number of sampling points in patterns ')
            strError = strError + ('must be higher than zero')
            raise ValueError(strError)
    
        # -----------------------------------------------------------------
        # Check if the time of patterns is equal to the time of signals to be
        # sampled
        if (self.tTau_real - self.tS) > self.tS/1e12:
            strError = ('The real time of patterns is different than the time ')
            strError = strError + ('of signals to be sampled')
            raise ValueError(strError)
    
        # -----------------------------------------------------------------
        # Check if the expected number of sampling points is lower or equal
        # to the number of grid points
        if not self.nK_g >= self.nK_s:
            strError = ('The real number of grid points in patterns must be ')
            strError = strError + ('higher or equal to the number of expected ')
            strError = strError + ('sampling points')
            raise ValueError(strError)
    
        # -----------------------------------------------------------------
        # Check if the signal representation sampling frequency is compatible
        # with the sampling period
        if np.round(self.Tg * self.fR) != (self.Tg * self.fR):
            strError = ('The chosen sampling grid period is incompatible with ')
            strError = strError + ('the signals representation sampling ')
            strError = strError + ('frequency')
            raise ValueError(strError)
    
        # -----------------------------------------------------------------
        return


    # Generate the sampling patterns
    def _generatePatterns(self):
        """
        This function generates the required number of sampling patterns.
    
        Args:
                none
                
        Returns:
                none

                List of variables added by function to the object:

                nSigs (number):       the number of input signals 
                mPatts (matrix):      the sampling patterns (grid indices)
                mPattsRep (matrix):   the sampling patterns (signal rep. sampling points)
                mPattsT (matrix):     the sampling patterns (time moments)
        """

        # Make the matrix with signals 2 dim, if it is 1 dim
        if self.mSig.ndim == 1:
            self.mSig = self.mSig.copy()            
            self.mSig.shape = (1, self.mSig.size)
        (nSigs, _) = self.mSig.shape          # The number of input signals

        # Allocate the matrix for all the sampling patterns
        mPatts = np.ones((nSigs, self.nK_s), dtype='int64')

        iSMaxPatt = 0   # Reset the max size of a pattern
        # Generate all the needed sampling patterns
        for inxP in np.arange(nSigs):
    
            # Generate a vector with a sampling pattern
            vPattern = self._js_engine(self.nK_s, self.nT, self.nK_g, self.iSigma)
            
            # Adjust the sampling pattern or a matrix with patterns
            (iS_v,) = vPattern.shape             # Get the size of the generated pattern
            iSMaxPatt = max((iS_v, iSMaxPatt))   # Update the max size of a pattern
            (iR_m, iC_m) = mPatts.shape          # Get the number of rows and columns in the matrix with patterns
            
            # Check the inequalities between matrix with vectors and the current vector with a pattern
            if iS_v < iC_m:     # <- the size of a generated pattern is lower than the
                                #    number of columns in the storage matrix
    
                iEmpty = iC_m - iS_v  # Calculate the size of empty space in the pattern
    
                vPatch = np.nan*np.ones(iEmpty)   # Update the pattern (fill up the empty spaces with a patch of -1)
                vPattern = np.hstack((vPattern, vPatch))   #
    
            elif iS_v > iC_m:   # <- the size of a generated pattern is higher than the number of columns in the storage matrix
    
                iEmpty = iS_v - iC_m   # The size of empty space in the storage matrix
                mPatch = np.nan*np.ones(iR_m, iEmpty)   # Update the storage matrix
                mPatts = np.hstack((mPatts, mPatch))
            # --------------------------------------------------------------
            
            mPatts[inxP, :] = vPattern   # Store the generated pattern

        vInx = range(0, iSMaxPatt)    # Clip the matrix with patterns
        mPatts = mPatts[:, vInx]      # ^

        # The patterns engine generates patterns in range  <1 ; N>, where
        # N is the number of possible positions of a sampling points.
        # Because Numpy indexes arrays from 0, the patterns should be represented 
        # in range from <0 ; N-1>
        mPatts = mPatts - 1

        # --------------------------------------------------------------

        # Compute the number of signal representation points which equals
        # one grid point
        iGridvsRep = int(np.round((self.Tg * self.fR)))

        # Recalculate the patterns to the signal representation sampling points
        mPattsRep = iGridvsRep * mPatts

        # --------------------------------------------------------------
        # Recalculate the patterns to the time moments
        vTSig = (1 / self.fR) * np.arange(int(np.round(self.tTau_real * self.fR)))   # The time vector of the input signal
        mPattsRep_ = mPattsRep.copy()                    
        (iTPoints, ) = vTSig.shape                        # Get the number of points in the time vector
        mPattsRep_[np.isnan(mPattsRep)] = iTPoints - 1    # Change nan into pointer to nan          
        mPattsT = vTSig[mPattsRep]

        self.nSigs = nSigs
        self.mPatts = mPatts
        self.mPattsRep = mPattsRep
        self.mPattsT = mPattsT
        return

    # Sample the signals
    def _sampleSignals(self):
        """
        This function samples signals using the previously generated
        sampling patterns.
    
        Args:
                none
        Returns:
                none

                List of variables added by function to the object:                
                mObSig (matrix):  the observed signals
        """
        mSig_ = np.hstack((self.mSig, np.nan*np.zeros((self.nSigs,1))))   # Add nan to the end of signals

        # Generate matrix with patterns where NaN is changed to index of NaN in mSig_
        mPattsRep_ = self.mPattsRep.copy()
        (_, nSamps) = self.mSig.shape                      # Get the number of samples in the signals
        mPattsRep_[np.isnan(self.mPattsRep)] = nSamps      # Change nan into pointer to nan
    
        self.mObSig = (mSig_[np.arange(self.nSigs), mPattsRep_.T.astype(int)]).T  # Generate correct observation signals
        return

    # Generate the observation matrices
    def _generObser(self):
        """
        This function generates the observation matrices.
    
        Args:
                none
            
        Returns:
                none
                
                List of variables added by function to the object:                
                lPhi (list): list with observation matrices
        """

        nSmp = int(round(self.tS * self.fR))  # The number of representation samples in the input signals

        lPhi = []    # Start the list with the observation matrices
    
        # Generate the observation matrices
        for inxPat in np.arange(self.nSigs):  # <- loop over all observation matrices
    
            # Get the current pattern
            vPatts = self.mPattsRep[inxPat, :]
            vPatts = vPatts[np.invert(np.isnan(vPatts))]   # Clean the pattern
            nPatSiz  = vPatts.size          # Size of the pattern
    
            # Generate the observation matrix for the current sampling pattern
            mPhi = np.zeros((nPatSiz, nSmp))  # Allocat the observation matrix
            inxRow = 0                        # Reset index of a row
            for inxCol in vPatts:   # <- loop over all sampling points in a pattern
                mPhi[inxRow, int(inxCol)] = 1
                inxRow = inxRow + 1
            lPhi.append(mPhi.copy())   # Add the matrix to the list
    
        # -----------------------------------------------------------------
        self.lPhi = lPhi
        return


    # =================================================================
    # JS engine
    # =================================================================
    def _js_engine(self, nK_s, nT, K_g, sigma):
    
        # -----------------------------------------------------------------
        # Allocate the vector for the sampling points
        vPattern = np.nan*np.zeros(2*nK_s)
    
        hatk = 0     # Reset the index of stored sampling time point
        n_hatk = 0   # Reset the current index of the grid
    
        # -----------------------------------------------------------------
        # Draw all time points
        for inxSmp in range(1, nK_s+1):
    
            # Draw the current time point
            x_k = np.random.randn()
            nstar_hatk = round(inxSmp*nT + np.sqrt(sigma) * x_k * nT)
    
            # Store the time point in the vector,
            # if it is somewhere in the sampling time due
            # and was not drawn yet
            if nstar_hatk > 0 and nstar_hatk <= K_g:
    
                # Store the time point
                n_hatk = nstar_hatk
                vPattern[hatk-1] = n_hatk
                hatk = hatk + 1
    
            # Check if the whole vector vPattern was
            # already filled up. If so, make it longer
            nSiz = vPattern.size
            if hatk == nSiz:
                vExtraSpace = np.nan*np.zeros(nK_s)
                vPattern = np.hstack((vPattern, vExtraSpace))
    
        # -----------------------------------------------------------------
        # Clear the pattern
        vPattern = vPattern[np.equal(np.isnan(vPattern), False)]
    
        # -----------------------------------------------------------------
        # Remove repeated moments
        vPattern = np.unique(vPattern)
    
        # -----------------------------------------------------------------
        return vPattern
