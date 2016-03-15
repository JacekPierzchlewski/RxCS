"""
This is a random gaussian noise generator module type 3.
This module generates the signal with oversampling=1, then oversamples the signal
to the wanted representation sampling frequency and finally it upconverts the signals, |br|

The generator is able to generate N random signals with a random frequency position within 
a given min and max boundaries. |br|


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

    - c. ****

    Optional parameters:

    - c. **fMin** (*float*): minimum frequency component in the signal   
                             [default = not regulated]

    - d. **fMax** (*float*): maximum frequency component in the signal   
                             [default = not regulated]

    - e. **iP** (*float*): signals' power  [default = 1W]

    - f. **nSigs** (*int*):  the number of signals to be generated  
                             [default = 1]


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
    0.01    | 15-MAR-2016 : * Version 1.0 released. |br|

*License*:
    BSD 2-Clause
"""


from __future__ import division
import numpy as np
import rxcs


class gaussNoise3(rxcs._RxCSobject):

    def __init__(self, *args):
        rxcs._RxCSobject.__init__(self)    # Make it a RxCS object

        self.strRxCSgroup = 'Signal generator'        # Name of group of RxCS modules
        self.strModuleName = 'Random gaussian noise (type 3)'  # Module name

        self.__parametersDefine()      # Define the parameters

        # Import tools
        self.gaussNoise = rxcs.sig.gaussNoise()          # Import basic gaussian noise generator
        self.oversampler = rxcs.sig.oversampler()        # Import oversampler
        self.upconvert = rxcs.sig.radio.upconvert()  # Upconversion
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

        # The lowest possible frequency component of the signal
        self.paramAddMan('fMin', 'The lowest possible frequency component of the signal', unit='Hz')
        self.paramType('fMin', (float, int))
        self.paramHE('fMin', 0)
        self.paramL('fMin', 'fMax')

        # The highest possible frequency component of the signal
        self.paramAddMan('fMax', 'The highest possible frequency component of the signal', unit='Hz')
        self.paramType('fMax', (float, int))
        self.paramH('fMax', 0)
        self.paramLE('fMax', 'fR', mul=0.5)

        # The frequency width of the signal
        self.paramAddMan('fWidth', 'Frequency width of the signal', unit='Hz')
        self.paramType('fWidth', (float, int))
        self.paramH('fWidth', 0)

        # The frequency gradation of the allowed spectrum
        self.paramAddMan('fGrad', 'The frequency gradation of the allowed spectrum', unit='Hz')
        self.paramType('fGrad', (float, int))
        self.paramH('fGrad', 0)

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

        # Check if there is enough space between the max and minimum frequency
        if ((self.fMax - self.fMin) < self.fWidth):
            strError = 'There is not enought space between the max and minimum frequncy!'
            raise ValueError(strError)

        # Compute the number of possible positions ofsignals
        iNPos = int(np.floor((self.fMax - self.fMin - self.fWidth)/self.fGrad)) + 1

        # Allocate matrix for signals
        self.mSig_ = np.nan*np.ones((self.nSigs, int(np.round(self.fR*self.tS))))

        # Generate the basic signals
        self.gaussNoise.fR = 2*self.fWidth
        self.gaussNoise.tS = self.tS
        self.gaussNoise.iP = 1
        self.gaussNoise.nSigs = self.nSigs
        self.gaussNoise.bMute = 1
        self.gaussNoise.fMax = self.fWidth/2
        
        self.gaussNoise.strFilt = 'butter'
        self.gaussNoise.nFiltOrd = 30
        self.gaussNoise.iRs = 100       
        self.gaussNoise.run()

        # Oversample the basic signals
        self.oversampler.mSig = self.gaussNoise.mSig
        self.oversampler.iFLow = 2*self.fWidth
        self.oversampler.iFHigh = self.fR
        self.oversampler.bMute = 1
        self.oversampler.run()

        # Upconvert 
        self.upconvert.fR = self.fR
        self.upconvert.tS = self.tS
        self.upconvert.bMute = 1
        vPos = np.random.randint(0, iNPos, self.nSigs)    # Draw positions of the signals
        for iInxSig in range(self.nSigs):
            fC = self.fMin + self.fWidth/2 + vPos[iInxSig] * self.fGrad
            self.upconvert.fC = fC
            self.upconvert.mSig = np.atleast_2d(self.oversampler.mSigOversamp[iInxSig, :])
            self.upconvert.run()
            self.mSig_[iInxSig, :] = self.upconvert.mSig[0, :]

        # Regulate the power of the signal and assign the signal with the regulated power
        # as the output signal
        self.powerRegulator.mSig = self.mSig_
        self.powerRegulator.iP = self.iP
        self.powerRegulator.bMute = 1
        self.powerRegulator.run()
        self.mSig = self.powerRegulator.mSigOut
        self.vP = self.powerRegulator.vP

        # Compute the number of samples in the output signal
        self.nSmp = int(np.round(self.fR * self.tS))
        return






