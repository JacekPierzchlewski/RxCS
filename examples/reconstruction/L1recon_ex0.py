from __future__ import division
import numpy as np
from cvxopt import matrix
import pylab
import rxcs


def _L1_recon_ex0():

    # ---------------------------------------------------------------------
    # Generate the dictionary

    # Settings
    iTSamp = 100    # The number of signal representation time samples
    iTones = 20     # The number of tones
    fSep = 1        # Tone separation

    (vT, mDict) = _CosDict(iTSamp, iTones, fSep)

    # ---------------------------------------------------------------------
    # Generate the signal.

    (iRows, iCols) = mDict.shape
    vX = np.zeros((iCols, 1))       # Here we define signal coefficients
    vX[2] = 1                       # 3 Hz
    vX[6] = 1                       # 7 Hz

    vSig = np.dot(mDict, vX)        # Here we define the signal

    # ---------------------------------------------------------------------
    # Sample the signal (non uniform sampling)

    # The number of samples in the observation signal
    nSamps = 10

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
    mTheta = np.dot(mPhi, mDict)

    # L1 minimization - find the signal coefficients
    dCS = {}
    dCS['m3Theta'] = mTheta
    dCS['iK'] = 0.2
    dCS['mObSig'] = vObSig
    dCS['bComplex'] = 1

    # Run the L1 minimization - generate signal coefficients
    mCoeff = rxcs.cs.cvxoptL1.main(dCS)
    vCoeff = mCoeff[:, 0]

    # Reconstruct the signal using the found signal coefficients
    vSigRecon = np.dot(mDict, vCoeff).real

    # ---------------------------------------------------------------------
    # Plot the original signal, reconstructed signal and signal samples
    pylab.figure(1, facecolor='w')
    pylab.subplot(111)
    pylab.plot(vT, vSig, '-',
               vT, vSigRecon, 'r--',
               np.dot(mPhi,vT), vObSig, '*r')
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
