from __future__ import division
import numpy as np
import scipy.signal as scsig
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
        dD1 = {}


        # vector Reference to a signal
        self.paramAddMan('vSigInRef', 'Vector reference to the input signal')
        self.paramType('vSigInRef',(float, int, np.ndarray, tuple, list, dict))        # Must be of a numpy array with float number
        #self.paramTypeEl('vSigInRef', (float, int, str))            # ...with float/int elements

        # Input signal
        self.paramAddMan('vSigIn', 'Input signal')
        self.paramType('vSigIn', (np.ndarray, tuple, list) )                # Must be of a numpy array with float number
        self.paramTypeEl('vSigIn', (float, int, str))            # ...with float/int elements
        #self.NaNAllowedEl('vSigIn')

        # Integer reference
        self.paramAddOpt('iSigInRef', 'Reference to the input signal')
        self.paramType('iSigInRef',(float, int))        # Must be of a numpy array with float number

        self.paramL('vSigIn', 'iSigInRef')

        #self.paramAllowed('iSigInRef', [np.nan)
        
        #self.paramLE('vSigIn', 'vSigInRef')      # Must be lower than +infinity...
        
        #self.paramLE('vSigIn', 'iSigInRef', mul=4)      # Must be lower than +infinity...
        #self.paramLE('vSigIn', 'vSigInRef', mul=4, add=1)      # Must be lower than +infinity...
        #self.paramH('vSigIn', -5)                      # ...and higher than -infinity

        #self.paramSiz('vSigIn', ( ))


    # Define parameters
    def __parametersDefine(self):

        # Amplifier coefficients
        #self.paramAddMan('vCoef', 'Amplifier coefficients', noprint=0)
        #self.paramType('vCoef', (np.ndarray, list))    # Must be of a numpy array...
        #self.paramTypeEl('vCoef',(int, float))         # ...with float/int elements
        #self.paramSizEq('vCoef',10)                    # Size must be equal to 10
        #self.paramSizL('vCoef',20)                     # Size must be lower than 20
        #self.paramSizH('vCoef',2)                      # Size must be higher than 2
        
        #self.paramL('vCoef', np.inf)                   # Elements must be lower than +infinity...
        #self.paramH('vCoef', -np.inf)                  # ...and higher than -infinity

        # --------------------------------------------------------------------

        # Mute the output flag
        self.paramAddOpt('bMute', 'Mute the output', noprint=1)  
        self.paramType('bMute', int)           # Must be of int type
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
