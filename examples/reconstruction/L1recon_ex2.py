"""
This script is an example of how to use the L1 optimization reconstruction
module (regularized regression scheme). |br|

A multitone signal is nonuniformly sampled and reconstructed with L1 reconstrucion
module from the RxCS toolbox. The module perfroms the regularized regression
optimization scheme and uses the external 'cvxopt' toolbox. |br|

After the signal generation and sampling, the original signal, the observed
samples, and the reconstructed signal are plot in the time domain. |br|

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0  | 18-SEP-2014 : * Version 1.0 released. |br|
    2.0  | 21-AUG-2015 : * Adjusted to the version 2.0 of the L1 solver |br|

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
    TIME = 200e-6     # Time of the signal is 200 us
    FSMP = 2e6        # Signal representation sampling frequency 2MHz

    DELTA = 5e3    # Tone separation is 5KHz
    FMAX = 100e3   # The highest possible frequency in the spectrum is 100 kHz

    # Things on the board:
    gen = rxcs.sig.randMult()      # Signal generator
    samp = rxcs.acq.nonuniANGIE()  # Sampler
    IDFT = rxcs.cs.dict.IDFT()     # IDFT dictionary generator
    L1recon = rxcs.cs.cvxoptL1()   # L1 reconstruction
    analysisSNR = rxcs.ana.SNR()   # SNR analysis

    # ---------------------------------------------------------------------
    # Generate the signal and sample it
    # ---------------------------------------------------------------------

    # Settings for the generator
    gen.tS = TIME    # Time of the signal
    gen.fR = FSMP    # The signal representation sampling frequency
    gen.fMax = FMAX    # Max frequency
    gen.fRes = DELTA   # The tone separation in the signals 

    gen.nTones = 3    # The number of random tones in the signals

    # Settings for the sampler
    samp.tS = TIME       # Time of the signal
    samp.fR = FSMP       # The signal representation sampling freuqnecy
    samp.Tg = 1e-6       # The sampling grid period
    samp.fSamp = 100e3   # The average sampling frequency

    # -----------------------------------------------------------------
    gen.run()               # Run the generator    
    samp.mSig = gen.mSig    # Connect the signal from the generator to the sampler 
    samp.run()              # Run the sampler

    # -----------------------------------------------------------------
    # Reconstruct the signal
    # -----------------------------------------------------------------

    # Generate the IDFT dictionary
    IDFT.tS = TIME    # Time of the dictionary is 1 ms
    IDFT.fR = FSMP    # Representation sampling frequency is 40 kHz
    IDFT.fDelta = DELTA   # The frequency separation between tones
    IDFT.nTones = int(FMAX / DELTA)  # The number of tones in the dictionary
    IDFT.run()

    # Cut down the dictionary matrix - take only first 20 rows
    #mDict = mDict[np.arange(int(Nt)),:]    
    
    # Compute the Theta matrix
    mDict = IDFT.mDict   # Take the dictionary matrix
    mPhi = samp.lPhi[0]  # Take the observation matrices
    mTheta = np.dot(mPhi, mDict.T)

    # Run the L1 minimization - generate signal coefficients
    vObSig = samp.mObSig[0, :]    # The observed signal
    L1recon.lTheta = [mTheta]     # Add the Theta matrix
    L1recon.lObserved = [vObSig]  # Add the observed signals
    L1recon.iK = 0.01             # Add the 'k' parameter
    L1recon.bComplex = 1          # Add info that the problem contains complex
                                  # numbers
    L1recon.run()  # Run the reconstruction
    
    # Reconstruct the signal using the found signal coefficients and the
    # dictionary
    vCoeff = L1recon.lCoeff[0]    
    vSigRecon = np.dot(mDict.T, vCoeff)
    vSigRecon = vSigRecon.real

    # -----------------------------------------------------------------
    # Measure the SNR of the reconstruction
    # -----------------------------------------------------------------
    analysisSNR.mSigRef = gen.mSigNN    # Nonnoisy signal from the generator is a a reference signal
    analysisSNR.mSig = vSigRecon        # Reconstructed signal is a signal under test
    analysisSNR.run()                   # Run the reconstruction
    
    # ---------------------------------------------------------------------
    # Plot the original signal, reconstructed signal and signal samples
    # ---------------------------------------------------------------------

    # Get the generated signal
    vSig = gen.mSig[0, :]

    # Get the signal time vector from the dictionary data
    vT = gen.vT

    # Plot the figure
    hFig1 = plt.figure(1)
    hSubPlot1 = hFig1.add_subplot(111)
    hSubPlot1.plot(vT, vSig, 'g-', label="original sig")
    hSubPlot1.plot(vT, vSigRecon, 'b--', label="reconstructed sig")
    hSubPlot1.plot(np.dot(mPhi, vT), vObSig,
                   '*r', label="observed samps",markersize=10)
    hSubPlot1.set_xlabel('time')
    hSubPlot1.grid(True)
    hSubPlot1.legend(loc="best")
    plt.show(block=True)

# =====================================================================
# Trigger when start as a script
# =====================================================================
if __name__ == '__main__':
    _L1_recon_ex2()
