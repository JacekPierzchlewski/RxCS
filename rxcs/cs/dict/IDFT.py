"""
This module generates Inverse Discrete Fourier Transform matrix (IDFT). |br|

Frequencies represented by the rows of the generated IDFT matrix:


  freq.
    ^        /.
    |       / .
    |      /  .  
    |     /   .
    |    /    .
    |   /     .
    |  /      .
    | /       . N+1
    |/        . .     
    |1-------N---------2N---->  indices of columns
    |           .      /
    |           .     /
    |           .    /
    |           .   /
    |           .  / 
    |           . /
    |           ./

where N is the number of tones in the dictionary.


*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0    |  8-SEP-2014 : * Initial version. |br|
    1.0r1  | 15-JAN-2015 : * Improvements in code comments |br|
    1.0r2  | 20-AUG-2015 : * File name changed |br|
    2,0    | 20-AUG-2015 : * Version 2.0 released |br|

*License*:
    BSD 2-Clause

"""
from __future__ import division
import rxcs
import numpy as np

class IDFT(rxcs._RxCSobject):

    def __init__(self, *args):
        rxcs._RxCSobject.__init__(self)    # Make it a RxCS object 
        
        self.strRxCSgroup = 'Dictionary generator'  # Name of group of RxCS modules
        self.strModuleName = 'IDFT'                 # Module name

        self.__parametersDefine()      # Define the parameters

    # Define parameters
    def __parametersDefine(self):

        # Time of the signal [s]
        self.paramAddMan('tS', 'Time of the signal', unit='s')
        self.paramType('tS', (int, float))
        self.paramH('tS', 0)
        self.paramL('tS', np.inf)
        
        # The dictionary representation sampling freuqency [Hz]
        self.paramAddMan('fR', 'The dictionary representation sampling freuqency', unit='Hz')
        self.paramType('fR', (int, float))
        self.paramH('fR', 0)
        self.paramL('fR', np.inf)

        # The optional time shift of starting time point
        self.paramAddOpt('tStart', 'The time shift of starting time point', unit='s', default=0)
        self.paramType('tStart', (int, float))
        self.paramH('tStart', -np.inf)
        self.paramL('tStart', np.inf)

        # The frequency separation between tones [Hz]
        self.paramAddMan('fDelta', 'The frequency separation between tones', unit='Hz')
        self.paramType('fDelta', (int, float))
        self.paramH('fDelta', 0)
        self.paramL('fDelta', np.inf)

        # The number of tones
        self.paramAddMan('nTones', 'The number of tones')
        self.paramType('nTones', int)
        self.paramH('nTones', 0)
        self.paramL('nTones', np.inf)

        # The first frequency in the spectrum
        self.paramAddOpt('fFirst', 'The first frequency in the spectrum', unit='Hz', default='$$fDelta')
        self.paramType('fFirst', (int, float))
        self.paramH('fFirst', 0)
        self.paramL('fFirst', np.inf)

        # 'Mute the output' flag
        self.paramAddOpt('bMute', 'Mute the output', noprint=1, default=0)
        self.paramType('bMute', int)           # Must be of int type
        self.paramAllowed('bMute',[0, 1])      # It can be either 1 or 0

    # Run
    def run(self):
 
        self.parametersCheck()         # Check if all the needed partameters are in place and are correct
        self.parametersPrint()         # Print the values of parameters        

        self.__engine()          # Run the engine
        return self.__dict__     # Return dictionary with the parameters

    # Engine of the function
    def __engine(self):

        # Check of the configuration make sense
        self._checkConf()

        # Compute time and frequency parameters of dictionaries
        (self.Tg, self.nSamp, self.tEnd) = self._computeParamT(self.tS, self.fR, self.tStart)
        (self.fFirstHigh, self.fHigh) = self._computeParamF(self.fDelta, self.nTones, self.fFirst)

        # Print some additional time and frequency parameters of the dictionary
        self._printExtraParam()

        self.engineStartsInfo()      # Info that the engine starts
        self.vF = self._generateFVector(self.fFirstHigh, self.fDelta, self.fHigh)   # Frequency vector
        self.vT = self._generateTVector(self.Tg, self.nSamp, self.tStart)           # Time vector
        self.mDict = self._generateIDFT(self.vT, self.vF)   # The dicionary matrix
        self.engineStopsInfo()       # Info that the engine ends
        return

    # Check configuration
    def _checkConf(self):
        """
        """

        # Check if the first frequency in the spectrum is compatible with the 
        # frequency separation between tones
        nTonesStart = self.fFirst / self.fDelta
        if not self.isequal(nTonesStart, np.round(nTonesStart), 1e-6):
            strE = 'The first frequency in the spectrum (fFirst) is '
            strE = strE + 'incompatible with the frequency separation between tones (fDelta)!'
            raise ValueError(strE)

        # Check if the time represented by dictionary is compatible
        # with the representation sampling period
        nSmp = self.tS * self.fR  # The number of signal samples
        if not self.isequal(nSmp, np.round(nSmp), 1e-6):
            strE = 'Time represented by dictionary (tS) is incompatible with '
            strE = strE + 'the dictionary representation sampling freuqency (fS)!'
            raise ValueError(strE)

        # Check if the optional time shift of starting time point is compatible
        # with the representation sampling period
        nSmptStart = self.tStart * self.fR
        if not self.isequal(nSmptStart, np.round(nSmptStart), 1e-6):
            strE = 'Time shift of starting time point (tS) is incompatible with '
            strE = strE + 'the dictionary representation sampling frequency (fS)!'
            raise ValueError(strE)

        # Check Nyquist
        fMax = self.fFirst + self.fDelta * (self.nTones - 1)
        if not (self.fR > 2 * fMax):
            strW = 'WARNING!  The representation sampling frequency (fR) is to low! '
            strW = strW + '(Ever heard about Nyqist principle?)'
            rxcs.console.newline()
            rxcs.console.warning(strW)

        # -----------------------------------------------------------------
        return
        
    # Compute time parameters of dictionaries
    def _computeParamT(self, tS, fR, tStart):
        """
        """
        # The signal representation period
        Tg = 1/fR

        # The number of signal samples
        nSamp = int(np.round(tS / Tg))

        # Signal time end
        tEnd = tStart + tS
        
        return (Tg, nSamp, tEnd)

    # Compute frequency parameters of dictionaries
    def _computeParamF(self, fDelta, nTones, fFirst):
        """
        """
        # The positive low frequency limit of the dictionary
        fFirstHigh = np.floor(fFirst/fDelta) * fDelta

        # The positive high frequency limit of the dictionary
        fHigh = fFirstHigh + fDelta * (nTones - 1)

        return (fFirstHigh, fHigh)

    # Print some additional time parameters of the dictionary
    def _printExtraParam(self):
        """
        """
        rxcs.console.bullet_param('The last time moment represented by the dictionary',
                                   self.tEnd, '-', 'seconds')

        rxcs.console.bullet_param('The signal representation sampling period',
                                  self.Tg, '-', 'seconds')

        rxcs.console.param('The number of signal samples', self.nSamp, '-', 'samples')

        rxcs.console.bullet_param('The maximum frequency represented by the dictionary',
                                  self.fHigh, '-', 'Hz')
        return

    # Generate the frequency vector
    def _generateFVector(self, fFirstHigh, fDelta, fHigh):

        # -----------------------------------------------------------------
        # Generate the frequency vector
        vF_pos = np.arange((fFirstHigh/fDelta), (fHigh/fDelta)+1)  # positive freqs
        vF_neg = -1 * vF_pos                                       # negative freqs
        vF_neg.sort()
        vF = fDelta * np.concatenate( (vF_pos, vF_neg) )
        vF.shape = (vF.size, )
        return vF

    # Generate the time vector
    def _generateTVector(self, Tg, nSamp, tStart):

        # -----------------------------------------------------------------
        # Generate the time vector
        vT =  Tg * np.arange(nSamp) + tStart
        vT.shape = (vT.size, )
        return vT

    # Generate the IDFT dictionary
    def _generateIDFT(self, vT, vF):
        
        # Change shape of the vectors, so that they can be multiplies
        vT.shape = (1, vT.size)
        vF.shape = (vF.size, 1)

        # -----------------------------------------------------------------
        # Generate the Dictionary matrix
        d = (1j * 2 * np.pi)   # d coefficient
        mDict = 0.5 * np.e**np.dot(vF, (d * vT))

        # -----------------------------------------------------------------
        vT.shape = (vT.size, )
        vF.shape = (vF.size, )
        return (mDict)