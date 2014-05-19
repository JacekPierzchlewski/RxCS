from __future__import division
import numpy as np

def main(dSig, dSigRecon, dAna):

  # Get the original unnoisy signals, the number of signal and their length
  mSig_orig = dSigOrig['mSigNN']
  (nSigs, nL_orig) = mSig_orig.shape()

  # Get the reconstructed signals and their length
  mSig_recon = dSigRecon['mSig']
  (_, nL_recon) = mSig_orig.shape()

  # -------------------------------------------------------------------

  # Compute the noise signals
  mNoise = np.abs(mSig_orig - mSig_recon)

  # Compute the power of noise
  vNoiseP = (np.sum(mNoise*mNoise,axis=1) / nL_orig).reshape(nSigs,1)

  # Compute the power of orignal signals
  vSigP = (np.sum(mSig_orig*mSig_orig,axis=1) / nL_orig).reshape(nSigs,1)

  # Compute the SNR for every reconstructed signal and add it to the dictionary
  # with system analysis results
  vSNR = 20*log10(vSigP/vNoiseP)
  dAna['vSNR'] = vSNR
  return dAna
