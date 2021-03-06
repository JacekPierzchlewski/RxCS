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


OR: 
if the **bFreqSym** [frequency symmetrical] flag is cleared, then 
the frequencies are organized like this:


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
    |           \      .
    |            \     .
    |             \    .
    |              \   .
    |               \  .
    |                \ .
    |                 \.

where N is the number of tones in the dictionary.

(the **bFreqSym** flag was added in v2.1, 14 January 2016).         


*Examples*:
    Please go to the *examples/dictionaries* directory for examples on how to 
    use the dictionary generator. |br|

*Settings*:
    Parameters of the generator are described below.

    Take a look on '__parametersDefine' function for more info on the 
    parameters.

    Parameters of the dictionary generator are attributes of the class which 
    must/can be set before the generator is run.

    Required parameters:

    - a. **tS** (*float*): time of input signals

    - b. **fR** (*float*): input signals' representation sampling frequency

    - c. **fDelta** (*float*): the frequency separation between tones 

    - d. **nTones** (*float*): the number of tones in the dictionary


    Optional parameters:

    - e. **tStart** (*float*):  the time shift of starting time point [default = 0]

    - f, **fFirst** (*float*):  the first frequency in the spectrum  [default = fDelta]

    - g. **bMute** (*int*):    mute the console output from the sampler [default = 0]


*Output*:
    Description of the dictionary generator output is below. 
    This is the list of attributes of the generator class which are available 
    after calling the 'run' method:

    - a. **mDict** (*Numpy array 2D*):  the generated dictionary, one tone in a row
 
    - b. **mDictR** (*Numpy array 2D*):  the generated dictionary, real only values, one tone in a row 
 
    - c. **vT** (*Numpy array 1D*):  time vector for the dictionary

    - d. **vF** (*Numpy array 1D*):  frequency vector for the dictionary    

 
    Additional parameters of the generated dictionary:

    - e. **Tg**  (*float*):  dictionary time representation period
    
    - f. **nSamp** (*int*):  the number of time representation samples

    - g. **bFreqSym** (*int*):  symmetrical/non-symmetrical frequency distribution flag


*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0    |  8-SEP-2014 : * Initial version. |br|
    1.0r1  | 15-JAN-2015 : * Improvements in code comments |br|
    1.0r2  | 20-AUG-2015 : * File name changed |br|
    2,0    | 20-AUG-2015 : * Version 2.0 released |br|
    2.0r1  | 25-AUG-2015 : * Improvements in code comments and in headers |br| 
    2.0r2  | 03-OCT-2015 : * Bug fixed in silent mode |br|
    2.1    | 14-JAN-2016 : * Frequencies of tones may be organized non-symetrical |br|
    2.2    | 28-JAN-2016 : * Function 'freqRange' which gives indices of columns corresponding to a given frequency
                             range is added |br|    
    2.3    | 28-JAN-2016 : * Additional, real-valued only version of IDFT dictionary is returned


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

        # The 'symmetrical frequency distribution' flag
        self.paramAddOpt('bFreqSym', 'Symmetrical frequency distribution', default=0)
        self.paramType('bFreqSym', (int))
        self.paramAllowed('bFreqSym',[0, 1])      # It can be either 1 or 0

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
        self.vF = self._generateFVector(self.fFirstHigh, self.fDelta, self.fHigh)            # Frequency vector
        self.vT = self._generateTVector(self.Tg, self.nSamp, self.tStart)                    # Time vector
        (self.mDict, self.mDictR, self.vF, self.vFr) = self._generateIDFT(self.vT, self.vF)  # The dicionary matrices
        self.engineStopsInfo()       # Info that the engine ends
        return

    # Check configuration
    def _checkConf(self):
        """
        This function checks if the configuration for the generator is correct
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
        This function computes additional time parameters of the dictionary.
        
        Args:
            tS (float):         time of input signals
            fR (float):         input signals' representation sampling frequency
            tStart (float):     the time shift of starting time point
    
        Returns:
            Tg (float):         dictionary time representation period
            nSamp (int):        the number of time representation samples 
            tEnd (float):       dictionary representation time end
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
        This function computes additional frequency parameters of the dictionary.
        
        Args:
            fDelta (float):   the frequency separation between tones       
            nTones (int):     the number of tones in the dictionary     
            fFirst (float):   the first frequency in the spectrum

        Returns:
            fFirstHigh (float):   the positive low frequency limit of the dictionary        
            fHigh (float):        the positive high frequency limit of the dictionary
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
        if (self.bMute == 0):
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
        """
        This function generates the frequency vector of the dictionary.

        Args:
            fFirstHigh (float):   the positive low frequency limit of the dictionary                
            fDelta (float):   the frequency separation between tones       
            nTones (int):     the number of tones in the dictionary     

        Returns:
            vF  (Numpy array 1D): frequency vector for the dictionary          
        """

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
        """
        This function generates the time vector of the dictionary.

        Args:
            Tg (float):      dictionary time representation period
            nSamp (float):   the number of time representation samples
            tStart (int):    the time shift of starting time point

        Returns:
            vT  (Numpy array 1D): time vector for the dictionary          
        """

        # -----------------------------------------------------------------
        # Generate the time vector
        vT =  Tg * np.arange(nSamp) + tStart
        vT.shape = (vT.size, )
        return vT

    # Generate the IDFT dictionary
    def _generateIDFT(self, vT, vF):
        """
        This function generates the IDFT dictionary.

        Args:
            vT  (Numpy array 1D): time vector for the dictionary          
            vF  (Numpy array 1D): frequency vector for the dictionary          
 
        Returns:
            mDict   (Numpy array 2D):  the generated dictionary         
            mDictR  (Numpy array 2D):  the generated dictionary, real values only
            vF (Numpy array 1D): frequencies vector
        """
        
        # Change shape of the vectors, so that they can be multiplies
        vT.shape = (1, vT.size)
        vF.shape = (vF.size, 1)

        # -----------------------------------------------------------------
        # Generate the Dictionary matrix
        d = (1j * 2 * np.pi)   # d coefficient
        mDict = 0.5 * np.e**np.dot(vF, (d * vT))
        if self.bFreqSym == 0:
            (nRows, _) = mDict.shape
            mDict[np.arange(int(nRows/2), nRows), :] = mDict[np.arange(int(nRows) - 1, int(nRows/2) - 1, -1), :]
            vF[np.arange(int(nRows/2), nRows)] = vF[np.arange(int(nRows) - 1, int(nRows/2) - 1, -1)]

        # -----------------------------------------------------------------
        (nRows, nCols ) = mDict.shape                 # Get the number of rows/cols in the dictionary
        mDictR = np.zeros((2*nRows, nCols))           # Construct a new empty real-only dictionary matrix
        mDictR[np.arange(int(nRows/2)), :] = mDict.real[np.arange(int(nRows/2)) , :]   
        mDictR[np.arange(int(nRows/2) , nRows), :] = -1 * mDict.real[np.arange(int(nRows/2), nRows), :]
        mDictR[np.arange(nRows, 2*nRows), :] = mDict.imag

        vT.shape = (vT.size, )
        vF.shape = (vF.size, )
        vFr = np.hstack((vF, vF))

        return (mDict, mDictR, vF, vFr)


    def freqRange(self, iFMin, iFMax):
        """
        Find indices of cols of the dictionary which correspond to a frequency range <iFMin, iFMax>
        """
        if not 'vF' in self.__dict__:
            raise RuntimeError('Dictionary generator did not generate a dictionary yet!')
        if iFMin > iFMax:
            raise RuntimeError('Low frequency defining the frequency range can not be higher than the high frequency!')
        if (iFMin < 0) or (iFMax < 0):
            raise RuntimeError('Frequencies which define the frequency range can not be lower than zero!')
        if (iFMin > self.fHigh):
            raise RuntimeError('Requested frequency range is not in the dictionary!')
                                 
        iNf = self.vF.size          # The number of frequencies in the dictionary
        vInx = np.arange(iNf)       # All the indices of frequencies in the dictionary
        vFiltInx_p = vInx[np.multiply(self.vF >= iFMin, self.vF <= iFMax)]
        vFiltInx_n = vInx[np.multiply(self.vF <= -iFMin, self.vF >= -iFMax)]
        vFiltInx = np.hstack((vFiltInx_n, vFiltInx_p))
        return vFiltInx
        
        
        
    def freqRangeR(self, iFMin, iFMax):
        """
        Find indices of cols of the dictionary which correspond to a frequency range <iFMin, iFMax>  
        (dictionary with only real values)
        """
        if not 'vFr' in self.__dict__:
            raise RuntimeError('Dictionary generator did not generate a dictionary yet!')
        if iFMin > iFMax:
            raise RuntimeError('Low frequency defining the frequency range can not be higher than the high frequency!')
        if (iFMin < 0) or (iFMax < 0):
            raise RuntimeError('Frequencies which define the frequency range can not be lower than zero!')
        if (iFMin > self.fHigh):
            raise RuntimeError('Requested frequency range is not in the dictionary!')
                                 
        iNf = self.vFr.size          # The number of frequencies in the dictionary
        vInx = np.arange(iNf)       # All the indices of frequencies in the dictionary
        vFiltInx_p = vInx[np.multiply(self.vFr >= iFMin, self.vFr <= iFMax)]
        vFiltInx_n = vInx[np.multiply(self.vFr <= -iFMin, self.vFr >= -iFMax)]
        vFiltInx = np.hstack((vFiltInx_n, vFiltInx_p))
        return vFiltInx        
        