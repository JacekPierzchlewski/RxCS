"""
This module contains SNR evaluation function of the reconstructed signals. |br|


*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    0.1  | 20-MAY-2014 : * Initial version. |br|
    0.2  | 21-MAY-2014 : * Success Ratio computation is added. |br|
    0.3  | 21-MAY-2014 : * Docstrings added. |br|
    0.4  | 21-MAY-2014 : * Configuration with a dictionary |br|
    0.5  | 21-MAY-2014 : * Progress and results printing |br|
    1.0  | 21-MAY-2014 : * Version 1.0 released. |br|
    
*License*:
    BSD 2-Clause
"""
from __future__ import division
import numpy as np
import rxcs


def main(dSigOrig, dSigRecon, dAna, dAnaConf):
    """
    This the main function of the generator and the only one which should be
    accessed by a user. |br|

    The function computes a noise of reconstrucion for every signal;
    this noise is equal to the difference between the reconstructed and
    the original signals.
    Afterwards the function computes the signal-to-noise ratio of
    the reconstruction for every signal.
    The ratio is computed as: SNR = 10log10(iPs/iPn),
    where:

            iPs - power of the original signal

            iPn - power of noise

    The function computes also the average signal-to-noise ratio of the
    reconstruction. |br|

    Additionally. the function computes the success ratio, which is equal to
    the ratio of reconstructed signal with reconstruction SNR higher than
    success threshold. |br|

    Args:
        dSigOrig (dict): dict. with the original signals
        dSigRecon (dict): dict. with the reconstructed signals
        dAna (dict): dict. with results of system analysis
        dAnaConf (dict): dict. with configuration for system analysis


    Returns:
        dAna (dict): dict. with results of system analysis
    """

    # -------------------------------------------------------------------
    # Get the signals
    (mSig_orig, mSig_recon, nSigs_orig, iSiz_orig) = \
        _getSignals(dSigOrig, dSigRecon)

    # Get the configuration
    # bMute        -  'mute the console output' flag
    # iSNRSuccess  -  success threshold
    (bMute,
     iSNRSuccess) = _getConf(dAnaConf)

    # -------------------------------------------------------------------
    # Print out the header of the SNR analysis
    if bMute == 0:
        rxcs.console.progress('System analysis',
                              'SNR of the reconstructed signal')
        tStart = rxcs.console.module_progress('SNR analysis starts!!!')

    # -------------------------------------------------------------------
    # Compute the SNR

    # Compute the noise
    mNoise = np.abs(mSig_orig - mSig_recon)
    (_, iSizNoise) = mNoise.shape  # Size of the noise

    # Compute the power of noise
    vNoiseP = (np.sum(mNoise * mNoise, axis=1) / iSizNoise)

    # Compute the power of orignal signals
    vSigP = (np.sum(mSig_orig * mSig_orig, axis=1) / iSiz_orig)

    # Compute the SNR for every reconstructed signal and the average SNR
    vSNR = 10 * np.log10(vSigP / vNoiseP)
    iSNR = vSNR.mean()

    # -------------------------------------------------------------------
    # Compute the success ratio
    iSR = (vSNR >= iSNRSuccess).mean()

    # -------------------------------------------------------------------
    # Add the vector with computed SNR to the dictionary with system
    # analysis results
    dAna['vSNR'] = vSNR

    # Add the average SNR to the dictionary with system analysis results
    dAna['iSNR'] = iSNR

    # Add the success ratio to the dictionary with system analysis results
    dAna['iSR'] = iSR

    # -------------------------------------------------------------------
    # SNR analysis is done
    if bMute == 0:
        rxcs.console.module_progress_done(tStart)

    # -------------------------------------------------------------------
    # Print results
    _printResults(iSNR, iSR, iSNRSuccess, bMute)

    # -------------------------------------------------------------------
    return dAna


# =================================================================
# Get the signals
# =================================================================
def _getSignals(dSigOrig, dSigRecon):
    """
    This function gets the reconstructed and the original signals from
    the data dicionaries.

    The function checks if:

        - the signals are present in the dictionaries

        - the signals have the same length

        - there is the same number of signals

    Args:
        dSigOrig (dict): dict. with the original signals
        dSigRecon (dict): dict. with the reconstructed signals

    Returns:
        mSig_orig (matrix): the original non noisy signal
        mSig_recon (matrix): the reconstructed signal
        nSigs (float): the number of signals
        iSigSiz (float): the length of signals
    """

    # -------------------------------------------------------------------
    # Get the original non noisy signals, the number of orignal signals
    # and their length
    strErr = 'The original signals (mSigNN) are missing in the "dSigOrig"'
    if not 'mSigNN' in dSigOrig:
        raise NameError(strErr)

    mSig_orig = dSigOrig['mSigNN']
    (nSigs_orig, iSiz_orig) = mSig_orig.shape

    # -------------------------------------------------------------------
    # Get the reconstructed signals, the number of reconstructed signals,
    # and their length
    strErr = 'The reconstructed signals (mSig) are missing in the "dSigRecon"'
    if not 'mSig' in dSigRecon:
        raise NameError(strErr)

    mSig_recon = dSigRecon['mSig']
    (nSigs_recon, iSiz_recon) = mSig_orig.shape

    # -------------------------------------------------------------------
    # Check if the original and the reconstructed signals have the same
    # length
    strErr = 'The original and reconstructed signals must have the same length'
    if iSiz_orig != iSiz_recon:
        raise ValueError(strErr)

    # -------------------------------------------------------------------
    # Check if there is the same number of original and reconstructed
    # signals
    strErr = 'There are more original signals than reconstructed signals!'
    if nSigs_orig > nSigs_recon:
        raise ValueError(strErr)
    strErr = 'There are more reconstructed signals than original signals!'
    if nSigs_recon > nSigs_orig:
        raise ValueError(strErr)

    # -------------------------------------------------------------------
    nSigs = nSigs_orig
    iSigSiz = iSiz_orig
    return (mSig_orig, mSig_recon, nSigs, iSigSiz)


# =================================================================
# Get the configuration
# =================================================================
def _getConf(dAnaConf):
    """
    This function gets the configuration of the module from the
    system analysis configuration dictionary.

    The function checks if the correct configuration fields are given in
    the configuration dictionary. If not, the default values are assigned to
    the configuration values.

    Args:
        dAnaConf (dict): dict. with the system analysis configuration

    Returns:
        bMute (float): 'mute the console output' flag
        iSNRSuccess (float): success threshold
    """

    # -------------------------------------------------------------------
    # Get the mute flag
    if not 'bMute' in dAnaConf:
        bMute = 0
    else:
        bMute = dAnaConf['bMute']

    # -------------------------------------------------------------------
    # Get the success threshold
    if not 'bMute' in dAnaConf:
        iSNRSuccess = 20
    else:
        iSNRSuccess = dAnaConf['iSNRSuccess']

    return (bMute, iSNRSuccess)


# =================================================================
# Print results of the analysis
# =================================================================
def _printResults(iSNR, iSR, iSNRSuccess, bMute):
    """
    This function print the results of the SNR analysis to the console,
    if the 'mute' flag is not set.

    Args:
        iSNR (float): the measured average SNR of the reconstrucion
        iSR (float): success ratio
        iSNRSuccess (float): success threshold
        bMute (float): 'mute the console output' flag

    Returns:
        nothing

    """

    if bMute == 0:
        rxcs.console.bullet_param('The average SNR of the reconstruction',
                                  iSNR, '-', 'dB')
        rxcs.console.bullet_param('The Success Ratio', iSR, ' ', '')
        rxcs.console.param('(success threshold)', iSNRSuccess, '-', 'dB')
    return
