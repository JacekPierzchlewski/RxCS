"""
This script is an example of how to use the L1 optimization reconstruction
module (regularized regression scheme). |br|

In this example an IDFT dictionary is generated.
Then, a 2 tone signal is generated using the dictionary. |br|

The signal is nonuniformly sampled and reconstructed with L1 reconstrucion
module from the RxCS toolbox. The module perfroms the regularized regression
optimization scheme and uses the external 'cvxopt' toolbox. |br|

After the signal generation and sampling, the original signal, the observed
samples, and the reconstructed signal are plot in the time domain. |br|

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0  | 18-SEP-2014 : * Version 1.0 released. |br|

*License*:
    BSD 2-Clause
"""

from __future__ import division
import numpy as np
import rxcs
from cvxopt import matrix
import matplotlib.pyplot as plt


def _L1_recon_ex3():

    # ---------------------------------------------------------------------
    # Settings for the example
    # ---------------------------------------------------------------------
    iT = 1e-3       # Time of the signal [s]
    fD = 1e3        # Tone separation [Hz]
    fRS = 2e6       # Signal representation sampling frequency

    # -----------------------------------------------------------------
    # Generate the signal
    # -----------------------------------------------------------------

    # First part of the spectrum
    dSigConf1 = {}
    dSigConf1['tS'] = iT        # Time of the signal
    dSigConf1['fR'] = fRS       # The signal representation sampling frequency
    dSigConf1['fMin'] = 11e3     # The lowest possible frequency in the signal
    dSigConf1['fMax'] = 20e3    # The highest possible frequency in the signal
    dSigConf1['fRes'] = fD      # The signal spectrum resolution is 1 kHz
    dSigConf1['nTones'] = 2     # The number of tones in the signal
    dSigConf1['nSigPack'] = 1   # The number of signals to be generated
    dSigConf1['iSNR'] = 20      # The number of signals to be generated    
    dSig1 = rxcs.sig.sigRandMult.main(dSigConf1)

    # Second part of the spectrum
    dSigConf2 = {}
    dSigConf2['tS'] = iT        # Time of the signal
    dSigConf2['fR'] = fRS       # The signal representation sampling frequency
    dSigConf2['fMin'] = 31e3     # The lowest possible frequency in the signal
    dSigConf2['fMax'] = 40e3    # The highest possible frequency in the signal
    dSigConf2['fRes'] = fD      # The signal spectrum resolution is 1 kHz
    dSigConf2['nTones'] = 2     # The number of tones in the signal
    dSigConf2['nSigPack'] = 1   # The number of signals to be generated
    dSigConf2['iSNR'] = 20      # The number of signals to be generated    
    dSig2 = rxcs.sig.sigRandMult.main(dSigConf2)

    # Add the signals
    mSig = dSig1['mSig'] + dSig2['mSig']
    dSig = dSig1.copy()
    dSig['mSigNN'] = mSig.copy()
    dSig['mSig'] = mSig.copy()
    
    # -----------------------------------------------------------------
    # Sample the signal
    # -----------------------------------------------------------------

    # Generate settings for the sampler
    dAcqConf = {}
    dAcqConf['Tg'] = 1e-6     # The sampling grid period
    dAcqConf['fSamp'] = 20e3   # The average sampling frequency
    dObSig = rxcs.acq.nonuniANGIE.main(dAcqConf, dSig)

    # Take the observed signal and the observation matrix
    vObSig = dObSig['mObSig'][0,:]
    mPhi = dObSig['m3Phi'][0,:,:]
    
    # -----------------------------------------------------------------
    # Reconstruct the signal
    # -----------------------------------------------------------------

    # Generate the IDFT dictionary
    
    # Dictionary which covers 1st part of the spectrum
    dCSConf1 = {}
    dCSConf1['tS'] = iT            # Time of the dictionary
    dCSConf1['fR'] = fRS           # The signal representation sampling freq.
    dCSConf1['fFirst'] = 11e3      # First frequency in the dictionary
    dCSConf1['fDelta'] = fD        # The frequency separation between tones
    dCSConf1['nTones'] = 10        # The number of tones in the dictionary
    (mDict1, _) = rxcs.cs.dict.IDFToNoDC.main(dCSConf1)
    
    dCSConf2 = {}
    dCSConf2['tS'] = iT            # Time of the dictionary
    dCSConf2['fR'] = fRS           # The signal representation sampling freq.
    dCSConf2['fFirst'] = 31e3      # First frequency in the dictionary
    dCSConf2['fDelta'] = fD        # The frequency separation between tones
    dCSConf2['nTones'] = 10        # The number of tones in the dictionary
    (mDict2, _) = rxcs.cs.dict.IDFToNoDC.main(dCSConf2)

    # Concatenate the dictonaries
    mDict = np.vstack((mDict1, mDict2))

    # Compute the Theta matrix
    mTheta = np.dot(mPhi, mDict.T)

    # Run the L1 minimization - generate signal coefficients
    dCS = {}                  # Initialize the dictionary
    dCS['m3Theta'] = mTheta   # Add the Theta matrix
    dCS['iK'] = 0.1          # Add the 'k' parameter
    dCS['mObSig'] = vObSig    # Add observed signal
    dCS['bComplex'] = 1       # Add info that the problem contains complex
                              # numbers
    mCoeff = rxcs.cs.cvxoptL1.main(dCS)
    vCoeff = mCoeff[:, 0]
    
    # Reconstruct the signal using the found signal coefficients and the
    # dictionary
    vSigRecon = np.dot(mDict.T, vCoeff)
    vSigRecon = vSigRecon.real

    # -----------------------------------------------------------------
    # Measure the SNR of the reconstruction
    # -----------------------------------------------------------------
     
    # Put the reconstructed signal into a 2D matrix, and put the matrix into
    # a dictionary
    vSigReconM = vSigRecon.copy()
    vSigReconM.shape = (vSigReconM.size, 1)
    dSigRecon = {}
    dSigRecon['mSig'] = vSigReconM.T 
     
    # Create a dictionary with configuration for the system analysis
    dAnaConf = {}
    dAnaConf['iSNRSuccess'] = 15  # SNR of the recon > 15dB == success
    dAna = rxcs.ana.SNR.main(dSig, dSigRecon, {}, dAnaConf)

    # ---------------------------------------------------------------------
    # Plot the original signal, reconstructed signal and signal samples in the 
    # time domain
    # ---------------------------------------------------------------------

    # Get the generated signal
    vSig = mSig[0, :]

    # Get the signal time vector from the dictionary data
    vTs = dSig1['vTSig']

    # Plot the figure
    hFig1 = plt.figure(1)
    hSubPlot1 = hFig1.add_subplot(111)
    hSubPlot1.plot(vTs, vSig, 'g-', label="original sig")
    hSubPlot1.plot(vTs, vSigRecon, 'b--', label="reconstructed sig")
    #hSubPlot1.plot(np.dot(mPhi,vTs), vObSig,
    #               '*r', label="observed samps",markersize=10)
    hSubPlot1.set_xlabel('time')
    hSubPlot1.grid(True)
    hSubPlot1.legend(loc="best")
    
    # ---------------------------------------------------------------------
    # Plot the original signal, reconstructed signal in the frequency domain
    # ---------------------------------------------------------------------

    # ---------------------------------------------------------------------

    # Original signal
    vFFT = np.fft.fft(vSig)   # Analyze the spectrum of the orignal signal
    iS = vFFT.size            # Get the size of the spectrum
    vFFTa = 2*np.abs(vFFT[np.arange(iS/2).astype(int)])/iS  # Get the amps

    # Reconstructed signal
    vFFTr = np.fft.fft(vSigRecon)   # Analyze the spectrum of the orignal signal
    iSr = vFFTr.size                # Get the size of the spectrum
    vFFTar = 2*np.abs(vFFTr[np.arange(iSr/2).astype(int)])/iSr  # Get the amps
   
    # Create a vector with frequencies of the signal spectrum
    fFFTR = dSig1['fFFTR']           # Signal FFT frequency resolution
    vF = fFFTR * np.arange(iS/2)
    # ---------------------------------------------------------------------

    # Plot half of the spectrum - original signal
    hFig2 = plt.figure(2)
    hSubPlot21 = hFig2.add_subplot(111)
    hSubPlot21.grid(True)
    hSubPlot21.set_title('Spectrum of an original signal')
    hSubPlot21.set_xlabel('Frequency [Hz]')
    (markerline, stemlines, baseline) = hSubPlot21.stem(vF, vFFTa,
                                                        linefmt='b-',
                                                        markerfmt='bo',
                                                        basefmt='r-')      
    hSubPlot21.set_xlim(-1*1e3, 51*1e3)
    hSubPlot21.set_ylim(-0.1, 3.1)
    plt.setp(stemlines, color='g', linewidth=2.0)
    plt.setp(markerline, color='g', markersize=10.0)

    # Plot half of the spectrum - original signal
    hFig3 = plt.figure(3)
    hSubPlot31 = hFig3.add_subplot(111)
    hSubPlot31.grid(True)
    hSubPlot31.set_title('Spectrum of the reconstructed signal')
    hSubPlot31.set_xlabel('Frequency [Hz]')
    (markerline, stemlines, baseline) = hSubPlot31.stem(vF, vFFTar,
                                                        linefmt='g-',
                                                        markerfmt='go',
                                                        basefmt='r-')
      
    hSubPlot31.set_xlim(-1*1e3, 51*1e3)
    hSubPlot31.set_ylim(-0.1, 3.1)
    plt.setp(stemlines, color='b', linewidth=2.0)
    plt.setp(markerline, color='b', markersize=10.0)
    plt.show(block=True)








# =====================================================================
# Trigger when start as a script
# =====================================================================
if __name__ == '__main__':
    _L1_recon_ex3()
