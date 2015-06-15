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
        self.paramAddMan('vSigIn', 'Input signal')
        self.paramType('vSigIn', (np.ndarray))             # Must be a numpy array, a tuple or a list...
        self.paramTypeEl('vSigIn', (float, int))           # ...with float/int elements


    # Define parameters
    def __parametersDefine(self):

        # Amplifier coefficients
        self.paramAddMan('vCoef', 'Amplifier coefficients')
        self.paramType('vCoef', (np.ndarray, list, tuple))    # Must be of a numpy array...
        self.paramTypeEl('vCoef', (int, float))               # ...with float/int elements
        self.paramSizH('vCoef', 0)                            # Size must be higher than 2

        # Mute the output flag
        self.paramAddOpt('bMute', 'Mute the output', noprint=1, default=0)  
        self.paramType('bMute', int)           # Must be of int type
        self.paramAllowed('bMute',[0, 1])      # It can be either 1 or 0


    # Run
    def run(self, *args):
        
        self.parametersProcess(*args)  # Get parameters given directly to 'run' function
        self.parametersCheck()         # Check if all the needed partameters are in place and are correct
        self.parametersPrint()         # Print the values of parameters

        self.__engine()                # Run the engine
        return self.__dict__           #


    # Engine of the function
    def __engine(self):
        
        self.engineStartsInfo()  # Info that the engine starts
        self.engineStopsInfo()   # Info that the engine ends
