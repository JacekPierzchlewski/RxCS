"""
This script is a simple example of how to use the single branch upconverter. |br|

In this example a baseband signal 200kHz is generated and upconverted with
2MHz carrier. 

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1,0  | 04-SEP-2015  : * Version 1.0 released. |br|

*License*:
    BSD 2-Clause
"""

import rxcs
import scipy.signal as scsig
import matplotlib.pyplot as plt


def _upconvert_ex0():

    # Things on the table:
    gaussNoise = rxcs.sig.gaussNoise()      # Gaussian noise generator
    upconvert = rxcs.sig.radio.upconvert()  # Upconversion

    # Settings:
    TIME = 1        # Time [1 sec]
    FREQ = 10e6     # Representation sampling frequency [10 MHz]

    # Configure the generator
    gaussNoise.fR = FREQ
    gaussNoise.tS = TIME
    gaussNoise.fMax = 200e3  # Maximum freq. component in the signal [200 kHz]

    # Configure the upconversion
    upconvert.fR = FREQ
    upconvert.tS = TIME
    upconvert.fC = 2e6    # Carrier frequency
    
    # ------------------------------------------------------------------------
    # Run the system
    gaussNoise.run()                   # Generate the signal...

    upconvert.mSig = gaussNoise.mSig   # ...connect it to the upconversion...   
    upconvert.run()                    # ...and upconvert it

    # -----------------------------------------------------------------
    # Analyze the signal and plot it
    vSigBase = gaussNoise.mSig[0, :]    # Baseband signal
    vSigUp = upconvert.mSig[0, :]      # Radio signal

    (vFxxB, vPxxB) = scsig.welch(vSigBase, fs=gaussNoise.fR, nperseg=1024, noverlap=512)
    (vFxxU, vPxxU) = scsig.welch(vSigUp, fs=gaussNoise.fR, nperseg=1024, noverlap=512)
    
    hFig1 = plt.figure(1)
    hSubPlot1 = hFig1.add_subplot(111)
    hSubPlot1.grid(True)
    hSubPlot1.set_title('Spectrum of the signals (psd)')
    hSubPlot1.set_xlabel('Frequency [kHz]')
    hSubPlot1.plot(vFxxB/1e3, vPxxB, '-', label='Baseband signal')
    hSubPlot1.plot(vFxxU/1e3, vPxxU, '-', label='Radio signal')
    hSubPlot1.legend()
    plt.show(block=True)


# =====================================================================
# Trigger when start as a script
# =====================================================================
if __name__ == '__main__':
    _upconvert_ex0()
