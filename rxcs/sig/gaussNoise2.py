"""
This is a random gaussian noise generator module type 2.
This module generates the signal with oversampling=1 and then oversamples the signal
to the wanted representation sampling frequency. |br|

The generator is able to generate N random signals with a given min and max
frequency components. |br|

*Examples*:
    Please go to the *examples/signals* directory for examples on how to use 
    the generator. |br|

*Settings*:
    Parameters of the generator described below.

    Take a look on '__parametersDefine' function for more info on the 
    parameters.

    Parameters of the generator are attributes of the class which must/can
    be set before the generator run.

    Required parameters:

    - a. **tS** (*float*): time of a signals

    - b. **fR** (*float*): signals' representation sampling frequency


    Optional parameters:

    - c. **fMin** (*float*): minimum frequency component in the signal   
                             [default = not regulated]

    - d. **fMax** (*float*): maximum frequency component in the signal   
                             [default = not regulated]

    - e. **iP** (*float*): signals' power  [default = 1W]

    - f. **nSigs** (*int*):  the number of signals to be generated  
                             [default = 1]

     Parameters given below are optional filter parameters.
     There parameters describe the filter which limits the signals' frequency components.
     The filter is applied only if **fMin** or **fMax** is given by user.

     - g. **strFilt**  (*string*):  filter type. The allowed values are:
                                    'butter', 'cheby1', 'cheby2', 'ellip', 'bessel'.
                                    [default = 'butter']

     - h. **nFiltOrd** (*int*):  the fitler order  [default = 10]
     
     - i. **iRp** (*float*):  max ripple in the filter's pass band.
                              Applicable to Chebyshev and elliptic filt. only.
                              [default = 0.1]
     
     - j. **iRs** (*float*):  min attenuation in the filter's stopband
                              Applicable to Chebyshev and elliptic filt. only.
                              [default = 60]

     - k. **bMute** (*int*):  mute the console output from the generator
                              [default = 0]


*Output*:
    Description of the generator output is below. 
    This is the list of attributes of the generator class which are available 
    after calling the 'run' method:

    - a. **mSig** (*Numpy array 2D*): Matrix with output signals, 
                                      one signal p. row

    - b. **nSmp** (*int*): The number of samples in the signals

    - c. **vP** (*Numpy array 1D*): Vector with the power of signals



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


class gaussNoise2(rxcs._RxCSobject):

    def __init__(self, *args):
        rxcs._RxCSobject.__init__(self)    # Make it a RxCS object

        self.strRxCSgroup = 'Signal generator'        # Name of group of RxCS modules
        self.strModuleName = 'Random gaussian noise (type 2)'  # Module name

        self.__parametersDefine()      # Define the parameters

        # Import tools
        self.gaussNoise = rxcs.sig.gaussNoise()          # Import basic gaussian noise generator
        self.oversampler = rxcs.sig.oversampler()        # Import oversampler
        self.powerRegulator = rxcs.sig.powerRegulator()  # Power regulator

    def __parametersDefine(self):
        """
            Internal method which defines the parameters    
        """

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

        # Minimum frequency of the signal
        self.paramAddOpt('fMin', 'Minimum frequency component in the signal', unit='Hz') 
        self.paramType('fMin', (float, int))
        self.paramHE('fMin', 0)
        self.paramL('fMin', 'fMax')

        # Maximum frequency of the signal
        self.paramAddOpt('fMax', 'Maximum frequency component in the signal', unit='Hz')
        self.paramType('fMax', (float, int))
        self.paramH('fMax', 0)
        self.paramLE('fMax', 'fR', mul=0.5)

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


    def run(self):
        """
            Run method, which starts the generator    
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

        # Generate the basic 
        if not self.wasParamGiven('fMax'):
            self.fMax = self.fR / 2
            
        # Generate the basic nosie signal
        self.gaussNoise.fR = 2*self.fMax
        self.gaussNoise.tS = self.tS
        self.gaussNoise.fMin = self.fMin
        self.gaussNoise.iP = 1
        self.gaussNoise.nSigs = self.nSigs
        self.gaussNoise.strFilt = self.strFilt
        self.gaussNoise.nFiltOrd = self.nFiltOrd
        self.gaussNoise.iRp = self.iRp
        self.gaussNoise.iRs = self.iRs
        self.gaussNoise.bMute = 1
        self.gaussNoise.run()

        # Oversample the generated signal and 
        self.oversampler.mSig = self.gaussNoise.mSig
        self.oversampler.iFLow = self.gaussNoise.fR
        self.oversampler.iFHigh = self.fR        
        self.oversampler.bMute = 1
        self.oversampler.run()

        # Regulate the power of the signal and assign the signal with the regulated power
        # as the output signal
        self.powerRegulator.mSig = self.oversampler.mSigOversamp
        self.powerRegulator.iP = self.iP
        self.powerRegulator.bMute = 1
        self.powerRegulator.run()
        self.mSig = self.powerRegulator.mSigOut
        self.vP = self.powerRegulator.vP

        # Compute the number of samples in the output signal
        self.nSmp = int(np.round(self.fR * self.tS))
        
        return        
        
        


