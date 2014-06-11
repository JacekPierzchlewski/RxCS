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

    # ---------------------------------------------------------------------
    # Settings for the example
    iT = 1          # Time of the signal [s]
    iTSamp = 100    # The number of signal representation time samples
    iTones = 20     # The number of tones
    fSep = 1        # Tone separation [Hz]

    # ---------------------------------------------------------------------
    # Generate the IDFT dictionary

    # Start the IDFT dictionary configuration
    dCSConf = {}
    dCSConf['tS'] = iT           # Time of the dictionary
    dCSConf['fR'] = iT * iTSamp  # The signal representation sampling freq.
    dCSConf['fDelta'] = fSep     # The frequency separation between tones
    dCSConf['nTones'] = iTones   # The number of tones in the dictionary

    # Generate the IDFT dictionary
    (mDict, dDict) = rxcs.cs.dict.IFFToNoDC.main(dCSConf)

    # The dictionary contains separate tones in rows.
    # The optimization modules requires the Theta matrix to be column-wise,
    # so let's transpose the dictionary
    mDict = mDict.T

    # Get the signal time vector from the dictionary data
    vTs = dDict['vT']

    # ---------------------------------------------------------------------
    # Generate the signal.
    #
    #
    # Dictionary matrix is as follows:
    #
    # indices of columns
    #  |
    #  |
    #  V
    # [0] = 1Hz            [20] = - 20Hz
    # [1] = 2Hz            [21] = - 19Hz
    # [2] = 3Hz            [22] = - 18Hz
    # [3] = 4Hz            [23] = - 17Hz
    # [4] = 5Hz            [24] = - 16Hz
    # [5] = 6Hz            [25] = - 15Hz
    # [6] = 7Hz            [26] = - 14Hz
    # [7] = 8Hz            [27] = - 13Hz
    # [8] = 9Hz            [28] = - 12Hz
    # [9] = 10Hz           [29] = - 11Hz
    #
    # [10] = 11Hz          [30] = - 10Hz
    # [11] = 12Hz          [31] = - 9Hz
    # [12] = 13Hz          [32] = - 8Hz
    # [13] = 14Hz          [33] = - 7Hz
    # [14] = 15Hz          [34] = - 6Hz
    # [15] = 16Hz          [35] = - 5Hz
    # [16] = 17Hz          [36] = - 4Hz
    # [17] = 18Hz          [37] = - 3Hz
    # [18] = 19Hz          [38] = - 2Hz
    # [19] = 20Hz          [39] = - 1Hz
    #

    # Generate the signal using the IDFT dictionary
    (iRows, iCols) = mDict.shape
    vX = np.zeros((iCols, 1)) + 1j*np.zeros((iCols, 1))
    # vX - vector with the signal coefficients

    # 3Hz (-45 deg) - coeffients  (1-1j): +3Hz, (1+1j): (-3Hz)
    vX[3] = 1-1j                          # 1-1j
    vX[37] = 1+1j                         # 1+1j

    # 7Hz (+45 deg) - coeffients  (1+1i): +3Hz, (1-1i): (-3Hz)
    vX[6] = 1+1j                          # 1+1j
    vX[33] = 1-1j                         # 1-1j

    # Here we generate the signal using the vector with coefficients and
    # the dictionary
    vSig = np.dot(mDict, vX).real

    # ---------------------------------------------------------------------
    # Sample the signal (non uniform sampling)

    # The number of samples in the observation signal
    nSamps = 20

    # Compute the oversampling ratio
    tS = 1/fSep           # Signal time
    fMax = fSep * iTones  # Maximum frequency in the dictionary
    fNyq = 2 * fMax       # Nyquist of the dictionary
    fS = nSamps / tS      # The average signal sampling
    iOSR = fS / fNyq      # the oversampling ratio
    print('The oversampling ratio is equal to  %.2f \n') % iOSR

    # Draw indices of signal representation samples which will sampled by ADC
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

    # L1 minimization - find the signal coefficients
    dCS = {}                  # Initialize the dictionary
    dCS['m3Theta'] = mTheta   # Add the Theta matrix
    dCS['iK'] = 0.1           # Add the 'k' parameter
    dCS['mObSig'] = vObSig    # Add observed signal
    dCS['bComplex'] = 1       # Add info that the problem contains complex
                              # numbers

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

    # Run the L1 minimization - generate signal coefficients
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
    _L1_recon_ex0()
