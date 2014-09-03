from __future__ import division
import rxcs
import numpy as np
import matplotlib.pyplot as plt


def _SNR_ex0():

    # -----------------------------------------------------------------
    # Generate signals using the random multitone signal generator

    dSigConf = {}               # Init dict. wth signal generator configuration
    dSigConf['tS'] = 1e-3       # Time of the signal
    dSigConf['fR'] = 1e6        # The signal representation sampling frequency
    dSigConf['fMax'] = 40e3     # The highest possible frequency in the signal
    dSigConf['fRes'] = 1e3      # The signal spectrum resolution is 1 kHz

    dSigConf['nTones'] = 2      # The number of tones

    dSigConf['nSigPack'] = 1   # The number of signals to be generated

    # Run the multtone signal generator
    dSig = rxcs.sig.sigRandMult.main(dSigConf)
    vSig = dSig['mSig'][0, :]
    vT = dSig['vTSig']

    # -----------------------------------------------------------------
    # Sample the generated signals

    dAcqConf = {}             # Init dict. with sampler configuration
    dAcqConf['Tg'] = 1e-6     # The sampling grid period
    dAcqConf['fSamp'] = 40e3  # The average sampling frequency

    # Run the sampler
    dObSig = rxcs.acq.nonuniANGIE.main(dAcqConf, dSig)
    vObSig = dObSig['mObSig'][0,:]

    # - - - - - - - -
    # Compute the oversampling ratio

    fMax = dSigConf['fMax']    # The highest possible frequency in the signal
    fSamp = dAcqConf['fSamp']  # The average sampling frequency
    iOSR = fSamp / (2 * fMax)      # the oversampling ratio
    rxcs.console.bullet_param('The oversampling ratio:', iOSR, ' ', '')

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
    (mDict, dDict) = rxcs.cs.dict.IFFToNoDC.main(dCSConf)

    # - - - - - - - -
    # Compute the Theta matrix
    m3Phi = dObSig['m3Phi']   # Get the observation matrix from the sampler
    mPhi = m3Phi[0, :, :]     # ^

    mTheta = np.dot(mPhi, mDict.T)

    # - - - - - - - -
    # Run the L1 optimization

    dCS = {}                  # Initialize the dictionary
    dCS['m3Theta'] = mTheta   # Add the Theta matrix
    dCS['iK'] = 0.5           # Add the 'k' parameter
    dCS['mObSig'] = vObSig    # Add observed signal
    dCS['bComplex'] = 1       # Problem contains complex numbers

    # Run the L1 minimization - find the signal coefficients
    mCoeff = rxcs.cs.cvxoptL1.main(dCS)

    # Reconstruct the signal using the found signal coefficients and the
    # dictionary
    vCoeff = mCoeff[:, 0]
    vSigRecon = np.dot(mDict.T, vCoeff).real

    # Put the reconstructed signal into a 2D matrix, and put the matrix into
    # a dictionary
    mSig = np.zeros((vSigRecon.size,1))
    mSig[:,0] = vSigRecon
    dSigRecon = {}
    dSigRecon['mSig'] = mSig.T

    # ---------------------------------------------------------------------
    # Measure the SNR of the reconstruction
    dAnaConf = {}  # Initialize dictionary with configuration for
                   # the system analysis

    dAnaConf['iSNRSuccess'] = 15  # if SNR of the reconstruction > 15dB
                                  # then the reconstrucion is successfull
    dAna = rxcs.ana.SNR.main(dSig, dSigRecon, {}, dAnaConf)


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
# Trigger when start as a script
# =====================================================================
if __name__ == '__main__':
    _SNR_ex0()
