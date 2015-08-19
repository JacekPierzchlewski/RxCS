"""
This is a model of a low-noise nonlinear amplifier (LNA). |br|

The output signal of the amplifier is:
   y(t)  =  a_1 * x(t) + a_2 * x(t)^2 + ... + a_n * x(t)^n

   where: 
     x(t) is the input signal,
     a_1, a_2, ..., a_n are the amplifier coefficients.


*Examples*:
    Please go to the *examples/signals* directory for examples on how to use 
    the LNA. |br|

*Settings*:
    Parameters of the LNA described below.

    Take a look on '__parametersDefine' function for more info on the 
    parameters.

    Parameters of the LNA are attributes of the class which must/can
    be set before the LNA run.

    Required parameters:

    - a. **mSig** (*Numpy array 2D*): Input signals
                                       
    - b. **vCoef** (*Numpy array 1D*):  Amplifier coefficients, 
                                        a_k = vCoef[k]

    Optional parameters:

     - c. **bMute** (*int*):  mute the console output from the LNA [default = 0]


*Output*:
    Description of the LNA output is below. 
    This is the list of attributes of the LNA class which are available 
    after calling the 'run' method:

    - a. **mSig** (*Numpy array 2D*): Matrix with output signals
 

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0    | 15-JUL-2014 : * Version 1.0 released. |br|
    1.0r1  | 18-AUG-2015 : * Adjusted to RxCSobject v1.0 |br|


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
    def run(self):
        
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

