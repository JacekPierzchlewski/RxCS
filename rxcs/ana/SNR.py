from __future__ import division
import numpy as np

def main(dSigOrig, dSigRecon, dAna):

    ## Get the original unnoisy signals, the number of signal and their length
    mSig_orig = dSigOrig['mSigNN']
    (iSigs_orig, iSiz_orig) = mSig_orig.shape

    # Get the reconstructed signals and their length
    mSig_recon = dSigRecon['mSig']
    (iSigs_recon, iSiz_recon) = mSig_orig.shape

    # Check if the original and the reconstructed signals have the same length
    strErr = 'The original and reconstructed signals must have the same length'
    if iSiz_orig != iSiz_recon:
        raise ValueError(strErr)

    # Check if there is the same number of original and reconstructed signals
    strErr = 'There are more original signals than reconstructed signals!'
    if iSigs_orig > iSigs_recon:
        raise ValueError(strErr)
    strErr = 'There are more reconstructed signals than original signals!'
    if iSigs_recon > iSigs_orig:
        raise ValueError(strErr)

    # -------------------------------------------------------------------

    # Compute the noise
    mNoise = np.abs(mSig_orig - mSig_recon)
    (_, iSizNoise) = mNoise.shape  # Size of the noise

    # Compute the power of noise
    vNoiseP = (np.sum(mNoise * mNoise,axis=1) / iSizNoise)

    # Compute the power of orignal signals
    vSigP = (np.sum(mSig_orig * mSig_orig,axis=1) / iSiz_orig)

    # Compute the SNR for every reconstructed signal and the average SNR
    vSNR = 10 * np.log10(vSigP / vNoiseP)
    iSNR = vSNR.mean()

    # Compute the
    # -------------------------------------------------------------------
    # Add the vector with computed SNR to the dictionary with system
    # analysis results
    dAna['vSNR'] = vSNR

    # Add the average SNR to the dictionary with system analysis results
    dAna['iSNR'] = iSNR

    # -------------------------------------------------------------------
    return dAna
