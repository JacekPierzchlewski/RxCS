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


def _L1_recon_ex2():

    # ---------------------------------------------------------------------
    # Settings for the example
    # ---------------------------------------------------------------------
    iT = 200e-6     # Time of the signal [s]
    fD = 5e3        # Tone separation [Hz]
    Nt = 20         # The number of tones in the signal
    fRS = 2e6       # Signal representation sampling frequency

    # -----------------------------------------------------------------
    # Generate the signal
    # -----------------------------------------------------------------
    dSigConf = {}
    dSigConf['tS'] = iT       # Time of the signal
    dSigConf['fR'] = fRS      # The signal representation sampling frequency
    dSigConf['fMax'] = fD*Nt  # The highest possible frequency in the signal
    dSigConf['fRes'] = fD     # The signal spectrum resolution is 1 kHz
    dSigConf['nTones'] = 3    # The number of tones in the signal
    dSigConf['nSigPack'] = 1  # The number of signals to be generated
    dSig = rxcs.sig.sigRandMult.main(dSigConf)

    # -----------------------------------------------------------------
    # Sample the signal
    # -----------------------------------------------------------------

    # Generate settings for the sampler
    dAcqConf = {}
    dAcqConf['Tg'] = 1e-6       # The sampling grid period
    dAcqConf['fSamp'] = 120e3   # The average sampling frequency
    dObSig = rxcs.acq.nonuniANGIE.main(dAcqConf, dSig)

    # -----------------------------------------------------------------
    # Reconstruct the signal
    # -----------------------------------------------------------------

    # Generate the IDFT dictionary
    dCSConf = {}
    dCSConf['tS'] = iT            # Time of the dictionary
    dCSConf['fR'] = iT * iTSamp   # The signal representation sampling freq.
    dCSConf['fDelta'] = fSep      # The frequency separation between tones
    dCSConf['nTones'] = Nt        # The number of tones in the dictionary
    (mDict, dDict) = rxcs.cs.dict.IDFToNoDC.main(dCSConf)

    # Construct the theta matrix
    mTheta = np.dot(mPhi, mDict.T)

    # Run the L1 minimization - generate signal coefficients
    dCS = {}                  # Initialize the dictionary
    dCS['m3Theta'] = mTheta   # Add the Theta matrix
    dCS['iK'] = 0.1           # Add the 'k' parameter
    dCS['mObSig'] = vObSig    # Add observed signal
    dCS['bComplex'] = 1       # Add info that the problem contains complex
                              # numbers
    mCoeff = rxcs.cs.cvxoptL1.main(dCS)
    vCoeff = mCoeff[:, 0]

    # Reconstruct the signal using the found signal coefficients and the
    # dictionary
    vSigRecon = np.dot(mDict.T, vCoeff)
    vSigRecon = vSigRecon.real

    # ---------------------------------------------------------------------
    # Plot the original signal, reconstructed signal and signal samples
    # ---------------------------------------------------------------------

    # Get the generated signal
    mSig = dSig['mSig']
    vSig = mSig[0, :]

    # Get the signal time vector from the dictionary data
    vTs = dDict['vT']

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
    _L1_recon_ex2()
