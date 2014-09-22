"""
Module contains console printing functions for the RXCS. |br|
All of the console print in RxCS should be done using functions
from this module.

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    0.1  | 14-MAY-2014 : * Initial version. |br|
    0.2  | 15-MAY-2014 : * Docstrings added.
    0.21 | 15-MAY-2014 : * New colors ('PARAM' + 'OK') added to the dictionary


*License*:
    BSD 2-Clause

"""
from __future__ import division
import sys
import numpy as np
import time


# =====================================================================
# Print signal pack header
# =====================================================================
def pack(inxPack):
    """
    .. role:: bash(code)
      :language: bash

    Function prints header of the signal pack processed by RxCS frames. |br|

    The function takes care of the proper coloring of the console output. |br|

    >>> console.pack(1)

    gives an output:

    :bash:`>>> SIGNAL PACK #1:`

    Args:
        inxPack (int): Index of the current signal pack

    Returns:
        nothing

    """

    strPackNumber = '#%d' % (inxPack)
    sys.stdout.write('\n')
    sys.stdout.write(_colors('PROGRESS') + '>>> ' + _colors('ENDC'))
    sys.stdout.write('SIGNAL PACK ')
    sys.stdout.write(_colors('PROGRESS') + strPackNumber + _colors('ENDC'))
    sys.stdout.write(':' + '\n')
    sys.stdout.flush()

    return


# =====================================================================
# Print the sys progress sign + current stage + name of the current module
# =====================================================================
def progress(strStage, strModule):
    """
    .. role:: bash(code)
      :language: bash

    Function prints progress of the RxCS frames. |br|
    It prints the progress sign ('>>') + the current stage (signal generation,
    sampler, reconstruction, etc...) + name of the current module. |br|

    The function takes care of the proper coloring of the console output. |br|

    >>> console.progress('Signal generator', 'Random multitone')

    gives an output:

    :bash:`|    >> Signal generator: Random multitone`


    Args:
        strStage (string): name of the stage |br|
        strModule (string): name of the module

    Returns:
        nothing
    """

    sys.stdout.write(_colors('PROGRESS') + '    >> ' + _colors('ENDC'))
    sys.stdout.write(strStage + ': ' + strModule + ' \n')
    sys.stdout.flush()

    return


# =====================================================================
# Print the module progress sign (>) + start the timer
# =====================================================================
def module_progress(strInfo):
    """
    Function prints an info about a module progress.
    The info is preceded by a tabulator and a module progress sign ('>'). |br|

    Additionally, the function starts a time counter. |br|

    The function takes care of the proper coloring of the console output. |br|

    >>> console.module_progress('The module X is starting')

    gives an output:

    :bash:`|        > The module X is starting...`


    Args:
        strInfo (string): progress info to be printed

    Returns:
        tStart (float): time stamp of the start
    """

    sys.stdout.write(_colors('PROGRESS') + '\n        > ' + _colors('ENDC'))
    sys.stdout.write(strInfo + '...')
    sys.stdout.flush()

    # Start the timer
    tStart = time.time()

    return tStart


# =====================================================================
# Finish the progress print + print the tme of execution
# =====================================================================
def progress_done(tStart):
    """
    Function adds 'done' to a console message previously printed by a
    'module_progress' function. |br|

    Additionally, the function print an info about an execution time of a
    module, based on the time stamp of the start of the module.  |br|

    The function takes care of the proper coloring of the console output. |br|

    >>> tStart = console.module_progress('The module X is starting')
    >>> time.sleep(1)
    >>> console.module_progress_done(tStart)

    gives an output:

    :bash:`|        > The module X is starting...done in 1.00 seconds`

    Args:
        tStart (float): time stamp of the start

    Returns:
        nothing
    """

    # Measure the time
    tTime = time.time() - tStart

    strTime = ('done in %.2f seconds') % (tTime)
    sys.stdout.write(_colors('OK') + strTime + _colors('ENDC'))
    sys.stdout.flush()

    return


# =====================================================================
# Finish the module progress print + print the tme of execution
# =====================================================================
def module_progress_done(tStart):
    """
    Function adds 'done' to a console message previously printed by a
    'module_progress' function. |br|

    Additionally, the function print an info about an execution time of a
    module, based on the time stamp of the start of the module.  |br|

    The function takes care of the proper coloring of the console output. |br|

    >>> tStart = console.module_progress('The module X is starting')
    >>> time.sleep(1)
    >>> console.module_progress_done(tStart)

    gives an output:

    :bash:`|        > The module X is starting...done in 1.00 seconds`

    Args:
        tStart (float): time stamp of the start

    Returns:
        nothing
    """

    # Measure the time
    tTime = time.time() - tStart

    strTime = ('done in %.2f seconds') % (tTime)
    sys.stdout.write(_colors('OK') + strTime + _colors('ENDC') + '\n\n\n')
    sys.stdout.flush()

    return

# =====================================================================
# Finish the module progress print + print the time of execution
# (with 1 newline instead of 3)
# =====================================================================
def module_progress_doneNoNew(tStart):
    """
    Function adds 'done' to a console message previously printed by a
    'module_progress' function. |br|

    Additionally, the function print an info about an execution time of a
    module, based on the time stamp of the start of the module.  |br|

    This function do not add new lines after 'done'.

    The function takes care of the proper coloring of the console output. |br|

    >>> tStart = console.module_progress('The module X is starting')
    >>> time.sleep(1)
    >>> console.module_progress_doneNoNew(tStart)

    gives an output:

    :bash:`|        > The module X is starting...done in 1.00 seconds`

    Args:
        tStart (float): time stamp of the start

    Returns:
        nothing
    """

    # Measure the time
    tTime = time.time() - tStart

    strTime = ('done in %.2f seconds') % (tTime)
    sys.stdout.write(_colors('OK') + strTime + _colors('ENDC') + '\n')
    sys.stdout.flush()

    return

# =====================================================================
# Print a warning
# =====================================================================
def warning(strWarn):
    """
    Function prints a warning preceded by a proper tabulator. |br|

    The function takes care of the proper coloring of the console output. |br|

    >>> console.warning('Mind the gap!')

    :bash:`|          Mind the gap!`

    Args:
        strWarn (string): warning to be printed

    Returns:
        nothing
    """

    # Add a tabulator to the warning message
    strWarn = ('          %s') % (strWarn)

    # Write the warning
    sys.stdout.write(_colors('WARN'))
    sys.stdout.write(strWarn)
    sys.stdout.write(_colors('ENDC') + '\n')
    sys.stdout.flush()

    return


# =====================================================================
# Print information
# =====================================================================
def info(strInfo):
    """
    Function prints an info preceded by a proper tabulator. |br|

    The function takes care of the proper coloring of the console output. |br|

    >>> console.info('Very important info')

    :bash:`|          Very important info`

    Args:
        strInfo (string): info to be printed

    Returns:
        nothing
    """

    # Add a tabulator to the info message
    strInfo = ('          %s') % (strInfo)

    # Write the info
    sys.stdout.write(_colors('INFO'))
    sys.stdout.write(strInfo)
    sys.stdout.write(_colors('ENDC') + '\n')
    sys.stdout.flush()

    return


# =====================================================================
# Print a bullet + information description + ':' + information
# =====================================================================
def bullet_info(strDesc, strInfo):
    """
    Function prints an info preceded by a proper tabulator, an info
    bullet '*' and a description of the info. |br|

    The function takes care of the proper coloring of the console output. |br|

    >>> console.bullet_info('Please remeber', 'mind the gap!')

    gives an output

    :bash:`|          * Please remeber: mind the gap!`

    Args:
        strDesc (string): description of the info |br|
        strInfo (string): info to be printed

    Returns:
        nothing
    """

    # Write the tabulator with a bullet
    sys.stdout.write('\n' + _colors('BULLET') + '        * ' + _colors('ENDC'))

    # Write the description
    sys.stdout.write(strDesc + ': ')

    # Write the info
    sys.stdout.write(_colors('BULLET_INFO'))
    sys.stdout.write(strInfo)
    sys.stdout.write(_colors('ENDC'))
    sys.stdout.write('\n')
    sys.stdout.flush()

    return


# =====================================================================
# Print a note (an information without coloring)
# =====================================================================
def note(strNote):
    """
    Function prints a note preceded by a proper tabulator. |br|

    There is no coloring of the output. |br|

    >>> console.note('mind the gap!')

    :bash:`|          mind the gap!`

    Args:
        strInfo (string): info to be printed

    Returns:
        nothing
    """

    # Add a tabulator to the info message
    strNote = ('          %s') % (strNote)

    # Write the info
    sys.stdout.write(strNote)
    sys.stdout.write('\n')
    sys.stdout.flush()

    return


# =====================================================================
# Print name of the parameter + the parameter
# =====================================================================
def param(strName, iVal, strForm, strUnit):
    """
    Function prints a parameter and a parameter unit.
    The parameter is preceeded by a tabulator and a parameter name. |br|

    The parameter value is recalculated to a requested order of magnitude,
    or the function may decide itself about the order of magnitude. The
    formatting string (3rd parameter) controls the order of magnitude of
    a printed value. If it contains the '-' character, the function will
    decide about an order of magnitude. If it contains a magnitude unit
    symbol, the function recalculates the value to the given order of
    magnitude. |br|

    The formatting string (3rd parameter) must contain one or two
    characters. If there are two characters, the value is printed in two
    orders of magnitude, second is in the parantheses. |br|

    Available symbols of orders of magnitude:

        (femto):  'f'  |br|
        (pico):   'p'  |br|
        (nano):   'n'  |br|
        (micro):  'u'  |br|
        (mili):   'm'  |br|
        (none):   ' '  |br|
        (kilo):   'k'  |br|
        (Mega):   'M'  |br|
        (Giga):   'G'  |br|
        (Tera):   'T'  |br|

        (second)  's'  |br|
        (hour):   'h'  |br|
    |br|

    If the first character in the formatting string is 's', then the
    parameter is treated as time expressed in seconds. In this case
    the second character may either not exists in the string, or be equal
    to 'h'. In the latter case the time will be also expressed in hours. |br|

    The last argument is a unit name which will be printed after the values
    of the paramter. If the first character in the formatting string is
    's', then the last argument shuld be empty. |br|

    The function takes care of the proper coloring of the console output. |br|

    Usage examples:

    >>> console.param('Size of a hard drive',500*1e9,'G ','bytes')

    :bash:`|          Size of a hard drive: 500.000 G (500000000000) [bytes]`

    >>> console.param('Dist. from Aalborg to Auckland',10889,'k ','miles')

    :bash:`|          Dist. from Aalborg to Auckland: 10.889 k (10889) [miles]`

    >>> console.param('The number of people in DK',5627235,'k-','souls')

    :bash:`|          The number of people in DK: 5627.235 k (5.627 M) [souls]`

    >>> console.param('>E.T.< running time',115*60,'sh','')

    :bash:`|          >E.T< running time: 6900.0 [seconds] (1.92 [hours])`

    >>> console.param('Honda Civic Type R 0-60',6.6,'s','')

    :bash:`|          Honda Civic Type R 0-60: 6.6 [seconds]`


    Args:
        strName (string): name of the parameter |br|
        iVal (float): value |br|
        strForm (string): format string |br|
        strUnit (string): unit |br|

    Returns:
        nothing
    """

    # Write the tabulator
    sys.stdout.write('          ')

    # Run the engine of parameter print
    _param(strName, iVal, strForm, strUnit)

    return


# =====================================================================
# Print a bullet + name of the parameter + the parameter
# =====================================================================
def bullet_param(strName, iVal, strForm, strUnit):
    """
    Function prints a parameter preceded by a proper tabulator, a bullet
    and a parameter name. |br|

    The function is identical to the previous 'param' function, the only
    difference is a bullet added before the parameter name. Please refer
    to the 'param' function for description of the function and its input
    parameters. |br|

    """

    # Write the tabulator with a bullet
    sys.stdout.write('\n' + _colors('BULLET') + '        * ' + _colors('ENDC'))

    # Run the engine of parameter print
    _param(strName, iVal, strForm, strUnit)

    return


# =====================================================================
# The engine of parameter print
# =====================================================================
def _param(strName, iVal, strForm, strUnit):
    """
    It is an engine of the formated parameter printing. |br|

    The input to the fuctcion is identical to the previous 'param' function.
    Please refer to the 'param' function for description of the function and
    its input parameters. |br|

    """

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
    sys.stdout.write(_colors('PARAM') + strVal + _colors('ENDC') + ' ')

    # ----------------------------------------------------------------
    # 2nd representation:

    # If the string has 2 characters, print also the recalculated number
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
            sys.stdout.write(_colors('PARAM') + strVal2 + _colors('ENDC'))
            sys.stdout.write(')' + ' ')

    # ----------------------------------------------------------------

    # Print the unit, if it is not empty
    lUnit = len(strUnit)
    if lUnit > 0:
        sys.stdout.write(_colors('PARAM'))
        sys.stdout.write('[' + strUnit + ']')
        sys.stdout.write(_colors('ENDC'))

    # ----------------------------------------------------------------

    sys.stdout.write('\n')

    return


# =====================================================================
# The engine of time paramer print
# =====================================================================
def _param_time_write(iVal, strForm):
    """
    It is an engine of the formated time parameter printing. |br|

    Args:
        iVal (float): value
        strForm (string): format string

    Returns:
        nothing
    """

    # The name of the function (for error purposes)
    strFunc = 'rxcs.console._param_time_write'

    # ----------------------------------------------------------------

    # Create a string with seconds
    strSeconds = ('%.1f [seconds]') % (iVal)

    # Print the seconds
    sys.stdout.write(_colors('PARAM') + strSeconds + _colors('ENDC') + ' ')

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
        sys.stdout.write(_colors('PARAM') + strHours + _colors('ENDC'))
        sys.stdout.write(')')

    # ----------------------------------------------------------------
    sys.stdout.write('\n')

    return


# =====================================================================
# Recalculate a unit symbol to a unit coefficient
# =====================================================================
def _unit2coef(strUnit):

    """
    Function returns a unit coefficient based on a unit symbol.
    Available unit names, symbols and coefficients:

        (femto):  'f' = 1e-15
        (pico):   'p' = 1e-12
        (nano):   'n' = 1e-9
        (micro):  'u' = 1e-6
        (mili):   'm' = 1e-3
        (none):   ' ' = 1
        (kilo):   'k' = 1e3
        (Mega):   'M' = 1e6
        (Giga):   'G' = 1e9
        (Tera):   'T' = 1e12

        (hour):   'h' = 3600

    Args:
        strUnit (string): key of the unit

    Returns:
        iCoef (int): unit coefficient
    """

    # The name of the function (for error purposes)
    strFunc = 'rxcs.console._unit2coef'

    # ----------------------------------------------------------------

    # femto
    if strUnit == 'f':
        iCoef = 1e-15

    # pico
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

    # Mega
    elif strUnit == 'M':
        iCoef = 1e6

    # Giga
    elif strUnit == 'G':
        iCoef = 1e9

    # Tera
    elif strUnit == 'T':
        iCoef = 1e12

    # hour
    elif strUnit == 'h':
        iCoef = 3600

    # ----------------------------------------------------------------
    # Unknown unit
    else:
        strErr = strFunc + ' : '
        strErr = strErr + ('> %s <  is an unknown unit symbol') % (strUnit)
        raise Exception(strErr)

    # ----------------------------------------------------------------

    return iCoef


# =====================================================================
# Recalculate a value to a unit symbol and a unit coefficient
# =====================================================================
def _val2unit(iVal):
    """
    Function returns the unit coefficient and a unit symbol.

    Args:
        iVal (float): value

    Returns:
        iCoef (int): unit coefficient
        strUnit (string): unit symbol
    """

    # femto
    if iVal < 1e-12:
        iCoef = 1e-15
        strUnit = 'f'

    # pico
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

    # Mega
    elif iVal < 1e9:
        iCoef = 1e6
        strUnit = 'M'

    # Giga
    elif iVal < 1e12:
        iCoef = 1e9
        strUnit = 'G'

    # Infinite
    elif np.isinf(iVal):
        iCoef = np.inf
        strUnit = ''

    # Tera
    else:
        iCoef = 1e12
        strUnit = 'T'

    # ----------------------------------------------------------------

    return (iCoef, strUnit)


# =====================================================================#
# Colors dictionary
# =====================================================================
def _colors(strKey):
    """
    Function gives access to the RxCS console colors dictionary. The
    Function returns a proper console color formating string (ANSI colors)
    based on the key given to the function. |br|

    Available keys:

        'PURPLE'
        'BLUE'
        'GREEN'
        'YELLOW'
        'RED'
        'BLACK'
        'DARK_MAGENTA'
        'AQUA'
        'BLUE_BG'
        'DARK_BLUE'
        'DARK_GREEN'
        'GREY30'
        'GREY70'

        'PROGRESS'          -> color for progress signs ('>>>', '>>', '>')
        'INFO'              -> color for info messages
        'BULLET_INFO'       -> color for bullet info messages
        'BULLET'            -> color for bullets ('*')
        'WARN'              -> color for warning messages
        'PARAM'             -> color for parameters printing
        'OK'                -> color for good messages
        'ENDC'              -> console formatting string which switches of
                               the coloring

    Args:
        strKey (string): key of the color

    Returns:
        strColor (string): console color formating string
    """

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

    # Define colors for communication
    dColors['PROGRESS'] = dColors['DARK_MAGENTA']
    dColors['INFO'] = dColors['DARK_GREEN']
    dColors['BULLET_INFO'] = dColors['BLUE']
    dColors['BULLET'] = dColors['DARK_MAGENTA']
    dColors['WARN'] = dColors['RED']
    dColors['PARAM'] = dColors['BLUE']
    dColors['OK'] = dColors['DARK_GREEN']
    dColors['ENDC'] = '\033[0m'

    # Return the correct color
    strColor = dColors[strKey]
    return strColor
