"""
This a nonuniform sampler with ANGIE sampling scheme. |br|

The modules samples the given signals nonuniformly. |br|
The sampling aptterns are generated using ANGIE scheme.

The used ANGIE patterns generator is described further in
"Generation and Analysis of Constrained Random Sampling Patterns",
available in arXiv: http://arxiv.org/abs/1409.1002

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    0.1  | 26-MAY-2014 : * Initial version. |br|
    0.2  | 27-MAY-2014 : * Docstrings added. |br|
    1.0  | 27-MAY-2014 : * Version 1.0 is ready. |br|
    1.1  | 11-JUN-2014 : * Observation matrices added to the output. |br|
    1.1r1| 18-SEP-2014 : * Bug in checking time of patterns is fixed. |br|
    1.1r2| 28-JAN-2015 : * Patterns generator adjusted to Numpy indexing. |br|
    2.0  | 11-AUG-2015 : * Objectified version (2.0) |br|

*License*:
    BSD 2-Clause
"""

from __future__ import division
import numpy as np
import math
import rxcs


class randMult(rxcs._RxCSobject):

    def __init__(self, *args):
        rxcs._RxCSobject.__init__(self)    # Make it a RxCS object 
        
        self.strRxCSgroup = 'Signal generator'     # Name of group of RxCS modules
        self.strModuleName = 'Random multitone'    # Module name        

        self.__inputSignals()          # Define input signals
        self.__parametersDefine()      # Define the parameters

        # If there are arguments given when the object was created, then run the engine  
        if len(args) > 0:
            self.run(*args)

    # Input signals
    def __inputSignals(self):

        # 2d array with input signals, one signal p. column
        self.paramAddMan('mSig', 'Input signals')

        # Input signals representation sampling frequency
        self.paramAddMan('fR', 'Input signals representation sampling frequency', unit='Hz')

        # Time of input signals
        self.paramAddMan('tS', 'Time of input signals', unit='s')


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

        # Minimum time between sampling points
        self.paramAddOpt('tMin', 'Minimum time between sampling points', default=0, unit='s')
        self.paramType('tMin', (int, float))     # Must be of int or float type
        self.paramHE('tMin', 0)                  # Minimum time must be higher or equal to zero
        self.paramL('tMin', np.inf)              # ...and lower than infinity

        # Maximum time between sampling points
        self.paramAddOpt('tMax', 'Maximum time between sampling points', default=np.inf, unit='s')
        self.paramType('tMax', (int, float))     # Must be of int or float type
        self.paramH('tMax', 0)                   # Maximum time must be higher than zero

        # 'Mute the output' flag
        self.paramAddOpt('bMute', 'Mute the output', noprint=1, default=0)
        self.paramType('bMute', int)           # Must be of int type
        self.paramAllowed('bMute',[0, 1])      # It can be either 1 or 0


    # Run
    def run(self, *args):

        self.parametersProcess(*args)  # Get parameters given directly to 'run' function
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
            nK_min (float):    min t between the samp pts as the number of grid pts
            nK_max (float):    max t between the samp pts as the number of grid pts
            tMin_real (float): the real minimum time between sampling points
            tMax_real (float): the real maximum time between sampling points
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

        # Minimum time between the sampling points as the number of grid:
        if np.isnan(self.tMin):
            nK_min = 1
        else:
            nK_min = int(math.ceil(self.tMin / self.Tg))
        tMin_real = nK_min * self.Tg   # The real minimum time between sampling points
    
        # Maximum time between the sampling points as the number of grid:
        if np.isnan(self.tMax):
            nK_max = np.inf
        else:
            nK_max = int(math.floor(self.tMax / self.Tg))
        tMax_real = nK_max * self.Tg   # The real maximum time between sampling points

        self.nK_g = nK_g              # the number of grid points in the sampling pattern
        self.tTau_real = tTau_real    # the real time of sampling patterns
        self.nK_s = nK_s              # the expected number of sampling points in a pattern
        self.f_s = f_s                # the expected average sampling frequency  
        self.nT = nT                  # the expected average sampling period (as grid pts)
        self.tT_s = tT_s              # the expected average sampling period
        self.nK_min = nK_min          # min t between the samp pts as the number of grid pts
        self.nK_max = nK_max          # max t between the samp pts as the number of grid pts
        self.tMin_real = tMin_real    # the real minimum time between sampling points
        self.tMax_real = tMax_real    # the real maximum time between sampling points
        return


    def _checkConf(self):

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
        # Check if the minimum time between the sampling points is lower or
        # equal to the average sampling period
        if not self.nT >= self.nK_min:
            strError = ('The minimum time between the sampling points must be ')
            strError = strError + ('lower or equal to the expected average ')
            strError = strError + ('sampling period ')
            raise ValueError(strError)
    
        # -----------------------------------------------------------------
        # Check if the maximum time between the sampling points is higher or
        # equal to the average sampling period
        if not self.nK_max >= self.nT:
            strError = ('The maximum time between the sampling points must be ')
            strError = strError + ('higher or equal to the expected average ')
            strError = strError + ('sampling period ')
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
        
        # --------------------------------------------------------------
        # Allocate the matrix for all the sampling patterns
        mPatts = np.ones((self.nPatts, self.nK_s), dtype='int64')

        # Generate all the needed sampling patterns
        for inxP in np.arange(self.nPatts):
    
            # Generate a vector with a sampling pattern
            vPattern = self._angie_engine(self.nK_s, self.nK_g, self.nK_min, self.nK_max, self.iSigma)
            mPatts[inxP, :] = vPattern   # Store the generated pattern

        # The patterns engine generates patterns in range  <1 ; N>, where
        # N is the number of possible positions of a sampling points.
        # Because Numpy indexes arrays from 0, the patterns should be represented 
        # in range from <0 ; N-1>
        mPatts = mPatts - 1
           
        # Compute the number of signal representation points which equals
        # one grid point
        iGridvsRep = int(np.round((Tg * fR)))
        
        # Recalculate the patterns to the signal representation frequency
        mPattsRep = iGridvsRep * mPatts  
    
        # --------------------------------------------------------------
        # Recalculate the patterns to the time moments
    
        # Get the time vector of the original signal (if it is given)
        if 'vTSig' in dSig:
            vTSig = dSig['vTSig']
        else:
            vTSig = (1 / fR) * np.arange(int(np.round(tTau_real*fR)))
            
        mPattsT = vTSig[mPattsRep]

        return
    
    # Sample the signals
    def _sampleSignals(self):    
        pass

    
    # Generate the observation matrices
    def _generObser(self):       
        pass


    def _angie_engine(self, nK_s, K_g, K_min, K_max, sigma):
        """
        This function is the engine of ANGIE sampling generator.
        It generates one sampling pattern.
    
        Args:
            nK_s (float):  the number of sampling points in a pattern
            K_g (float):   the number of grid points in a pattern
            K_min (float): minimum distance between sampling points
            K_max (float): maximum distance between sampling points
            sigma (float): the sigma parameter
    
        Returns:
            vPattern (vector): vector with the sampling pattern
        """
    
        # Allocate the vector for the sampling points
        vPattern = np.nan*np.zeros(nK_s)
    
        # Reset the current sampling moment
        nk = 0
    
        # -----------------------------------------------------------------
        # Reset the minimum and maximum limits:
    
        # Reset the minimum the minimum limit
        nminus_k = 1
    
        # Reset the maximum limit
        nplus_k = K_g - K_min*(nK_s-1)
    
        # -----------------------------------------------------------------
        # Draw all the points
        for k in range(nK_s):    # <- Loop over all the expected points
    
            # -------------------------------------------------------------
            # The number of sampling points left
            nLeft = nK_s - k
    
            # -------------------------------------------------------------
            # Calculate the expected position of the sample:
    
            # Calculate the average sampling period for the rest of sampling
            # points (in the grid indices)
            nddag_k = round((K_g - nk) / (nLeft + 1))
    
            # Calculate the expected position (in the grid indices)
            Enk = nk + nddag_k
    
            # -------------------------------------------------------------
            # Distances between the expected position and the limits
    
            # Calculate distance to the minimum limit
            ndminus_k = abs(Enk - nminus_k)
    
            # Calculate distance to the maximum limit
            ndplus_k = nplus_k - Enk
    
            # Get the correct distance
            nd_k = min(ndminus_k, ndplus_k)
    
            # -------------------------------------------------------------
            # Draw the sampling point:
    
            # -------------------------------------------------------------
            # Soft start, if enabled
            # -------------------------------------------------------------
            # First sampling point is different, if soft start is enabled
            if k == 0:
    
                # Draw the sampling moment (uniformly)
                nk = math.ceil(np.random.rand()*nddag_k)
            # -------------------------------------------------------------
            # -------------------------------------------------------------
    
            else:
                # Draw Gaussian
                xk = np.random.randn()
    
                # Draw the sampling point
                nk = Enk + math.sqrt(sigma)*xk*nd_k
                nk = round(nk)
    
            # -------------------------------------------------------------
            # Check limits
            if nk < nminus_k:
                nk = nminus_k
    
            elif nk > nplus_k:
                nk = nplus_k
    
            # -------------------------------------------------------------
            # Store the drawn sampling point
            vPattern[k] = nk
    
            # -------------------------------------------------------------
            # Calculate the minimum and maximum limits:
    
            # Move the minimum limit forward (by the minimum distance)
            nminus_k = nk + K_min
    
            # Move the maximum limit forward
            nplus_k = K_g - K_min*(nLeft-2)
    
            nplus_k = min(nplus_k, nk + K_max)  # <- Add maximum limit (this line
                                                #    can be removed if there is no
                                                #    need for maximum limit)
                                                #
        # -----------------------------------------------------------------
        return vPattern


