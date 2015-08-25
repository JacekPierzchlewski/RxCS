"""
This script is an example of how to use the L1 optimization reconstruction
module (regularized regression scheme). |br|

In this example 1000 signals is generated and processed.

Firstly, a multitone signal is generated. The signal model is as follows. 
There are two random tones randomly distributed in the spectrum 
from 11kHz to 20kHz and two random tones randomly distributed
in the spectrum from 31kHz to 40kHz.

                                                         o 
                  o                                      |
           o      |                                      |
           |      |                              o       |
           |      |                              |       |
           |      |                              |       | 
----11kHz<----------->20kHz------\\--------31kHz<----------->40kHz-->
                                                                     f [kHz]

The signal is nonuniformly sampled and reconstructed with L1 reconstrucion
module from the RxCS toolbox. The module perfroms the regularized regression
optimization scheme and uses the external 'cvxopt' toolbox. |br|

After the signal generation and sampling, the results are plot in both 
the time domain and the frequency domain for two randomly chosen signals. |br|

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0  | 25-AUG-2015 : * Version 1.0 released. |br|

*License*:
    BSD 2-Clause
"""

from __future__ import division
import numpy as np
import rxcs
import matplotlib.pyplot as plt


def _L1_recon_ex2():

    # ---------------------------------------------------------------------
    # Settings for the example
    # ---------------------------------------------------------------------

    # General settings:
    TIME = 1e-3     # time of the signal is 1 ms
    FSMP = 2e6      # signal representation sampling frequency 2MHz

    # Signals:
    NSIGS = int(1e4)  # the number of signals
    FDELTA = 1e3      # tone separation in both signals is 1kHz 

    FMIN1 =  11e3  # spectrum #1: 11kHz <-> 20kHz    
    FMAX1 =  20e3  # ^
    NTNS1 =  2     # the number of tones is in the spectrum (11kHz <-> 20kHz)
    FMIN2 =  31e3  # spectrum #2: 31kHz <-> 40kHz    
    FMAX2 =  40e3  # ^
    NTNS2 =  2     # the number of tones is 2 in the spectrum (31kHz <-> 40kHz)

    POWER = 1   # Power of the signal is 1 W

    # Sampler:
    GRIDT = 1e-6   # sampling grid period is 1 us
    FSAMP = 25e3   # the average sampling frequency is 25 kHz

    # Things on the board:
    gen1 = rxcs.sig.randMult()   # Signal generator #1 - for the 1st part of the spectrum
    gen2 = rxcs.sig.randMult()   # Signal generator #2 - for the 2nd part of the spectrum

    samp = rxcs.acq.nonuniANGIE()  # Sampler
    
    IDFT = rxcs.cs.dict.IDFT()       # IDFT dictionary generator
    makeTheta = rxcs.cs.makeTheta()  # Theta matrix generator 
    L1recon = rxcs.cs.cvxoptL1()     # L1 reconstruction

    analysisSNR = rxcs.ana.SNR()   # SNR analysis

    # ---------------------------------------------------------------------
    # Generate the original signals
    # ---------------------------------------------------------------------

    # Settings for the generator #1
    gen1.nSigs = NSIGS     # the number of signals to be generated
    gen1.tS = TIME         # time
    gen1.fR = FSMP         # sig. representation sampling frequency
    gen1.fRes = FDELTA     # tone separation
    gen1.fMin = FMIN1      # Spectrum #1
    gen1.fMax = FMAX1      # ^
    gen1.nTones = NTNS1    # ^
    gen1.iP = POWER/2      # power

    # Settings for the generator #2
    gen2.nSigs = NSIGS     # the number of signals to be generated
    gen2.tS = TIME         # time
    gen2.fR = FSMP         # sig. representation sampling frequency
    gen2.fRes = FDELTA     # tone separation
    gen2.fMin = FMIN2      # Spectrum #1
    gen2.fMax = FMAX2      # ^
    gen2.nTones = NTNS2    # ^
    gen2.iP = POWER/2      # power

    # ------------------------
    gen1.run()                    # run the generators
    gen2.run()                    # ^
    mSig = gen1.mSig + gen2.mSig  # the original signal  is a sum of the two generated signals
   
    # ---------------------------------------------------------------------
    # Sample the original signals
    # ---------------------------------------------------------------------
    
    # Settings for the sampler
    samp.tS = TIME        # time of the signal
    samp.fR = FSMP        # the signal representation sampling freuqnecy
    samp.Tg = GRIDT       # the sampling grid period
    samp.fSamp = FSAMP    # the average sampling frequency
    samp.tMin = 5e-6

    # ------------------------
    samp.mSig = mSig     # connect the original signal to the sampler 
    samp.run()           # run the sampler

    # -----------------------------------------------------------------
    # Generate the dictionary and the Theta matrices
    # -----------------------------------------------------------------

    # Generate the IDFT dictionaries:

    # dictionary #1
    IDFT.tS = TIME         # time of the dictionaries
    IDFT.fR = FSMP         # representation sampling frequency
    IDFT.fDelta = FDELTA   # the frequency separation between tones
    IDFT.fFirst = FMIN1    # minimum frequency in the dictionary
    IDFT.nTones = int((FMAX1 - FMIN1) / FDELTA)  # the number of tones
    IDFT.run()
    mDict1 = IDFT.mDict.copy()   # Take the dictionary matrix for the 1st part 
                                 # of the spectrum

    # dictionary #2
    IDFT.fFirst = FMIN2    # minimum frequency in the dictionary
    IDFT.nTones = int((FMAX2 - FMIN2) / FDELTA)  # the number of tones
    IDFT.run()
    mDict2 = IDFT.mDict.copy()   # Take the dictionary matrix for the 2nd part 
                                 # of the spectrum

    # Concatenate the dictionary matrices
    (nRows, _) = mDict1.shape                     # Cut down the dictionary matrix #1
    mDict1 = mDict1[np.arange(int(nRows/2)), :]   # ^   
    (nRows, _) = mDict2.shape                     # Cut down the dictionary matrix #2
    mDict2 = mDict2[np.arange(int(nRows/2)), :]   # ^
    mDict = np.vstack((mDict1, mDict2))      

    # Compute the Theta matrix    
    makeTheta.lPhi = samp.lPhi    # Add the observation matrix
    makeTheta.lDict = [mDict.T]   # Add the dictionary  
    makeTheta.run()

    # -----------------------------------------------------------------
    # Generate the dictionary
    # -----------------------------------------------------------------

    # Run the L1 minimization - generate signals coefficients
    L1recon.lTheta = makeTheta.lTheta   # add the Theta matrix
    L1recon.lObserved = samp.lObSig     # add the observed signals
    L1recon.iK = 0.1                    # add the 'k' parameter
    L1recon.bComplex = 1                # add info that the problem contains complex
                                        # numbers
    L1recon.run()  # Run the reconstruction

    # Reconstruct the signals using the found signal coefficients and the dictionary
    NSMP = gen1.nSmp           # The number of representation samples in the signals    
    mReconstructed = np.zeros((NSIGS, NSMP))
    for inxSig in np.arange(NSIGS):
        vCoeff = L1recon.lCoeff[inxSig]
        vSigRecon = np.dot(mDict.T, vCoeff)
        mReconstructed[inxSig, :] = vSigRecon.real
  
    # -----------------------------------------------------------------
    # Measure the SNR of the reconstruction
    # -----------------------------------------------------------------
    mSigNN = gen1.mSigNN + gen2.mSigNN  # the original reference (unnoisy signal)    
    analysisSNR.iSNRSuccess = 15
    analysisSNR.mSigRef = mSigNN        # nonnoisy signal from the generator is a a reference signal
    analysisSNR.mSig = mReconstructed   # reconstructed signals are signals under test
    analysisSNR.run()                   # run the reconstruction

    # ---------------------------------------------------------------------
    plot(gen1, gen2, samp, mSig, mReconstructed, NSIGS)
    plt.show(block=True)
    

def plot(gen1, gen2, samp, mSig, mReconstructed, NSIGS):
    """
    This function takes care of plotting the results.
    """

    # ---------------------------------------------------------------------
    # Plot the original signal, reconstructed signal and signal samples
    # in the time domain
    # ---------------------------------------------------------------------

    # ---------------------------------------------------------------------
    # Get the signals

    vT = gen1.vTSig       # Get the time vector for the signals
    fFFTR = gen1.fFFTR    # Get the FFT frequency resolution for signals
    
    # Draw random indices for signals
    vInx = np.random.permutation(NSIGS)[np.arange(2)]
    vInx.sort()
    iInx1 = vInx[0]
    iInx2 = vInx[1]

    vSig1 = mSig[iInx1, :]   # Get the original signal #1
    vSig2 = mSig[iInx2, :]   # Get the original signal #2

    vObSig1 = samp.lObSig[iInx1]   # The observed signal # 1
    vObSig2 = samp.lObSig[iInx2]   # The observed signal # 2
    
    mPhi1 = samp.lPhi[iInx1]       # The observation matrix #1
    mPhi2 = samp.lPhi[iInx2]       # The observation matrix #2

    vSigRecon1 = mReconstructed[iInx1, :]  # The reconstructed signal #1
    vSigRecon2 = mReconstructed[iInx2, :]  # The reconstructed signal #2

    # ---------------------------------------------------------------------
     
    # Plot the original, observed and reconstructed signals
    plotOrigObRecon(vT, vSig1, np.dot(mPhi1, vT), vObSig1, vSigRecon1, fFFTR, 1, iInx1)
    plotOrigObRecon(vT, vSig2, np.dot(mPhi2, vT), vObSig2, vSigRecon2, fFFTR, 2, iInx2)
    
    return

def plotOrigObRecon(vT, vSig, vTObSig, vObSig, vSigRecon, fFFTR, inxFig, inxSig):
    """
    This function plots chosen orignal and reconstructed signals 
    in the time and frequency domain.
    """    
    
    hFig = plt.figure(inxFig)
    
    # ---------------------------------------------------------------------
    # Plot the original signal and the reconstructed signal 
    # in the time domain
    # ---------------------------------------------------------------------
    hSubPlot1 = hFig.add_subplot(211)
    hSubPlot1.plot(vT, vSig, 'g-', label="original sig")
    hSubPlot1.plot(vT, vSigRecon, 'b--', label="reconstructed sig")
    hSubPlot1.plot(vTObSig, vObSig, '*r', label="observed samps", markersize=10)
    hSubPlot1.set_xlabel('Time [s]')
    hSubPlot1.grid(True)
    hSubPlot1.legend(loc="best")
    strTitle = 'Signal #%d' % inxSig
    hSubPlot1.set_title(strTitle)

    # ---------------------------------------------------------------------
    # Plot the original signal and the reconstructed signal 
    # in the frequency domain
    # ---------------------------------------------------------------------

    # ---------------------------------------------------------------------
    # Compute representation of signals in the frequency domain
    vFFT = np.fft.fft(vSig)   # Analyze the spectrum of the orignal signal
    iS = vFFT.size            # Get the size of the spectrum
    vFFTa = 2 * np.abs(vFFT[np.arange(iS / 2).astype(int)]) / iS  # Get the amplitudes of the signal
                                                                  # for half of the spectrum
    
    # Reconstructed signal
    vFFTR = np.fft.fft(vSigRecon)   # Analyze the spectrum of the reconstructed signal
    iS = vFFT.size                  # Get the size of the spectrum
    vFFTRa = 2 * np.abs(vFFTR[np.arange(iS / 2).astype(int)]) / iS  # Get the amps
    
    # Create a vector with frequencies of the signal spectrum
    vF = fFFTR * np.arange(iS / 2)

    # ---------------------------------------------------------------------
    # Plot in the frequency domain
    hSubPlot2 = hFig.add_subplot(212)
    
    # Original signal
    (mo, so, _) = hSubPlot2.stem(vF, vFFTa,  markerfmt='o', basefmt='g-', label="original signal")
    plt.setp(so, color='g', linewidth=2.0)
    plt.setp(mo, color='g', markersize=10.0)
 
    # Reconstructed signal
    (mr, sr, _) = hSubPlot2.stem(vF, vFFTRa, markerfmt='x', basefmt='b-', label="reconstructed signal")
    plt.setp(sr, color='b', linewidth=2.0)
    plt.setp(mr, color='b', markersize=10.0)

    hSubPlot2.grid(True)
    hSubPlot2.set_xlabel('Frequency [Hz]')
    hSubPlot2.set_xlim(-1*1e3, 51*1e3)
    hSubPlot2.set_ylim(-0.1, 3.1)
    hSubPlot2.legend(loc="best")
    return


# =====================================================================
# Trigger when start as a script
# =====================================================================
if __name__ == '__main__':
    _L1_recon_ex2()
