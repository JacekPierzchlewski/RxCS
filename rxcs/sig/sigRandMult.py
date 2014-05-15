#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#% sigRandMult: THE "AnSpar" PACKAGE - MULTITONE SIGNAL GENERATOR
#%                                     File version 1.0r1 (28th March 2011)
#%
#% Function generates multitone signal.
#% "1 tone" is a cosine function.
#% ------------------------------------------------------------------------
#% Input:
#%       1. sSigConf: Signal generator configuration structure
#%       2. sVerbConf: Verbose configuraion strucuture
#%
#% --------------------------------
#% Configuration fields needed:
#% sSigConf:
#%               .strType:   "RandMult"
#%               .randmult:  <- this module configuration substructure.
#%
#% sSigConf.randmult:
#%
#%               .fSmpRepFrq: signal representation sampling frequency
#%               .tSigTime:   signal time due
#%               .iSNR:       signal to noise ratio
#%
#%               .fSpecMax:   maximum frequency in the signal spectrum
#%               .fSpecRes:   resolution frequency in the signal spectrum
#%
#%               .vFrqs:      given frequencies vector
#%               .vAmps:      amplitudes for given frequencies
#%               .vPhs:       phases for given frequencies
#%
#%               .nTones:    Number of additional random tones in the signal
#%                           (not described in the vFrqs/vAmps/vPhs vectors)
#%
#%               .iMinAmp:   Minimum aplitude for tones with random value
#%               .iStpAmp:   Resolution of the random amplitude value
#%               .iMaxAmp:   Maximum aplitude for tones with random value
#%
#%               .iMinPhs:   Minimum phase for tones with random value
#%               .iStpPhs:   Resolution of the random phase value
#%               .iMaxPhs:   Maximum phase for tones with random value
#%
#% --------------------------------
#% Struture returned by the generator:
#% .sSig:
#%               .vSig:      vector with the signal
#%               .vSigNN:    vector with the original, non noisy signal
#%               .vTSig:     time vector for the signal
#%
#%               .fRS:       signal representation sampling frequency
#%               .tST:       signal time
#%               .nSmp:      the number of smaples in the signal
#%               .iSNR:      signal to noise ratio
#%
#%               .vFrqs:     vector with frequencies of tones
#%               .vAmps:     vector with amplitudes of tones
#%               .vPhs:      vector with phases of tones
#%               .vAmPh:     complex vector with amplitudes/phases of tones
#%               .fNq:       the signal Nyquist frequency
#%
#% ------------------------------------------------------------------------
#% Copyright (c) 2010 - 2011 Jacek Pierzchlewski, (AAU TPS)
#%                           AALBORG UNIVERSITY, Denmark
#%                           Technology Platforms Section (AAU TPS)
#%                           Email:    jap@es.aau.dk (Jacek)
#%
#%                           Comments and bug reports are very welcome!
#%
#% Licensing: This software is published under the terms of the:
#%            GNU GENERAL PUBLIC LICENSE, Version 3, 29th June 2007
#%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
from __future__ import division
import numpy as np
import sys
import rxcs
from sys import stdout

def main(dSigConf):

    # The name of the function (for error purposes)
    strFunc = 'sigRandMult.main'

    # =================================================================
    # Get the given data
    # =================================================================

    # -----------------------------------------------------------------
    # Get the number of signals to be generated
    nSigs = int(round(dSigConf['nSigPack']))

    # -----------------------------------------------------------------
    # Mute the output parameters:
    if not 'bMute' in dSigConf:
        bMute = 0
    else:
        bMute = dSigConf['bMute']

    # -----------------------------------------------------------------
    # Signal time parameters:

    # The time of the signal [s]
    # If not given, it is an error
    strErr = ('The time of the signal [s] (tS) ')
    strErr = strErr + ('is not given in the configuration!')
    if not 'tS' in dSigConf:
        rxcs.console.cerror(strFunc, strErr)
    tS = dSigConf['tS']

    # The signal representation sampling freuqency [Hz]
    # If not given, it is an error
    strErr = ('The signal representation sampling freuqency [Hz] (fR) ')
    strErr = strErr + ('is not given in the configuration!')
    if not 'fR' in dSigConf:
        rxcs.console.cerror(strFunc, strErr)
    fR = dSigConf['fR']

    # -----------------------------------------------------------------
    # Signal noise
    if 'iSNR' in dSigConf:
        iSNR = dSigConf['iSNR']
    else:
        iSNR = np.inf

    # -----------------------------------------------------------------
    # Get the requested power of signals
    if 'iP' in dSigConf:
        iP = dSigConf['iP']
    else:
        iP = np.nan

    # -----------------------------------------------------------------
    # Signal spectrum parameters

    # The highest possible frequency in the signal [Hz]
    # If not given, it is an error
    strErr = ('The highest possible frequency in the signal [Hz] (fMax) ')
    strErr = strErr + ('is not given in the configuration!')
    if not 'fMax' in dSigConf:
        rxcs.console.cerror(strFunc, strErr)
    fMax = dSigConf['fMax']

    # Signal spectrum resolution [Hz]
    # If not given, it is an error
    strErr = ('Signal spectrum resolution [Hz] (fRes) ')
    strErr = strErr + ('is not given in the configuration!')
    if not 'fRes' in dSigConf:
        rxcs.console.cerror(strFunc, strErr)
    fRes = dSigConf['fRes']

    # - - - - - - - - - - - - - - - - - - -
    # Get the vectors with signal cosine tones content

    # Get the vector with given frequencies of signal cosine tones content
    # (if this vector exists)
    if 'vFrqs' in dSigConf:
        vFrqs = dSigConf['vFrqs']
    else:
        vFrqs = np.zeros(0)

    # Create the vector with given and specified frequencies (not np.nan)
    vFrqs_ = vFrqs[np.isnan(vFrqs) == False]

    # Get the vector with given amplitudes of signal cosine tones content
    # (if this vector exists)
    if 'vAmps' in dSigConf:
        vAmps = dSigConf['vAmps']
    else:
        vAmps = np.zeros(0)

    # Get the vector with given phases of signal cosine tones content
    # (if this vector exists)
    if 'vPhs' in dSigConf:
        vPhs = dSigConf['vPhs']
    else:
        vPhs = np.zeros(0)

    # - - - - - - - - - - - - - - - - - - -
    # Get the number of additional tones
    # (if the number exists)
    if 'nTones' in dSigConf:
        nTones = int(round(dSigConf['nTones']))
    else:
        nTones = 0

    # - - - - - - - - - - - - - - - - - - -
    # Get the boundaries for amplitudes

    # Amplitude min value
    if 'iMinAmp' in dSigConf:
        iMinAmp = dSigConf['iMinAmp']
    else:
        iMinAmp = 0

    # Amplitude gradation
    if 'iGraAmp' in dSigConf:
        iGraAmp = dSigConf['iGraAmp']
    else:
        iGraAmp = 0.1

    # Amplitude max value
    if 'iMaxAmp' in dSigConf:
        iMaxAmp = dSigConf['iMaxAmp']
    else:
        iMaxAmp = 0

    # - - - - - - - - - - - - - - - - - - -
    # Get the boundaries for phases

    # Phase min value
    if 'iMinPhs' in dSigConf:
        iMinPhs = dSigConf['iMinPhs']
    else:
        iMinPhs = 0

    # Phase gradation
    if 'iGraPhs' in dSigConf:
        iGraPhs = dSigConf['iGraPhs']
    else:
        iGraPhs = 0.1

    # Phase max value
    if 'iMaxPhs' in dSigConf:
        iMaxPhs = dSigConf['iMaxPhs']
    else:
        iMaxPhs = 0

    # =================================================================
    # Perform some precomputations
    # =================================================================

    # Calculate the number of given frequencies
    nFG = vFrqs.size

    # Calculate the number of given amplitudes
    nAG = vAmps.size

    # Calculate the number of given phases
    nPG = vPhs.size

    # - - - - - - - - - - - - - - - - - - -

    # Calculate the number of samples in the signal
    nSmp = int(round(tS*fR))

    # Calculate the FFT frequency resolution
    fFFTR = fR/nSmp

    # - - - - - - - - - - - - - - - - - - -

    # The number of tones in the maximum possible signal spectrum
    nSpectTones = int(fMax/fRes)

    # The total number of tones in the signal
    nSigTones = nFG + nTones

    # Signal sparsity
    iSpar = 1- nSigTones/nSpectTones

    # - - - - - - - - - - - - - - - - - - -

    # =================================================================
    # Check the configuration
    # =================================================================

    # Check the Nyquist vs. highest possible frequency
    strErr = 'The representation sampling frequency is to low!'
    if fR <= 2*fMax:
        rxcs.console.cerror(strFunc, strErr)

    # - - - - - - - - - - - - - - - - - - -
    # Check the highest possible frequency in the signal vs spectrum resolution
    strErr = 'The highest possible frequency in the signal is not a multiple '
    strErr = strErr + 'of the signal spectrum resolution'
    if (round(fMax/fRes) - fMax/fRes) > 1e-15:
        rxcs.console.cerror(strFunc, strErr)

    # - - - - - - - - - - - - - - - - - - -
    # Check if there is a space for all the frequencies requested in the signal
    strErr = 'The signal spectrum consists of %d tones. ' % (nSpectTones)
    strErr = strErr + 'I can not put there %d [vFrqs] + %d [nTones] tones' \
        % (nFG,nTones)
    if nSpectTones < nSigTones:
        rxcs.console.cerror(strFunc, strErr)

    # - - - - - - - - - - - - - - - - - - -

    # Check the vector with given frequencies, if it is longer then 0
    if nFG > 0:

        # 1. resolution:
        if np.abs(np.sum(np.round(vFrqs_/fRes) - (vFrqs_/fRes))) > 1e-15:
            strErr = ('A frequency given in the vFrqs vector is ')
            strErr = strErr + ('incoherent with the resolution of signal ')
            strErr = strErr + ('spectrum!\n')
            rxcs.console.cerror(strFunc, strErr)

        # Correct possible representation errors in the vector with frequencies
        vFrqs = np.round(vFrqs/fRes)*fRes

        # 2. max frequency:
        if max(vFrqs) > fMax:
            strErr = ('The highest frequency in vFrqs vector is higher than ')
            strErr = strErr + ('the highest possible in the signal spectrum!')
            rxcs.console.cerror(strFunc, strErr)

        # 3. Repeated frequency
        # Check if there is any frequency repeated in the
        # vector with given frequencies (vFrqs)
        # (only if the vector is longer than 1)
        if nFG > 1:
            vFrqsUnique = np.unique(vFrqs)

            if (vFrqsUnique.size != vFrqs.size):
                strErr = ('There are frequencies repeated in ')
                strErr = strErr + ('the vFrqs vector!')
                rxcs.console.cerror(strFunc, strErr)

        # 4. All the frequencies higher than 0
        vFrqsLowerOrEqualZero = vFrqs[vFrqs <= 0]
        if vFrqsLowerOrEqualZero.size > 0:
            strErr = ('Frequencies in the vFrqs vector must be higher than 0!')
            rxcs.console.cerror(strFunc, strErr)

    # Check the vector with given frequencies is equal to
    # the vector with given amplitudes
    # and the vector with given phases
    if not ((nFG == nAG) and (nFG == nPG)):

        strErr = ('Size of the vector with given frequencies (vFrqs) must ')
        strErr = strErr + ('be equal to size of the vectors vAmps and vPhs')
        rxcs.console.cerror(strFunc, strErr)

    # - - - - - - - - - - - - - - - - - - -
    # Check the vector with given amplitudes, if it is longer then 0
    if nAG > 0:

        # 1. All the amplitudes higher than 0
        vAmpsLowerOrEqualZero = vAmps[vAmps <= 0]
        if vAmpsLowerOrEqualZero.size > 0:
            strErr = ('Amplitudes in the vAmps vector must be higher than 0!')
            rxcs.console.cerror(strFunc, strErr)

    # - - - - - - - - - - - - - - - - - - -
    # Check the vector with given phases, if it is longer then 0
    if nPG > 0:

        # 1. All the phases must be higher than -180
        vPhsLowerOrEqualMin180 = vPhs[vPhs <= -180]
        if vPhsLowerOrEqualMin180.size > 0:
            strErr = ('Phases in the vPhs vector must be higher than -180!')
            rxcs.console.cerror(strFunc, strErr)

        # 2. All the phases must be lower than 180
        vPhsHigher180 = vPhs[vPhs > 180]
        if vPhsHigher180.size > 0:
            strErr = ('Phases in the vPhs vector must be lower than 180!')
            rxcs.console.cerror(strFunc, strErr)

    # - - - - - - - - - - - - - - - - - - -
    # The number of additional tones can not be lower than 0
    if (nTones < 0):

        strErr = ('The number of additional tones can not be lower')
        strErr = strErr + (' than 0')
        rxcs.console.cerror(strFunc, strErr)

    # - - - - - - - - - - - - - - - - - - -
    # Check if the given amplitudes boundaries make sense

    # 1. min amplitude vs. max amplitude
    if iMinAmp > iMaxAmp:
        strErr = ('Minimum possible amplitude can not be greater ')
        strErr = strErr + ('than the maximum possible amplitude!')
        rxcs.console.cerror(strFunc, strErr)

    # 2. amplitude gradation
    if iGraAmp <= 0:
        strErr = ('Amplitude gradation must be higher than zero!')
        rxcs.console.cerror(strFunc, strErr)

    # 3. Min amplitude and max amplitude must be higher than 0
    if iMinAmp < 0:
        strErr = ('Minimum amplitude must be higher than zero!')
        rxcs.console.cerror(strFunc, strErr)
    if iMaxAmp < 0:
        strErr = ('Maximum amplitude must be higher than zero!')
        rxcs.console.cerror(strFunc, strErr)

    # - - - - - - - - - - - - - - - - - - -
    # Check if the given phase boundaries make sense

    # 1. min phase vs. max phase
    if iMinPhs > iMaxPhs:
        strErr = ('Minimum possible phase can not be greater than ')
        strErr = strErr + ('the maximum possible phase!')
        rxcs.console.cerror(strFunc, strErr)

    # 2. phase gradation
    if iGraPhs <= 0:
        strErr = ('Phase gradation must be higher than zero!')
        rxcs.console.cerror(strFunc, strErr)

    # 3. Min phase and max phase must be higher than -180 and lower than + 180
    if iMinPhs <= -180:
        strErr = ('Minimum phase must be higher than -180!')
        rxcs.console.cerror(strFunc, strErr)
    if iMinPhs > 180:
        strErr = ('Minimum phase must be lower than 180!')
        rxcs.console.cerror(strFunc, strErr)
    if iMaxPhs <= -180:
        strErr = ('Maximum phase must be higher than -180!')
        rxcs.console.cerror(strFunc, strErr)
    if iMaxPhs > 180:
        strErr = ('Maximum phase must be lower than 180!')
        rxcs.console.cerror(strFunc, strErr)

    # - - - - - - - - - - - - - - - - - - -
    # Check the number of signals to be generated
    if (nSigs < 1):
        strErr = ('The number of signals to be generated must ')
        strErr = strErr + ('be higher than one!')
        rxcs.console.cerror(strFunc, strErr)

    # - - - - - - - - - - - - - - - - - - -
    # Check if there is a frequency leackage
    if abs(round(fRes/fFFTR) - fRes/fFFTR) > 0:
        strErr = ('Frequency leackage! Signal spectrum resolution can not be ')
        strErr = strErr + ('represented with the current signal parameters!')
        rxcs.console.cerror(strFunc, strErr)

    #----------------------------------------------------------------------

    # =================================================================
    # Print the signal parameters to the console
    # =================================================================

    if bMute == 0:

        # Print out the header of the signal generator
        rxcs.console.progress('Signal generator','Random multitone')

        # Time parameters
        rxcs.console.bullet_param('signal time',tS,'-m','seconds')
        rxcs.console.param('representation sampling frequency',
                                fR,'-M','MHz')
        rxcs.console.param('the number of samples',nSmp,'-','samples')

        # Frequency parameters
        rxcs.console.bullet_param('the highest possible freq. in the signal',
                                fMax,'-k','Hz')
        rxcs.console.param('signal spectrum resolution',fRes,'k','Hz')
        rxcs.console.param('the number of tones in the max possible spectrum',
                        nSpectTones,'-','')
        rxcs.console.param('the total number of tones in the signal',
                        nSigTones,'-','')
        rxcs.console.param('the signal sparsity',
                        iSpar,' ','')

        # Frequency content
        rxcs.console.bullet_param('the number of given frequencies',
                                nFG,'-','')

        rxcs.console.bullet_param('the number of additional tones',
                                nTones,'-','')

        rxcs.console.param('minimum amplitude',iMinAmp,' ','')
        rxcs.console.param('amplitude gradation',iGraAmp,' ','')
        rxcs.console.param('maximum amplitude',iMaxAmp,' ','')

        rxcs.console.param('minimum phase',iMinPhs,' ','')
        rxcs.console.param('amplitude phase',iGraPhs,' ','')
        rxcs.console.param('maximum phase',iMaxPhs,' ','')

        # Noise
        if np.isinf(iSNR) or np.isnan(iSNR):
            rxcs.console.bullet_info('noise',
                                     'not added to the signal (SNR=inf)')
        else:
            rxcs.console.bullet_param('noise (SNR)',iSNR,'-','dB')

        # Signal power
        if np.isinf(iP) or np.isnan(iP):
            rxcs.console.bullet_info('signal power','not adjusted')
        else:
            rxcs.console.bullet_param('signal power',iP,'-','W')

        # The number of signals
        rxcs.console.bullet_param('the number of signals to be generated',
                                nSigs,'-','signals')

        # Information about the computations start
        tStart = rxcs.console.module_progress('signal generation starts!!!')

    # =================================================================
    # Draw frequencies for all the signals
    # =================================================================

    #----------------------------------------------------------------------
    # Recalculate frequencies to indices of tones in the spectrum

    # Recalculate the vector with frequencies from frequency to index
    # of a frequency in the spectrum
    vFrqsInx = (vFrqs / fRes)

    # Create a vector with GIVEN (not nan) indices of frequencies in the
    # vFrqs vector
    vFrqsInx_ =(vFrqsInx[np.isnan(vFrqsInx) == False]).astype(int)

    #----------------------------------------------------------------------
    # Create the vector with indices of avaialble frequencies in the spectrum

    # Create a vector with inidces of all the tones in the spectrum
    vSpecInx = np.arange(1,nSpectTones+1)

    # Boolean vector which indicates if the frequency is free
    vFreqIsFree = np.ones(nSpectTones).astype(bool)
    vFreqIsFree[vFrqsInx_-1] = False

    # Create the vector with indices of available frequencies
    vAvailFreqsInx = vSpecInx[vFreqIsFree]

    #----------------------------------------------------------------------
    # Construct a vector with indices of frequencies for all the needed signals

    # Add unknown frequencies of the additional tones to the vFrqsInx vector
    vFrqsInx = np.concatenate((vFrqsInx,np.nan*np.zeros(nTones)))

    # Calculate the number of missing frequencies in the vector with
    # frequencies
    iMissF = len(vFrqsInx) - len(vFrqsInx_)

    # Construct a matrix with indices of frequencies for all the needed signals
    mFrqsInx = np.tile(vFrqsInx,(nSigs,1))

    #----------------------------------------------------------------------

    # Draw the frequencies
    for inxSig in np.arange(nSigs):

      # Permute all the indices of frequencies in the spectrum
      vPermutedFreqsInx = ((np.random.permutation(vAvailFreqsInx)).T)

      # From the permuted indices of frequencices take as many as it is missing
      vTakenFreqsInx = vPermutedFreqsInx[np.arange(iMissF)]

      # Put the taken indices of frequencies to the matrix with frequency
      # indices for all the signals
      mFrqsInx[inxSig,np.isnan(mFrqsInx[inxSig,:])] = vTakenFreqsInx

    # =================================================================
    # Draw amplitudes of the signals
    # =================================================================

    # Add unknown amplitudes of the additional tones to the vAmps vector
    vAmps = np.concatenate((vAmps,np.nan*np.zeros(nTones)))

    # Compute the number of missing amplitudes for every signal
    iMissA = (vAmps[np.isnan(vAmps)]).size

    #----------------------------------------------------------------------

    # Compute the number of possible amplitude values
    nAmpVal = np.floor((iMaxAmp - iMinAmp)/iGraAmp) + 1

    #----------------------------------------------------------------------

    # Draw the missing amplitudes for all the signals
    vDrawAmps = \
        iMinAmp + iGraAmp*(np.random.randint(0, nAmpVal, (nSigs*iMissA)))

    # Construct a matrix with amplitudes of tones for all the needed signals
    mAmps = np.tile(vAmps,(nSigs,1))

    # Put the draw amplitudes to the matrix with amplitudes of tones for
    # all the needed signals
    mAmps[np.isnan(mAmps)] = vDrawAmps

    # =================================================================
    # Draw phases of the signals
    # =================================================================

    # Add unknown phases of the additional tones to the vAmps vector
    vPhs = np.concatenate((vPhs,np.nan*np.zeros(nTones)))

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
    mPhs = np.tile(vPhs,(nSigs,1))

    # Put the draw phases to the matrix with phases of tones for
    # all the needed signals
    mPhs[np.isnan(mPhs)] = vDrawPhs

    # =================================================================
    # Generate the signals by IFFT
    # =================================================================

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
        vInx = mIFFTFrqsInx[inxSig,:]

        # Put the tones for the current signal
        mIFFT[inxSig, vInx]  = mAmPh[inxSig,:]

        # IFFT indices of conjugate tones for the current signal
        vInxConj = (nSmp - mIFFTFrqsInx[inxSig,:]).astype(int)

        # Put the conjugate tones for the current signal
        mIFFT[inxSig, vInxConj] = mAmPh_conj[inxSig,:]

    #----------------------------------------------------------------------
    # Generate the signals (perform the IFFT)
    mSig = np.fft.ifftn(mIFFT,axes=[1]).real

    # =================================================================
    # Adjust the signal power
    # =================================================================

    # Measure the power of the signals
    vP = (np.sum(mSig*mSig,axis=1) / nSmp).reshape(nSigs,1)

    # Adjust the signal power, if needed
    if not np.isnan(iP) or np.isinf(iP):

        # Compute power adjustments coefficients for the noise signals
        vPCoef = np.sqrt(iP/vP)

        # Adjust the signal power
        mPCoef = np.tile(vPCoef,(1,nSmp))
        mSig = mSig * mPCoef

        # Adjust the reported amplitudes of tones
        (_,nAmps) = mAmps.shape
        mPCoef = np.tile(vPCoef,(1,nAmps))
        mAmps = mAmps * mPCoef
        mAmPh = mAmPh * mPCoef

        # Measure the power of the adjusted signals
        vP = np.sum(mSig*mSig,axis=1) / nSmp

    else:
        # Power adjustment coefficients are 1 (no adjustment)
        vPCoef = np.ones((nSigs,1))

    # =================================================================
    # Add the AWGN noise to the signals
    # =================================================================

    # Backup the non noisy signals
    mSigNN = mSig.copy()      # Matrix with signals
    vPNN = vP.copy()          # Power of non noisy signals

    # Add the noise, if needed
    if not (np.isnan(iSNR) or np.isinf(iSNR)):

        # Generate the noise
        mNoise = np.random.randn(nSigs, nSmp)

        # Measure the current powers of the noise signals
        vNoisePReal = (np.sum(mNoise*mNoise,axis=1) / nSmp).reshape(nSigs,1)

        # Compute the requested noise power for every signal
        vNoiseP = (vP/(10**(iSNR/10))).reshape(nSigs,1)

        # Compute power adjustments coefficients for the noise signals
        vPNoiseCoef = np.sqrt(vNoiseP/vNoisePReal)

        # Adjust the noise power
        mPNoiseCoef = np.tile(vPNoiseCoef,(1,nSmp))
        mNoise = mPNoiseCoef * mNoise

        # Add the noise to the signals
        mSig = mSig + mNoise

        # Measure the power of the signals
        vP = np.sum(mSig*mSig,axis=1) / nSmp

    # =================================================================
    # Generate the output dictionary
    # =================================================================

    # Start the output dictionary
    dSig = {}

    # - - - - - - - - - - - - - - - - - - -
    dSig['mSig'] = mSig       # Matrix with output signals
    dSig['mSigNN'] = mSigNN   # Matrix with nonnoisy output signals

    dSig['nSigs'] = nSigs     # The number of generated signals

    # - - - - - - - - - - - - - - - - - - -

    dSig['fR'] = fR      # Signal representation sampling frequency
    dSig['tS'] = tS      # The time of the signals [s]
    dSig['nSmp'] = nSmp  # The number of samples in the signals

    # Generate the time vector for the signal
    vTSig = np.arange(1,nSmp+1) / fR
    dSig['vTSig'] = vTSig  # The time vector for the generated signals

    # - - - - - - - - - - - - - - - - - - -

    dSig['iSNR'] = iSNR     # Signal 2 noise ratio

    # - - - - - - - - - - - - - - - - - - -

    dSig['iP'] = iP           # Requested power of the signals
    dSig['vP'] = vP           # Power of the signals
    dSig['vPNN'] = vPNN       # Power of the non noisy signals
    dSig['vPCoef'] = vPCoef   # Power adjustment coefficients

    # - - - - - - - - - - - - - - - - - - -

    dSig['mFrqs'] = mFrqs     # Frequencies of tones in the signals
    dSig['mAmps'] = mAmps     # Amplitudes of tones in the signals
    dSig['mPhs'] = mPhs       # Phases of tones in the signals

    dSig['mAmPh'] = mAmPh     # Amp/Phases tones complex vector

    dSig['fFFTR'] = fFFTR     # Signal FFT frequency resolution

    # =================================================================
    # Signal generation is done!
    # =================================================================
    if bMute == 0:
        rxcs.console.module_progress_done(tStart)

    return dSig

