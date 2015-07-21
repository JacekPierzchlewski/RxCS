"""
This a Random Multitone Signal Generator module. |br|

It is able to generate *N* multitone random signals according to settings
given by a user. |br|

Please go to the *examples* directory for examples on how to use the
generator. |br|

Parameters of the generator (attributes of the class which must/can be set before the generator run):

    Required parameters:

    - a. **tS** (*float*): time of a signals

    - b. **fR** (*float*): signals representation frequency

    - c. **fMax** (*float*): maximum frequency present in signals

    - d. **fRes** (*float*): tones frequency resolution


    Optional parameters:

    - e. **fMin** (*float*): minimum allowed frequency present in the spectrum  [default = fRes]

    - f. **nSigs** (*int*): the number of signals to be generated  [default = 1]

    - g. **iSNR** (*float*): level of noise in signals [dB] (SNR)  [default = +int]

    - h. **iP** (*float*): requested power of signals  [default = do not regulate the power]


    - i. **vFrqs** (*Numpy array vector*): vector with requested frequencies of tones  [default = empty vector]

    - j. **vAmps** (*Numpy array vector*): vector with requested amplitudes of tones   [default = empty vector]

    - k. **vPhs** (*Numpy array vector*): vector with requested phases of tones        [default = empty vector]

    
    - l. **nTones** (*int*): the number of additional tones    [default = 0]

    - m. **iMinAmp** (*float*): min amplitude of a tone present in a signal      [default = 0.1]

    - n. **iGraAmp** (*float*): gradation of a random amplitude of a tone        [default = 0.1]

    - o. **iMaxAmp** (*float*): max amplitude of a tone present in a signal      [default = 1.0]

    - p. **iMinPhs** (*float*): min allowed phase of a tone present in a signal  [default = -179 deg]

    - q. **iGraPhs** (*float*): gradation of a random phase of a tone            [default = 1 deg]

    - r. **iMaxPhs** (*float*): max allowed phase of a tone present in a signal  [default = +180 deg]


    - s. **bMute** (*int*): mute the console output from the generator [default = 0]


Available atributes of 'randMult' class after calling 'run' method:

    Fields in the output dictionary:

    - a. **mSig** (*int*): Matrix with output signals

    - b. **mSigNN** (*float*): Matrix with nonnoisy output signals

    - c. **nSigs** (*float*): The number of generated signals

    - d. **fR** (*float*): Signal representation sampling frequency

    - e. **tS** (*float*): The time of the signals [s]

    - f. **nSmp** (*float*): The number of samples in the signals

    - g. **vTSig** (*float*): The time vector for the generated signals

    - h. **iSNR** (*vector*): Signal 2 noise ratio

    - i. **iP** (*vector*): Requested power of the signals

    - j. **vP** (*vector*): Power of the signals

    - k. **vPNN** (*vector*): Power of the non noisy signals

    - l. **vPCoef** (*vector*): Power adjustment coefficients

    - m. **mFrqs** (*matrix*): Frequencies of tones in the signals

    - n. **mAmps** (*matrix*): Amplitudes of tones in the signals

    - o. **mPhs** (*matrix*): Phases of tones in the signals

    - p. **mAmPh** (*matrix*): Complex matrix with amplitudes/phases of tones

    - q. **fFFTR** (*float*): Signal FFT frequency resolution

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    0.1  | 15-MAY-2014 : * Initial version. |br|
    0.2  | 16-MAY-2014 : * Docstrings added. |br|
    0.3  | 19-MAY-2014 : * The main func. divided into smaller functions. |br|
    0.4  | 20-MAY-2014 : * Errors are served by 'raise'. |br|
    0.5  | 20-MAY-2014 : * Docstrings are added to the internal functions. |br|
    0.5r1| 20-MAY-2014 : * Order of the internal functions was changed. |br|
    1.0  | 20-MAY-2014 : * Version 1.0 released. |br|
    1.0r1| 21-MAY-2014 : * Error in progress printing is fixed. |br|
    1.0r2| 21-MAY-2014 : * Error in default random amplitude is fixed. |br|
    1.0r3| 21-MAY-2014 : * Error in progress printing (if muted) is fixed. |br|
    1.0r4| 27-MAY-2014 : * Error in the number of given frqs is fixed. |br|
    1.0r5| 27-MAY-2014 : * Error in the vector with signal time is fixed. |br|
    2.0  | 21-JUL-2015 : * Objectified version (2.0) |br|

*License*:
    BSD 2-Clause
"""

from __future__ import division
import numpy as np
import rxcs


class randMult(rxcs._RxCSobject):

    def __init__(self, *args):
        rxcs._RxCSobject.__init__(self)    # Make it a RxCS object 
        
        self.strRxCSgroup = 'Signal generator'     # Name of group of RxCS modules
        self.strModuleName = 'Random multitone'    # Module name        

        self.__parametersDefine()      # Define the parameters

        # If there are arguments given when the object was created, then run the engine  
        if len(args) > 0:
            self.run(*args)

    # Define parameters
    def __parametersDefine(self):

        # Time of the signal [s]
        self.paramAddMan('tS', 'Time of the signal')
        self.paramType('tS', (int, float))
        self.paramH('tS', 0)
        self.paramL('tS', np.inf)       

        # The signal representation sampling freuqency [Hz]
        self.paramAddMan('fR', 'The signal representation sampling freuqency')
        self.paramType('fR', (int, float))
        self.paramH('fR', 0)
        self.paramL('fR', np.inf)
 
        # The highest possible frequency in the signal [Hz]
        self.paramAddMan('fMax', 'The highest possible frequency in the signal')
        self.paramType('fMax', (int, float))
        self.paramH('fMax', 0)
        self.paramL('fMax', 'fR', mul=0.5)  # Nyquist principle

        # Signal spectrum resolution [Hz]
        self.paramAddMan('fRes', 'Signal spectrum resolution')
        self.paramType('fRes', (int, float))
        self.paramH('fRes', 0)
        self.paramL('fRes', np.inf)


        # The minimum frequency of additional tones
        self.paramAddOpt('fMin', 'Minimum frequency of additional tones', default='$$fRes')
        self.paramType('fMin', (int, float))
        self.paramH('fMin', 0)
        self.paramLE('fMin', 'fMax')

        # The number of signals to be generated
        self.paramAddOpt('nSigs', 'The number of signals to be generated', default=1)
        self.paramType('nSigs', (int))
        self.paramH('nSigs', 0)            # The number of signals must be higher than zero
        self.paramL('nSigs', np.inf)       # ...and lower than infinity

        # Signal noise [dB]
        self.paramAddOpt('iSNR', 'Signal to noise ratio', default=np.inf)
        self.paramType('iSNR', (int, float))

        # Power of signals [W]
        self.paramAddOpt('iP', 'Power of signals', default=np.nan)
        self.paramType('iP', (int, float))
        self.paramH('iP', 0)
        self.paramL('iP', np.inf)

        # Vector with given frequencies of signal cosine tones
        self.paramAddOpt('vFrqs', 'Vector with given frequencies of signal cosine tones', default=np.zeros(0), noprint=1)
        self.paramType('vFrqs', np.ndarray)        
        strError = 'Frequencies in \'vFrqs\' vector must not be higher than the highest possible in the signal spectrum!'
        self.paramLE('vFrqs', 'fMax', errnote=strError)           
        strError = 'Frequencies in the \'vFrqs\' must be higher than 0!'
        self.paramH('vFrqs', 0, errnote=strError)   
        strError = 'Frequencies in \'vFrqs\' vector must not be lower than the lowest possible in the signal spectrum!'
        self.paramHE('vFrqs', 'fMin', errnote=strError)
        strError = 'Size of the vector with given frequencies \'vFrqs\' must be equal to size of the vectors \'vAmps\' and \'vPhs\''
        self.paramSizEq('vFrqs', 'vAmps', errnote=strError)
        self.paramSizEq('vFrqs', 'vPhs', errnote=strError)
        self.paramNDimEq('vFrqs', 1)
        strError = 'There are frequencies repeated in the \'vFrqs\' vector!'
        self.paramUnique('vFrqs', errnote=strError)
        self.NaNAllowedEl('vFrqs')


        # Vector with given amplitudes of signal cosine tones
        self.paramAddOpt('vAmps', 'Vector with given amplitudes of signal cosine tones', default=np.zeros(0), noprint=1)
        self.paramType('vAmps', np.ndarray)
        self.paramH('vAmps', 0, errnote='Amplituides of tones must be higher than 0')
        self.paramNDimEq('vAmps', 1)
        self.NaNAllowedEl('vAmps')

        # Vector with given phases of signal cosine tones content
        self.paramAddOpt('vPhs', 'Vector with given phases of signal cosine tones', default=np.zeros(0), noprint=1)
        self.paramType('vPhs', np.ndarray)
        self.paramH('vPhs', -180, errnote='Phases of tones must be higher than -180 [deg]')
        self.paramLE('vPhs', 180, errnote='Phases of tones must be lower or equal to 180 [deg]')
        self.paramNDimEq('vPhs', 1)
        self.NaNAllowedEl('vPhs')

        # The number of additional tones
        self.paramAddOpt('nTones', 'The number of additional tones', default=0)
        self.paramType('nTones', (int))
        self.paramHE('nTones', 0)

        # The boundaries for amplitudes: amplitude min value
        self.paramAddOpt('iMinAmp', 'Minimum value of random amplitudes', default=0.1)
        self.paramType('iMinAmp', (int, float))
        self.paramH('iMinAmp', 0)
        self.paramLE('iMinAmp','iMaxAmp')
 
        # The boundaries for amplitudes: amplitude gradation
        self.paramAddOpt('iGraAmp', 'Gradation of value of random amplitudes', default=0.1)
        self.paramType('iGraAmp', (int, float))
        self.paramH('iGraAmp', 0)
        
        # The boundaries for amplitudes: amplitude max value
        self.paramAddOpt('iMaxAmp', 'Maximum value of random amplitudes', default=1.0)
        self.paramType('iMaxAmp', (int, float))
        self.paramH('iMaxAmp', 0)

        # The boundaries for amplitudes: phase min value
        self.paramAddOpt('iMinPhs', 'Minimum value of random phase', default=-179)
        self.paramType('iMinPhs', (int, float))
        self.paramH('iMinPhs',-180)
        self.paramLE('iMinPhs',180)
        self.paramLE('iMinPhs','iMaxPhs')
        
        # The boundaries for amplitudes: phase gradation
        self.paramAddOpt('iGraPhs', 'Gradation of value of random phase', default=1)
        self.paramType('iGraPhs', (int, float))
        self.paramH('iGraPhs', 0)

        # The boundaries for amplitudes: phase max value
        self.paramAddOpt('iMaxPhs', 'Maximum value of random phase', default=180)
        self.paramType('iMaxPhs', (int, float))
        self.paramH('iMaxPhs',-180)
        self.paramLE('iMaxPhs',180)

        # 'Mute the output' flag
        self.paramAddOpt('bMute', 'Mute the output', noprint=1, default=0)
        self.paramType('bMute', int)           # Must be of int type
        self.paramAllowed('bMute',[0, 1])      # It can be either 1 or 0


    # Run
    def run(self, *args):

        self.parametersProcess(*args)  # Get parameters given directly to 'run' function
        self.parametersCheck()         # Check if all the needed partameters are in place and are correct
        self.parametersPrint()         # Print the values of parameters
        
        self.engineStartsInfo()  # Info that the engine starts
        self.__engine()          # Run the engine
        self.engineStopsInfo()   # Info that the engine ends
        return self.__dict__     # Return dictionary with the parameters


    # Engine of the function
    def __engine(self):
        self._checkConf()

        # - - - - - - - - - - - - - - - - - - -        
        # Signal generation starts here:
        
        self.mFrqsInx = self._drawFreq(self.vFrqs, self.nTones, self.fMin, self.fMax, self.nSigs, self.fRes)         # Draw frequencies of the signals
        self.mAmps = self._drawAmps(self.vAmps, self.nTones, self.nSigs, self.iMinAmp, self.iGraAmp, self.iMaxAmp)   # Draw amplitudes of the signals
        self.mPhs = self._drawPhases(self.vPhs, self.nTones, self.nSigs, self.iMinPhs, self.iGraPhs, self.iMaxPhs)   # Draw phases of the signals
        
        # Generate the signals by IFFT
        (mSig, self.mAmPh, self.mFrqs, self.fFFTR) = \
            self._genSigs(self.mFrqsInx, self.mAmps, self.mPhs, self.nSigs, self.tS, self.fR, self.fRes)
    
        # - - - - - - - - - - - - - - - - - - -
    
        # Adjust the signal power
        (mSig, vP, self.vPCoef, self.mAmps, self.mAmPh) = self._adjPower(mSig, self.iP, self.mAmps, self.mAmPh)
    
        # Add the AWGN noise to the signals
        (self.mSigNN, self.vPNN, self.mSig, self.vP) = self._addNoise(mSig, vP, self.iSNR)
        
        # Generate the time vector for the signal
        self.vTSig = np.arange(self.nSmp) / self.fR 

        return


    def _checkConf(self):
        """
        This function checks the configuration of the generator.    
        """
        #----------------------------------------------------------------------
        # If the minimum frequency was not given, it is equal to the frequency resolution
        if np.isnan(self.fMin):
            self.fMin = self.fRes
        
        #----------------------------------------------------------------------
        # Check the lowest possible frequency in the signal vs spectrum
        # resolution
        strErr = 'The lowest possible frequency in the signal is not a multiple '
        strErr = strErr + 'of the signal spectrum resolution'
        if (round(self.fMin/self.fRes) - self.fMin/self.fRes) > 1e-15:
            raise ValueError(strErr)
                  
        #----------------------------------------------------------------------
        # Check the highest possible frequency in the signal vs spectrum
        # resolution
        strErr = 'The highest possible frequency in the signal is not a multiple '
        strErr = strErr + 'of the signal spectrum resolution'
        if (round(self.fMax/self.fRes) - self.fMax/self.fRes) > 1e-15:
            raise ValueError(strErr)
    
        #----------------------------------------------------------------------
        # Check if there is a space for all the frequencies requested in
        # the signal, both given in the vFrqs vector and requested to be 
        # chosen randomly 
    
        # Compute the total number of tones in the max possible spectrum
        nSpectTones = int(self.fMax/self.fRes) - int(self.fMin/self.fRes) + 1 
                                                                               
        nFG = self.vFrqs.size          # The number of frequencies given in the vector with frequencies
        nSigTones = nFG + self.nTones  # The total number of tones which will be present in the signal

        strErr = 'The signal spectrum consists of %d tones. ' % (nSpectTones)
        strErr = strErr + 'I can not put there %d [vFrqs] + %d [nTones] tones' \
            % (nFG, self.nTones)
        if nSpectTones < nSigTones:
            raise ValueError(strErr)

        #----------------------------------------------------------------------
        # Check if there is a frequency leackage
        self.nSmp = int(round(self.tS*self.fR))  # Calculate the number of samples in the signals
        fFFTR = self.fR/self.nSmp    # Calculate the FFT frequency resolution
    
        if abs(round(self.fRes/fFFTR) - self.fRes/fFFTR) > 0:
            strErr = ('Frequency leackage! Signal spectrum resolution can not be ')
            strErr = strErr + ('represented with the current signal parameters!')
            raise ValueError(strErr)
    
        #----------------------------------------------------------------------
        # Check the vector with given frequencies
    
        # Check the vector with given frequencies, if it is longer then 0
        if nFG > 0:
    
            # Create the vector with given and specified frequencies (not np.nan)
            vFrqs_ = self.vFrqs[np.isnan(self.vFrqs) == 0]

            # 1. check resolution of given frequencies:
            if np.abs(np.sum(np.round(vFrqs_/self.fRes) - (vFrqs_/self.fRes))) > 1e-15:
                strErr = ('A frequency given in the vFrqs vector is ')
                strErr = strErr + ('incoherent with the resolution of signal ')
                strErr = strErr + ('spectrum!\n')
                raise ValueError(strErr)
    
            # Do correction of possible representation errors in the vector with frequencies
            self.vFrqs = np.round(self.vFrqs/self.fRes)*self.fRes
                        
        #----------------------------------------------------------------------
        return


    # =================================================================
    # Draw frequencies of the signals
    # =================================================================
    def _drawFreq(self, vFrqs, nTones, fMin, fMax, nSigs, fRes):
        """
        This function draws frequencies of tones for all the signals
        according to the rules specified by users,
    
        Args:
            vFrqs (vector):  vector with specified frequencies
            nTones (int):    the number of additional tones
            fMin (int):      the min allowed frequency in the signal spectrum
            fMax (int):      the max allowed frequency in the signal spectrum
            nSigs (int):     the number of signals to be generated
            fRes (int):      signal spectrum resolution
                             (distance between the tones in the spectrum)
    
        Returns:
            mFrqsInx (matrix):  matrix with frequencies of tones for all
                                the signals (one row - one signal)
                                The frequencies are represented as indices of
                                frequencies from the allowed signal spectrum.
    
        """
       
        #----------------------------------------------------------------------
        # Recalculate frequencies to indices of tones in the spectrum
    
        # Recalculate the vector with frequencies from frequency to index
        # of a frequency in the spectrum
        vFrqsInx = (vFrqs / fRes)
    
        # Create a vector with GIVEN (not nan) indices of frequencies in the
        # vFrqs vector
        vFrqsInx_ = (vFrqsInx[np.isnan(vFrqsInx) == 0]).astype(int)
    
        #----------------------------------------------------------------------
        # Create the vector with indices of avaialble frequencies in the spectrum
    
        # Create a vector with indices of all the available tones in the spectrum
        vSpecInx = np.arange(1, int(fMax/fRes) + 1)
    
        # Boolean vector which indicates if the frequency is free
        vFreqIsFree = np.ones(int(fMax/fRes)).astype(bool)
        
        # Mark all the frequencies below min frequency as unavailable 
        for inxF in np.arange(int(fMin/fRes)-1):
            vFreqIsFree[inxF] = 0
    
        # Mark the frequencies taken by vFreq vector as unavailable
        vFreqIsFree[vFrqsInx_ - 1] = 0
    
        # Create the vector with indices of available frequencies
        vAvailFreqsInx = vSpecInx[vFreqIsFree]
    
        #----------------------------------------------------------------------
        # Construct a vector with indices of frequencies for all the needed signals
    
        # Add unknown frequencies of the additional tones to the vFrqsInx vector
        vFrqsInx = np.concatenate((vFrqsInx, np.nan*np.zeros(nTones)))
    
        # Calculate the number of missing frequencies in the vector with
        # frequencies
        iMissF = len(vFrqsInx) - len(vFrqsInx_)
    
        # Construct a matrix with indices of frequencies for all the needed signals
        mFrqsInx = np.tile(vFrqsInx, (nSigs, 1))
    
        #----------------------------------------------------------------------
        # Draw the frequencies
        for inxSig in np.arange(nSigs):
    
            # Permute all the indices of frequencies in the spectrum
            vPermutedFreqsInx = ((np.random.permutation(vAvailFreqsInx)).T)
    
            # From the permuted indices of frequencices take as many
            # as it is missing
            vTakenFreqsInx = vPermutedFreqsInx[np.arange(iMissF)]
    
            # Put the taken indices of frequencies to the matrix with frequency
            # indices for all the signals
            mFrqsInx[inxSig, np.isnan(mFrqsInx[inxSig, :])] = vTakenFreqsInx
    
        return mFrqsInx


    # =================================================================
    # Draw amplitudes of the signals
    # =================================================================
    def _drawAmps(self, vAmps, nTones, nSigs, iMinAmp, iGraAmp, iMaxAmp):
        """
        This function draws amplitudes of tones for all the signals
        according to the rules specified by users,
    
        Args:
            vAmps (vector):  vector with specified amplitudes of tones in signals
            nTones (int):    the number of additional tones
            nSigs (int):     the number of signals to be generated
            iMinAmp (int):   min amplitude of a random tone present in a signal
            iGraAmp (int):   gradation of a amplitude of a random tone
            iMaxAmp (int):   max amplitude of a random tone present in a signal
    
        Returns:
            mAmps (matrix):  matrix with amplitudes of tones for all
                             the signals (one row - one signal)
    
        """
    
        # Add unknown amplitudes of the additional tones to the vAmps vector
        vAmps = np.concatenate((vAmps, np.nan*np.zeros(nTones)))
    
        # Compute the number of missing amplitudes for every signal
        iMissA = (vAmps[np.isnan(vAmps)]).size
    
        #----------------------------------------------------------------------
    
        # Compute the number of possible amplitude values
        nAmpVal = np.floor((iMaxAmp - iMinAmp) / iGraAmp) + 1
    
        #----------------------------------------------------------------------
    
        # Draw the missing amplitudes for all the signals
        vDrawAmps = \
            iMinAmp + iGraAmp*(np.random.randint(0, nAmpVal, (nSigs*iMissA)))
    
        # Construct a matrix with amplitudes of tones for all the needed signals
        mAmps = np.tile(vAmps, (nSigs, 1))
    
        # Put the draw amplitudes to the matrix with amplitudes of tones for
        # all the needed signals
        mAmps[np.isnan(mAmps)] = vDrawAmps
    
        return mAmps
    
    
    # =================================================================
    # Draw phases of the signals
    # =================================================================
    def _drawPhases(self, vPhs, nTones, nSigs, iMinPhs, iGraPhs, iMaxPhs):
        """
        This function draws phases of tones for all the signals
        according to the rules specified by users,
    
        Args:
            vPhs (vector):   vector with specified phases of tones in signals
            nTones (int):    the number of additional tones
            nSigs (int):     the number of signals to be generated
            iMinPhs (int):   min phase of a random tone present in a signal
            iGraPhs (int):   gradation of a phase of a random tone
            iMaxPhs (int):   max phase of a random tone present in a signal
    
        Returns:
            mPhs (matrix):   matrix with phases of tones for all
                             the signals (one row - one signal)
    
        """
    
        # Add unknown phases of the additional tones to the vAmps vector
        vPhs = np.concatenate((vPhs, np.nan*np.zeros(nTones)))
    
        # Compute the number of missing phases for every signal
        iMissP = (vPhs[np.isnan(vPhs)]).size
    
        #----------------------------------------------------------------------
    
        # Compute the number of possible phase values
        nPhsVal = np.floor((iMaxPhs - iMinPhs)/iGraPhs) + 1
    
        #----------------------------------------------------------------------
    
        # Draw the missing phases for all the signals
        vDrawPhs = \
            iMinPhs + iGraPhs*(np.random.randint(0, nPhsVal, (nSigs*iMissP)))
    
        # Construct a matrix with phases of tones for all the needed signals
        mPhs = np.tile(vPhs, (nSigs, 1))
    
        # Put the draw phases to the matrix with phases of tones for
        # all the needed signals
        mPhs[np.isnan(mPhs)] = vDrawPhs
    
        return mPhs
    
    
    # =================================================================
    # Generate the signals by IFFT
    # =================================================================
    def _genSigs(self, mFrqsInx, mAmps, mPhs, nSigs, tS, fR, fRes):
        """
        This function generate the multitone signals using the IFFT algorithm.
    
        Args:
            mFrqsInx (matrix):  matrix with freqs of tones for all the signals
                                (as indices of tones in the allowed spectrum)
            mAmps (matrix):     matrix with amplitudes of tones for all the signals
            mPhs (matrix):      matrix with phases of tones for all the signals
            nSigs (float):      the number of signals
            tS (float):         time of the signals
            fR (float):         signal representation sampling frequency
            fRes (float):       signal spectrum resolution
                                (distance between the tones in the spectrum)
    
        Returns:
            mSig (matrix):   matrix with signals (one row - one signal)
            mAmPh (float):   complex matrix with amplitudes/phases of tones
            mFrqs (matrix):  matrix with freqs of tones for all the signals
            fFFTR (float):   signal FFT frequency resolution
        """
    
        # Calculate the number of samples in the signals
        nSmp = int(round(tS*fR))
    
        # Calculate the FFT frequency resolution
        fFFTR = fR/nSmp
    
        #----------------------------------------------------------------------
    
        # Adjust the amplitudes value to the number of points
        mAmpsAdj = mAmps * nSmp/2
    
        # Change phases into radians
        mPhsRad = mPhs*np.pi/180
    
        # Generate a one complex matrix for all the signals and its conjugated copy
        mAmPh = mAmpsAdj*np.cos(mPhsRad) + 1j*mAmpsAdj*np.sin(mPhsRad)
        mAmPh_conj = np.conjugate(mAmPh)
    
        #----------------------------------------------------------------------
        # Put the complex matrix with amplitudes and phases of tones into
        # one matrix dedicated for IFFT
    
        # Recalculate the matrix with indices of frequencies in the spectrum
        # to real frequencies
        mFrqs = mFrqsInx*fRes
    
        # Recalculate the matrix with indices of frequencies in the spectrum
        # to indices of frequencies in the IFFT transform
        mIFFTFrqsInx = np.around(mFrqs/fFFTR).astype(int)
    
        # Allocate the vector for the ifft coefficients for all the signals
        # (one signal in one row)
        mIFFT = np.zeros((nSigs, nSmp)) + 1j*np.zeros((nSigs, nSmp))
    
        # Put the complex vector with tones values into the IFFT matrix
        for inxSig in np.arange(nSigs):
    
            # IFFT indices of tones for the current signal
            vInx = mIFFTFrqsInx[inxSig, :]
    
            # Put the tones for the current signal
            mIFFT[inxSig, vInx] = mAmPh[inxSig, :]
    
            # IFFT indices of conjugate tones for the current signal
            vInxConj = (nSmp - mIFFTFrqsInx[inxSig, :]).astype(int)
    
            # Put the conjugate tones for the current signal
            mIFFT[inxSig, vInxConj] = mAmPh_conj[inxSig, :]
    
        #----------------------------------------------------------------------
        # Generate the signals (perform the IFFT)
        mSig = np.fft.ifftn(mIFFT, axes=[1]).real
    
        return (mSig, mAmPh, mFrqs, fFFTR)
    
    
    # =================================================================
    # Adjust the signal power
    # =================================================================
    def _adjPower(self, mSig, iP, mAmps, mAmPh):
        """
        This function adjustes powers of the generated signals.
        If the requested power of the signals is equal to NaN or inf, then
        the signals are not adjusted.
    
        Args:
            mSig (matrix):   matrix with signals (one row - one signal)
            iP (float):      requested power of the signals
            mAmps (matrix):  matrix with amplitudes of tones in the signals
            mAmPh (matrix):  complex matrix with amplitudes/phases of tones
    
        Returns:
            mSig (matrix):   matrix with noisy signals
            vP (vector):     vector with powers of noisy signals
            vPCoef (vector): vector with coefficients which adjsuted the signals
            mAmps (matrix):  matrix with adjusted amplitudes of tones
            mAmPh (matrix):  complex matrix with adjusted amplitudes/phases
        """
    
        # Get the number of signals and the size of signals (the number of samples)
        (nSigs, nSmp) = mSig.shape
    
        # Measure the power of the signals
        vP = (np.sum(mSig * mSig, axis=1) / nSmp).reshape(nSigs, 1)
    
        # Adjust the signal power, if needed
        if not np.isnan(iP) or np.isinf(iP):
    
            # Compute power adjustments coefficients for the noise signals
            vPCoef = np.sqrt(iP / vP)
    
            # Adjust the signal power
            mPCoef = np.tile(vPCoef, (1, nSmp))
            mSig = mSig * mPCoef
    
            # Adjust the reported amplitudes of tones
            (_, nAmps) = mAmps.shape
            mPCoef = np.tile(vPCoef, (1, nAmps))
            mAmps = mAmps * mPCoef
            mAmPh = mAmPh * mPCoef
    
            # Measure the power of the adjusted signals
            vP = np.sum(mSig*mSig, axis=1) / nSmp
    
        else:
            # Power adjustment coefficients are equal to 1 (no adjustment)
            vPCoef = np.ones((nSigs, 1))
    
        return (mSig, vP, vPCoef, mAmps, mAmPh)
    
    
    # =================================================================
    # Add the AWGN noise to the signals
    # =================================================================
    def _addNoise(self, mSig, vP, iSNR):
        """
        This function adds noise to the generated signals.
        If the requested level of noise is equal to NaN or inf,
        then no noise is added.
    
    
        Args:
            mSig (matrix):   matrix with signals (one row - one signal)
            vP (vector):     vector with powers of signals
            iSNR (float):    wanted level of noise in the signals
    
        Returns:
            mSigNN (matrix): matrix with non noisy signals
            vPNN (vector):   vector with powers of non noisy signals
            mSig (matrix):   matrix with noisy signals
            vP (vector):     vector with powers of noisy signals
        """
    
        # Backup the non noisy signals
        mSigNN = mSig.copy()      # Matrix with signals
        vPNN = vP.copy()          # Power of non noisy signals
    
        # Add the noise, if needed
        if not (np.isnan(iSNR) or np.isinf(iSNR)):
    
            # Get the number of signals and the size of signals
            # (the number of samples)
            (nSigs, nSmp) = mSig.shape
    
            # Generate the noise
            mNoise = np.random.randn(nSigs, nSmp)
    
            # Measure the current powers of the noise signals
            vNoisePReal = (np.sum(mNoise*mNoise, axis=1) / nSmp).reshape(nSigs, 1)
    
            # Compute the requested noise power for every signal
            vNoiseP = (vP / (10**(iSNR/10))).reshape(nSigs, 1)
    
            # Compute power adjustments coefficients for the noise signals
            vPNoiseCoef = np.sqrt(vNoiseP / vNoisePReal)
    
            # Adjust the noise power
            mPNoiseCoef = np.tile(vPNoiseCoef, (1, nSmp))
            mNoise = mPNoiseCoef * mNoise
    
            # Add the noise to the signals
            mSig = mSig + mNoise
    
            # Measure the power of the signals
            vP = np.sum(mSig * mSig, axis=1) / nSmp
    
        return (mSigNN, vPNN, mSig, vP)
  
    