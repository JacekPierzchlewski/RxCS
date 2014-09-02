"""
This script is an example of how to use the L1 optimization reconstruction
module (regularized regression scheme). |br|

In this example a simple dictionary which contains only cosine tones is
generated. Then, a 2 tone signal is generated using the dictionary. |br|

The signal is nonuniformly sampled and reconstructed with L1 reconstrucion
module from the RxCS toolbox. The module perfroms the regularized regression
optimization scheme and uses the external 'cvxopt' toolbox. |br|

After the signal generation and sampling, the original signal, the observed
samples, and the reconstructed signal are plot in the time domain. |br|

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0  | 11-JUN-2014 : * Version 1.0 released. |br|

*License*:
    BSD 2-Clause
"""

from __future__ import division
import numpy as np
import rxcs
from cvxopt import matrix
import matplotlib.pyplot as plt


def _L1_recon_ex0():
    """
        This is the main function of the example
    """

    # ---------------------------------------------------------------------
    # Generate the dictionary

    # Settings for the dictionary
    iTSamp = 100    # The number of signal representation time samples
    iTones = 20     # The number of tones in the dictionaru
    fSep = 1        # Tone frequency separation [Hz]

    # Run the dictionary generator
    (vT, mDict) = _CosDict(iTSamp, iTones, fSep)
    #
    #
    # vT     [numpy vector] - time vector for the signal generated with
    #                         the dictionary
    #
    # mDict  [numpy matrix] - the dictionary
    #

    # ---------------------------------------------------------------------
    # Generate the signal.

    (iRows, iCols) = mDict.shape
    vX = np.zeros((iCols, 1))       # Here we define signal coefficients
    vX[2] = 1                       # 3 Hz - amplitude = 1
    vX[6] = 2                       # 7 Hz - amplitude = 2

    # Here we generate the signal using the vector with coefficients and
    # the dictionary
    vSig = np.dot(mDict, vX)

    # ---------------------------------------------------------------------
    # Sample the signal (non uniform sampling)

    # The number of samples in the observation signal
    nSamps = 15

    # Compute the oversampling ratio
    tS = 1/fSep           # Signal time
    fMax = fSep * iTones  # Maximum frequency in the dictionary
    fNyq = 2 * fMax       # Nyquist of the dictionary
    fS = nSamps / tS      # The average signal sampling
    iOSR = fS / fNyq      # the oversampling ratio
    print('The oversampling ratio is equal to  %.2f \n') % iOSR

    # Draw indices of signal representation samples which will be acquired
    vSampInx = np.random.permutation(iTSamp)
    vSampInx = vSampInx[0:nSamps]
    vSampInx.sort()

    # Generate the observation matrix (nonuniform sampling)
    inxRow = 0
    mPhi = np.zeros((nSamps, iTSamp))
    for inxCol in vSampInx:
        mPhi[inxRow, inxCol] = 1
        inxRow = inxRow + 1

    # Sample the signal using the generated observation matrix
    vObSig = np.dot(mPhi, vSig)

    # ---------------------------------------------------------------------
    # Signal reconstruction

    # Construct the theta matrix
    #
    # Theta matrix = observation matrix * dictionary matrix
    #
    mTheta = np.dot(mPhi, mDict)

    # Generate the input dictionary for the L1 reconstruction module
    #
    dCS = {}                  # Initialize the dictionary
    dCS['m3Theta'] = mTheta   # Add the Theta matrix
    dCS['iK'] = 0.2           # Add the 'k' parameter
    dCS['mObSig'] = vObSig    # Add observed signal
    dCS['bComplex'] = 0       # Add info that problem does not contain
                              # complex numbers

    # INFO:
    #
    # The optimization scheme is:
    #
    #   min(  |Ax - y|_2^2  +  k * |x|_1  )
    #                          ^
    #                          |
    #                          |
    #                   the 'k' parameter
    #
    #
    #
    # THETA MATRICES:
    # The optimization module 'rxcs.cs.cvxoptL1' is designed to work
    # with multiple observed signals, so that many signals can be reconstructed
    # with one module call.
    #
    # Therefore, by default the input matrix with Theta is a 3D matrix, so that
    # many Theta matrices may be given to the module (one page of the
    # 3D matrix = one Theta matrix).
    #
    # If there is a need to reconstruct only 1 signal, then the input
    # Theta matrix may be 2D, the module will handle that.
    #
    #
    # OBSERVATION SIGNALS:
    # Similarly, the observed signals are given as a 2D matrix (one column -
    # one observed signal). If there is a need to reconstruct only 1 signal
    # then the field 'mObSig' in the input dictionary may be a simple vector
    # with the observed signal, as it is in the example.
    #
    #
    # Always the number of columns in the mObSig matrix must equal the number
    # of pages in the m3Theta matrix.
    #
    #
    # COMPLEX OPTIMIZATION FLAG:
    # If the 'bComplex' is set, then the module converts the complex
    # optimization problem into a real problem. This flag may not exists in
    # the dictionary, by default it is cleared.
    #
    # Warning: the module does not support reconstruction of complex signals!
    #          Therefore the conversion to real problem is done with assumption
    #          that the complex part of the reconstructed signal is 0.
    #
    #

    # Run the L1 minimization - find the signal coefficients
    mCoeff = rxcs.cs.cvxoptL1.main(dCS)

    # The module is designed to perform optimization for many signals with
    # one module call, so the output is a matrix with found coefficients
    # (one column - one vector with coefficients).
    #
    # If there was only one signal given to be reconstructed (as in the
    # example), then the reconstructed coefficients are in the first column
    # of the output matrix.
    #
    vCoeff = mCoeff[:, 0]

    # Reconstruct the signal using the found signal coefficients and the
    # dictionary
    vSigRecon = np.dot(mDict, vCoeff)

    # Due to numerical inaccuracies and reconstruction inaccuracies
    # the reconstructed signal may contain trace amounts of complex
    # values. Let's cut these values out.
    vSigRecon = vSigRecon.real

    # ---------------------------------------------------------------------
    # Plot the original signal, reconstructed signal and signal samples

    hFig1 = plt.figure(1)
    hSubPlot1 = hFig1.add_subplot(111)
    hSubPlot1.plot(vT, vSig, 'g-', label="original sig")
    hSubPlot1.plot(vT, vSigRecon, 'b--', label="reconstructed sig")
    hSubPlot1.plot(np.dot(mPhi,vT), vObSig,
                   '*r', label="observed samps",markersize=10)
    hSubPlot1.set_xlabel('time')
    hSubPlot1.grid(True)
    hSubPlot1.legend(loc="best")
    plt.show(block=True)


# =====================================================================
# Return a dictionary with cosine tones
# =====================================================================
def _CosDict(iTSamp, iTones, fSep):
    """
        This function generates a dictionary with cosine tones.
        One column contains one cosine tone.

        Args:
            iTSamp (float): the number of time samples
            iTones (float): the number of tones
            fSep (float):  frequency separation between tones
    """

    # ---------------------------------------------------------------------
    # Generate the time vector
    tS = 1 / fSep   # Time of the signal
    vT = tS/iTSamp*np.arange(iTSamp)

    # ---------------------------------------------------------------------
    # Allocate the dictionary matrix
    mDict = np.zeros((iTSamp,iTones))

    # ---------------------------------------------------------------------
    # Generate the dictionary matrix - loop over all tones
    for inxTone in np.arange(iTones):
        fFreq = (inxTone + 1)*fSep         # Frequency of a tone
        vTone = np.cos(2*np.pi*fFreq*vT)   # Create a tone
        mDict[:,inxTone] = vTone           # Put the tone into the matrix

    return (vT, mDict)


# =====================================================================
# Trigger when start as a script
# =====================================================================
if __name__ == '__main__':
    _L1_recon_ex0()
