"""
This is a model of a single branch upconverter. |br|

*Examples*:
    Please go to the *examples/signals* directory for examples on how to use 
    the upconverter. |br|

*Settings*:
    Parameters of the upconverter are described below.

    Take a look on '__parametersDefine' function for more info on the 
    parameters.

    Parameters of the upconverter are attributes of the class which must/can
    be set before the upconverter run.

    Required parameters:

    - a. **mSig** (*Numpy array 2D*): Input signals

    - b. **fR** (*float*): signals' representation sampling frequency

    - c. **tS** (*float*): time of a signals

    - d. **fC** (*float*): carrier frequency


    Optional parameters:

     - e. **bMute** (*int*):  mute the console output from the LNA [default = 0]


*Output*:
    Description of the upconverter output is below. 
    This is the list of attributes of the upconverter class which are available 
    after calling the 'run' method:

    - a. **mSig** (*Numpy array 2D*): Matrix with output upconverter signals

    - b. **vCarrier** (*Numpy array 1D*): Carrier signal
 

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0    | 04-SEP-2015 : * Version 1.0 released. |br|

*License*:
    BSD 2-Clause
"""


from __future__ import division
import numpy as np
import rxcs


class upconvert(rxcs._RxCSobject):

    def __init__(self, *args):
        rxcs._RxCSobject.__init__(self)    # Make it a RxCS object 
        
        self.strRxCSgroup = 'Signal generator'    # Name of group of RxCS modules
        self.strModuleName = 'Upconversion'       # Module name

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

        # Representation sampling frequency
        self.paramAddMan('fR', 'Representation sampling frequency', unit='Hz')
        self.paramType('fR', (int, float))
        self.paramH('fR', 0)                  # Rep. samp. freq. must be higher than zero
        self.paramL('fR', np.inf)             # ...and lower than infinity

        # Time of signal
        self.paramAddMan('tS', 'Signal time', unit='s')
        self.paramType('tS', (float, int))
        self.paramH('tS', 0)            # Time must be higher than zero
        self.paramL('tS', np.inf)       # ...and lower than infinity

        # Carrier frequency
        self.paramAddMan('fC', 'Carrier frequency')
        self.paramType('fC', (float, int))
        self.paramH('fC', 0)
        self.paramL('fC', np.inf)

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

        # Generate the carrier
        genC = rxcs.sig.randMult()

        genC.tS = self.tS        # Time of the signal
        genC.fR = self.fR        # The signal rep. sampling frequency
        genC.fRes = self.fC      # The signal spectrum resolution
        genC.vFrqs = np.array([self.fC]) 
        genC.vAmps = np.array([1])
        genC.vPhs = np.array([0])
        genC.bMute = 1
        genC.run()
        self.vCarrier = genC.mSig[0, :]

        # Upconvert the input signal        
        mSigIn = self.mSig.copy()        
        self.mSig = mSigIn * genC.mSig 

