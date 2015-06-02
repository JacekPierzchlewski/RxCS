from __future__ import division
import numpy as np
import scipy.signal as scsig
import rxcs


class LNA(rxcs._RxCSobject):

    def __init__(self, *args):
        rxcs._RxCSobject.__init__(self)    # Make it a RxCS object 
        
        self.strRxCSgroup = 'Signal generator'          # Name of group of RxCS modules
        self.strModuleName = 'Nonlinear low-noise amp'  # Module name        

        self.__inputDefine()          # Define the input signals
        self.__parametersDefine()      # Define the parameters

        # If there are arguments given when the object was created, then run the engine  
        if len(args) > 0:
            self.run(*args)

    # Define input signals
    def __inputDefine(self):

        # Input signal
        self.paramAddMan('vCoef', 'Input signal')
        self.paramType('vCoef','numpy array float')    # Must be of a numpy array with float number
        self.paramL('fs', np.inf)                      # Must be lower than +infinity...
        self.paramH('fs', -np.inf)                     # ...and higher than -infinity

 
    # Define parameters
    def __parametersDefine(self):

        # Amplifier coefficients
        self.paramAddMan('vCoef', 'Amplifier coefficients', noprint=0)
        self.paramType('vCoef','numpy array float')    # Must be of a numpy array with float number
        self.paramL('fs', np.inf)                      # Must be lower than +infinity...
        self.paramH('fs', -np.inf)                     # ...and higher than -infinity

        # --------------------------------------------------------------------

        # Mute the output flag
        self.paramAddOpt('bMute', 'Mute the output', noprint=1)  
        self.paramType('bMute','int')          # Must be of int type
        self.paramAllowed('bMute',[0, 1])      # It can be either 1 or 0


    # Run
    def run(self, *args):
        
        self.parametersProcess(*args)  # Get parameters given directly to 'run' function
        self.parametersCheck()         # Check if all the needed partameters are in place and are correct
        self.parametersPrint()         # Print the values of

        self.__engine()                #
        return self.__dict__           #


    # Engine of the function
    def __engine(self):
        
        self.engineStartsInfo()  # Info that the engine starts


        self.engineStopsInfo()   # Info that the engine ends
