"""
This script is a simple example of how to use the low-noise linear amplififer 
model. |br|


*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1,0  | 02-SEP-2015  : * Version 1.0 released. |br|
    1,1  | 03-SEP-2015  : * Improvements in signals plotting. |br|

*License*:
    BSD 2-Clause
"""

from __future__ import division
import rxcs
import matplotlib.pyplot as plt
import numpy as np

def _LNA_ex0():

    # Things on the table:
    gen = rxcs.sig.randMult()    # Random multitone generator
    lna = rxcs.sig.LNA()         # Low-noise linear amplifier
    
    # Settings for the generator
    gen.tS = 2e-6     # Time of the signal is 2 us
    gen.fR = 1e9      # The signal representation sampling frequency is 1 GHz
    gen.fRes = 1e6    # The signal spectrum resolution is 1 MHz

    gen.vFrqs = np.array([ 10e6 ])  # There is one tone: 10 MHz cosine... 
    gen.vAmps = np.array([ 1 ])     # ...with amplitude = 1/...
    gen.vPhs =  np.array([ 0 ])     # and no phase shift

    # Settings for the low-noise amplifier
    lna.vCoef = np.array([1.0, 0.0, -0.5, 0.0, -0.43])    # Vector with LNA coefficients

    # Run the generator and get the output    
    gen.run()    
    
    lna.mSig = gen.mSig  # Get the generated signal and connect it to LNA
    lna.run()    

    # -----------------------------------------------------------------
    # Plot signals in the time domain
    vOrgSig = gen.mSig[0, :]   # Get the original signal
    vTSig = gen.vTSig          # Get the time vector of the signal

    vLNASig = lna.mSig[0, :] # Get the signal after LNA

    hFig1 = plt.figure(1)
    hSubPlot1 = hFig1.add_subplot(111)
    hSubPlot1.grid(True)
    hSubPlot1.set_title('Signal in the time domain')
    hSubPlot1.set_xlabel('Time [Seconds]')
    hSubPlot1.plot(vTSig, vOrgSig, 'b-', label='original')
    hSubPlot1.plot(vTSig, vLNASig, 'k-', label='after the LNA')
    hSubPlot1.legend()    
    hSubPlot1.set_ylim(-3.0, 3.0)

    # -----------------------------------------------------------------
    # Analyze the signals and plot it in the frequency domain

    # Analyze spectrum of the signals
    fFFTR =  gen.fFFTR     # Get the signal FFT frequency resolution

    (vFFTOrg, vFOrg) = _fftAnalysis(vOrgSig, fFFTR, minamp=1e-3)  # The original signal
    (vFFTLNA, vFLNA) = _fftAnalysis(vLNASig, fFFTR, minamp=1e-3)  # The signal after the LNA

    hFig2 = plt.figure(2)
    hSubPlot1 = hFig2.add_subplot(111)
    hSubPlot1.grid(True)
    hSubPlot1.set_title('Signals in the frequency domain')
    hSubPlot1.set_xlabel('Frequency [Hz]')
    
    # original signal
    (m, s, _) = hSubPlot1.stem(vFOrg, vFFTOrg, basefmt='.', label='original')
    plt.setp(s, color='b', linewidth=2.0)
    plt.setp(m, color='b', markersize=10.0)

    # signal after the LNA
    (m, s, _) = hSubPlot1.stem(vFLNA, vFFTLNA, basefmt='.', label='after the LNA')
    plt.setp(s, color='k', linewidth=2.0)
    plt.setp(m, color='k', markersize=10.0)
   
    hSubPlot1.set_xlim(-1e6, 100*1e6)
    hSubPlot1.set_ylim(-0.1, 1.5)
    hSubPlot1.legend()    

    # -----------------------------------------------------------------
    plt.show(block=True)

def _fftAnalysis(vSig, fFFTR, minamp=0.0):
    """
    This function analyse the signal in the frequency domain.
    It return the positive half of the signal spectrum.

    Args:
        vSig (1D Numpy array):  signal to be analysed
        fFFTR: (float):         FFT frequency resolution of the signal
        minamp: (float):        minimum amplitude which should be included in
                                the spectrum plot [default = 0.0  - include all]

    Returns:
       vFFTa_half (1D Numpy array):  amplitudes of tones in the spectrum
       vF_half (1D Numpy array):     frequencies of tones in the spectrum
    """
    
    # FFT analysis
    vFFT = np.fft.fft(vSig)    
    
    # Get the size of the spectrums
    iS = vFFT.size             

    # Compute correct amplitudes 
    vFFTa = 2*np.abs(vFFT)/iS   # ^

    # Take the positive half of the spectrum 
    vFFTa_half = vFFTa[np.arange(iS/2).astype(int)]

    # Create a vector with frequencies of the signal spectrum
    vF_half = fFFTR * np.arange(iS/2)

    # Take only the important amplitudes
    if minamp > 0.0:
        vF_half = vF_half[vFFTa_half >= minamp] 
        vFFTa_half = vFFTa_half[vFFTa_half >= minamp]
    
    return (vFFTa_half, vF_half)

# =====================================================================
# Trigger when start as a script
# =====================================================================
if __name__ == '__main__':
    _LNA_ex0()
