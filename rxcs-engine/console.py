"""
Module contains console printing functions for the RXCS. All of the console
print in RxCS should be done using function from this module.

This module is a part of the "IRfDUCS" PROJECT 2013 - 2016,

.. module:: console.py

   :platform: Linux, Mac

.. moduleauthor:: Jacek Pierzchlewski, Aalborg University, DK, <jap@es.aau.dk>

"""
import sys
import numpy as np
import time


# =====================================================================
# Print signal pack header
# =====================================================================
def pack(inxPack):

    strPackNumber = '#%d' % (inxPack)
    sys.stdout.write('\n')
    sys.stdout.write(_colors('PROGRESS') + '>>> ' + _colors('ENDC'))
    sys.stdout.write('SIGNAL PACK ')
    sys.stdout.write(_colors('PROGRESS') + strPackNumber + _colors('ENDC'))
    sys.stdout.write(':' + '\n')

    return


# =====================================================================
# Print the sys progress sign (>>) + current stage + name of the current module
# =====================================================================
def progress(strProg, strName):

    sys.stdout.write(_colors('PROGRESS') + '    >> ' + _colors('ENDC'))
    sys.stdout.write(strProg + ': ' + strName + ' \n')

    return


# =====================================================================
# Print the module progress sign (>) + start the timer
# =====================================================================
def module_progress(strInfo):

    sys.stdout.write(_colors('PROGRESS') + '\n        > ' + _colors('ENDC'))
    sys.stdout.write(strInfo + '...')

    # Start the timer
    tStart = time.time()

    return tStart


# =====================================================================
# Finish the module progress print + print the tme of execution
# =====================================================================
def module_progress_done(tStart):

    # Measure the time
    tTime = time.time() - tStart

    strTime = ('done in %.2f seconds') % (tTime)
    sys.stdout.write(_colors('OK') + strTime + _colors('ENDC') + '\n\n\n')

    return


# =====================================================================
# Print a warning
# =====================================================================
def warning(strWarn):

    # Add a tabulator to the warning message
    strWarn = ('          %s') % (strWarn)

    # Write the warning
    sys.stdout.write(_colors('WARN'))
    sys.stdout.write(strWarn)
    sys.stdout.write(_colors('ENDC') + '\n')

    return


# =====================================================================
# Print a bullet + information description + ':' + information
# =====================================================================
def bullet_info(strDesc, strInfo):

    # Write the tabulator with a bullet
    sys.stdout.write('\n' + _colors('BULLET') + '        * ' + _colors('ENDC'))

    # Write the description
    sys.stdout.write(strDesc + ': ')

    # Write the info
    sys.stdout.write(_colors('INFO'))
    sys.stdout.write(strInfo)
    sys.stdout.write(_colors('ENDC'))
    sys.stdout.write('\n')

    return


# =====================================================================
# Print information
# =====================================================================
def info(strInfo):

    # Add a tabulator to the info message
    strInfo = ('          %s') % (strInfo)

    # Write the info
    sys.stdout.write(_colors('OK'))
    sys.stdout.write(strInfo)
    sys.stdout.write(_colors('ENDC') + '\n')

    return


# =====================================================================
# Print a note (an information without coloring)
# =====================================================================
def note(strNote):

    # Add a tabulator to the info message
    strNote = ('          %s') % (strNote)

    # Write the info
    sys.stdout.write(strNote)
    sys.stdout.write('\n')

    return


# =====================================================================
# Print a bullet + name of the parameter + the parameter
# =====================================================================
def bullet_param(strName, iVal, strForm, strUnit):

    # Write the tabulator with a bullet
    sys.stdout.write('\n' + _colors('BULLET') + '        * ' + _colors('ENDC'))

    # Run the engine of parameter print
    _param(strName, iVal, strForm, strUnit)

    return


# =====================================================================
# Print name of the parameter + the parameter
# =====================================================================
def param(strName, iVal, strForm, strUnit):

    # Write the tabulator
    sys.stdout.write('          ')

    # Run the engine of parameter print
    _param(strName, iVal, strForm, strUnit)

    return


# =====================================================================#
# Colors dictionary
# =====================================================================
def _colors(strKey):

    # Define colors
    dColors = {}
    dColors['PURPLE'] = '\033[95m'
    dColors['BLUE'] = '\033[94m'
    dColors['GREEN'] = '\033[92m'
    dColors['YELLOW'] = '\033[93m'
    dColors['RED'] = '\033[91m'
    dColors['BLACK'] = '\033[30m'
    dColors['DARK_MAGENTA'] = '\033[35m'
    dColors['AUQA'] = '\033[96m'
    dColors['BLUE_BG'] = '\033[44m'
    dColors['DARK_BLUE'] = '\033[34m'
    dColors['DARK_GREEN'] = '\033[32m'
    dColors['GREY30'] = '\033[30m'
    dColors['GREY70'] = '\033[97m'
    dColors['ENDC'] = '\033[0m'

    # Define colors for communication
    dColors['PROGRESS'] = dColors['DARK_MAGENTA']
    dColors['OK'] = dColors['DARK_GREEN']
    dColors['ERROR'] = dColors['RED']
    dColors['INFO'] = dColors['BLUE']
    dColors['BULLET'] = dColors['DARK_MAGENTA']
    dColors['WARN'] = dColors['RED']

    # Return the correct color
    return dColors[strKey]


# =====================================================================
# The engine of paramer print
# =====================================================================
def _param(strName, iVal, strForm, strUnit):

    # The name of the function (for error purposes)
    strFunc = 'rxcs.console._param'

    # ----------------------------------------------------------------

    # Write the parameter name
    sys.stdout.write(strName + ': ')

    # Check the length of the format string, it should be 1 or 2
    lForm = len(strForm)
    if lForm < 1 or lForm > 2:
        strErr = strFunc + ' : '
        strErr = strErr + ('Parameter format string must be 1 or 2 characters')
        raise Exception(strErr)

    # ----------------------------------------------------------------

    # Recalculate the unit to coefficient, if it is asked for
    if strForm[0] == '-':  # <- the function should recalculate the unit
        (iCoef, strUnitRecalc) = _val2unit(iVal)

    elif strForm[0] == 's':  # <- the parameter contains seconds
        _param_time_write(iVal, strForm)
        return

    else:  # <- there is a correct unit already given

        # Get the name of the magnitude unit
        strUnitRecalc = strForm[0]

        # Get the correct coefficient for the 2nd representation
        iCoef = _unit2coef(strUnitRecalc)

    # Recalculate the value of the parameter
    iVal_recal = iVal / iCoef

    # Create a string with value
    if iCoef == 1:  # <- there is no need to recalculate the value

        # Put the number as it is, but pay attention if it is float or int
        if isinstance(iVal, int):
            strVal = ('%d') % (iVal_recal)
        else:
            strVal = ('%.3f') % (iVal_recal)

    elif np.isinf(iCoef):  # <- the value is an infinite
        strVal = ('inf')

    else:  # <- the value should be recalculated
        strVal = ('%.3f %s') % (iVal_recal, strUnitRecalc)

    # Write the value
    sys.stdout.write(_colors('INFO') + strVal + _colors('ENDC') + ' ')

    # ----------------------------------------------------------------
    # 2nd representation:

    # If the string is has 2 characters, print also the recalculated number
    # (the 2nd representation)
    if lForm == 2:

        # Check if the user wants it to be recalculated to a given magnitude
        # or the function should decide
        if strForm[1] == '-':  # <- the function should decide

            # Get the correct coefficient and magnitude unit
            (iCoef2, strUnit2Recalc) = _val2unit(iVal)

        else:  # <- the user gives the magnitude representation

            # Get the name of the magnitude unit
            strUnit2Recalc = strForm[1]

            # Get the correct coefficient for the 2nd representation
            iCoef2 = _unit2coef(strUnit2Recalc)

        # If the magnitudes are identical, do no print the 2nd representation
        if iCoef != iCoef2:

            # Recalculate the value to the 2nd representation
            iVal_2Rep = iVal / iCoef2

            # Create the string with the 2nd representation
            if iCoef2 == 1:
                strVal2 = ('%d') % (iVal_2Rep)
            else:
                strVal2 = ('%.3f %s') % (iVal_2Rep, strUnit2Recalc)

            # Print out the 2nd representation
            sys.stdout.write('(')
            sys.stdout.write(_colors('INFO') + strVal2 + _colors('ENDC'))
            sys.stdout.write(')' + ' ')

    # ----------------------------------------------------------------

    # Print the unit, if it is not empty
    lUnit = len(strUnit)
    if lUnit > 0:
        sys.stdout.write(_colors('INFO'))
        sys.stdout.write('[' + strUnit + ']')
        sys.stdout.write(_colors('ENDC'))

    # ----------------------------------------------------------------

    sys.stdout.write('\n')

    return


# =====================================================================
# The engine of time paramer print
# =====================================================================
def _param_time_write(iVal, strForm):

    # The name of the function (for error purposes)
    strFunc = 'rxcs.console._param_time_write'

    # ----------------------------------------------------------------

    # Create a string with seconds
    strSeconds = ('%d [seconds]') % (iVal)

    # Print the seconds
    sys.stdout.write(_colors('INFO') + strSeconds + _colors('ENDC') + ' ')

    # Get the length of the format string
    lForm = len(strForm)

    # ----------------------------------------------------------------
    # Add an info about the hours, if needed
    if lForm == 2:
        if not (strForm[1] == 'h'):
            strErr = strFunc + ' : '
            strErr = strErr + ('If the first argument with parameter format ')
            strErr = strErr + (' is >s< then the second must be >h< or empty!')
            raise Exception(strErr)

        # Recalculate seconds to hours and create a propoer string with hours
        iHours = iVal/3600
        strHours = ('%.2f [hours]') % (iHours)

        # Print the hours
        sys.stdout.write('(')
        sys.stdout.write(_colors('INFO') + strHours + _colors('ENDC'))
        sys.stdout.write(')')

    # ----------------------------------------------------------------
    sys.stdout.write('\n')

    return


# =====================================================================
# Recalculate unit string to unit coefficient
# =====================================================================
def _unit2coef(strUnit):

    # The name of the function (for error purposes)
    strFunc = 'rxcs.console._unit2coef'

    # ----------------------------------------------------------------

    # femto
    if strUnit == 'f':
        iCoef = 1e-15

    # piko
    elif strUnit == 'p':
        iCoef = 1e-12

    # nano
    elif strUnit == 'n':
        iCoef = 1e-9

    # micro
    elif strUnit == 'u':
        iCoef = 1e-6

    # mili
    elif strUnit == 'm':
        iCoef = 1e-3

    # none
    elif strUnit == ' ':
        iCoef = 1

    # kilo
    elif strUnit == 'k':
        iCoef = 1e3

    # mega
    elif strUnit == 'M':
        iCoef = 1e6

    # giga
    elif strUnit == 'G':
        iCoef = 1e9

    # tera
    elif strUnit == 'T':
        iCoef = 1e12

    # hours
    elif strUnit == 'h':
        iCoef = 3600

    # ----------------------------------------------------------------
    # Unknown unit
    else:
        strErr = strFunc + ' : '
        strErr = strErr + ('> %s <  is an unknown parameter unit') % (strUnit)
        raise Exception(strErr)

    # ----------------------------------------------------------------

    return iCoef


# =====================================================================
# Recalculate value to unit (string) and unit coefficient
# =====================================================================
def _val2unit(iVal):

    # femto
    if iVal < 1e-12:
        iCoef = 1e-15
        strUnit = 'f'

    # piko
    elif iVal < 1e-9:
        iCoef = 1e-12
        strUnit = 'p'

    # nano
    elif iVal < 1e-6:
        iCoef = 1e-9
        strUnit = 'n'

    # micro
    elif iVal < 1e-3:
        iCoef = 1e-6
        strUnit = 'u'

    # mili
    elif iVal < 1:
        iCoef = 1e-3
        strUnit = 'm'

    # none
    elif iVal < 1e3:
        iCoef = 1
        strUnit = ' '

    # kilo
    elif iVal < 1e6:
        iCoef = 1e3
        strUnit = 'k'

    # mega
    elif iVal < 1e9:
        iCoef = 1e6
        strUnit = 'M'

    # giga
    elif iVal < 1e12:
        iCoef = 1e9
        strUnit = 'G'

    # infinite
    elif np.isinf(iVal):
        iCoef = np.inf
        strUnit = ''

    # tera
    else:
        iCoef = 1e12
        strUnit = 'T'

    # ----------------------------------------------------------------

    return (iCoef, strUnit)
