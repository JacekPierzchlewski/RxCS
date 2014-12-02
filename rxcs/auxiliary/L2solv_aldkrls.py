"""
Module contains a solver which finds x which minimizes ||y - Ax||_2 for a given A and y.
The solver uses Kernel Recurive Least Squares algorithm with linear kenrel. |br|

Take a look on  'L2solve_aldkrls_ex0.py' in *examples* directory for examples of using the module.

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0  | 2-DEC-2014 : * Initial version. |br|

*License*:
    BSD 2-Clause

"""

from __future__ import division
import numpy as np
import aldkrls_linker

# =====================================================================
# For a given A and y, find x which minimizes ||y - Ax||_2
# =====================================================================
def main(mA, vY):
    """
    Main function of the module. The function finds x which minimizes ||y - Ax||_2 for a given A and y |br|

    Args:
        mA (numpy array): Matrix A from the above equation

        vY (numpy array): Vector y from the above equation

    Returns:
        vX (numpy array): Vector x which solves the above problem

    """

    dAldKRLS = aldkrls_linker.init()  # Construct a 'aldKRLSL2' object

    (iR, _) = mA.shape                # Get the number of rows in the matrix A

    # Training loop (loop over all rows in the matrix A)
    for i in np.arange(iR):
        dAldKRLS = aldkrls_linker.train(dAldKRLS , mA[i,:], vY[i])

    vX_KRLS = aldkrls_linker.evaluate(dAldKRLS)
    return vX_KRLS
