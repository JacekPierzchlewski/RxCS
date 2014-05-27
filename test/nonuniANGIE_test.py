"""
.. role:: bash(code)
    :language: bash

This is a test module for the nonuniform sampler with ANGIE scheme. |br|

It tests the sampler with a number of test cases, and analyzes
the observed signals. |br|

The following tests are performed on the generated signals:

- if the average sampling frequency is correct?

- if the the signals were sampled in the time sampling moments which
  are reported?

To start the test run this module directly as a script:

    :bash:`$ python nonuniANGIE_test.py`

when in *rxcs/test* directory. The results are then printed to the console.
|br|

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0  | 27-MAY-2014 : * Version 1.0 released. |br|


*License*:
    BSD 2-Clause
"""
from __future__ import division
import numpy as np
import rxcs


# =====================================================================
# Main function of the test
# =====================================================================
def _nonuniANGIE_test():
    """
    This is main function of the test.

    It runs the test case functions.
    An info that a test was passed is printed to the console if a case
    function returns.

    Args:
        None

    Returns:
        Nothing
    """

    # Print out the header of the signal generator test
    print('')
    rxcs.console.progress('Function under test',
                          'nonuniform sampler with ANGIE scheme')

    # -----------------------------------------------------------------
    # Tests start here:

    # Tolerance of expected vs measured is 0.1%
    iTolerance = 0.1 * 1e-2

    _TestCase1(iTolerance)
    rxcs.console.info('case 1 OK!')

    _TestCase2(iTolerance)
    rxcs.console.info('case 2 OK!')

    _TestCase3(iTolerance)
    rxcs.console.info('case 3 OK!')

    _TestCase4(iTolerance)
    rxcs.console.info('case 4 OK!')


# =====================================================================
# Test case 1
# =====================================================================
def _TestCase1(iTolerance):
    """
    This is test case function #1. |br|

    The function configures the nonunform sampler with ANGIE scheme,
    generates random signals, samples them and checks the observed signals.

    Args:
        iTolerance: maximum tolerance of a difference between an expected value
        and a real value

    Returns:
        Nothing
    """

    # Start the dictionary with signal acquisition configuration
    dAcqConf = {}

    # The sampling grid period
    dAcqConf['Tg'] = 1e-6

    # The average sampling frequency
    dAcqConf['fSamp'] = 50e3

    # -----------------------------------------------------------------
    # Check the sampler
    _checkSampler(dAcqConf, iTolerance)

    # -----------------------------------------------------------------

    return


# =====================================================================
# Test case 2
# =====================================================================
def _TestCase2(iTolerance):
    """
    This is test case function #2. |br|

    The function configures the nonunform sampler with ANGIE scheme,
    generates random signals, samples them and checks the observed signals.

    Args:
        iTolerance: maximum tolerance of a difference between an expected value
        and a real value

    Returns:
        Nothing
    """

    # Start the dictionary with signal acquisition configuration
    dAcqConf = {}

    # The sampling grid period
    dAcqConf['Tg'] = 1e-6

    # The average sampling frequency
    dAcqConf['fSamp'] = 100e3

    # -----------------------------------------------------------------
    # Check the sampler
    _checkSampler(dAcqConf, iTolerance)

    # -----------------------------------------------------------------

    return


# =====================================================================
# Test case 3
# =====================================================================
def _TestCase3(iTolerance):
    """
    This is test case function #3. |br|

    The function configures the nonunform sampler with ANGIE scheme,
    generates random signals, samples them and checks the observed signals.

    Args:
        iTolerance: maximum tolerance of a difference between an expected value
        and a real value

    Returns:
        Nothing
    """

    # Start the dictionary with signal acquisition configuration
    dAcqConf = {}

    # The sampling grid period
    dAcqConf['Tg'] = 1e-3

    # The average sampling frequency
    dAcqConf['fSamp'] = 500

    # -----------------------------------------------------------------
    # Check the sampler
    _checkSampler(dAcqConf, iTolerance)

    # -----------------------------------------------------------------

    return


# =====================================================================
# Test case 4
# =====================================================================
def _TestCase4(iTolerance):
    """
    This is test case function #4. |br|

    The function configures the nonunform sampler with ANGIE scheme,
    generates random signals, samples them and checks the observed signals.

    Args:
        iTolerance: maximum tolerance of a difference between an expected value
        and a real value

    Returns:
        Nothing
    """

    # Start the dictionary with signal acquisition configuration
    dAcqConf = {}

    # The sampling grid period
    dAcqConf['Tg'] = 1e-3

    # The average sampling frequency
    dAcqConf['fSamp'] = 100

    # The minimum distance between sampling points
    dAcqConf['tMin'] = 5e-3

    # The maximum distance between sampling points
    dAcqConf['tMax'] = 15e-3

    # -----------------------------------------------------------------
    # Check the sampler
    _checkSampler(dAcqConf, iTolerance)

    # -----------------------------------------------------------------

    return


# =====================================================================
# ENGINE OF THE TEST: Check the sampeld signals
# =====================================================================
def _checkSampler(dAcqConf, iTolerance):
    """
    This function is the engine of all the tests. |br|

    The function geenrates a random single-tone signals, samples it and
    checks the observed signals.

    Args:
        dAcqConf: dictionary with the configuration of the sampler |br|

        iTolerance: maximum tolerance of a difference between an expected
                    value and a real value |br|

    Returns:
        Nothing
    """

    # Generated signals which will be sampled
    tStart = rxcs.console.module_progress('signals generation')
    dSig = _generateSigs(dAcqConf)
    rxcs.console.module_progress_done(tStart)

    # Sample the signals
    dAcqConf['bMute'] = 1   # Mute the output from the sampler
    tStart = rxcs.console.module_progress('signals sampling')
    dObSig = rxcs.acq.nonuniANGIE.main(dAcqConf, dSig)
    rxcs.console.module_progress_done(tStart)

    # Check the average sampling frequency
    _check_sampFreq(dAcqConf, dObSig, iTolerance)

    # Check if the signal was sampled in the time sampling moments which
    # are reported
    _check_sampTMoments(dSig, dObSig, iTolerance)

    return


# =====================================================================
# Generate signals to be sampled
# =====================================================================
def _generateSigs(dAcqConf):
    """
    This function generates a single-tone random signals. |br|

    The parameters of the signals are computed based on the parameters
    of sampling, so that the sampling process will be possible.

    Args:
        dAcqConf: dictionary with the configuration of the sampler |br|

    Returns:
        dSig: dictionary with signals to be sampled
    """

    # Start the dictionary with configuration for random signal generator
    dSigConf = {}

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # Time of the signal is equal to 100*grid
    dSigConf['tS'] = 1000*dAcqConf['Tg']

    # The signal representation sampling frequency is 2 x the grid frequency
    dSigConf['fR'] = 2/dAcqConf['Tg']

    # The signal spectrum resolution
    dSigConf['fRes'] = 1/dSigConf['tS']

    # The highest possible frequency in the signal is 10 time the resolution
    dSigConf['fMax'] = 10*dSigConf['fRes']

    # - - - - - - - - - - - - - - - -

    # The number of tones
    dSigConf['nTones'] = 1

    # The number of signals to be generated
    dSigConf['nSigPack'] = 1e4

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # Phase of all the signals equals zero
    dSigConf['iMinPhs'] = 0
    dSigConf['iMaxPhs'] = 0

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # Mute the output from the generator
    dSigConf['bMute'] = 1

    # -----------------------------------------------------------------
    # Run the multtone signal generator
    dSig = rxcs.sig.sigRandMult.main(dSigConf)

    return dSig


# =====================================================================
# This function checks the average sampling frequency
# =====================================================================
def _check_sampFreq(dAcqConf, dObSig, iTolerance):
    """
    This function function checks the average sampling frequency. |br|

    Args:
        dAcqConf: dictionary with the configuration of the sampler |br|
        dSig: dictionary with the observed signals
        iTolerance: maximum tolerance of a difference between an expected
                    value and a real value |br|

    Returns:
        nothing
    """

    # -----------------------------------------------------------------
    # Check if the reported average sampling frequency
    # equals the requested

    # Get the requested average sampling frequency
    fSamp_req = dAcqConf['fSamp']

    # Get the reported average sampling frequency
    fSamp_rep = dObSig['f_s']

    if not _isequal(fSamp_req, fSamp_rep, fSamp_rep*iTolerance):
        strErr = ('the reported average samp. freq is ')
        strErr = strErr + ('different than the requested: error!!!')
        raise Exception(strErr)

    # -----------------------------------------------------------------
    # Check if the real average sampling frequency is correct

    # Get the real length of a sampling pattern
    tTau_real = dObSig['tTau_real']

    # Calculate the correct number of sampling points
    nK_s_corr = int(np.round(fSamp_req * tTau_real))

    # Get the real number of samples in the observed signals
    (_, nK_s_real) = (dObSig['mPatts']).shape

    if nK_s_corr != nK_s_real:
        strErr = ('the number of samples in the observed signals is ')
        strErr = strErr + ('incorrect: error!!!')
        raise Exception(strErr)

    # -----------------------------------------------------------------
    # Check if the reported average sampling frequency
    # equals the real

    # Get the reported number of samples in the observed signals
    nK_s_rep = dObSig['nK_s']

    if nK_s_rep != nK_s_real:
        strErr = ('the reported number of samples in the observed signals is ')
        strErr = strErr + ('different than the real number: error!!!')
        raise Exception(strErr)

    # -----------------------------------------------------------------
    rxcs.console.note('sampling frequency:                  ok!')
    return


# =====================================================================
# This function checks if the signals were sampled in the time
# sampling moments which are reported
# =====================================================================
def _check_sampTMoments(dSig, dObSig, iTolerance):
    """
    This function checks if the signals were sampled in the time
    sampling moments which are reported. |br|

    Args:
        dAcqConf: dictionary with the configuration of the sampler |br|
        dSig: dictionary with the observed signals
        iTolerance: maximum tolerance of a difference between an expected
                    value and a real value |br|

    Returns:
        nothing
    """

    # Get the observed signals
    mObSig = dObSig['mObSig']

    # Get the number of observed signals and the number of samples in
    # the signals
    (nSigs, nK_s) = mObSig.shape

    # Get the sampling patterns (in time domain)
    mPattsT = dObSig['mPattsT']

    # - - - - - - - - - - - - - - - - - - -

    # Get the frequencies of signals
    mFrqs = dSig['mFrqs']

    # Get the amplitudes of signals
    mAmps = dSig['mAmps']

    # Get the phases of signals
    mPhs = dSig['mPhs']

    # Get the time vector for signals
    vTSig = dSig['vTSig']

    for inxSig in np.arange(nSigs):  # <- loop over all signals

        # Get the frequency, amplitude and phase of the current signal
        iF = mFrqs[inxSig, 0]
        iAmp = mAmps[inxSig, 0]
        iPhs = mPhs[inxSig, 0]

        # Get the current observed signal
        vObSig = mObSig[inxSig, :]

        # Get the current sampling pattern (in time domain)
        vPattT = mPattsT[inxSig, :]

        # Generate the correct observed signal samples
        vObSig_corr = iAmp*np.cos(2 * np.pi * iF * vPattT)

        # Check if the observed samples are identical to correct samples
        for inxSamp in np.arange(nK_s):  # <- Loop over all signal samples

            # The current observed sample
            iOb = vObSig[inxSamp]

            # The current correct observed sample
            iOb_corr = vObSig_corr[inxSamp]

            if not _isequal(iOb, iOb_corr, iOb * iTolerance):
                strErr = ('%d sample of  %s signal is incorrect: error!!!') % \
                    (inxSamp + 1, inxSig + 1)
                raise Exception(strErr)

    # -----------------------------------------------------------------
    rxcs.console.note('observed signals:                    ok!')
    return


# =====================================================================
# This function compares two values.
# The function allows for a very small error margin
# =====================================================================
def _isequal(iX, iY, iMargin):
    """
    This function checks if a difference between two values is in the
    given allowed margin.

    Args:
        iX: the first value |br|
        iY: the second value |br|
        iMargin: the allowed margin |br|

    Returns:
        1: if the difference between the given values does not exceed the
           given margin |br|
        0: if the difference between the given values does exceed the
           given margin |br|
    """

    if iX < 1e-12:  # <- very small values will create problems due to
                    #    floating point representation problems
        return 1

    if (abs(iX - iY) <= np.abs(iMargin)):
        return 1
    else:
        return 0


# =====================================================================
# Trigger when start as a script
# =====================================================================
if __name__ == '__main__':
    _nonuniANGIE_test()
