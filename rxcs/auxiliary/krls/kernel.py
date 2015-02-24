"""
This module contains implementation of kernels used by Kernel Recursive Least Squares algorithms. |br|

Implemented kernels:

        - Gaussian kernel

        - Laplace kernel

        - Polynomial kernel

        - Linear kernel

*Authors*:

This implementation is based on Matlab implementation in 'Kafbox' by Steven Van Vaerenbergh.

    2012 - 2014 Steven Van Vaerenbergh (Matlab version: http://sourceforge.net/projects/kafbox/)
    2014        Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0  | 3-DEC-2014 : * Initial version. |br|

*License*:
    BSD 2-Clause

"""
from __future__ import division
import numpy as np


def main(vX1, vX2, strKernel, KernelPar):

    # Check if vX1 is a number? If so, make a 1x1 numpy array
    if type(vX1) is not np.ndarray:
        vX1 = np.array([[vX1]])
    # Check if vX1 is a 1-dim np array? If so, make is a 2-dim numpy array
    elif vX1.ndim == 1:
        vX1 = np.array([vX1]).T
    elif vX1.ndim == 2:
        pass
    else:
        strErr = ('Input vector must be 1dim or 2dim numpy array or an integer')
        raise ValueError(strErr)

    # Check if vX2 is a number? If so, make a 1x1 numpy array
    if type(vX2) is not np.ndarray:
        vX2 = np.array([[vX2]])
    # Check if vX2 is a 1-dim np array? If so, make is a 2-dim numpy array
    elif vX2.ndim == 1:
        vX2 = np.array([vX2]).T
    elif vX2.ndim == 2:
        pass
    else:
        strErr = ('Input vector must be 1dim or 2dim numpy array or an integer')
        raise ValueError(strErr)

    # Get the number of rows
    (iN1, _) = vX1.shape
    (iN2, _) = vX2.shape

    # Gaussian kernel
    if strKernel == 'gauss':

        vNorms1 = np.expand_dims(np.sum(vX1**2,1),1)
        vNorms2 = np.expand_dims(np.sum(vX2**2,1),1)

        mMat1 = np.tile(vNorms1, (1, iN2))
        mMat2 = np.tile(vNorms2.T, (iN1, 1))

        mDist2 = mMat1 + mMat2 - 2*np.dot(vX1,vX2.T)  # full distance matrix
        mK = np.exp(-mDist2/(2*KernelPar**2))

        return mK

    # Laplace kernel
    if strKernel == 'laplace':

        vNorms1 = np.expand_dims(np.sum(vX1**2,1),1)
        vNorms2 = np.expand_dims(np.sum(vX2**2,1),1)

        mMat1 = np.tile(vNorms1, (1, iN2))
        mMat2 = np.tile(vNorms2.T, (iN1, 1))

        mDist2 = mMat1 + mMat2 - 2*np.dot(vX1,vX2.T)  # full distance matrix
        mK = np.exp(-np.sqrt(mDist2)/(2*KernelPar**2))

        return mK

    # Polynomial kernel
    if strKernel == 'gauss-aniso':

        iP = KernelPar['PolynomeOrder']     # Polynome order
        iC = KernelPar['AdditiveConstant']  # Additive constant

        mK = (np.dot(vX1,vX2.T) + iC)**iP
        return mK

    # Linear kernel
    if strKernel == 'linear':

        mK = np.dot(vX1*vX2.T)
        return mK

    # Error: Unknown kernel
    else:
        strErr = ('%s is unknown type of kernel') % ('strKernel')
        raise ValueError(strErr)
