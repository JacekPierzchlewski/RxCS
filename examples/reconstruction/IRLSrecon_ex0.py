"""
This script is an example of how to use the L1 optimization reconstruction
module (iterative reweighted least squares). |br|

In this example an IDFT dictionary is generated.
Then, a 2 tone signal is generated using the dictionary. |br|

The signal is nonuniformly sampled and reconstructed with L1 reconstrucion
module (IRLS) from the RxCS toolbox. The module performs l1 optimization using
Iteratively Reweighted Lease Squares algorithm. |br|

After the signal generation and sampling, the original signal, the observed
samples, and the reconstructed signal are plot in the time domain. |br|

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0  | 23-JAN-2015 : * Version 1.0 released. |br|

*License*:
    BSD 2-Clause
"""

from __future__ import division
import numpy as np
import rxcs
import matplotlib.pyplot as plt


def _IRLS_recon_ex0():

    # ---------------------------------------------------------------------
    # Settings for the example
    # ---------------------------------------------------------------------
    iT = 200e-6     # Time of the signal [s]
    fD = 5e3        # Tone separation [Hz]
    Nt = 20         # The number of tones in the signal spectrum
    fRS = 2e6       # Signal representation sampling frequency

    # -----------------------------------------------------------------
    # Generate the signal
    # -----------------------------------------------------------------
    dSigConf = {}
    dSigConf['tS'] = iT        # Time of the signal
    dSigConf['fR'] = fRS       # The signal representation sampling frequency
    dSigConf['fMax'] = fD*Nt   # The highest possible frequency in the signal
    dSigConf['fRes'] = fD      # The signal spectrum resolution is 1 kHz
    dSigConf['nTones'] = 2     # The number of tones in the signal
    dSigConf['nSigPack'] = 1   # The number of signals to be generated
    dSig = rxcs.sig.sigRandMult.main(dSigConf)

    # -----------------------------------------------------------------
    # Sample the signal
    # -----------------------------------------------------------------

    # Generate settings for the sampler
    dAcqConf = {}
    dAcqConf['Tg'] = 1e-6       # The sampling grid period
    dAcqConf['fSamp'] = 100e3   # The average sampling frequency
    dObSig = rxcs.acq.nonuniANGIE.main(dAcqConf, dSig)

    # Take the observed signal and the observation matrix
    vObSig = dObSig['mObSig'][0,:]
    mPhi = dObSig['m3Phi'][0,:,:]
    
    # -----------------------------------------------------------------
    # Reconstruct the signal
    # -----------------------------------------------------------------

    # Generate the IDFT dictionary
    dCSConf = {}
    dCSConf['tS'] = iT            # Time of the dictionary
    dCSConf['fR'] = fRS           # The signal representation sampling freq.
    dCSConf['fDelta'] = fD        # The frequency separation between tones
    dCSConf['nTones'] = Nt        # The number of tones in the dictionary
    (mDict, _) = rxcs.cs.dict.IDFToNoDC.main(dCSConf)
    
    # Cut down the dictionary matrix - take only first 20 rows
    mDict = mDict[np.arange(int(Nt)),:]    
    
    # Compute the Theta matrix
    mTheta = np.dot(mPhi, mDict.T)

    # Run the L1 minimization - generate signal coefficients
    dCS = {}                  # Initialize the dictionary
    dCS['m3Theta'] = mTheta   # Add the Theta matrix
    dCS['iK'] = 0.01          # Add the 'k' parameter
    dCS['mObSig'] = vObSig    # Add observed signal
    dCS['bComplex'] = 1       # Add info that the problem contains complex
                              # numbers
    mCoeff = rxcs.cs.irlsL1.main(dCS)
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
    vSigRecon.shape = (vSigRecon.size, 1)
    dSigRecon = {}
    dSigRecon['mSig'] = vSigRecon.T 
     
    # Create a dictionary with configuration for the system analysis
    dAnaConf = {}
    dAnaConf['iSNRSuccess'] = 15  # SNR of the recon > 15dB == success
    rxcs.ana.SNR.main(dSig, dSigRecon, {}, dAnaConf)

    # ---------------------------------------------------------------------
    # Plot the original signal, reconstructed signal and signal samples
    # ---------------------------------------------------------------------

    # Get the generated signal
    mSig = dSig['mSig']
    vSig = mSig[0, :]

    # Get the signal time vector from the dictionary data
    vTs = dSig['vTSig']

    # Plot the figure
    hFig1 = plt.figure(1)
    hSubPlot1 = hFig1.add_subplot(111)
    hSubPlot1.plot(vTs, vSig, 'g-', label="original sig")
    hSubPlot1.plot(vTs, vSigRecon, 'b--', label="reconstructed sig")
    hSubPlot1.plot(np.dot(mPhi,vTs), vObSig,
                   '*r', label="observed samps",markersize=10)
    hSubPlot1.set_xlabel('time')
    hSubPlot1.grid(True)
    hSubPlot1.legend(loc="best")
    plt.show(block=True)

# =====================================================================
# Trigger when start as a script
# =====================================================================
if __name__ == '__main__':
    _IRLS_recon_ex0()
