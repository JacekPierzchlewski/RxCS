"""
This is a power regulator module. |br|

*Examples*:
    Please go to the *examples/signals* directory for examples on how to use 
    the regulator. |br|

*Settings*:
    Parameters of the regulator are described below.

    Take a look on '__parametersDefine' function for more info on the 
    parameters.

    Parameters of the regulator are attributes of the class which must/can
    be set before the regulator run.

    Required parameters:

    - a. **mSig** (*Numpy array 2D*): Input signals

    Optional parameters:

     - b. **iP** (*float*): signals' power  [default = not regulated]

     - c. **bMute** (*int*):  mute the console output from the LNA [default = 0]


*Output*:
    Description of the regulator output is below. 
    This is the list of attributes of the generator class which are available 
    after calling the 'run' method:

    - a. **mSigOut** (*Numpy array 2D*): Matrix with regulated signals, 

    - b. **vP** (*Numpy array 1D*): Vector with the power of signals


*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0    | 20-JAN-2016 : * Version 1.0 released. |br|

*License*:
    BSD 2-Clause
"""


from __future__ import division
import numpy as np
import rxcs


class powerRegulator(rxcs._RxCSobject):

    def __init__(self, *args):
        rxcs._RxCSobject.__init__(self)    # Make it a RxCS object

        self.strRxCSgroup = 'Signal generator'  # Name of group of RxCS modules
        self.strModuleName = 'Power regulator'  # Module name

        self.__inputDefine()           # Define the input signals
        self.__parametersDefine()      # Define the parameters

    # Define input signals
    def __inputDefine(self):

        # Input signal
        self.paramAddMan('mSig', 'Input signals')
        self.paramType('mSig', (np.ndarray))             # Must be a numpy array...
        self.paramTypeEl('mSig', (float, int))           # ...with float/int elements
        self.paramSizH('mSig', 0)                        # Size must be higher than 0
        self.paramNDimHE('mSig', 1)                      # The allowed number of dimensions is {1, 2}
        self.paramNDimLE('mSig', 2)                      # ^


    def __parametersDefine(self):
        """
            Internal method which defines the parameters    
        """

        # Power of a signal
        self.paramAddOpt('iP', 'Signal power', unit='W')
        self.paramType('iP',(float, int))
        self.paramH('iP', 0)            # Power of the signal must be higher than zero
        self.paramL('iP', np.inf)       # ...and lower than infinity

        # --------------------------------------------------------------------

        # Mute the output flag
        self.paramAddOpt('bMute', 'Mute the output', noprint=1, default=0)
        self.paramType('bMute', int)          # Must be of int type
        self.paramAllowed('bMute',[0, 1])      # It can be either 1 or 0


    def run(self):
        """
            Run method, which starts the regulator    
        """
        self.parametersCheck()         # Check if all the needed partameters are in place and are correct
        self.parametersPrint()         # Print the values of parameters

        self.engineStartsInfo()   # Info that the engine starts
        self.__engine()           # Run the engine
        self.engineStopsInfo()    # Info that the engine ends

        return self.__dict__           # Return dictionary with the parameters


    def __engine(self):
        """
            Engine of the function    
        """
        self.mSigOut = self.mSig.copy()
        self.mSigOut = self.makeArray2Dim(self.mSigOut)

        if self.wasParamGiven('iP'):
            (self.mSigOut, self.vP) = self._adjPower(self.mSig, self.iP)
        return


    def _adjPower(self, mSig, iP):
        """
        This function adjustes powers of the generated signals.
        If the requested power of the signals is equal to NaN or inf, then
        the signals are not adjusted.
    
        Args:
            mSig (matrix):   matrix with signals (one row - one signal)
            iP (float):      requested power of the signals
    
        Returns:
            mSig (matrix):   matrix with noisy signals
            vP (vector):     vector with powers of noisy signals
        """
    
        # Get the number of signals and the size of signals (the number of samples)
        (nSigs, nSmp) = mSig.shape
    
        # Measure the power of the signals
        vP = (np.sum(mSig * mSig, axis=1) / nSmp).reshape(nSigs, 1)
    
        # Adjust the signal power, if needed
        if not np.isnan(iP) or np.isinf(iP):
    
            # Compute power adjustments coefficients for the noise signals
            vPCoef = np.sqrt(iP / vP)

            # Adjust the signal power
            mPCoef = np.tile(vPCoef, (1, nSmp))
            mSig = mSig * mPCoef
        
            # Measure the power of the adjusted signals
            vP = np.sum(mSig*mSig, axis=1) / nSmp
    
        return (mSig, vP)
