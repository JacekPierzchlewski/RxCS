from __future__ import division
import rxcs
import numpy as np
import matplotlib.pyplot as plt

def _dict_IDFT_ex0():

    # -----------------------------------------------------------------
    # Generate settings for the IDFT dictionary

    # Start the configuration dictionary
    dCSConf = {}

    # Time of the dictionary is 1 ms
    dCSConf['tS'] = 1e-3

    # The signal representation sampling frequency is 40 kHz
    dCSConf['fR'] = 4e4

    # The frequency separation between tones
    dCSConf['fDelta'] = 1e3

    # The number of tones in the dictionary
    dCSConf['nTones'] = 10

    # -----------------------------------------------------------------
    # Generate the IDFT dictionary
    (mIDFT, dDict) = rxcs.cs.dict.IDFToNoDC.main(dCSConf)

    # Get the signal time vector from the dictionary
    vT = dDict['vT']

    # -----------------------------------------------------------------
    # Generate the signal using the dictionary

    # Vector with Fourier coefficients
    vFcoef = np.zeros((1,20)).astype(complex)
    vFcoef[0, 0] = 1
    vFcoef[0, 19] = 1

    # Generate a signal and change its shape to a single vector
    vSig = np.real(np.dot(vFcoef,mIDFT))
    vSig.shape = (vSig.size,)


    # -----------------------------------------------------------------
    # Plot signal in the time domain
    hFig1 = plt.figure(1)
    hSubPlot1 = hFig1.add_subplot(111)
    hSubPlot1.grid(True)
    hSubPlot1.set_title('Signal')
    hSubPlot1.set_xlabel('Time [s]')
    hSubPlot1.plot(vT, vSig)
    hSubPlot1.set_xlim(min(vT), max(vT))
    hSubPlot1.set_ylim(-1.1, 1.1)
    plt.show(block=True)

# =====================================================================
# Trigger when start as a script
# =====================================================================
if __name__ == '__main__':
    _dict_IDFT_ex0()
