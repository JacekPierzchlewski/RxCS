from __future__ import division
import rxcs
import numpy as np
import matplotlib.pyplot as plt


def _SNR_ex1():

    # Settings
    N_SIGS = 1e3

    # -----------------------------------------------------------------
    # Generate signals using the random multitone signal generator

    dSigConf = {}               # Init dict. wth signal generator configuration
    dSigConf['tS'] = 1e-3       # Time of the signal
    dSigConf['fR'] = 1e6        # The signal representation sampling frequency
    dSigConf['fMax'] = 40e3     # The highest possible frequency in the signal
    dSigConf['fRes'] = 1e3      # The signal spectrum resolution is 1 kHz

    dSigConf['nTones'] = 2      # The number of tones

    dSigConf['nSigPack'] = N_SIGS  # The number of signals to be generated

    # Run the multtone signal generator
    dSig = rxcs.sig.sigRandMult.main(dSigConf)

    # -----------------------------------------------------------------
    # Sample the generated signals

    dAcqConf = {}             # Init dict. with ssampler configuration
    dAcqConf['Tg'] = 1e-6     # The sampling grid period
    dAcqConf['fSamp'] = 40e3  # The average sampling frequency

    # Run the sampler
    dObSig = rxcs.acq.nonuniANGIE.main(dAcqConf, dSig)

    # - - - - - - - -
    # Compute the oversampling ratio
    fMax = dSigConf['fMax']    # The highest possible frequency in the signal
    fSamp = dAcqConf['fSamp']  # The average sampling frequency
    iOSR = fSamp / (2 * fMax)      # the oversampling ratio
    rxcs.console.bullet_param('The oversampling ratio:', iOSR, ' ', '')
    print('\n')

    # -----------------------------------------------------------------
    # Reconstruct the signals

    # - - - - - - - -
    # Generate the dictionary matrix
    dCSConf = {}
    dCSConf['tS'] = 1e-3         # Time of the dictionary is 1 ms
    dCSConf['fR'] = 1e6          # The signal representation sampling frequency
    dCSConf['fDelta'] = 1e3      # The frequency separation between tones
    dCSConf['nTones'] = 40       # The number of tones in the dictionary

    # Generate the IDFT dictionary
    (mDict, dDict) = rxcs.cs.dict.IDFToNoDC.main(dCSConf)

    # - - - - - - - -
    # Compute the Theta matrices for all the signals
    m3Phi = dObSig['m3Phi']                  # Get the observation matrices

    mTheta = np.dot(m3Phi[0,:,:], mDict.T)   # Compute the 1st Theta matrix
    m3Theta = np.tile(mTheta,(N_SIGS,1,1))   # Allocate 3D matrix for all the
                                             # Theta matrices

    for inxTh in np.arange(1, N_SIGS):  # <-loop over all the signals
        m3Theta[inxTh, :, :] = np.dot(m3Phi[inxTh, :, :], mDict.T)

    # - - - - - - - -
    # Run the L1 optimization

    dCS = {}                             # Initialize the dictionary
    dCS['m3Theta'] = m3Theta             # Add the Theta matrix
    dCS['iK'] = 0.1                      # Add the 'k' parameter
    dCS['mObSig'] = dObSig['mObSig'].T   # Add observed signalss
    dCS['bComplex'] = 1                  # Problem contains complex numbers

    # Run the L1 minimization - find the signal coefficients
    mCoeff = rxcs.cs.cvxoptL1.main(dCS)

    # - - - - - - - -
    # Reconstruct the signals using the found signals coefficients and the
    # dictionary
    vSigRecon = np.dot(mDict.T, mCoeff[:, 0]).real  # Reconstruct 1st signal

    vSigRecon.shape = (vSigRecon.size, 1)         # Allocate matrix for all
    mSigRecon = np.tile(vSigRecon, (1, N_SIGS))   # the reconstructed signals
                                                  # based on the shape of the
                                                  # 1st reconstructed signal

    for inxSig in np.arange(1, N_SIGS):  # <-loop over all the signals
        mSigRecon[:, inxSig] = np.dot(mDict.T, mCoeff[:, inxSig]).real

    # Put the reconstructed signal into a 2D matrix, and put the matrix into
    # a dictionary
    dSigRecon = {}
    dSigRecon['mSig'] = mSigRecon.T

    # ---------------------------------------------------------------------
    # Measure the SNR of the reconstruction

    dAnaConf = {}  # Initialize dictionary with configuration for
                   # the system analysis

    dAnaConf['iSNRSuccess'] = 15  # if SNR of the reconstruction > 15dB
                                  # then the reconstrucion is successfull
    dAna = rxcs.ana.SNR.main(dSig, dSigRecon, {}, dAnaConf)


# =====================================================================
# Trigger when start as a script
# =====================================================================
if __name__ == '__main__':
    _SNR_ex1()
