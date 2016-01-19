"""
This is a signal oversampler. |br|

*Examples*:
    Please go to the *examples/signals* directory for examples on how to use 
    the LNA. |br|

*Settings*:
    Parameters of the module are described below.

    Take a look on '__parametersDefine' function for more info on the 
    parameters.

    Parameters of the oversampler are attributes of the class which must/can
    be set before the LNA run.

    Required parameters:

    - a. **mSig** (*Numpy array 2D*): Input signals

    - b. **iFLow** (*float*):  Representation sampling frequency of the original input signal

    - c. **iFHigh** (*float*):  Representation sampling frequency of the oversampled signal


    Optional parameters:

     - d. **bMute** (*int*):  mute the console output from the LNA [default = 0]


*Output*:
    Description of the oversampler output is below. 
    This is the list of attributes of the oversampler class which are available 
    after calling the 'run' method:

    - a. **mSigOversamp** (*Numpy array 2D*): Matrix with output signals
 
    - b. **vTOversamp** (*Numpy array 1D*): Time vector for the output signal


*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0    | 19-JAN-2016 : * Version 1.0 released. |br|


*License*:
    BSD 2-Clause
"""

from __future__ import division
import numpy as np
import rxcs


class oversampler(rxcs._RxCSobject):

    def __init__(self, *args):
        rxcs._RxCSobject.__init__(self)    # Make it a RxCS object 
        
        self.strRxCSgroup = 'Signal generator'      # Name of group of RxCS modules
        self.strModuleName = 'Oversampler'          # Module name        

        self.__inputDefine()           # Define the input signals
        self.__parametersDefine()      # Define the parameters

    # Define input signals
    def __inputDefine(self):

        # Input signal
        self.paramAddMan('mSig', 'Input signal')
        self.paramType('mSig', (np.ndarray))             # Must be a numpy array...
        self.paramTypeEl('mSig', (float, int))           # ...with float/int elements
        self.paramSizH('mSig', 0)                        # Size must be higher than 0
        self.paramNDimHE('mSig', 1)                      # The allowed number of dimensions is {1, 2}
        self.paramNDimLE('mSig', 2)                      # ^


    # Define parameters
    def __parametersDefine(self):

        # Original low sampliing signal frequency
        self.paramAddMan('iFLow', 'Original low frequency')
        self.paramType('iFLow', (int, float))     
        self.paramH('iFLow', 0)

        # High sampling frequency of the oversampled signal
        self.paramAddMan('iFHigh', 'High sampling frequency of the oversampled signal')
        self.paramType('iFHigh', (int, float))     
        self.paramH('iFHigh', 0)
        self.paramH('iFHigh', 'iFLow')

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
        
        # Generate the time vectors
        (self.vTLow, self.vTHigh, self.iNSampH) = self._generateTimeVectors(self.mSig, self.iFLow, self.iFHigh)
        
        if self.mSig.ndim == 1:
            self.mSigOversamp = np.zeros((1, self.iNSampH))    # Allocate matrix for the oversampled signals            
            self.mSigOversamp[0, :] = np.interp(self.vTHigh, self.vTLow, self.mSig)
        else:
            (nSignals, _) = self.mSig.shape                       # Get the number of signals
            self.mSigOversamp = np.zeros((nSignals, self.iNSampH))    # Allocate matrix for the oversampled signals

            # Loop over all signals
            for inxSignal in np.arange(nSignals):
                self.mSigOversamp[inxSignal, :] = np.interp(self.vTHigh, self.vTLow, self.mSig[inxSignal, :])

        self.vTOversamp = self.vTHigh


    def _generateTimeVectors(self, mSig, iFLow, iFHigh):
        """
        Generate the time vectors for the original and oversampled signal
        """

        if mSig.ndim == 1: 
            iNSampL = mSig.size                  # The number of samples in the original signal
        else:
            (_, iNSampL) = mSig.shape
        
        iTSig = iNSampL/iFLow;                   # Time of the signal
        iNSampH = int(np.round(iTSig * iFHigh))  # The number of samples in the oversampled signal

        vTLow = np.arange(1, iNSampL+1)/iFLow     # Time vector for the low frequency        
        vTHigh = np.arange(1, iNSampH+1)/iFHigh   # Time vector for the high frequency        
        
        return (vTLow, vTHigh, iNSampH)

