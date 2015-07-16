"""
This is a model of a low-noise nonlinear amplifier (LNA). |br|

For description of parameters of the amplifier, take a look on '__parametersDefine' function.
For examples of usage, go to examples/signals directory. |br|

Atributes of 'LNA' class after calling 'run' method:

    - mSig [Numpy array (2D)] - matrix with generated signals, one signal p. column

|br|

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0  | 15-JUL-2014 : * Version 1.0 released. |br|

*License*:
    BSD 2-Clause
"""

from __future__ import division
import numpy as np
import rxcs


class LNA(rxcs._RxCSobject):

    def __init__(self, *args):
        rxcs._RxCSobject.__init__(self)    # Make it a RxCS object 
        
        self.strRxCSgroup = 'Signal generator'          # Name of group of RxCS modules
        self.strModuleName = 'Nonlinear low-noise amp'  # Module name        

        self.__inputDefine()           # Define the input signals
        self.__parametersDefine()      # Define the parameters

        # If there are arguments given when the object was created, then run the engine  
        if len(args) > 0:
            self.run(*args)


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

        # Amplifier coefficients
        self.paramAddMan('vCoef', 'Amplifier coefficients')
        self.paramType('vCoef', (np.ndarray))    # Must be of a numpy array...
        self.paramTypeEl('vCoef', (int, float))               # ...with float/int elements
        self.paramSizH('vCoef', 0)                            # Size must be higher than 0
        self.paramNDimEq('vCoef', 1)                          # vCoef must be 1-dimensional

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
        
        # Store the input signal        
        mSigIn = self.mSig.copy()        
        
        # Apply the first coefficient 
        self.mSig = self.vCoef[0] * mSigIn
        
        # Apply all the rest of coefficients
        iExp = 2    # The current exponent
        for iCoef in self.vCoef[1:len(self.vCoef)]:    
            self.mSig = self.mSig + iCoef*mSigIn**iExp
            iExp = iExp + 1

