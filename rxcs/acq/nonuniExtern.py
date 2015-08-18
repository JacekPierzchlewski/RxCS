"""
This a nonuniform sampler with externally acquired sampling scheme. |br|

The module samples the given signals nonuniformly. |br|
The sampling patterns are taken from a file with sampling patterns
or from a dictionary given to the sampler. In particular the sampling
pattern may be uniform.

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    0.1  | 1-SEP-2014 : * Initial version. |br|
    1.0  | 12-SEP-2014 : * Version 1.0 is ready. |br|
    2.0  | 18-AUG-2015 : * Version 2.0 is ready. |br|

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

        # 1d/2d array with input signals, one signal p. row
        self.paramAddMan('mSig', 'Input signals', noprint=1)
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

        # Matrix with sampling patterns
        self.paramAddMan('mPatterns', 'Sampling patterns', noprint=1)
        self.paramType('mPatterns', np.ndarray)
        self.paramTypeEl('mPatterns', (int))
        self.paramNDimEq('mPatterns', 2)
        self.paramDimSizH('mPatterns',0, 'rows')  # There must be at least one sampling pattern

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
        self.paramDimSiqEq('vPattInx', 'mSig', 0, 'rows')   # The number of indices must equal the number of signals in mSig
        self.pamramH('vPattInx', 0)  # All the indices must be higher than 0

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
        self._checkConf()       # Check configuration of sampling
        self._sample()          # Sample the signals
        

    def _checkConf(self):
        """
        This function checks configuration of sampling

        Args:
            none
    
        Returns:
            none
        """

        # -----------------------------------------------------------------
        # Check if the signal representation sampling frequency is compatible
        # with the sampling period
        if np.abs(np.round(self.Tg * self.fR) - (self.Tg * self.fR)) > (1e-9*(self.Tg * self.fR)):
            strError = ('The sampling grid period of pattern is incompatible with')
            strError = strError + (' the signals representation sampling ')
            strError = strError + ('frequency')
            raise ValueError(strError)

        # -----------------------------------------------------------------
        # Check if the sampling patterns are not sampling outside the time
        # of signals
        tMax = np.max(self.mPatterns) * self.Tg 
        if tMax > self.tS:
            strError = 
            raise ValueError(strError)
    
        # -----------------------------------------------------------------
        # Check if the indices od samplin patterns which should be used are 
        # not higher than the number of sampling patterns
        #nPatts = 




    
    
    
    