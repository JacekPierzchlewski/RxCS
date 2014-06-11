from __future__ import division
import numpy as np
from cvxopt import matrix
import pylab
import rxcs


def _L1_recon_ex0():

    # ---------------------------------------------------------------------
    # Settings
    iT = 1          # Time of the signal
    iTSamp = 100    # The number of signal representation time samples
    iTones = 20     # The number of tones
    fSep = 1        # Tone separation

    # ---------------------------------------------------------------------
    # Generate the dictionary

    # Start the dictionary with dictionary configuration
    dCSConf = {}

    # Time of the dictionary is 1 s
    dCSConf['tS'] = iT

    # The signal representation sampling frequency is 10 Hz
    dCSConf['fR'] = iT * iTSamp

    # The frequency separation between tones
    dCSConf['fDelta'] = fSep

    # The number of tones in the dictionary
    dCSConf['nTones'] = iTones

    # Generate the IFFT dictionary
    (mDict, dDict) = rxcs.cs.dict.IFFToNoDC.main(dCSConf)

    # Get the signal time vector from the dictionary
    vTs = dDict['vT']

    # Get the size of the IFFT dictionary
    (iRows, iCols) = mDict.T.shape

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

    # Generate the signal using the real IFFT dictionary
    vX = np.zeros((iCols, 1)) + 1j*np.zeros((iCols, 1))   # Here we define
                                                          # signal coefficients

    # 3Hz (-45 deg) - coeffients  (1-1j): +3Hz, (1+1j): (-3Hz)
    vX[3] = 1-1j                          # 1-1j
    vX[37] = 1+1j                         # 1-1j

    # 7Hz (+45 deg) - coeffients  (1+1i): +3Hz, (1-1i): (-3Hz)
    #vX[6] = 1+1j                          # 1+1j
    #vX[33] = 1-1j                         # 1-1j

    vSig = np.dot(mDict.T, vX).real       # Here we generate the signal

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

    # Sample the signal
    vObSig = np.dot(mPhi, vSig)

    # ---------------------------------------------------------------------
    # Signal reconstruction

    # Construct the theta matrix
    mTheta = np.dot(mPhi, mDict.T)

    # L1 minimization - find the signal coefficients
    dCS = {}
    dCS['m3Theta'] = mTheta
    dCS['iK'] = 0.1
    dCS['mObSig'] = vObSig
    dCS['bComplex'] = 1

    # Run the L1 minimization - generate signal coefficients
    mCoeff = rxcs.cs.cvxoptL1.main(dCS)
    vCoeff = mCoeff[:, 0]
    print(vCoeff)

    # Reconstruct the signal using the found signal coefficients
    vSigRecon = np.dot(mDict.T, vCoeff).real

    # ---------------------------------------------------------------------
    # Plot the original signal, reconstructed signal and signal samples
    pylab.figure(1, facecolor='w')
    pylab.subplot(111)
    pylab.plot(vTs, vSig, '-',
               vTs, vSigRecon, 'r--',
               np.dot(mPhi,vTs), vObSig, '*r')
    pylab.show()


# =====================================================================
# Return a dictionary with cosine tones
# =====================================================================
def _CosDict(iTSamp, iTones, fSep):

    # ---------------------------------------------------------------------
    # Generate the time vector
    tS = 1 / fSep   # Time of the signal
    vT = tS/iTSamp*np.arange(iTSamp)

    # ---------------------------------------------------------------------
    # Allocate the dictionary matrix
    mDict = np.zeros((iTSamp,iTones))

    # ---------------------------------------------------------------------
    # Loop over all tones
    for inxTone in np.arange(iTones):
        fFreq = (inxTone + 1)*fSep         # Frequency of a tone
        vTone = np.cos(2*np.pi*fFreq*vT)   # Create a tone
        mDict[:,inxTone] = vTone           # Putthe tone into the matrix

    return (vT, mDict)


# =====================================================================
# Trigger when start as a script
# =====================================================================
if __name__ == '__main__':
    _L1_recon_ex0()
