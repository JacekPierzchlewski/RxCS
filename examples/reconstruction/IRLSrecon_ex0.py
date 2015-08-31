"""
This script is an example of how to use the L1 IRLS optimization 
reconstruction module (iterative reweighted least squares). |br|

In this example an IDFT dictionary is generated.
Then, a 3 tone signal is generated using the dictionary. |br|

The signal is nonuniformly sampled and reconstructed with L1 reconstrucion
module (IRLS) from the RxCS toolbox. The module performs l1 optimization using
Iteratively Reweighted Lease Squares algorithm. |br|

After the signal generation and sampling, the original signal, the observed
samples, and the reconstructed signal are plot in the time domain. |br|

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0  | 23-JAN-2015 : * Version 1.0 released. |br|
    2.0  | 31-AUG-2015 : * Adjusted to the version 2.0 of the L1 IRLS solver |br|


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
    TIME = 200e-6     # Time of the signal is 200 us
    FSMP = 2e6        # Signal representation sampling frequency 2MHz

    DELTA = 5e3    # Tone separation is 5KHz
    FMAX = 100e3   # The highest possible frequency in the spectrum is 100 kHz

    # Things on the board:
    gen = rxcs.sig.randMult()      # Signal generator
    samp = rxcs.acq.nonuniANGIE()  # Sampler
      
    IDFT = rxcs.cs.dict.IDFT()        # IDFT dictionary generator
    makeTheta = rxcs.cs.makeTheta()   # Theta matrix generator 
    irlsL1 = rxcs.cs.irlsL1()        # L1 IRLS reconstruction

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
    mDict = IDFT.mDict       # Take the dictionary matrix
    (nRows, _) = mDict.shape                   # Cut down the dictionary matrix - 
    mDict = mDict[np.arange(int(nRows/2)), :]  # take only first 20 rows 

    # Compute the Theta matrix    
    makeTheta.lPhi = samp.lPhi    # Add the observation matrix
    makeTheta.lDict = [mDict.T]   # Add the dictionary  
    makeTheta.run()

    # Run the L1 minimization - generate signal coefficients
    vObSig = samp.mObSig[0, :]            # The observed signal
    irlsL1.lTheta = makeTheta.lTheta     # Add the Theta matrix
    irlsL1.lObserved = [vObSig]          # Add the observed signals
    irlsL1.bComplex = 1                  # Add info that the problem contains complex
                                          # numbers
    irlsL1.run()  # Run the reconstruction
    
    # Reconstruct the signal using the found signal coefficients and the
    # dictionary
    vCoeff = irlsL1.lCoeff[0]    
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

    # Get the observation matrix
    mPhi = samp.lPhi[0]

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
    _IRLS_recon_ex0()
