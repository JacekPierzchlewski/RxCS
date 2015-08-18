"""
This is a random gaussian noise generator module. |br|

The generator is able to generate N random signals with a given bandwidth. |br|

For description of parameters of the generator, take a look on '__parametersDefine' function.
For examples of usage, go to examples/signals directory. |br|

Atributes of 'gaussNoise' class after calling 'run' method:

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
import scipy.signal as scsig
import rxcs


class gaussNoise(rxcs._RxCSobject):

    def __init__(self, *args):
        rxcs._RxCSobject.__init__(self)    # Make it a RxCS object

        self.strRxCSgroup = 'Signal generator'        # Name of group of RxCS modules
        self.strModuleName = 'Random gaussian noise'  # Module name

        self.__parametersDefine()      # Define the parameters

    def __parametersDefine(self):
        """
        Internal method which defines the parameters    
        """

        # Representation sampling frequency
        self.paramAddMan('fs', 'Representation sampling frequency', unit='Hz')
        self.paramType('fs', (int, float))
        self.paramH('fs', 0)                  # Rep. samp. freq. must be higher than zero
        self.paramL('fs', np.inf)             # ...and lower than infinity

        # Time of signal
        self.paramAddMan('tS', 'Signal time', unit='s')
        self.paramType('tS', (float, int))
        self.paramH('tS', 0)            # Time must be higher than zero
        self.paramL('tS', np.inf)       # ...and lower than infinity

        # Baseband
        self.paramAddOpt('fB', 'Baseband', unit='Hz')
        self.paramType('fB', (float, int))
        self.paramHE('fB', 0)                           # Signal baseband must be higher or equal to zero
                                                        # (if it is equal to zero, the baseband is defined by fs)
        self.paramL('fB', np.inf)                       # ...and lower than infinity
        self.paramLE('fB', 'fs', mul=0.5)               # Signal baseband must be lower or equal to half the rep. sampling
                                                        # frequency
        # Power of a signal
        self.paramAddOpt('iP', 'Signal power', unit='W', default=1)
        self.paramType('iP',(float, int))
        self.paramH('iP', 0)            # Power of the signal must be higher than zero
        self.paramL('iP', np.inf)       # ...and lower than infinity

        # The number of signals
        self.paramAddOpt('nSigs', 'The number of signals', unit='', default=1)
        self.paramType('nSigs',(int))
        self.paramH('nSigs', 0)            # The number of signals must be higher than zero
        self.paramL('nSigs', np.inf)       # ...and lower than infinity

        # --------------------------------------------------------------------
        # Filter parameters:

        # Filter type
        self.paramAddOpt('strFilt', 'Filter type', unit='', default='butter')
        self.paramType('strFilt',str)
        self.paramAllowed('strFilt',['butter', 'cheby1', 'cheby2', 'ellip', 'bessel'])

        # Filter order
        self.paramAddOpt('nFiltOrd', 'Filter order', unit='', default=10)
        self.paramType('nFiltOrd',int)
        self.paramHE('nFiltOrd',1)
        self.paramLE('nFiltOrd', 100)

        # Max ripple in the pass band
        self.paramAddOpt('iRp', 'Max ripple in the passband', unit='db', default=0.1, noprint=1)
        self.paramType('iRp',(float, int))
        self.paramH('iRp',0)

        # Min attenuation in the stopband
        self.paramAddOpt('iRs', 'Min attenuation in the stopband', unit='db', default=60, noprint=1)
        self.paramType('iRs',(float, int))
        self.paramH('iRs',0)

        # --------------------------------------------------------------------

        # Mute the output flag
        self.paramAddOpt('bMute', 'Mute the output', noprint=1, default=0)
        self.paramType('bMute', int)          # Must be of int type
        self.paramAllowed('bMute',[0, 1])      # It can be either 1 or 0


    def run(self, *args):
        """
        Run method, which starts the generator    
        """

        self.parametersProcess(*args)  # Get parameters given directly to 'run' function
        self.parametersCheck()         # Check if all the needed partameters are in place and are correct
        self.parametersPrint()         # Print the values of parameters

        self.__engine()                # Run the engine
        return self.__dict__           # Return dictionary with the parameters


    def __engine(self):
        """
            Engine of the function    
        """

        self.engineStartsInfo()  # Info that the engine starts

        # ---------------------------------------------------------------------
        # Generate the base signal
        self.nSigSamp = round(self.fs * self.tS)     # The number of samples in the output signal
        self.mSig = np.random.randn(self.nSigs, self.nSigSamp)   # Generate the noise

        # ---------------------------------------------------------------------
        # Filter the signal with a low pass filter, if it is needed
        if (self.fB > 0):

            # Design a iir low pass filter
            iCFP = self.fB/(0.5*self.fs)   # Compute the filter parameter
            (vN, vD) = scsig.iirfilter(self.nFiltOrd, iCFP, btype='lowpass', ftype=self.strFilt,
                                       rs=self.iRs, rp=self.iRp)
            # Apply the filter
            self.mSig = scsig.lfilter(vN, vD, self.mSig)
            self.mSig = self.mSig.T  # The output matrix should be column wise, not row wise

        self.engineStopsInfo()   # Info that the engine ends

