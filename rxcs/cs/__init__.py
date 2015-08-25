
# Import signal dictionaries
import dict

# Import L1 reconstruction which uses cvxopt
cvxoptOK = 1
try:
    import cvxopt
except ImportError:
    print('RxCS DEPENDENCY WARNING !!!                                                ')
    print('RxCS Warning: no \'cvxopt\' software found! Some reconstruction methods will not work!')
    print('')
    cvxoptOK = 0
    
if cvxoptOK == 1:
    from cvxoptL1 import cvxoptL1


# Import irls L1 reconstruction
import irlsL1


# Import Theta matrix generator
from makeTheta import makeTheta

