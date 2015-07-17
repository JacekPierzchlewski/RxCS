"""
            This module contains tests for _RxCSobject class.

            License:
                    BSD 2-clause

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

            Last modification:
                    19 June 2015
"""
import numpy as np

# Import the main tested object
from rxcs.RxCSobject import _RxCSobject

# Import errors
from rxcs.RxCSobject import ParameterMissingError
from rxcs.RxCSobject import ParameterTypeError
from rxcs.RxCSobject import ElementTypeError
from rxcs.RxCSobject import AllowedValuesError
from rxcs.RxCSobject import RelationalError
from rxcs.RxCSobject import SizeError
from rxcs.RxCSobject import NDimError
from rxcs.RxCSobject import DimSizError
from rxcs.RxCSobject import UniqnessError


class RxCS_object_tester1():

    def __init__(self):
        self.iMaxCols = 150   # The max number of columns in the console output
        self._iNTests = 0     # Index of the test

    def run(self):

        # Are mandatory defined parameters in place?
        self.__defined_parameters()

        # Type check
        self.__types_of_parameters()
        self.__types_of_elements_of_parameters()

        # Allowed elements:
        self.__allowed_elements()

        # Relational restrictions:
        self.__relational_restrictions_on_numbers()

        self.__relational_restrictions_on_tuples()
        self.__relational_restrictions_on_lists()

        self.__relational_restrictions_on_NumpyVectors()
        self.__relational_restrictions_on_NumpyMatrices()

        # Size restriction
        self.__size_restrictions()

        # Restrictions on the number of dimensions
        self.__NDim_restrictions()

        # Restrictions on sizes of dimensions
        self.__DimSiz_restrictions()
        
        # Restrictions of uniqness of elements
        self.__Unique_restrictions()

        # Optional parameter, which default value depends on another parameter
        self.__Opt_default()


    # Tests on check of mandatory parameters
    def __defined_parameters(self):

        print('TESTS ON DEFINED PARAMETERS:')
        self.__mandatory_after_optional()
        self.__mandatory_is_not_given()
        self.__mandatory_is_given()
        self.__optional_is_not_given()
        print('')

    # Tests on checks of types of parameters
    def __types_of_parameters(self):
        print('TESTS ON TYPES OF PARAMETERS:')
        self.__type_correct_int()
        self.__type_incorrect_int()
        self.__type_correct_tuple()
        self.__type_incorrect_tuple_lists()
        print('')

    # Tests on checks of types of parameters' elements
    def __types_of_elements_of_parameters(self):
        print('TESTS ON TYPES OF ELEMENTS OF PARAMETERS:')
        self.__type_of_elements_correct_floats_in_list()
        self.__type_of_elements_incorrect_floats_in_tuple()
        self.__type_of_elements_incorrect_dicts_in_tuple()
        self.__type_of_elements_incorrect_elem_in_dict()
        self.__type_of_elements_correct_long_Numpy_vector()
        self.__type_of_elements_incorrect_float_in_Numpy_vector()
        self.__type_of_elements_correct_long_Numpy_matrix()
        self.__type_of_elements_incorrect_long_Numpy_matrix()
        self.__type_of_elements_incorrect_dict_in_long_list()
        print('')

    # Tests on checks of allowed elements
    def __allowed_elements(self):
        print('TESTS ON ALLOWED VALUES OF PARAMETERS:')
        self.__allowed_values_correct_string()
        self.__allowed_values_inccorrect_string()
        self.__allowed_values_correct_number()
        self.__allowed_values_inccorrect_number()
        self.__allowed_values_correct_tuple()
        self.__allowed_values_incorrect_list()
        self.__allowed_values_incorrect_vector()
        self.__allowed_values_correct_matrix()
        self.__allowed_values_incorrect_list_with_allowed_values()
        print('')

    # Tests on checks of relational restrictions imposed on numbers
    def __relational_restrictions_on_numbers(self):
        print('TESTS ON RELATIONAL RESTRICTIONS ON NUMBERS:')
        self.__relational_restriction_correct_parameter_vs_number()
        self.__relational_restriction_incorrect_parameter_vs_number()
        self.__relational_restriction_correct_parameter_vs_parameter()
        self.__relational_restriction_incorrect_parameter_vs_parameter()
        print('')

    # Tests on checks of relational restrictions imposed on tuples
    def __relational_restrictions_on_tuples(self):
        print('TESTS ON RELATIONAL RESTRICTIONS ON TUPLES:')
        self.__relational_restriction_correct_tuple_vs_number()
        self.__relational_restriction_incorrect_tuple_vs_number()
        self.__relational_restriction_correct_tuple_vs_parameter()
        self.__relational_restriction_incorrect_tuple_vs_parameter()
        self.__relational_restriction_correct_tuple_vs_list()
        self.__relational_restriction_incorrect_tuple_vs_list()
        print('')

    # Tests on checks of relational restrictions imposed on lists
    def __relational_restrictions_on_lists(self):
        print('TESTS ON RELATIONAL RESTRICTIONS ON LISTS:')
        self.__relational_restriction_correct_list_vs_number()
        self.__relational_restriction_incorrect_list_vs_number()
        self.__relational_restriction_correct_list_vs_parameter()
        self.__relational_restriction_incorrect_list_vs_parameter()
        self.__relational_restriction_correct_list_vs_tuple()
        self.__relational_restriction_incorrect_list_vs_tuple()
        self.__relational_restriction_correct_list_vs_list()
        self.__relational_restriction_incorrect_list_vs_list()
        self.__relational_restriction_correct_list_vs_NumpyVector()
        self.__relational_restriction_incorrect_list_vs_NumpyVector()
        print('')

    # Tests on checks of relational restrictions imposed on Numpy Vectors
    def __relational_restrictions_on_NumpyVectors(self):
        print('TESTS ON RELATIONAL RESTRICTIONS ON NUMPY VECTORS:')
        self.__relational_restriction_correct_NumpyVector_vs_number()
        self.__relational_restriction_incorrect_NumpyVector_vs_number()
        self.__relational_restriction_correct_NumpyVector_vs_parameter()
        self.__relational_restriction_incorrect_NumpyVector_vs_parameter()
        self.__relational_restriction_correct_NumpyVector_vs_tuple()
        self.__relational_restriction_incorrect_NumpyVector_vs_tuple()
        self.__relational_restriction_correct_NumpyVector_vs_list()
        self.__relational_restriction_incorrect_NumpyVector_vs_list()
        self.__relational_restriction_correct_NumpyVector_vs_NumpyVector()
        self.__relational_restriction_incorrect_NumpyVector_vs_NumpyVector()
        print('')

    # Tests on checks of relational restrictions imposed on Numpy Matrices
    def __relational_restrictions_on_NumpyMatrices(self):
        print('TESTS ON RELATIONAL RESTRICTIONS ON NUMPY MATRICES:')
        self.__relational_restriction_correct_NumpyMatrix_vs_number()
        self.__relational_restriction_incorrect_NumpyMatrix_vs_number()
        self.__relational_restriction_correct_NumpyMatrix_vs_parameter()
        self.__relational_restriction_incorrect_NumpyMatrix_vs_parameter()
        self.__relational_restriction_correct_NumpyMatrix_vs_tuple()
        self.__relational_restriction_incorrect_NumpyMatrix_vs_tuple()
        self.__relational_restriction_correct_NumpyMatrix_vs_list()
        self.__relational_restriction_incorrect_NumpyMatrix_vs_list()
        self.__relational_restriction_correct_NumpyMatrix_vs_NumpyVector()
        self.__relational_restriction_incorrect_NumpyMatrix_vs_NumpyVector()
        print('')

    # Tests on checks of size restrictions
    def __size_restrictions(self):
        print('TESTS ON SIZE RESTRICTIONS:')
        self.__size_restriction_correct_string_number()
        self.__size_restriction_incorrect_string_number()
        self.__size_restriction_correct_string_parameter()
        self.__size_restriction_incorrect_string_parameter()
        self.__size_restriction_correct_string_string()
        self.__size_restriction_inccorrect_string_string()
        self.__size_restriction_correct_string_tuple()
        self.__size_restriction_inccorrect_string_tuple()
        self.__size_restriction_correct_string_list()
        self.__size_restriction_inccorrect_string_list()

        self.__size_restriction_correct_tuple_number()
        self.__size_restriction_incorrect_tuple_number()
        self.__size_restriction_correct_tuple_parameter()
        self.__size_restriction_incorrect_tuple_parameter()

        self.__size_restriction_correct_list_number()
        self.__size_restriction_incorrect_list_number()
        self.__size_restriction_correct_list_parameter()
        self.__size_restriction_incorrect_list_parameter()
        self.__size_restriction_correct_list_list()
        self.__size_restriction_incorrect_list_list()

        self.__size_restriction_correct_vector_number()
        self.__size_restriction_incorrect_vector_number()
        self.__size_restriction_correct_vector_tuple()
        self.__size_restriction_incorrect_vector_tuple()
        self.__size_restriction_correct_vector_vector()
        self.__size_restriction_incorrect_vector_vector()

        self.__size_restriction_correct_matrix_number()
        self.__size_restriction_incorrect_matrix_number()
        self.__size_restriction_correct_matrix_parameter()
        self.__size_restriction_incorrect_matrix_parameter()
        self.__size_restriction_correct_matrix_string()
        self.__size_restriction_incorrect_matrix_string()
        self.__size_restriction_correct_matrix_matrix()
        self.__size_restriction_incorrect_matrix_matrix()
        print('')

    # Tests on checks of restrictions imposed on the number of dimensions
    def __NDim_restrictions(self):
        print('TESTS ON RESTRICTIONS ON THE NUMBER OF DIMENSIONS:')
        self.__NDim_restriction_correct_list_number()
        self.__NDim_restriction_incorrect_list_number()
        self.__NDim_restriction_correct_list_parameter()
        self.__NDim_restriction_incorrect_list_parameter()

        self.__NDim_restriction_correct_ndarray_number()
        self.__NDim_restriction_incorrect_ndarray_number()
        self.__NDim_restriction_correct_ndarray_parameter()
        self.__NDim_restriction_incorrect_ndarray_parameter()
        self.__NDim_restriction_correct_ndarray_tuple()
        self.__NDim_restriction_incorrect_ndarray_tuple()
        self.__NDim_restriction_correct_ndarray_list()
        self.__NDim_restriction_incorrect_ndarray_list()
        self.__NDim_restriction_correct_ndarray_ndarray()
        self.__NDim_restriction_incorrect_ndarray_ndarray()
        print('')

    # Tests on checks of restrictions imposed on sizes of dimensions
    def __DimSiz_restrictions(self):
        print('TESTS ON DIMENSION RESTRICTIONS')
        self.__DimSiz_restriction_correct_list_number()
        self.__DimSiz_restriction_incorrect_list_number()
        self.__DimSiz_restriction_correct_list_number_pedantic()
        self.__DimSiz_restriction_incorrect_list_number_pedantic()

        self.__DimSiz_restriction_correct_list_parameter()
        self.__DimSiz_restriction_incorrect_list_parameter()
        self.__DimSiz_restriction_correct_list_parameter_pedantic()
        self.__DimSiz_restriction_incorrect_list_parameter_pedantic()

        self.__DimSiz_restriction_correct_ndarray_number()
        self.__DimSiz_restriction_incorrect_ndarray_number()
        self.__DimSiz_restriction_correct_ndarray_number2()
        self.__DimSiz_restriction_incorrect_ndarray_number2()
        self.__DimSiz_restriction_correct_ndarray_number_pedantic()
        self.__DimSiz_restriction_incorrect_ndarray_number_pedantic()
        self.__DimSiz_restriction_correct_ndarray_number_pedantic2()
        self.__DimSiz_restriction_incorrect_ndarray_number_pedantic2()

        self.__DimSiz_restriction_correct_ndarray_parameter()
        self.__DimSiz_restriction_incorrect_ndarray_parameter()
        self.__DimSiz_restriction_correct_ndarray_parameter_pedantic()
        self.__DimSiz_restriction_incorrect_ndarray_parameter_pedantic()

        self.__DimSiz_restriction_correct_ndarray_tuple()
        self.__DimSiz_restriction_incorrect_ndarray_tuple()
        self.__DimSiz_restriction_correct_ndarray_tuple_pedantic()
        self.__DimSiz_restriction_incorrect_ndarray_tuple_pedantic()

        self.__DimSiz_restriction_correct_ndarray_ndarray()
        self.__DimSiz_restriction_incorrect_ndarray_ndarray()
        self.__DimSiz_restriction_correct_ndarray_ndarray2()
        self.__DimSiz_restriction_incorrect_ndarray_ndarray2()
        self.__DimSiz_restriction_correct_ndarray_ndarray3()
        self.__DimSiz_restriction_incorrect_ndarray_ndarray3()
        self.__DimSiz_restriction_correct_ndarray_ndarray4()
        self.__DimSiz_restriction_incorrect_ndarray_ndarray4()

        self.__DimSiz_restriction_correct_ndarray_ndarray_pedantic()
        self.__DimSiz_restriction_incorrect_ndarray_ndarray_pedantic()
        self.__DimSiz_restriction_correct_ndarray_ndarray_pedantic2()
        self.__DimSiz_restriction_incorrect_ndarray_ndarray_pedantic2()
        self.__DimSiz_restriction_correct_ndarray_ndarray_pedantic3()
        self.__DimSiz_restriction_incorrect_ndarray_ndarray_pedantic3()
        print('')

    # Tests on checks of uniqness of parameters
    def __Unique_restrictions(self):
        print('TESTS ON RESTRICTIONS OF UNIQNESS')
        self.__Unique_restriction_correct_ndarray()
        self.__Unique_restriction_incorrect_ndarray()
        print('')
        
    # Tests on the value of an optional parameter, which default value depends on another parameter
    def __Opt_default(self):
        print('TESTS VALUE PROPAGATION ONTO OPTIONAL PARAMETERS')
        self.__Opt_value_depends_on_another_correct()
        print('')


    def __mandatory_after_optional(self):
        """
            Test of mandatory/optional parameter check.
            Wanted output: RuntimeError
        """

        strTestName = 'Mandatory parameter cannot be defined after optional (incorrect)'
        RxCSObject = _RxCSobject()

        self._iNTests = self._iNTests + 1
        strTestIndex = 'Test #%d:  ' % (self._iNTests)

        try:
            RxCSObject.paramAddOpt('iOpt', 'Temporary optional parameter')
            RxCSObject.paramAddMan('iMan', 'Temporary optional parameter')

        except RuntimeError:
            print(strTestIndex + strTestName + (self.iMaxCols - len(strTestName) - len(strTestIndex)) * '.' + 'Test ok!')
        except:
            print(strTestIndex + strTestName + (self.iMaxCols - len(strTestName) - len(strTestIndex)) * '.' + 'Test failed!')

    def __mandatory_is_not_given(self):
        """
            Test of mandatory/optional parameter check.
            Wanted output: ParameterMissingError
        """

        strTestName = 'Mandatory parameter must be given (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('mandatory_parameter', 'Mandatory parameter')

        self.__parametersCheck_error(RxCSObject, ParameterMissingError, strTestName)

    def __mandatory_is_given(self):
        """
            Test of mandatory/optional parameter check.
            Wanted output: correct
        """

        strTestName = 'Mandatory parameter is given (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('mandatory_parameter', 'Mandatory parameter')
        RxCSObject.mandatory_parameter = 1

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __optional_is_not_given(self):
        """
            Test of mandatory/optional parameter check.
            Wanted output: correct
        """

        strTestName = 'Optional parameter is not given (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddOpt('optional_parameter', 'Optional parameter')

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __type_correct_int(self):
        """
            Test of parameter type check.
            Wanted output: correct
        """

        strTestName = 'Type (int) is given (correct)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddOpt('parameter1', 'type \'int\' parameter')
        RxCSObject.paramType('parameter1', (int))
        RxCSObject.parameter1 = int(1)

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __type_incorrect_int(self):
        """
            Test of parameter type check.
            Wanted output: ParameterTypeError
        """

        strTestName = 'Type (int instead of float) is given (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddOpt('parameter1', 'types \'int\' or \'float\' parameter')
        RxCSObject.paramType('parameter1', (int, float))
        RxCSObject.parameter1 = 1

        RxCSObject.paramAddOpt('parameter2', 'type \'int\' parameter')
        RxCSObject.paramType('parameter2', (int))
        RxCSObject.parameter2 = int(2)

        RxCSObject.paramAddOpt('parameter3', 'type \'int\' parameter')
        RxCSObject.paramType('parameter3', (int))
        RxCSObject.parameter3 = float(3)

        self.__parametersCheck_error(RxCSObject, ParameterTypeError, strTestName)

    def __type_correct_tuple(self):
        """
            Test of parameter type check.
            Wanted output: Correct
        """

        strTestName = 'Type (tuple) is given (correct)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddOpt('parameter1', 'type \'tuple\' parameter')
        RxCSObject.paramType('parameter1', (tuple))
        RxCSObject.parameter1 = (1, 4)

        RxCSObject.paramAddOpt('parameter2', 'type \'list\' parameter')
        RxCSObject.paramType('parameter2', (list))
        RxCSObject.parameter2 = [10, 40]

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __type_incorrect_tuple_lists(self):
        """
            Test of parameter type check.
            Wanted output: ParameterTypeError
        """

        strTestName = 'Type (dict instead of tuple or list) is given (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddOpt('parameter1', 'type \'tuple\' parameter')
        RxCSObject.paramType('parameter1', (tuple))
        RxCSObject.parameter1 = (1, 4)

        RxCSObject.paramAddOpt('parameter2', 'type \'tuple or list\' parameter')
        RxCSObject.paramType('parameter2', (tuple, list))
        RxCSObject.parameter2 = {}

        self.__parametersCheck_error(RxCSObject, ParameterTypeError, strTestName)

    def __type_of_elements_correct_floats_in_list(self):
        """
            Test of parameter elements type check.
            Wanted output: Correct
        """
        strTestName = 'Float elements in a list (correct)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'type \'tuple\' parameter')
        RxCSObject.paramType('parameter1', (tuple))
        RxCSObject.parameter1 = (1, 4)

        RxCSObject.paramAddMan('parameter2', 'type \'tuple or list\' parameter')
        RxCSObject.paramType('parameter2', (tuple, list))
        RxCSObject.parameter2 = [4, 5, 9]

        RxCSObject.paramAddMan('parameter3', 'type \'list\' parameter')
        RxCSObject.paramType('parameter3', (list))
        RxCSObject.paramTypeEl('parameter3', (float))
        RxCSObject.parameter3 = [4.1, 5.3, 9.0]

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __type_of_elements_incorrect_floats_in_tuple(self):
        """
            Test of parameter elements type check.
            Wanted output: ElementTypeError
        """
        strTestName = 'Float elements in a list (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'type \'tuple\' parameter')
        RxCSObject.paramType('parameter1', (tuple))
        RxCSObject.paramTypeEl('parameter1', (tuple))
        RxCSObject.parameter1 = (1.2, 4.9)

        self.__parametersCheck_error(RxCSObject, ElementTypeError, strTestName)

    def __type_of_elements_incorrect_dicts_in_tuple(self):
        """
            Test of parameter elements type check.
            Wanted output: ElementTypeError
        """
        strTestName = 'Elements (dicts) given in a tuple (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'type \'tuple\' parameter #1')
        RxCSObject.paramType('parameter1', (tuple))

        RxCSObject.paramAddMan('parameter2', 'type \'tuple\' parameter #2')
        RxCSObject.paramType('parameter2', (tuple))
        RxCSObject.paramTypeEl('parameter2', (int))

        RxCSObject.parameter1 = (1, 10)
        dD1 = {}
        dD2 = {}
        RxCSObject.parameter2 = (dD1, dD2)

        self.__parametersCheck_error(RxCSObject, ElementTypeError, strTestName)

    def __type_of_elements_incorrect_elem_in_dict(self):
        """
            Test of parameter elements type check.
            Wanted output: ValueError
        """
        strTestName = 'Elements type check assigned to a dictionary (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'type \'dictionary\' parameter')
        RxCSObject.paramType('parameter1', (dict))
        RxCSObject.paramTypeEl('parameter1', (int))

        dD1 = {}
        dD1['field1'] = 3
        dD1['field2'] = 2
        dD1['field3'] = 13
        RxCSObject.parameter1 = dD1

        self.__parametersCheck_error(RxCSObject, ValueError, strTestName)

    def __type_of_elements_correct_long_Numpy_vector(self):
        """
            Test of parameter elements type check.
            Wanted output: Correct
        """
        strTestName = 'Int elements in a long Numpy vector (correct)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'long Numpy vector')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramTypeEl('parameter1', (float))

        RxCSObject.parameter1 = np.random.randn(1e6)

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __type_of_elements_incorrect_float_in_Numpy_vector(self):
        """
            Test of parameter elements type check.
            Wanted output: ElementTypeError
        """
        strTestName = 'Float elements in a Numpy vector (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'Numpy vector #1')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramTypeEl('parameter1', (float))

        RxCSObject.paramAddMan('parameter2', 'Numpy vector #2')
        RxCSObject.paramType('parameter2', np.ndarray)
        RxCSObject.paramTypeEl('parameter2', (int))

        RxCSObject.parameter1 = np.random.randn(1e2)
        RxCSObject.parameter2 = np.random.randn(1e2)

        self.__parametersCheck_error(RxCSObject, ElementTypeError, strTestName)

    def __type_of_elements_correct_long_Numpy_matrix(self):
        """
            Test of parameter elements type check.
            Wanted output: Correct
        """
        strTestName = 'Float elements in a Numpy matrix (correct)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'Numpy matrix #1')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramTypeEl('parameter1', (int, float))

        RxCSObject.paramAddMan('parameter2', 'Numpy vector #2')
        RxCSObject.paramType('parameter2', np.ndarray)
        RxCSObject.paramTypeEl('parameter2', (int, float))

        RxCSObject.parameter1 = np.random.randn(1e2,1e2)
        RxCSObject.parameter2 = np.random.randn(1e2,1e2)

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __type_of_elements_incorrect_long_Numpy_matrix(self):
        """
            Test of parameter elements type check.
            Wanted output: ElementTypeError
        """
        strTestName = 'Float elements in a Numpy matrix (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'Numpy matrix #1')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramTypeEl('parameter1', (int))

        RxCSObject.paramAddMan('parameter2', 'Numpy vector #2')
        RxCSObject.paramType('parameter2', np.ndarray)
        RxCSObject.paramTypeEl('parameter2', (int))

        RxCSObject.parameter1 = np.random.randn(1e2,1e2)
        RxCSObject.parameter2 = np.random.randn(1e2,1e2)

        self.__parametersCheck_error(RxCSObject, ElementTypeError, strTestName)


    def __type_of_elements_incorrect_dict_in_long_list(self):
        """
            Test of parameter elements type check.
            Wanted output: ElementTypeError
        """
        strTestName = 'Element in a long list (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'long list')
        RxCSObject.paramType('parameter1', list)
        RxCSObject.paramTypeEl('parameter1', (str))

        lLongList = int(1e6) * ['string1', 'string2']
        lLongList[len(lLongList) - 1] = {}
        RxCSObject.parameter1 = lLongList

        self.__parametersCheck_error(RxCSObject, ElementTypeError, strTestName)

    def __allowed_values_correct_string(self):
        """
            Test of allowed values of a parameter check.
            Wanted output: Correct
        """
        strTestName = 'Values of a string (correct)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'string')
        RxCSObject.paramType('parameter1', str)
        RxCSObject.paramAllowed('parameter1', ['Allowed string #1', 'Allowed string #2'])

        RxCSObject.parameter1 = 'Allowed string #2'

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __allowed_values_inccorrect_string(self):
        """
            Test of allowed values of a parameter check.
            Wanted output: AllowedValuesError
        """
        strTestName = 'Values of a string (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'number #1')
        RxCSObject.paramAddMan('parameter2', 'number #2')

        RxCSObject.paramAddMan('parameter3', 'string')
        RxCSObject.paramType('parameter3', str)
        RxCSObject.paramAllowed('parameter3', ['Allowed string #1', 'Allowed string #2'])

        RxCSObject.parameter1 = 11
        RxCSObject.parameter2 = 21
        RxCSObject.parameter3 = 'Allowed string #3'

        self.__parametersCheck_error(RxCSObject, AllowedValuesError, strTestName)

    def __allowed_values_correct_number(self):
        """
            Test of allowed values of a parameter check.
            Wanted output: Correct
        """
        strTestName = 'Values of a number (correct)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'number #1')
        RxCSObject.paramAddMan('parameter2', 'number #2')
        RxCSObject.paramAllowed('parameter2', range(10))

        RxCSObject.parameter1 = 11
        RxCSObject.parameter2 = 0

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __allowed_values_inccorrect_number(self):
        """
            Test of allowed values of a parameter check.
            Wanted output: AllowedValuesError
        """
        strTestName = 'Values of a number (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'number #1')
        RxCSObject.paramAddMan('parameter2', 'number #2')
        RxCSObject.paramAllowed('parameter2', range(10))

        RxCSObject.parameter1 = 11
        RxCSObject.parameter2 = 1.4

        self.__parametersCheck_error(RxCSObject, AllowedValuesError, strTestName)

    def __allowed_values_correct_tuple(self):
        """
            Test of allowed values of a parameter check.
            Wanted output: Correct
        """
        strTestName = 'Values of a tuple (correct)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'tuple')
        RxCSObject.paramAllowed('parameter1', ('Allowed string #1', 'Allowed string #2', 3, 4, 11))
        RxCSObject.parameter1 = (11, 3, 'Allowed string #1')

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __allowed_values_incorrect_list(self):
        """
            Test of allowed values of a parameter check.
            Wanted output: AllowedValuesError
        """
        strTestName = 'Values of a list (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'tuple')
        RxCSObject.paramAddMan('parameter2', 'list')

        RxCSObject.paramAllowed('parameter2', ('Allowed string #1', 'Allowed string #2', 3, 4, 11))
        RxCSObject.parameter1 = (1, 3, 4)
        RxCSObject.parameter2 = [11, 3, 'Allowed string #1', 'Allowed string #11']

        self.__parametersCheck_error(RxCSObject, AllowedValuesError, strTestName)

    def __allowed_values_incorrect_vector(self):
        """
            Test of allowed values of a parameter check.
            Wanted output: AllowedValuesError
        """
        strTestName = 'Values of a Numpy Array 1D (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'Numpy Array 1D')
        RxCSObject.paramAllowed('parameter1', range(int(1e4)))

        vA = np.random.randint(1, 1e3, 1e3)
        vA[vA.size - 1] = 2e4
        RxCSObject.parameter1 = vA

        self.__parametersCheck_error(RxCSObject, AllowedValuesError, strTestName)

    def __allowed_values_correct_matrix(self):
        """
            Test of allowed values of a parameter check.
            Wanted output: Correct
        """
        strTestName = 'Values of a Numpy Array 2D (correct)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'Numpy Array 2D')
        RxCSObject.paramAllowed('parameter1', range(int(2e3)))
        RxCSObject.parameter1 = np.random.randint(1, 1e3, (1e2, 1e1))

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __allowed_values_incorrect_list_with_allowed_values(self):
        """
            Test of allowed values of a parameter check.
            Wanted output: ValueError
        """
        strTestName = 'Value NaN given in a list with allowed values (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'Numpy Array 2D')
        RxCSObject.paramAllowed('parameter1', range(int(2e3)) + [np.NaN])
        RxCSObject.parameter1 = np.random.randint(1, 1e3, (1e2, 1e1))

        self.__parametersCheck_error(RxCSObject, ValueError, strTestName)

    def __relational_restriction_correct_parameter_vs_number(self):
        """
            Test of relational restriction of a parameter check.
            Wanted output: Correct
        """
        strTestName = 'A parameter higher than a number (correct)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('iParameter1', 'Int parameter')
        RxCSObject.paramType('iParameter1', int)
        RxCSObject.paramH('iParameter1', 2)

        RxCSObject.iParameter1 = 4

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __relational_restriction_incorrect_parameter_vs_number(self):
        """
            Test of relational restriction of a parameter check.
            Wanted output: RelationalError
        """
        strTestName = 'A parameter lower than a number (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('iParameter1', 'Int parameter')
        RxCSObject.paramType('iParameter1', int)
        RxCSObject.paramH('iParameter1', 2, mul=0.5, add=3)  # In English, iParameter must be higher than 4

        RxCSObject.iParameter1 = 4

        self.__parametersCheck_error(RxCSObject, RelationalError, strTestName)

    def __relational_restriction_correct_parameter_vs_parameter(self):
        """
            Test of relational restriction of a parameter check.
            Wanted output: Correct
        """
        strTestName = 'Parameter lower or equal to a parameter (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('iRefParameter1', 'Int parameter')
        RxCSObject.paramType('iRefParameter1', int)

        # Now, the parameter 2 must be lower or equal to 3*iRefParameter-4
        RxCSObject.paramAddMan('iParameter2', 'Int parameter')
        RxCSObject.paramType('iParameter2', int)
        RxCSObject.paramLE('iParameter2', 'iRefParameter1', mul=3, add=-4)  # In English, iParameter must be higher than 4

        RxCSObject.iRefParameter1 = 3
        RxCSObject.iParameter2 = 5

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __relational_restriction_incorrect_parameter_vs_parameter(self):
        """
            Test of relational restriction of a parameter check.
            Wanted output: RelationalError
        """
        strTestName = 'Parameter higher or equal to a parameter (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('iRefParameter1', 'Int parameter')
        RxCSObject.paramType('iRefParameter1', int)

        # Now, the parameter 2 must be lower or equal to 3*iRefParameter-4
        RxCSObject.paramAddMan('iParameter2', 'Int parameter')
        RxCSObject.paramType('iParameter2', int)
        RxCSObject.paramHE('iParameter2', 'iRefParameter1', mul=3, add=-4)  # In English, iParameter must be higher than 4

        RxCSObject.iRefParameter1 = 3
        RxCSObject.iParameter2 = 4

        self.__parametersCheck_error(RxCSObject, RelationalError, strTestName)

    def __relational_restriction_correct_tuple_vs_number(self):
        """
            Test of relational restriction of a parameter check.
            Wanted output: Correct
        """
        strTestName = 'Tuple higher or equal to a number (correct)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('tParameter1', 'Tuple parameter')
        RxCSObject.paramType('tParameter1', tuple)
        RxCSObject.paramHE('tParameter1', 10, mul=0.2)  # In English, all the elements of the tuple must be higher or equal to 2

        RxCSObject.tParameter1 = (3, 8, 9, 11, 2, 5, 7, 101)

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __relational_restriction_incorrect_tuple_vs_number(self):
        """
            Test of relational restriction of a parameter check.
            Wanted output: RelationalError
        """
        strTestName = 'Tuple lower or equal to a number (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('tParameter1', 'Tuple parameter')
        RxCSObject.paramType('tParameter1', tuple)
        RxCSObject.paramLE('tParameter1', 2, mul=4, add=-3)  # In English, all the elements of the tuple must be lower or equal to 5
        RxCSObject.tParameter1 = (13, 8, 9, 11, 2, 5, 7, 101)

        self.__parametersCheck_error(RxCSObject, RelationalError, strTestName)

    def __relational_restriction_correct_tuple_vs_parameter(self):
        """
            Test of relational restriction of a parameter check.
            Wanted output: Correct
        """
        strTestName = 'Tuple lower than a parameter (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('iRefParameter1', 'Int parameter')
        RxCSObject.paramType('iRefParameter1', int)

        # Now, let us define a tuple
        RxCSObject.paramAddMan('tParameter1', 'Tuple parameter')
        RxCSObject.paramType('tParameter1', tuple)
        RxCSObject.paramL('tParameter1', 'iRefParameter1', mul=2, add=1)

        RxCSObject.iRefParameter1 = 3
        RxCSObject.tParameter1 = (1, 2, 3, 4, 5, 6, -1, -101)

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __relational_restriction_incorrect_tuple_vs_parameter(self):
        """
            Test of relational restriction of a parameter check.
            Wanted output: RelationalError
        """
        strTestName = 'Tuple lower than a parameter (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('iRefParameter1', 'Int parameter')
        RxCSObject.paramType('iRefParameter1', int)

        # Now, let us define a tuple
        RxCSObject.paramAddMan('tParameter1', 'Tuple parameter')
        RxCSObject.paramType('tParameter1', tuple)
        RxCSObject.paramL('tParameter1', 'iRefParameter1', mul=2, add=1)

        RxCSObject.iRefParameter1 = 3
        RxCSObject.tParameter1 = (1, 2, 3, 4, 5, 7, -1, -101)

        self.__parametersCheck_error(RxCSObject, RelationalError, strTestName)

    def __relational_restriction_correct_tuple_vs_list(self):
        """
            Test of relational restriction of a parameter check.
            Wanted output: Correct
        """
        strTestName = 'Tuple higher than a list (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('lRefParameter1', 'List parameter')
        RxCSObject.paramType('lRefParameter1', list)

        # Now, let us define a tuple
        RxCSObject.paramAddMan('tParameter1', 'Tuple parameter')
        RxCSObject.paramType('tParameter1', tuple)
        RxCSObject.paramH('tParameter1', 'lRefParameter1', mul=3, add=-1)

        RxCSObject.lRefParameter1 = [0, 1, 2]
        RxCSObject.tParameter1 = (1, 12, 13)

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __relational_restriction_incorrect_tuple_vs_list(self):
        """
            Test of relational restriction of a parameter check.
            Wanted output: RelationalError
        """
        strTestName = 'Tuple higher or equal to a list (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('lRefParameter1', 'List parameter')
        RxCSObject.paramType('lRefParameter1', list)

        # Now, let us define a tuple
        RxCSObject.paramAddMan('tParameter1', 'Tuple parameter')
        RxCSObject.paramType('tParameter1', tuple)
        RxCSObject.paramHE('tParameter1', 'lRefParameter1', mul=-3)

        RxCSObject.lRefParameter1 = [0, 1, 2]
        RxCSObject.tParameter1 = (-101, 2, 3)

        self.__parametersCheck_error(RxCSObject, RelationalError, strTestName)

    def __relational_restriction_correct_list_vs_number(self):
        """
            Test of relational restriction of a parameter check.
            Wanted output: Correct
        """
        strTestName = 'List higher or equal to a number (correct)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('lParameter1', 'List parameter')
        RxCSObject.paramType('lParameter1', list)
        RxCSObject.paramHE('lParameter1', 1, mul=3)

        RxCSObject.lParameter1 = [3, 8, 9, 11, 3, 5, 7, 101]

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __relational_restriction_incorrect_list_vs_number(self):
        """
            Test of relational restriction of a parameter check.
            Wanted output: RelationalError
        """
        strTestName = 'List lower than a number (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('lParameter1', 'List parameter')
        RxCSObject.paramType('lParameter1', list)
        RxCSObject.paramL('lParameter1', 1)

        RxCSObject.lParameter1 = [3, 8, 9, 11, 3, 5, 7, 101]

        self.__parametersCheck_error(RxCSObject, RelationalError, strTestName)

    def __relational_restriction_correct_list_vs_parameter(self):
        """
            Test of relational restriction of a parameter check.
            Wanted output: Correct
        """
        strTestName = 'List lower than a parameter (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('iRefParameter1', 'Int parameter')
        RxCSObject.paramType('iRefParameter1', int)

        # Now, let us define a list
        RxCSObject.paramAddMan('lParameter1', 'List parameter')
        RxCSObject.paramType('lParameter1', list)
        RxCSObject.paramL('lParameter1', 'iRefParameter1', add=4)

        RxCSObject.iRefParameter1 = 0
        RxCSObject.lParameter1 = [3, 1, -9, 2, 2, 3, 0, -101]

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __relational_restriction_incorrect_list_vs_parameter(self):
        """
            Test of relational restriction of a parameter check.
            Wanted output: RelationalError
        """
        strTestName = 'List lower than a parameter (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('iRefParameter1', 'Int parameter')
        RxCSObject.paramType('iRefParameter1', int)

        # Now, let us define a list
        RxCSObject.paramAddMan('lParameter1', 'List parameter')
        RxCSObject.paramType('lParameter1', list)
        RxCSObject.paramL('lParameter1', 'iRefParameter1', add=4)

        RxCSObject.iRefParameter1 = 0
        RxCSObject.lParameter1 = [3, 1, -9, 12, 2, 3, 0, -101]

        self.__parametersCheck_error(RxCSObject, RelationalError, strTestName)

    def __relational_restriction_correct_list_vs_tuple(self):
        """
            Test of relational restriction of a parameter check.
            Wanted output: Correct
        """
        strTestName = 'List lower or equal to a tuple (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('tRefParameter1', 'Tuple parameter')
        RxCSObject.paramType('tRefParameter1', tuple)

        # Now, let us define a list
        RxCSObject.paramAddMan('lParameter1', 'List parameter')
        RxCSObject.paramType('lParameter1', list)
        RxCSObject.paramLE('lParameter1', 'tRefParameter1', mul=-0.2, add=4)

        RxCSObject.tRefParameter1 = (5, 10, 15)  # (-1, 2, 1)
        RxCSObject.lParameter1 = [-3, 1, 1]

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __relational_restriction_incorrect_list_vs_tuple(self):
        """
            Test of relational restriction of a parameter check.
            Wanted output: RelationalError
        """
        strTestName = 'List higher or equal to a tuple (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('tRefParameter1', 'Tuple parameter')
        RxCSObject.paramType('tRefParameter1', tuple)

        # Now, let us define a list
        RxCSObject.paramAddMan('lParameter1', 'List parameter')
        RxCSObject.paramType('lParameter1', list)
        RxCSObject.paramHE('lParameter1', 'tRefParameter1', mul=-0.2, add=4)

        RxCSObject.tRefParameter1 = (5, 10, 15)  # (-1, 2, 1)
        RxCSObject.lParameter1 = [-3, 1, 1]

        self.__parametersCheck_error(RxCSObject, RelationalError, strTestName)

    def __relational_restriction_correct_list_vs_list(self):
        """
            Test of relational restriction of a parameter check.
            Wanted output: Correct
        """
        strTestName = 'List higher than a list (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('lRefParameter1', 'List reference parameter')
        RxCSObject.paramType('lRefParameter1', list)

        # Now, let us define a list
        RxCSObject.paramAddMan('lParameter1', 'List parameter')
        RxCSObject.paramType('lParameter1', list)
        RxCSObject.paramH('lParameter1', 'lRefParameter1')

        RxCSObject.lRefParameter1 = [5, 10, 15, 20]
        RxCSObject.lParameter1 = [6, 11, 16, 21]

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __relational_restriction_incorrect_list_vs_list(self):
        """
            Test of relational restriction of a parameter check.
            Wanted output: RelationalError
        """
        strTestName = 'List lower than a list (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('lRefParameter1', 'List reference parameter')
        RxCSObject.paramType('lRefParameter1', list)

        # Now, let us define a list
        RxCSObject.paramAddMan('lParameter1', 'List parameter')
        RxCSObject.paramType('lParameter1', list)
        RxCSObject.paramL('lParameter1', 'lRefParameter1')

        RxCSObject.lRefParameter1 = [5, 10, 15, 20]
        RxCSObject.lParameter1 = [4, 11, 16, 21]

        self.__parametersCheck_error(RxCSObject, RelationalError, strTestName)

    def __relational_restriction_correct_list_vs_NumpyVector(self):
        """
            Test of relational restriction of a parameter check.
            Wanted output: Correct
        """
        strTestName = 'List lower or equal to a Numpy vector (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('vRefParameter1', 'Numpy 1D array reference parameter')
        RxCSObject.paramType('vRefParameter1', np.ndarray)

        # Now, let us define a list
        RxCSObject.paramAddMan('lParameter1', 'List parameter')
        RxCSObject.paramType('lParameter1', list)
        RxCSObject.paramLE('lParameter1', 'vRefParameter1')

        RxCSObject.vRefParameter1 = np.array([5, 10, 15, 20])
        RxCSObject.lParameter1 = [4, 5, 7, 20]

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __relational_restriction_incorrect_list_vs_NumpyVector(self):
        """
            Test of relational restriction of a parameter check.
            Wanted output: RelationalError
        """
        strTestName = 'List lower or equal to a Numpy vector (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('vRefParameter1', 'Numpy 1D array reference parameter')
        RxCSObject.paramType('vRefParameter1', np.ndarray)

        # Now, let us define a list
        RxCSObject.paramAddMan('lParameter1', 'List parameter')
        RxCSObject.paramType('lParameter1', list)
        RxCSObject.paramLE('lParameter1', 'vRefParameter1', add=1)

        RxCSObject.vRefParameter1 = np.array([5, 10, 15, 20])
        RxCSObject.lParameter1 = [4, 5, 7, 120]

        self.__parametersCheck_error(RxCSObject, RelationalError, strTestName)

    def __relational_restriction_correct_NumpyVector_vs_number(self):
        """
            Test of relational restriction of a parameter check.
            Wanted output: Correct
        """
        strTestName = 'Numpy vector lower or equal to a number (correct)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('vParameter1', 'Vector parameter')
        RxCSObject.paramType('vParameter1', np.ndarray)
        RxCSObject.paramLE('vParameter1', 5)

        RxCSObject.vParameter1 = np.array([4, 2, 1, -1, -4])
        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __relational_restriction_incorrect_NumpyVector_vs_number(self):
        """
            Test of relational restriction of a parameter check.
            Wanted output: RelationalError
        """
        strTestName = 'Numpy vector lower or equal to a number (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('vParameter1', 'Vector parameter')
        RxCSObject.paramType('vParameter1', np.ndarray)
        RxCSObject.paramLE('vParameter1', 5, mul=1.4)

        RxCSObject.vParameter1 = np.array([4, 2, 11, -1, -4])

        self.__parametersCheck_error(RxCSObject, RelationalError, strTestName)

    def __relational_restriction_correct_NumpyVector_vs_parameter(self):
        """
            Test of relational restriction of a parameter check.
            Wanted output: Correct
        """
        strTestName = 'Numpy vector higher than a parameter (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('iRefParameter1', 'Int parameter')
        RxCSObject.paramType('iRefParameter1', int)

        # Now, let us define a vector parameter
        RxCSObject.paramAddMan('vParameter1', 'Vector parameter')
        RxCSObject.paramType('vParameter1', np.ndarray)
        RxCSObject.paramH('vParameter1', 'iRefParameter1', mul=2)

        RxCSObject.iRefParameter1 = 2
        RxCSObject.vParameter1 = np.array([5, 12, 11, 10, 14])

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __relational_restriction_incorrect_NumpyVector_vs_parameter(self):
        """
            Test of relational restriction of a parameter check.
            Wanted output: RelationalError
        """
        strTestName = 'Numpy vector lower than a parameter (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('iRefParameter1', 'Int parameter')
        RxCSObject.paramType('iRefParameter1', int)

        # Now, let us define a vector parameter
        RxCSObject.paramAddMan('vParameter1', 'Vector parameter')
        RxCSObject.paramType('vParameter1', np.ndarray)
        RxCSObject.paramL('vParameter1', 'iRefParameter1', mul=2)

        RxCSObject.iRefParameter1 = 2
        RxCSObject.vParameter1 = np.array([5, 12, 11, 10, 14])

        self.__parametersCheck_error(RxCSObject, RelationalError, strTestName)

    def __relational_restriction_correct_NumpyVector_vs_tuple(self):
        """
            Test of relational restriction of a parameter check.
            Wanted output: Correct
        """
        strTestName = 'Numpy vector lower or equal to a tuple (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('tRefParameter1', 'Tuple parameter')
        RxCSObject.paramType('tRefParameter1', tuple)

        # Now, let us define a vector parameter
        RxCSObject.paramAddMan('vParameter1', 'Vector parameter')
        RxCSObject.paramType('vParameter1', np.ndarray)
        RxCSObject.paramLE('vParameter1', 'tRefParameter1', mul=4)

        RxCSObject.tRefParameter1 = (10, 10, 20, 10, 15)
        RxCSObject.vParameter1 = np.array([5, 12, 11, 10, 14])

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __relational_restriction_incorrect_NumpyVector_vs_tuple(self):
        """
            Test of relational restriction of a parameter check.
            Wanted output: RelationalError
        """
        strTestName = 'Numpy vector lower or equal to a tuple (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('tRefParameter1', 'Tuple parameter')
        RxCSObject.paramType('tRefParameter1', tuple)

        # Now, let us define a vector parameter
        RxCSObject.paramAddMan('vParameter1', 'Vector parameter')
        RxCSObject.paramType('vParameter1', np.ndarray)
        RxCSObject.paramLE('vParameter1', 'tRefParameter1')

        RxCSObject.tRefParameter1 = (10, 10, 20, 10, 15)
        RxCSObject.vParameter1 = np.array([15, 42, 11, 10, 14])

        self.__parametersCheck_error(RxCSObject, RelationalError, strTestName)

    def __relational_restriction_correct_NumpyVector_vs_list(self):
        """
            Test of relational restriction of a parameter check.
            Wanted output: Correct
        """
        strTestName = 'Numpy vector higher or equal to a list (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('lRefParameter1', 'List parameter')
        RxCSObject.paramType('lRefParameter1', list)

        # Now, let us define a vector parameter
        RxCSObject.paramAddMan('vParameter1', 'Vector parameter')
        RxCSObject.paramType('vParameter1', np.ndarray)
        RxCSObject.paramHE('vParameter1', 'lRefParameter1')

        RxCSObject.lRefParameter1 = [10, 10, 20, 10, 15]
        RxCSObject.vParameter1 = np.array([15, 42, 20, 10, 16])

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __relational_restriction_incorrect_NumpyVector_vs_list(self):
        """
            Test of relational restriction of a parameter check.
            Wanted output: RelationalError
        """
        strTestName = 'Numpy vector higher than a list (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('lRefParameter1', 'List parameter')
        RxCSObject.paramType('lRefParameter1', list)

        # Now, let us define a vector parameter
        RxCSObject.paramAddMan('vParameter1', 'Vector parameter')
        RxCSObject.paramType('vParameter1', np.ndarray)
        RxCSObject.paramH('vParameter1', 'lRefParameter1')

        RxCSObject.lRefParameter1 = [10, 10, 20, 10, 15]
        RxCSObject.vParameter1 = np.array([15, 42, 20, 10, 16])

        self.__parametersCheck_error(RxCSObject, RelationalError, strTestName)

    def __relational_restriction_correct_NumpyVector_vs_NumpyVector(self):
        """
            Test of relational restriction of a parameter check.
            Wanted output: Correct
        """
        strTestName = 'Numpy vector higher or equal to a Numpy vector (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('vRefParameter1', 'Vector reference parameter')
        RxCSObject.paramType('vRefParameter1', np.ndarray)

        # Now, let us define a vector parameter
        RxCSObject.paramAddMan('vParameter1', 'Vector parameter')
        RxCSObject.paramType('vParameter1', np.ndarray)
        RxCSObject.paramHE('vParameter1', 'vRefParameter1')

        RxCSObject.vRefParameter1 = np.array([10, 10, 20, 10, 15])
        RxCSObject.vParameter1 = np.array([15, 42, 20, 10, 16])

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __relational_restriction_incorrect_NumpyVector_vs_NumpyVector(self):
        """
            Test of relational restriction of a parameter check.
            Wanted output: RelationalError
        """
        strTestName = 'Numpy vector higher than a Numpy vector (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('vRefParameter1', 'Vector reference parameter')
        RxCSObject.paramType('vRefParameter1', np.ndarray)

        # Now, let us define a vector parameter
        RxCSObject.paramAddMan('vParameter1', 'Vector parameter')
        RxCSObject.paramType('vParameter1', np.ndarray)
        RxCSObject.paramH('vParameter1', 'vRefParameter1')

        RxCSObject.vRefParameter1 = np.array([10, 10, 20, 10, 15])
        RxCSObject.vParameter1 = np.array([15, 42, 20, 10, 16])

        self.__parametersCheck_error(RxCSObject, RelationalError, strTestName)

    def __relational_restriction_correct_NumpyMatrix_vs_number(self):
        """
            Test of relational restriction of a parameter check.
            Wanted output: Correct
        """
        strTestName = 'Numpy matrix higher than a number (correct)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('mParameter1', 'Matrix parameter')
        RxCSObject.paramType('mParameter1', np.ndarray)
        RxCSObject.paramH('mParameter1', 0)

        RxCSObject.mParameter1 = np.random.randint(1, 10, (2, 2))

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __relational_restriction_incorrect_NumpyMatrix_vs_number(self):
        """
            Test of relational restriction of a parameter check.
            Wanted output: RelationalError
        """
        strTestName = 'Numpy matrix higher than a number (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('mParameter1', 'Matrix parameter')
        RxCSObject.paramType('mParameter1', np.ndarray)
        RxCSObject.paramH('mParameter1', 11)

        RxCSObject.mParameter1 = np.random.randint(1, 10, (2, 2))

        self.__parametersCheck_error(RxCSObject, RelationalError, strTestName)

    def __relational_restriction_correct_NumpyMatrix_vs_parameter(self):
        """
            Test of relational restriction of a parameter check.
            Wanted output: Correct
        """
        strTestName = 'Numpy matrix lower than a parameter (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('iRefParameter1', 'Int parameter')
        RxCSObject.paramType('iRefParameter1', int)

        # Now, let us define a matrix parameter
        RxCSObject.paramAddMan('mParameter1', 'Matrix parameter')
        RxCSObject.paramType('mParameter1', np.ndarray)
        RxCSObject.paramL('mParameter1', 'iRefParameter1', mul=4)

        RxCSObject.iRefParameter1 = 1
        RxCSObject.mParameter1 = np.random.randint(1, 3, (2, 2))

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __relational_restriction_incorrect_NumpyMatrix_vs_parameter(self):
        """
            Test of relational restriction of a parameter check.
            Wanted output: RelationalError
        """
        strTestName = 'Numpy matrix lower or equal to a parameter (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('iRefParameter1', 'Int parameter')
        RxCSObject.paramType('iRefParameter1', int)

        # Now, let us define a matrix parameter
        RxCSObject.paramAddMan('mParameter1', 'Matrix parameter')
        RxCSObject.paramType('mParameter1', np.ndarray)
        RxCSObject.paramLE('mParameter1', 'iRefParameter1', mul=4)

        RxCSObject.iRefParameter1 = 1
        RxCSObject.mParameter1 = np.random.randint(1, 3, (2, 2))
        RxCSObject.mParameter1[1, 1] = 15

        self.__parametersCheck_error(RxCSObject, RelationalError, strTestName)

    def __relational_restriction_correct_NumpyMatrix_vs_tuple(self):
        """
            Test of relational restriction of a parameter check.
            Wanted output: Correct
        """
        strTestName = 'Numpy matrix higher or equal to a tuple (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('tRefParameter1', 'Tuple parameter')
        RxCSObject.paramType('tRefParameter1', tuple)

        # Now, let us define a matrix parameter
        RxCSObject.paramAddMan('mParameter1', 'Matrix parameter')
        RxCSObject.paramType('mParameter1', np.ndarray)
        RxCSObject.paramHE('mParameter1', 'tRefParameter1', add=-2)

        RxCSObject.tRefParameter1 = (1, 1, 2, 1)
        RxCSObject.mParameter1 = np.random.randint(2, 9, (2, 2))

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __relational_restriction_incorrect_NumpyMatrix_vs_tuple(self):
        """
            Test of relational restriction of a parameter check.
            Wanted output: RelationalError
        """
        strTestName = 'Numpy matrix higher than a tuple (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('tRefParameter1', 'Tuple parameter')
        RxCSObject.paramType('tRefParameter1', tuple)

        # Now, let us define a matrix parameter
        RxCSObject.paramAddMan('mParameter1', 'Matrix parameter')
        RxCSObject.paramType('mParameter1', np.ndarray)
        RxCSObject.paramH('mParameter1', 'tRefParameter1')

        RxCSObject.tRefParameter1 = (1, 1, 2, 1, 3, 33)
        RxCSObject.mParameter1 = np.random.randint(2, 9, (3, 2))

        self.__parametersCheck_error(RxCSObject, RelationalError, strTestName)

    def __relational_restriction_correct_NumpyMatrix_vs_list(self):
        """
            Test of relational restriction of a parameter check.
            Wanted output: Correct
        """
        strTestName = 'Numpy matrix higher or equal to a list (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('lRefParameter1', 'List parameter')
        RxCSObject.paramType('lRefParameter1', list)

        # Now, let us define a matrix parameter
        RxCSObject.paramAddMan('mParameter1', 'Matrix parameter')
        RxCSObject.paramType('mParameter1', np.ndarray)
        RxCSObject.paramHE('mParameter1', 'lRefParameter1')

        RxCSObject.lRefParameter1 = [-1, -1, -2, -1, -3, -33]
        RxCSObject.mParameter1 = np.random.randint(1, 9, (3, 2))

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __relational_restriction_incorrect_NumpyMatrix_vs_list(self):
        """
            Test of relational restriction of a parameter check.
            Wanted output: RelationalError
        """
        strTestName = 'Numpy matrix higher or equal to a list (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('lRefParameter1', 'List parameter')
        RxCSObject.paramType('lRefParameter1', list)

        # Now, let us define a matrix parameter
        RxCSObject.paramAddMan('mParameter1', 'Matrix parameter')
        RxCSObject.paramType('mParameter1', np.ndarray)
        RxCSObject.paramHE('mParameter1', 'lRefParameter1')

        RxCSObject.lRefParameter1 = [-1, -1, -2, -1, -3, 33]
        RxCSObject.mParameter1 = np.random.randint(1, 9, (3, 2))

        self.__parametersCheck_error(RxCSObject, RelationalError, strTestName)

    def __relational_restriction_correct_NumpyMatrix_vs_NumpyVector(self):
        """
            Test of relational restriction of a parameter check.
            Wanted output: Correct
        """
        strTestName = 'Numpy matrix lower than a Numpy Vector (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('vRefParameter1', 'Vector reference parameter')
        RxCSObject.paramType('vRefParameter1', np.ndarray)

        # Now, let us define a matrix parameter
        RxCSObject.paramAddMan('mParameter1', 'Matrix parameter')
        RxCSObject.paramType('mParameter1', np.ndarray)
        RxCSObject.paramL('mParameter1', 'vRefParameter1')

        RxCSObject.vRefParameter1 = np.random.randint(8, 9, 1e2 * 1e2)
        RxCSObject.mParameter1 = np.random.randint(1, 6, (1e2, 1e2))

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __relational_restriction_incorrect_NumpyMatrix_vs_NumpyVector(self):
        """
            Test of relational restriction of a parameter check.
            Wanted output: RelationalError
        """
        strTestName = 'Numpy matrix lower than a Numpy Vector (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('vRefParameter1', 'Vector reference parameter')
        RxCSObject.paramType('vRefParameter1', np.ndarray)

        # Now, let us define a matrix parameter
        RxCSObject.paramAddMan('mParameter1', 'Matrix parameter')
        RxCSObject.paramType('mParameter1', np.ndarray)
        RxCSObject.paramL('mParameter1', 'vRefParameter1')

        RxCSObject.vRefParameter1 = np.random.randint(1, 9, 1e3 * 1e2)
        RxCSObject.mParameter1 = np.random.randint(1, 9, (1e3, 1e2))

        self.__parametersCheck_error(RxCSObject, RelationalError, strTestName)

    def __size_restriction_correct_string_number(self):
        """
            Test of 'parameter size' restriction check.
            Wanted output: Correct
        """

        strTestName = 'String size equal to a string (correct)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'String parameter')
        RxCSObject.paramType('parameter1', str)
        RxCSObject.paramSizEq('parameter1', 4)

        RxCSObject.parameter1 = 'aaaa'

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __size_restriction_incorrect_string_number(self):
        """
            Test of 'parameter size' restriction check.
            Wanted output: SizeError
        """

        strTestName = 'String size lower than a number (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'String parameter')
        RxCSObject.paramType('parameter1', str)
        RxCSObject.paramSizHE('parameter1', 4, mul=2, add=3)

        RxCSObject.parameter1 = 'aaa'

        self.__parametersCheck_error(RxCSObject, SizeError, strTestName)

    def __size_restriction_correct_string_parameter(self):
        """
            Test of 'parameter size' restriction check.
            Wanted output: Correct
        """
        strTestName = 'String size higher than a parameter (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('iRefParameter1', 'Int parameter')
        RxCSObject.paramType('iRefParameter1', int)

        # Now, let me define a string
        RxCSObject.paramAddMan('parameter1', 'String parameter')
        RxCSObject.paramType('parameter1', str)
        RxCSObject.paramSizH('parameter1', 'iRefParameter1')

        RxCSObject.iRefParameter1 = 2
        RxCSObject.parameter1 = 'aaabbbab'

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __size_restriction_incorrect_string_parameter(self):
        """
            Test of 'parameter size' restriction check.
            Wanted output: SizeError
        """

        strTestName = 'String size higher or equal to a parameter (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('iRefParameter1', 'Int parameter')
        RxCSObject.paramType('iRefParameter1', int)

        # Now, let me define a string
        RxCSObject.paramAddMan('parameter1', 'String parameter')
        RxCSObject.paramType('parameter1', str)
        RxCSObject.paramSizHE('parameter1', 'iRefParameter1', mul=2, add=3)

        RxCSObject.iRefParameter1 = 2
        RxCSObject.parameter1 = 'aaabb'

        self.__parametersCheck_error(RxCSObject, SizeError, strTestName)

    def __size_restriction_correct_string_string(self):
        """
            Test of 'parameter size' restriction check.
            Wanted output: Correct
        """

        strTestName = 'String size lower or equal to the size of another string (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('strRefParameter1', 'Str ref. parameter')
        RxCSObject.paramType('strRefParameter1', str)

        # Now, let me define a string
        RxCSObject.paramAddMan('parameter1', 'String parameter')
        RxCSObject.paramType('parameter1', str)
        RxCSObject.paramSizLE('parameter1', 'strRefParameter1')

        RxCSObject.strRefParameter1 = 'bbbccc'
        RxCSObject.parameter1 = 'aaabb'

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __size_restriction_inccorrect_string_string(self):
        """
            Test of 'parameter size' restriction check.
            Wanted output: SizeError
        """

        strTestName = 'String size equal to the size of another string (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('strRefParameter1', 'Str ref. parameter')
        RxCSObject.paramType('strRefParameter1', str)

        # Now, let me define a string
        RxCSObject.paramAddMan('parameter1', 'String parameter')
        RxCSObject.paramType('parameter1', str)
        RxCSObject.paramSizEq('parameter1', 'strRefParameter1')

        RxCSObject.strRefParameter1 = 'bbbcca'
        RxCSObject.parameter1 = 'aaabb'

        self.__parametersCheck_error(RxCSObject, SizeError, strTestName)

    def __size_restriction_correct_string_tuple(self):
        """
            Test of 'parameter size' restriction check.
            Wanted output: Correct
        """

        strTestName = 'String size lower than the size of a tuple (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('tRefParameter1', 'Tuple ref. parameter')
        RxCSObject.paramType('tRefParameter1', tuple)

        # Now, let me define a string
        RxCSObject.paramAddMan('parameter1', 'String parameter')
        RxCSObject.paramType('parameter1', str)
        RxCSObject.paramSizL('parameter1', 'tRefParameter1')

        RxCSObject.tRefParameter1 = (4, 5, 8, 9)
        RxCSObject.parameter1 = 'abb'

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __size_restriction_inccorrect_string_tuple(self):
        """
            Test of 'parameter size' restriction check.
            Wanted output: SizeError
        """

        strTestName = 'String size higher than the size of a tuple (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('tRefParameter1', 'Tuple ref. parameter')
        RxCSObject.paramType('tRefParameter1', tuple)

        # Now, let me define a string
        RxCSObject.paramAddMan('parameter1', 'String parameter')
        RxCSObject.paramType('parameter1', str)
        RxCSObject.paramSizH('parameter1', 'tRefParameter1')

        RxCSObject.tRefParameter1 = (4, 5, 8, 9)
        RxCSObject.parameter1 = 'abbc'

        self.__parametersCheck_error(RxCSObject, SizeError, strTestName)

    def __size_restriction_correct_string_list(self):
        """
            Test of 'parameter size' restriction check.
            Wanted output: Correct
        """

        strTestName = 'String size higher or equal to the size of a list (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('lRefParameter1', 'List ref. parameter')
        RxCSObject.paramType('lRefParameter1', list)

        # Now, let me define a string
        RxCSObject.paramAddMan('parameter1', 'String parameter')
        RxCSObject.paramType('parameter1', str)
        RxCSObject.paramSizHE('parameter1', 'lRefParameter1')

        RxCSObject.lRefParameter1 = [4, 5, 8, 9]
        RxCSObject.parameter1 = 'abbce'

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __size_restriction_inccorrect_string_list(self):
        """
            Test of 'parameter size' restriction check.
            Wanted output: SizeError
        """

        strTestName = 'String size equal to the size of a list (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('lRefParameter1', 'List ref. parameter')
        RxCSObject.paramType('lRefParameter1', list)

        # Now, let me define a string
        RxCSObject.paramAddMan('parameter1', 'String parameter')
        RxCSObject.paramType('parameter1', str)
        RxCSObject.paramSizEq('parameter1', 'lRefParameter1')

        RxCSObject.lRefParameter1 = [13, -4, 6, 5, -8, 9]
        RxCSObject.parameter1 = 'abcde'

        self.__parametersCheck_error(RxCSObject, SizeError, strTestName)

    def __size_restriction_correct_tuple_number(self):
        """
            Test of 'parameter size' restriction check.
            Wanted output: Correct
        """

        strTestName = 'Tuple size equal to a number (correct)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'Tuple parameter')
        RxCSObject.paramType('parameter1', tuple)
        RxCSObject.paramSizEq('parameter1', 3, mul=2)

        RxCSObject.parameter1 = (1, 2, 3, 4, 5, 6)

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __size_restriction_incorrect_tuple_number(self):
        """
            Test of 'parameter size' restriction check.
            Wanted output: SizeError
        """

        strTestName = 'Tuple size lower than a number (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'Tuple parameter')
        RxCSObject.paramType('parameter1', tuple)
        RxCSObject.paramSizL('parameter1', 3, mul=2)

        RxCSObject.parameter1 = (1, 2, 3, 4, 5, 6)

        self.__parametersCheck_error(RxCSObject, SizeError, strTestName)

    def __size_restriction_correct_tuple_parameter(self):
        """
            Test of 'parameter size' restriction check.
            Wanted output: Correct
        """

        strTestName = 'Tuple size higher than a parameter (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('iRefParameter1', 'Ref. parameter')
        RxCSObject.paramType('iRefParameter1', int)

        # Now, let us define a tuple
        RxCSObject.paramAddMan('parameter1', 'Tuple parameter')
        RxCSObject.paramType('parameter1', tuple)
        RxCSObject.paramSizH('parameter1', 'iRefParameter1', mul=2, add=1)

        RxCSObject.iRefParameter1 = 2
        RxCSObject.parameter1 = (1, 2, 3, 4, 5, 6)

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __size_restriction_incorrect_tuple_parameter(self):
        """
            Test of 'parameter size' restriction check.
            Wanted output: SizeError
        """

        strTestName = 'Tuple size lower or equal to a parameter (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('iRefParameter1', 'Ref. parameter')
        RxCSObject.paramType('iRefParameter1', int)

        # Now, let us define a tuple
        RxCSObject.paramAddMan('parameter1', 'Tuple parameter')
        RxCSObject.paramType('parameter1', tuple)
        RxCSObject.paramSizLE('parameter1', 'iRefParameter1')

        RxCSObject.iRefParameter1 = 2
        RxCSObject.parameter1 = (1, 2, 3, 4, 5, 6)

        self.__parametersCheck_error(RxCSObject, SizeError, strTestName)

    def __size_restriction_correct_list_number(self):
        """
            Test of 'parameter size' restriction check.
            Wanted output: Correct
        """

        strTestName = 'List size higher than a number (correct)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'List parameter')
        RxCSObject.paramType('parameter1', list)
        RxCSObject.paramSizH('parameter1', 3)

        RxCSObject.parameter1 = [1, 2, 3, 4, 5, 6]

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __size_restriction_incorrect_list_number(self):
        """
            Test of 'parameter size' restriction check.
            Wanted output: SizeError
        """

        strTestName = 'List size lower or equal to a number (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'List parameter')
        RxCSObject.paramType('parameter1', list)
        RxCSObject.paramSizLE('parameter1', 3)

        RxCSObject.parameter1 = [1, 2, 3, 4, 5, 6]

        self.__parametersCheck_error(RxCSObject, SizeError, strTestName)

    def __size_restriction_correct_list_parameter(self):
        """
            Test of 'parameter size' restriction check.
            Wanted output: Correct
        """

        strTestName = 'List size equal to a parameter (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('iRefParameter1', 'Ref. parameter')
        RxCSObject.paramType('iRefParameter1', int)

        # Now, let us define a tuple
        RxCSObject.paramAddMan('parameter1', 'List parameter')
        RxCSObject.paramType('parameter1', list)
        RxCSObject.paramSizEq('parameter1', 'iRefParameter1')

        RxCSObject.iRefParameter1 = 3
        RxCSObject.parameter1 = [11, 12, 13]

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __size_restriction_incorrect_list_parameter(self):
        """
            Test of 'parameter size' restriction check.
            Wanted output: SizeError
        """

        strTestName = 'List size equal to a parameter (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('iRefParameter1', 'Ref. parameter')
        RxCSObject.paramType('iRefParameter1', int)

        # Now, let us define a list
        RxCSObject.paramAddMan('parameter1', 'List parameter')
        RxCSObject.paramType('parameter1', list)
        RxCSObject.paramSizEq('parameter1', 'iRefParameter1')

        RxCSObject.iRefParameter1 = 14
        RxCSObject.parameter1 = [11, 12, 13]

        self.__parametersCheck_error(RxCSObject, SizeError, strTestName)

    def __size_restriction_correct_list_list(self):
        """
            Test of 'parameter size' restriction check.
            Wanted output: Correct
        """

        strTestName = 'List size higher than the size of other list (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('lRefParameter1', 'Ref. parameter')
        RxCSObject.paramType('lRefParameter1', list)

        # Now, let us define a list
        RxCSObject.paramAddMan('parameter1', 'List parameter')
        RxCSObject.paramType('parameter1', list)
        RxCSObject.paramSizEq('parameter1', 'lRefParameter1', mul=0.5)

        RxCSObject.lRefParameter1 = [21, 22, 23, 24, 25, 26]
        RxCSObject.parameter1 = [11, 12, 13]

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __size_restriction_incorrect_list_list(self):
        """
            Test of 'parameter size' restriction check.
            Wanted output: SizeError
        """

        strTestName = 'List size higher or equal to the size of other list (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('lRefParameter1', 'Ref. parameter')
        RxCSObject.paramType('lRefParameter1', list)

        # Now, let us define a list
        RxCSObject.paramAddMan('parameter1', 'List 1D parameter')
        RxCSObject.paramType('parameter1', list)
        RxCSObject.paramSizHE('parameter1', 'lRefParameter1', mul=0.5)

        RxCSObject.lRefParameter1 = [21, 22, 23, 24, 25, 26]
        RxCSObject.parameter1 = [11, 12]

        self.__parametersCheck_error(RxCSObject, SizeError, strTestName)

    def __size_restriction_correct_vector_number(self):
        """
            Test of 'parameter size' restriction check.
            Wanted output: Correct
        """

        strTestName = 'Vector size equal to a number (correct)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'Numpy array 1D parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramSizEq('parameter1', 5)

        RxCSObject.parameter1 = np.random.randn(5)

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __size_restriction_incorrect_vector_number(self):
        """
            Test of 'parameter size' restriction check.
            Wanted output: SizeError
        """

        strTestName = 'Vector size lower or equal to a number (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'Numpy array 1D parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramSizLE('parameter1', 3)

        RxCSObject.parameter1 = np.random.randn(5)

        self.__parametersCheck_error(RxCSObject, SizeError, strTestName)

    def __size_restriction_correct_vector_tuple(self):
        """
            Test of 'parameter size' restriction check.
            Wanted output: Correct
        """

        strTestName = 'Vector size higher than the size of a tuple (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('tRefParameter1', 'Tuple ref. parameter')
        RxCSObject.paramType('tRefParameter1', tuple)

        # Now, let me define a Numpy vector
        RxCSObject.paramAddMan('parameter1', 'Numpy array 1D parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramSizH('parameter1', 'tRefParameter1', mul=2)

        RxCSObject.tRefParameter1 = (0, 1, 0)
        RxCSObject.parameter1 = np.random.randn(7)

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __size_restriction_incorrect_vector_tuple(self):
        """
            Test of 'parameter size' restriction check.
            Wanted output: SizeError
        """

        strTestName = 'Vector size equal to the size of a tuple (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('tRefParameter1', 'Tuple ref. parameter')
        RxCSObject.paramType('tRefParameter1', tuple)

        # Now, let me define a Numpy vector
        RxCSObject.paramAddMan('parameter1', 'Numpy array 1D parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramSizEq('parameter1', 'tRefParameter1', mul=2)

        RxCSObject.tRefParameter1 = (0, 1, 0, 4)
        RxCSObject.parameter1 = np.random.randn(9)

        self.__parametersCheck_error(RxCSObject, SizeError, strTestName)

    def __size_restriction_correct_vector_vector(self):
        """
            Test of 'parameter size' restriction check.
            Wanted output: Correct
        """

        strTestName = 'Vector size lower or equal to the size of a vector (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('vRefParameter1', 'Vector ref. parameter')
        RxCSObject.paramType('vRefParameter1', np.ndarray)

        # Now, let me define a Numpy vector
        RxCSObject.paramAddMan('parameter1', 'Numpy array 1D parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramSizLE('parameter1', 'vRefParameter1', mul=3)

        RxCSObject.vRefParameter1 = np.array([0, 1, 0, 4])
        RxCSObject.parameter1 = np.random.randn(9)

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __size_restriction_incorrect_vector_vector(self):
        """
            Test of 'parameter size' restriction check.
            Wanted output: SizeError
        """

        strTestName = 'Vector size lower than the size of a vector (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('vRefParameter1', 'Vector ref. parameter')
        RxCSObject.paramType('vRefParameter1', np.ndarray)

        # Now, let me define a Numpy vector
        RxCSObject.paramAddMan('parameter1', 'Numpy array 2D parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramSizL('parameter1', 'vRefParameter1')

        RxCSObject.vRefParameter1 = np.array([0, 1, 0, 4])
        RxCSObject.parameter1 = np.random.randn(4)

        self.__parametersCheck_error(RxCSObject, SizeError, strTestName)

    def __size_restriction_correct_matrix_number(self):
        """
            Test of 'parameter size' restriction check.
            Wanted output: Correct
        """

        strTestName = 'Matrix size higher or equal to a number (correct)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'Numpy array 2D parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramSizHE('parameter1', 13)

        RxCSObject.parameter1 = np.random.randn(3, 5)

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __size_restriction_incorrect_matrix_number(self):
        """
            Test of 'parameter size' restriction check.
            Wanted output: SizeError
        """

        strTestName = 'Matrix size lower than a number (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'Numpy array 2D parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramSizL('parameter1', 15)

        RxCSObject.parameter1 = np.random.randn(3, 5)

        self.__parametersCheck_error(RxCSObject, SizeError, strTestName)

    def __size_restriction_correct_matrix_parameter(self):
        """
            Test of 'parameter size' restriction check.
            Wanted output: Correct
        """

        strTestName = 'Matrix size equal to a parameter (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('iRefParameter1', 'Ref. parameter')
        RxCSObject.paramType('iRefParameter1', int)

        # Now, let us define a matrix
        RxCSObject.paramAddMan('parameter1', 'Numpy array 2D parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramSizEq('parameter1', 'iRefParameter1')

        RxCSObject.iRefParameter1 = 20
        RxCSObject.parameter1 = np.random.randn(5, 4)

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __size_restriction_incorrect_matrix_parameter(self):
        """
            Test of 'parameter size' restriction check.
            Wanted output: SizeError
        """

        strTestName = 'Matrix size higher or equal to a parameter (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('iRefParameter1', 'Ref. parameter')
        RxCSObject.paramType('iRefParameter1', int)

        # Now, let us define a matrix
        RxCSObject.paramAddMan('parameter1', 'Numpy array 2D parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramSizHE('parameter1', 'iRefParameter1', add=2)

        RxCSObject.iRefParameter1 = 20
        RxCSObject.parameter1 = np.random.randn(4, 4)

        self.__parametersCheck_error(RxCSObject, SizeError, strTestName)

    def __size_restriction_correct_matrix_string(self):
        """
            Test of 'parameter size' restriction check.
            Wanted output: Correct
        """

        strTestName = 'Matrix size lower than the size of a string (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('strRefParameter1', 'String ref. parameter')
        RxCSObject.paramType('strRefParameter1', str)

        # Now, let us define a matrix
        RxCSObject.paramAddMan('parameter1', 'Numpy array 2D parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramSizL('parameter1', 'strRefParameter1')

        RxCSObject.strRefParameter1 = 'abcde'
        RxCSObject.parameter1 = np.random.randn(2, 2)

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __size_restriction_incorrect_matrix_string(self):
        """
            Test of 'parameter size' restriction check.
            Wanted output: SizeError
        """

        strTestName = 'Matrix size higher than the size of a string (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('strRefParameter1', 'String ref. parameter')
        RxCSObject.paramType('strRefParameter1', str)

        # Now, let us define a matrix
        RxCSObject.paramAddMan('parameter1', 'Numpy array 2D parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramSizH('parameter1', 'strRefParameter1')

        RxCSObject.strRefParameter1 = 'abcde'
        RxCSObject.parameter1 = np.random.randn(2, 2)

        self.__parametersCheck_error(RxCSObject, SizeError, strTestName)

    def __size_restriction_correct_matrix_matrix(self):
        """
            Test of 'parameter size' restriction check.
            Wanted output: Correct
        """

        strTestName = 'Matrix size equal to the size of a matrix (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('mRefParameter1', 'String ref. parameter')
        RxCSObject.paramType('mRefParameter1', np.ndarray)

        # Now, let us define a matrix
        RxCSObject.paramAddMan('parameter1', 'Numpy array 2D parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramSizEq('parameter1', 'mRefParameter1')

        RxCSObject.mRefParameter1 = np.random.randn(2, 2)
        RxCSObject.parameter1 = np.random.randn(2, 2)

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __size_restriction_incorrect_matrix_matrix(self):
        """
            Test of 'parameter size' restriction check.
            Wanted output: SizeError
        """

        strTestName = 'Matrix size lower than the size of a matrix (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('mRefParameter1', 'String ref. parameter')
        RxCSObject.paramType('mRefParameter1', np.ndarray)

        # Now, let us define a matrix
        RxCSObject.paramAddMan('parameter1', 'Numpy array 2D parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramSizL('parameter1', 'mRefParameter1')

        RxCSObject.mRefParameter1 = np.random.randn(2, 2)
        RxCSObject.parameter1 = np.random.randn(2, 2)

        self.__parametersCheck_error(RxCSObject, SizeError, strTestName)

    def __NDim_restriction_correct_list_number(self):
        """
            Test of 'the number of dimensions' restriction check.
            Wanted output: Correct
        """

        strTestName = 'The number of dimensions in a list equals a number (correct)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'List parameter')
        RxCSObject.paramType('parameter1', list)
        RxCSObject.paramNDimEq('parameter1', 1)

        RxCSObject.parameter1 = [4, 2, 11, -1, -4]

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __NDim_restriction_incorrect_list_number(self):
        """
            Test of 'the number of dimensions' restriction check.
            Wanted output: NDimError
        """

        strTestName = 'The number of dimensions in a list higher than a number (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'List parameter')
        RxCSObject.paramType('parameter1', list)
        RxCSObject.paramNDimH('parameter1', 1)

        RxCSObject.parameter1 = [4, 2, 11, -1, -4]

        self.__parametersCheck_error(RxCSObject, NDimError, strTestName)

    def __NDim_restriction_correct_list_parameter(self):
        """
            Test of 'the number of dimensions' restriction check.
            Wanted output: Correct
        """

        strTestName = 'The number of dimensions in a list lower than a parameter (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('iRefParameter1', 'Int parameter')
        RxCSObject.paramType('iRefParameter1', int)

        # Now, let us define a list parameter
        RxCSObject.paramAddMan('parameter1', 'List parameter')
        RxCSObject.paramType('parameter1', list)
        RxCSObject.paramNDimH('parameter1', 'iRefParameter1')

        RxCSObject.iRefParameter1 = 0
        RxCSObject.parameter1 = [4, 2, 11, -1, -4]

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __NDim_restriction_incorrect_list_parameter(self):
        """
            Test of 'the number of dimensions' restriction check.
            Wanted output: NDimError
        """

        strTestName = 'The number of dimensions in a list lower or equal to a parameter (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('iRefParameter1', 'Int parameter')
        RxCSObject.paramType('iRefParameter1', int)

        # Now, let us define a list parameter
        RxCSObject.paramAddMan('parameter1', 'List parameter')
        RxCSObject.paramType('parameter1', list)
        RxCSObject.paramNDimLE('parameter1', 'iRefParameter1', mul=0.5, add=-1)

        RxCSObject.iRefParameter1 = 2
        RxCSObject.parameter1 = [4, 2, 11, -1, -4]

        self.__parametersCheck_error(RxCSObject, NDimError, strTestName)

    def __NDim_restriction_correct_ndarray_number(self):
        """
            Test of 'the number of dimensions' restriction check.
            Wanted output: Correct
        """

        strTestName = 'The number of dimensions in a Numpy array higher than a number (correct)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'Numpy array parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramNDimH('parameter1', 1)

        RxCSObject.parameter1 = np.random.rand(3, 4)

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __NDim_restriction_incorrect_ndarray_number(self):
        """
            Test of 'the number of dimensions' restriction check.
            Wanted output: NDimError
        """

        strTestName = 'The number of dimensions in a Numpy array higher or equal to a number (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'Numpy array parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramNDimHE('parameter1', 3)

        RxCSObject.parameter1 = np.random.rand(3, 4)

        self.__parametersCheck_error(RxCSObject, NDimError, strTestName)

    def __NDim_restriction_correct_ndarray_parameter(self):
        """
            Test of 'the number of dimensions' restriction check.
            Wanted output: Correct
        """

        strTestName = 'The number of dimensions in a Numpy array lower or equal to a parameter (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('iRefParameter1', 'Int parameter')
        RxCSObject.paramType('iRefParameter1', int)

        # Now, let us define a Numpy array parameter
        RxCSObject.paramAddMan('parameter1', 'Numpy array parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramNDimLE('parameter1', 'iRefParameter1')

        RxCSObject.iRefParameter1 = 3
        RxCSObject.parameter1 = np.random.rand(3, 4, 5)

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __NDim_restriction_incorrect_ndarray_parameter(self):
        """
            Test of 'the number of dimensions' restriction check.
            Wanted output: NDimError
        """

        strTestName = 'The number of dimensions in a Numpy array equals a parameter (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('iRefParameter1', 'Int parameter')
        RxCSObject.paramType('iRefParameter1', int)

        # Now, let us define a Numpy array parameter
        RxCSObject.paramAddMan('parameter1', 'Numpy array parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramNDimEq('parameter1', 'iRefParameter1')

        RxCSObject.iRefParameter1 = 3
        RxCSObject.parameter1 = np.random.rand(3, 4)

        self.__parametersCheck_error(RxCSObject, NDimError, strTestName)

    def __NDim_restriction_correct_ndarray_tuple(self):
        """
            Test of 'the number of dimensions' restriction check.
            Wanted output: Correct
        """

        strTestName = 'The number of dimensions in a Numpy array equals the number of dimensions in a tuple (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('tRefParameter1', 'Tuple parameter')
        RxCSObject.paramType('tRefParameter1', tuple)

        # Now, let us define a Numpy array parameter
        RxCSObject.paramAddMan('parameter1', 'Numpy array parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramNDimEq('parameter1', 'tRefParameter1')

        RxCSObject.tRefParameter1 = (1, 11, 12)
        RxCSObject.parameter1 = np.random.rand(4, )

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __NDim_restriction_incorrect_ndarray_tuple(self):
        """
            Test of 'the number of dimensions' restriction check.
            Wanted output: NDimError
        """

        strTestName = 'The number of dimensions in a Numpy array lower then the number of dimensions in a tuple (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('tRefParameter1', 'Tuple parameter')
        RxCSObject.paramType('tRefParameter1', tuple)

        # Now, let us define a Numpy array parameter
        RxCSObject.paramAddMan('parameter1', 'Numpy array parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramNDimL('parameter1', 'tRefParameter1', mul=2, add=1)

        RxCSObject.tRefParameter1 = (1, 11, 12)
        RxCSObject.parameter1 = np.random.rand(4, 2, 4)

        self.__parametersCheck_error(RxCSObject, NDimError, strTestName)

    def __NDim_restriction_correct_ndarray_list(self):
        """
            Test of 'the number of dimensions' restriction check.
            Wanted output: Correct
        """

        strTestName = 'The number of dimensions in a Numpy array higher then the number of dimensions in a list (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('lRefParameter1', 'List parameter')
        RxCSObject.paramType('lRefParameter1', list)

        # Now, let us define a Numpy array parameter
        RxCSObject.paramAddMan('parameter1', 'Numpy array parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramNDimH('parameter1', 'lRefParameter1')

        RxCSObject.lRefParameter1 = [1, 11, 12]
        RxCSObject.parameter1 = np.random.rand(4, 2, 4)

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __NDim_restriction_incorrect_ndarray_list(self):
        """
            Test of 'the number of dimensions' restriction check.
            Wanted output: NDimError
        """

        strTestName = 'The number of dimensions in a Numpy array higher or equal to the number of dimensions in a list (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('lRefParameter1', 'List parameter')
        RxCSObject.paramType('lRefParameter1', list)

        # Now, let us define a Numpy array parameter
        RxCSObject.paramAddMan('parameter1', 'Numpy array parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramNDimHE('parameter1', 'lRefParameter1', mul=2)

        RxCSObject.lRefParameter1 = [1, 11, 12]
        RxCSObject.parameter1 = np.random.rand(4)

        self.__parametersCheck_error(RxCSObject, NDimError, strTestName)

    def __NDim_restriction_correct_ndarray_ndarray(self):
        """
            Test of 'the number of dimensions' restriction check.
            Wanted output: Correct
        """

        strTestName = 'The number of dimensions in a Numpy array equals the number of dimensions in another Numpy array (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('m4RefParameter1', 'Numpy array reference parameter')
        RxCSObject.paramType('m4RefParameter1', np.ndarray)

        # Now, let us define a Numpy array parameter
        RxCSObject.paramAddMan('parameter1', 'Numpy array parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramNDimHE('parameter1', 'm4RefParameter1', add=1)

        RxCSObject.m4RefParameter1 = np.random.rand(4, 2, 9)
        RxCSObject.parameter1 = np.random.rand(2, 1, 9, 5)

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __NDim_restriction_incorrect_ndarray_ndarray(self):
        """
            Test of 'the number of dimensions' restriction check.
            Wanted output: NDimError
        """

        strTestName = 'The number of dimensions in a Numpy array lower than the number of dimensions in another Numpy array (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('vRefParameter1', 'Numpy array reference parameter')
        RxCSObject.paramType('vRefParameter1', np.ndarray)

        # Now, let us define a Numpy array parameter
        RxCSObject.paramAddMan('parameter1', 'Numpy array parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramNDimL('parameter1', 'vRefParameter1', mul=2)

        RxCSObject.vRefParameter1 = np.random.rand(4)
        RxCSObject.parameter1 = np.random.rand(2, 1, 9)

        self.__parametersCheck_error(RxCSObject, NDimError, strTestName)

    def __DimSiz_restriction_correct_list_number(self):
        """
            Test of 'size of a dimension' restriction check.
            Wanted output: Correct
        """

        strTestName = 'The size of a list dimension equal to a number (correct)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'List parameter')
        RxCSObject.paramType('parameter1', list)
        RxCSObject.paramDimEq('parameter1', 1, 1)  # Size of dimension 1 must be 1

        RxCSObject.parameter1 = [0, 1, 2]

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __DimSiz_restriction_incorrect_list_number(self):
        """
            Test of 'size of a dimension' restriction check.
            Wanted output: DimSizError
        """

        strTestName = 'The size of a list dimension higher than a number (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'List parameter')
        RxCSObject.paramType('parameter1', list)
        RxCSObject.paramDimH('parameter1', 2, 0, mul=3)   # Size of dimension 0 must be higher than 3 * 2 = 6

        RxCSObject.parameter1 = [0, 1, 2, 4]

        self.__parametersCheck_error(RxCSObject, DimSizError, strTestName)

    def __DimSiz_restriction_correct_list_number_pedantic(self):
        """
            Test of 'size of a dimension' restriction check.
            Wanted output: Correct
        """

        strTestName = 'The size of a list dimension equal to a number [pedantic] (correct)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'List parameter')
        RxCSObject.paramType('parameter1', list)
        RxCSObject.paramDimEq('parameter1', 4, 0, pedantic=1)   # Size of dimension 0 must be 4

        RxCSObject.parameter1 = [0, 1, 2, 4]

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __DimSiz_restriction_incorrect_list_number_pedantic(self):
        """
            Test of 'size of a dimension' restriction check.
            Wanted output: DimSizError
        """

        strTestName = 'The size of a list dimension higher than a number [pedantic] (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'List parameter')
        RxCSObject.paramType('parameter1', list)
        RxCSObject.paramDimH('parameter1', 2, 1, pedantic=1)   # Size of dimension 0 must be 4

        RxCSObject.parameter1 = [0, 1, 2, 4]

        self.__parametersCheck_error(RxCSObject, DimSizError, strTestName)

    def __DimSiz_restriction_correct_list_parameter(self):
        """
            Test of 'size of a dimension' restriction check.
            Wanted output: Correct
        """

        strTestName = 'The size of a list dimension lower than a parameter (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('iParameter1', 'Int parameter')
        RxCSObject.paramType('iParameter1', int)

        # Now, let us define a list
        RxCSObject.paramAddMan('parameter1', 'List parameter')
        RxCSObject.paramType('parameter1', list)
        RxCSObject.paramDimL('parameter1', 'iParameter1', 0)   # Size of dimension 0 must be lower than 'iParameter1'

        RxCSObject.iParameter1 = 5
        RxCSObject.parameter1 = [0, 1, 2, 4]

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __DimSiz_restriction_incorrect_list_parameter(self):
        """
            Test of 'size of a dimension' restriction check.
            Wanted output: DimSizError
        """

        strTestName = 'The size of a list dimension higher than a parameter (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('iParameter1', 'Int parameter')
        RxCSObject.paramType('iParameter1', int)

        # Now, let us define a list
        RxCSObject.paramAddMan('parameter1', 'List parameter')
        RxCSObject.paramType('parameter1', list)
        RxCSObject.paramDimH('parameter1', 'iParameter1', 0, mul=2)   # Size of dimension 0 must be higher than 2 * 'iParameter1'

        RxCSObject.iParameter1 = 2
        RxCSObject.parameter1 = [0, 1, 2, 4]

        self.__parametersCheck_error(RxCSObject, DimSizError, strTestName)

    def __DimSiz_restriction_correct_list_parameter_pedantic(self):
        """
            Test of 'size of a dimension' restriction check.
            Wanted output: Correct
        """

        strTestName = 'The size of a list dimension lower than a parameter [pedantic] (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('iParameter1', 'Int parameter')
        RxCSObject.paramType('iParameter1', int)

        # Now, let us define a list
        RxCSObject.paramAddMan('parameter1', 'List parameter')
        RxCSObject.paramType('parameter1', list)
        RxCSObject.paramDimL('parameter1', 'iParameter1', 0, mul=2, pedantic=1)   # Size of dimension 0 must be lower than 2 * 'iParameter1'

        RxCSObject.iParameter1 = 2
        RxCSObject.parameter1 = [0, 1, 4]

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __DimSiz_restriction_incorrect_list_parameter_pedantic(self):
        """
            Test of 'size of a dimension' restriction check.
            Wanted output: DimSizError
        """

        strTestName = 'The size of a list dimension higher than a parameter [pedantic] (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('iParameter1', 'Int parameter')
        RxCSObject.paramType('iParameter1', int)

        # Now, let us define a list
        RxCSObject.paramAddMan('parameter1', 'List parameter')
        RxCSObject.paramType('parameter1', list)
        RxCSObject.paramDimH('parameter1', 'iParameter1', 0, mul=2, pedantic=1)   # Size of dimension 0 must be higher than 2 * 'iParameter1'

        RxCSObject.iParameter1 = 2
        RxCSObject.parameter1 = [0, 1, 4]

        self.__parametersCheck_error(RxCSObject, DimSizError, strTestName)

    def __DimSiz_restriction_correct_ndarray_number(self):
        """
            Test of 'size of a dimension' restriction check.
            Wanted output: Correct
        """

        strTestName = 'The size of a dimension of a Numpy array higher or equal to a number (correct)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'Numpy array parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramDimHE('parameter1', 3, 1)   # Size of dimension 1 must be higher than 3'

        RxCSObject.parameter1 = np.random.randn(3, 3)

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __DimSiz_restriction_incorrect_ndarray_number(self):
        """
            Test of 'size of a dimension' restriction check.
            Wanted output: DimSizError
        """

        strTestName = 'The size of a dimension of a Numpy array lower or equal to a number (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'Numpy array parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramDimLE('parameter1', 3, 1)   # Size of dimension 1 must be higher than 3'

        RxCSObject.parameter1 = np.random.randn(3, 4)

        self.__parametersCheck_error(RxCSObject, DimSizError, strTestName)

    def __DimSiz_restriction_correct_ndarray_number2(self):
        """
            Test of 'size of a dimension' restriction check.
            Wanted output: Correct
        """

        strTestName = 'The number of columns of a Numpy array lower or equal to a number (correct)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'Numpy array parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramDimLE('parameter1', 3, 'columns')

        RxCSObject.parameter1 = np.random.randn(3)

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __DimSiz_restriction_incorrect_ndarray_number2(self):
        """
            Test of 'size of a dimension' restriction check.
            Wanted output: DimSizError
        """

        strTestName = 'The number of rows of a Numpy array equals to a number (correct)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'Numpy array parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramDimEq('parameter1', 1, 'columns')

        RxCSObject.parameter1 = np.random.randn(3)

        self.__parametersCheck_error(RxCSObject, DimSizError, strTestName)

    def __DimSiz_restriction_correct_ndarray_number_pedantic(self):
        """
            Test of 'size of a dimension' restriction check.
            Wanted output: Correct
        """

        strTestName = 'The size of a dimension of a Numpy array higher or equal to a number [pedantic] (correct)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'Numpy array parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramDimHE('parameter1', 3, 'rows', pedantic=1)

        RxCSObject.parameter1 = np.random.randn(3, 3)

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __DimSiz_restriction_incorrect_ndarray_number_pedantic(self):
        """
            Test of 'size of a dimension' restriction check.
            Wanted output: DimSizError
        """

        strTestName = 'The size of a dimension of a Numpy array lower or equal to a number [pedantic] (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'Numpy array parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramDimLE('parameter1', 13, 'pages', pedantic=1)

        RxCSObject.parameter1 = np.random.randn(14, 3, 3)

        self.__parametersCheck_error(RxCSObject, DimSizError, strTestName)

    def __DimSiz_restriction_correct_ndarray_number_pedantic2(self):
        """
            Test of 'size of a dimension' restriction check.
            Wanted output: Correct
        """

        strTestName = 'The size of a dimension of a Numpy array higher or equal to a number (2) [pedantic] (correct)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'Numpy array parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramDimHE('parameter1', 3, 'pages', pedantic=1)

        RxCSObject.parameter1 = np.random.randn(10, 3, 3)

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __DimSiz_restriction_incorrect_ndarray_number_pedantic2(self):
        """
            Test of 'size of a dimension' restriction check.
            Wanted output: DimSizError
        """

        strTestName = 'The size of a dimension of a Numpy array lower or equal to a number (2) [pedantic] (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'Numpy array parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramDimLE('parameter1', 2, 'rows', pedantic=1)

        RxCSObject.parameter1 = np.random.randn(3, 3)

        self.__parametersCheck_error(RxCSObject, DimSizError, strTestName)

    def __DimSiz_restriction_correct_ndarray_parameter(self):
        """
            Test of 'size of a dimension' restriction check.
            Wanted output: Correct
        """

        strTestName = 'The size of a dimension of a Numpy array equals a parameter (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('iParameter1', 'Int parameter')
        RxCSObject.paramType('iParameter1', int)

        # Now, let us define a Numpy Array
        RxCSObject.paramAddMan('parameter1', 'Numpy array parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramDimEq('parameter1', 'iParameter1', 'pages')

        RxCSObject.iParameter1 = 1
        RxCSObject.parameter1 = np.random.randn(4, 3)

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __DimSiz_restriction_incorrect_ndarray_parameter(self):
        """
            Test of 'size of a dimension' restriction check.
            Wanted output: DimSizError
        """

        strTestName = 'The size of a dimension of a Numpy array lower than a parameter (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('iParameter1', 'Int parameter')
        RxCSObject.paramType('iParameter1', int)

        # Now, let us define a Numpy Array
        RxCSObject.paramAddMan('parameter1', 'Numpy array parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramDimL('parameter1', 'iParameter1', 'columns')

        RxCSObject.iParameter1 = 4
        RxCSObject.parameter1 = np.random.randn(2, 4, 7)

        self.__parametersCheck_error(RxCSObject, DimSizError, strTestName)

    def __DimSiz_restriction_correct_ndarray_parameter_pedantic(self):
        """
            Test of 'size of a dimension' restriction check.
            Wanted output: Correct
        """

        strTestName = 'The size of a dimension of a Numpy array lower or equal to a parameter [pedantic] (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('iParameter1', 'Int parameter')
        RxCSObject.paramType('iParameter1', int)

        # Now, let us define a Numpy Array
        RxCSObject.paramAddMan('parameter1', 'Numpy array parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramDimLE('parameter1', 'iParameter1', 'rows', pedantic=1)

        RxCSObject.iParameter1 = 10
        RxCSObject.parameter1 = np.random.randn(2, 4, 7)

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __DimSiz_restriction_incorrect_ndarray_parameter_pedantic(self):
        """
            Test of 'size of a dimension' restriction check.
            Wanted output: DimSizError
        """

        strTestName = 'The size of a dimension of a Numpy array higher or equal to a parameter [pedantic] (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('iParameter1', 'Int parameter')
        RxCSObject.paramType('iParameter1', int)

        # Now, let us define a Numpy Array
        RxCSObject.paramAddMan('parameter1', 'Numpy array parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramDimHE('parameter1', 'iParameter1', 'pages', pedantic=1)

        RxCSObject.iParameter1 = 10
        RxCSObject.parameter1 = np.random.randn(2, 2, 2)

        self.__parametersCheck_error(RxCSObject, DimSizError, strTestName)

    def __DimSiz_restriction_correct_ndarray_tuple(self):
        """
            Test of 'size of a dimension' restriction check.
            Wanted output: Correct
        """

        strTestName = 'The size of a dimension of a Numpy array equals the size of a tuple (correct) '
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('tParameter1', 'Tuple parameter')
        RxCSObject.paramType('tParameter1', tuple)

        # Now, let us define a Numpy Array
        RxCSObject.paramAddMan('parameter1', 'Numpy array parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramDimEq('parameter1', 'tParameter1', 'pages', 1, mul=2, add=-1)

        RxCSObject.tParameter1 = (3, 4, 5, 6, 7)
        RxCSObject.parameter1 = np.random.randn(2, 2)

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __DimSiz_restriction_incorrect_ndarray_tuple(self):
        """
            Test of 'size of a dimension' restriction check.
            Wanted output: DimSizError
        """

        strTestName = 'The size of a dimension of a Numpy array higher than the size of a tuple (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('tParameter1', 'Tuple parameter')
        RxCSObject.paramType('tParameter1', tuple)

        # Now, let us define a Numpy Array
        RxCSObject.paramAddMan('parameter1', 'Numpy array parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramDimH('parameter1', 'tParameter1', 'pages', 1, mul=2)

        RxCSObject.tParameter1 = (3, 4, 5, 6, 7)
        RxCSObject.parameter1 = np.random.randn(2, 2)

        self.__parametersCheck_error(RxCSObject, DimSizError, strTestName)

    def __DimSiz_restriction_correct_ndarray_tuple_pedantic(self):
        """
            Test of 'size of a dimension' restriction check.
            Wanted output: Correct
        """

        strTestName = 'The size of a dimension of a Numpy array lower than the size of a tuple [pedantic] (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('tParameter1', 'Tuple parameter')
        RxCSObject.paramType('tParameter1', tuple)

        # Now, let us define a Numpy Array
        RxCSObject.paramAddMan('parameter1', 'Numpy array parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramDimL('parameter1', 'tParameter1', 'rows', 0, pedantic=1)

        RxCSObject.tParameter1 = (3, 4, 5, 6, 7)
        RxCSObject.parameter1 = np.random.randn(4, 2)

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __DimSiz_restriction_incorrect_ndarray_tuple_pedantic(self):
        """
            Test of 'size of a dimension' restriction check.
            Wanted output: ValueError
        """

        strTestName = 'The size of a dimension of a Numpy array equals the size of a tuple [pedantic] (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('tParameter1', 'Tuple parameter')
        RxCSObject.paramType('tParameter1', tuple)

        # Now, let us define a Numpy Array
        RxCSObject.paramAddMan('parameter1', 'Numpy array parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramDimEq('parameter1', 'tParameter1', 'columns', 1, pedantic=1)

        RxCSObject.tParameter1 = (3, 4, 5, 6, 7)
        RxCSObject.parameter1 = np.random.randn(4, 2)

        self.__parametersCheck_error(RxCSObject, ValueError, strTestName)

    def __DimSiz_restriction_correct_ndarray_ndarray(self):
        """
            Test of 'size of a dimension' restriction check.
            Wanted output: Correct
        """

        strTestName = 'The size of a dimension of a Numpy array equals the size of a dimension of another Numpy array (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('aParameter1', 'Numpy array parameter')
        RxCSObject.paramType('aParameter1', np.ndarray)

        # Now, let us define a Numpy Array
        RxCSObject.paramAddMan('parameter1', 'Numpy array parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramDimEq('parameter1', 'aParameter1', 'columns', 'rows')

        RxCSObject.parameter1 = np.random.randn(5, 4, 3)  # 5 pages, 4 rows, 3 columns *
        RxCSObject.aParameter1 = np.random.randn(3, 4)    # 3 rows* , *2 columns

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __DimSiz_restriction_incorrect_ndarray_ndarray(self):
        """
            Test of 'size of a dimension' restriction check.
            Wanted output: DimSizError
        """

        strTestName = 'The size of a dimension of a Numpy array higher than the size of a dimension of another Numpy array (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('aParameter1', 'Numpy array parameter')
        RxCSObject.paramType('aParameter1', np.ndarray)

        # Now, let us define a Numpy Array
        RxCSObject.paramAddMan('parameter1', 'Numpy array parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramDimH('parameter1', 'aParameter1', 'rows')

        RxCSObject.parameter1 = np.random.randn(5, 3, 3)  # 5 pages, * 3 rows, 3 columns
        RxCSObject.aParameter1 = np.random.randn(3, 4)    # * 3 rows, 4 columns

        self.__parametersCheck_error(RxCSObject, DimSizError, strTestName)

    def __DimSiz_restriction_correct_ndarray_ndarray2(self):
        """
            Test of 'size of a dimension' restriction check.
            Wanted output: Correct
        """

        strTestName = 'The size of a dimension of a Numpy array lower or equal to the size of a dimension of another Numpy array (2) (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('aParameter1', 'Numpy array parameter')
        RxCSObject.paramType('aParameter1', np.ndarray)

        # Now, let us define a Numpy Array
        RxCSObject.paramAddMan('parameter1', 'Numpy array parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramDimLE('parameter1', 'aParameter1', 'columns', 2, mul=5)

        RxCSObject.parameter1 = np.random.randn(5, 3, 3)     # 5 pages, 3 rows, *3 columns
        RxCSObject.aParameter1 = np.random.randn(4, 3, 1)    # 4pages, 3 rows, *1 column

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __DimSiz_restriction_incorrect_ndarray_ndarray2(self):
        """
            Test of 'size of a dimension' restriction check.
            Wanted output: DimSizError
        """

        strTestName = 'The size of a dimension of a Numpy array higher than the size of a dimension of another Numpy array (2) (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('aParameter1', 'Numpy array parameter')
        RxCSObject.paramType('aParameter1', np.ndarray)

        # Now, let us define a Numpy Array
        RxCSObject.paramAddMan('parameter1', 'Numpy array parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramDimH('parameter1', 'aParameter1', 'columns', 'pages', mul=5, add=2)

        RxCSObject.parameter1 = np.random.randn(3, 3, 4)     # 5 pages, 3 rows, *4 columns
        RxCSObject.aParameter1 = np.random.randn(4, 3, 1)    # *4pages, 3 rows, 1 column

        self.__parametersCheck_error(RxCSObject, DimSizError, strTestName)

    def __DimSiz_restriction_correct_ndarray_ndarray3(self):
        """
            Test of 'size of a dimension' restriction check.
            Wanted output: Correct
        """

        strTestName = 'The size of a dimension of a Numpy array higher than the size of a dimension of another Numpy array (3) (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('aParameter1', 'Numpy array parameter')
        RxCSObject.paramType('aParameter1', np.ndarray)

        # Now, let us define a Numpy Array
        RxCSObject.paramAddMan('parameter1', 'Numpy array parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramDimH('parameter1', 'aParameter1', 'pages', 'pages', mul=2)

        RxCSObject.parameter1 = np.random.randn(10, 3, 4)     # *5 pages, 3 rows, 4 columns
        RxCSObject.aParameter1 = np.random.randn(4, 3, 1)     # *4 pages, 3 rows, 1 column

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __DimSiz_restriction_incorrect_ndarray_ndarray3(self):
        """
            Test of 'size of a dimension' restriction check.
            Wanted output: DimSizError
        """

        strTestName = 'The size of a dimension of a Numpy array higher than the size of a dimension of another Numpy array (3) (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('aParameter1', 'Numpy array parameter')
        RxCSObject.paramType('aParameter1', np.ndarray)

        # Now, let us define a Numpy Array
        RxCSObject.paramAddMan('parameter1', 'Numpy array parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramDimH('parameter1', 'aParameter1', 'pages', 'pages', mul=2)

        RxCSObject.parameter1 = np.random.randn(8, 3, 4)     # * 5 pages, 3 rows, *4 columns
        RxCSObject.aParameter1 = np.random.randn(4, 3, 1)    # * 4pages, 3 rows, *1 column

        self.__parametersCheck_error(RxCSObject, DimSizError, strTestName)

    def __DimSiz_restriction_correct_ndarray_ndarray4(self):
        """
            Test of 'size of a dimension' restriction check.
            Wanted output: Correct
        """

        strTestName = 'The size of a dimension of a Numpy array higher or equal to the size of a dimension of another Numpy array (4) (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('aParameter1', 'Numpy array parameter')
        RxCSObject.paramType('aParameter1', np.ndarray)

        # Now, let us define a Numpy Array
        RxCSObject.paramAddMan('parameter1', 'Numpy array parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramDimHE('parameter1', 'aParameter1', 'pages', 'columns', mul=2)

        RxCSObject.parameter1 = np.random.randn(2, 3, 4)     # * 5 pages, 3 rows, 4 columns
        RxCSObject.aParameter1 = np.random.randn(4, 3, 1)    # 4 pages, 3 rows, * 1 column

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __DimSiz_restriction_incorrect_ndarray_ndarray4(self):
        """
            Test of 'size of a dimension' restriction check.
            Wanted output: DimSizError
        """

        strTestName = 'The size of a dimension of a Numpy array higher than the size of a dimension of another Numpy array (4) (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('aParameter1', 'Numpy array parameter')
        RxCSObject.paramType('aParameter1', np.ndarray)

        # Now, let us define a Numpy Array
        RxCSObject.paramAddMan('parameter1', 'Numpy array parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramDimH('parameter1', 'aParameter1', 'pages', 'columns', mul=2)

        RxCSObject.parameter1 = np.random.randn(2, 3, 4)     # * 5 pages, 3 rows, 4 columns
        RxCSObject.aParameter1 = np.random.randn(4, 3, 1)    # 4 pages, 3 rows, * 1 column

        self.__parametersCheck_error(RxCSObject, DimSizError, strTestName)

    def __DimSiz_restriction_correct_ndarray_ndarray_pedantic(self):
        """
            Test of 'size of a dimension' restriction check.
            Wanted output: Correct
        """

        strTestName = 'The size of a dimension of a Numpy array lower or equal to the size of a dimension of another Numpy array [pedantic] (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('aParameter1', 'Numpy array parameter')
        RxCSObject.paramType('aParameter1', np.ndarray)

        # Now, let us define a Numpy Array
        RxCSObject.paramAddMan('parameter1', 'Numpy array parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramDimLE('parameter1', 'aParameter1', 'pages', 'rows', pedantic=1)

        RxCSObject.parameter1 = np.random.randn(2, 3, 4)     # * 12 pages, 3 rows, 4 columns
        RxCSObject.aParameter1 = np.random.randn(4, 3, 1)    # 4 pages, * 3 rows, 1 column

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __DimSiz_restriction_incorrect_ndarray_ndarray_pedantic(self):
        """
            Test of 'size of a dimension' restriction check.
            Wanted output: DimSizError
        """

        strTestName = 'The size of a dimension of a Numpy array lower than the size of a dimension of another Numpy array [pedantic] (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('aParameter1', 'Numpy array parameter')
        RxCSObject.paramType('aParameter1', np.ndarray)

        # Now, let us define a Numpy Array
        RxCSObject.paramAddMan('parameter1', 'Numpy array parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramDimL('parameter1', 'aParameter1', 'rows', 'columns', pedantic=1)

        RxCSObject.parameter1 = np.random.randn(3, 4)    # *3 rows, 4 columns
        RxCSObject.aParameter1 = np.random.randn(3, 2)   # 3 rows, * 2 columns

        self.__parametersCheck_error(RxCSObject, DimSizError, strTestName)

    def __DimSiz_restriction_correct_ndarray_ndarray_pedantic2(self):
        """
            Test of 'size of a dimension' restriction check.
            Wanted output: Correct
        """

        strTestName = 'The size of a dimension of a Numpy array higher than the size of a dimension of another Numpy array [pedantic] (2) (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('aParameter1', 'Numpy array parameter')
        RxCSObject.paramType('aParameter1', np.ndarray)

        # Now, let us define a Numpy Array
        RxCSObject.paramAddMan('parameter1', 'Numpy array parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramDimH('parameter1', 'aParameter1', 'pages', 'columns', pedantic=1, add=1)

        RxCSObject.parameter1 = np.random.randn(4, 3, 4)    # *3 rows, 4 columns
        RxCSObject.aParameter1 = np.random.randn(3, 2)   # 3 rows, * 2 columns

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __DimSiz_restriction_incorrect_ndarray_ndarray_pedantic2(self):
        """
            Test of 'size of a dimension' restriction check.
            Wanted output: DimSizError
        """

        strTestName = 'The size of a dimension of a Numpy array higher than the size of a dimension of another Numpy array [pedantic] (2) (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('aParameter1', 'Numpy array parameter')
        RxCSObject.paramType('aParameter1', np.ndarray)

        # Now, let us define a Numpy Array
        RxCSObject.paramAddMan('parameter1', 'Numpy array parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramDimH('parameter1', 'aParameter1', 'columns', 'columns', pedantic=1, add=-1)

        RxCSObject.parameter1 = np.random.randn(4)
        RxCSObject.aParameter1 = np.random.randn(6)

        self.__parametersCheck_error(RxCSObject, DimSizError, strTestName)

    def __DimSiz_restriction_correct_ndarray_ndarray_pedantic3(self):
        """
            Test of 'size of a dimension' restriction check.
            Wanted output: Correct
        """

        strTestName = 'The size of a dimension of a Numpy array higher or equal to the size of a dimension of another Numpy array [pedantic] (3) (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('aParameter1', 'Numpy array parameter')
        RxCSObject.paramType('aParameter1', np.ndarray)

        # Now, let us define a Numpy Array
        RxCSObject.paramAddMan('parameter1', 'Numpy array parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramDimHE('parameter1', 'aParameter1', 'rows', 'columns', pedantic=1, add=1)

        RxCSObject.parameter1 = np.random.randn(4, 3, 4)
        RxCSObject.aParameter1 = np.random.randn(3, 2)

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __DimSiz_restriction_incorrect_ndarray_ndarray_pedantic3(self):
        """
            Test of 'size of a dimension' restriction check.
            Wanted output: ValueError
        """

        strTestName = 'The size of a dimension of a Numpy array higher than the size of a dimension of another Numpy array [pedantic] (3) (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('aParameter1', 'Numpy array parameter')
        RxCSObject.paramType('aParameter1', np.ndarray)

        # Now, let us define a Numpy Array
        RxCSObject.paramAddMan('parameter1', 'Numpy array parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramDimHE('parameter1', 'aParameter1', 1, 'pages', pedantic=1)

        RxCSObject.parameter1 = np.random.randn(3, 4)
        RxCSObject.aParameter1 = np.random.randn(3, 2)

        self.__parametersCheck_error(RxCSObject, ValueError, strTestName)

    def __Unique_restriction_correct_ndarray(self):
        """
            Test of element uniqness restriction check.
            Wanted output: Correct
        """
        strTestName = 'Uniqness of elements in Numpy array (correct)'
        RxCSObject = _RxCSobject()

        # Let us define a Numpy Array
        RxCSObject.paramAddMan('parameter1', 'Numpy array parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramUnique('parameter1')

        RxCSObject.parameter1 =  np.unique(np.random.randint(1, 1e6, 1e6))
        
        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)

    def __Unique_restriction_incorrect_ndarray(self):
        """
            Test of element uniqness restriction check.
            Wanted output: UniqnessError
        """
        strTestName = 'Uniqness of elements in Numpy array (incorrect)'
        RxCSObject = _RxCSobject()

        # Let us define a Numpy Array
        RxCSObject.paramAddMan('parameter1', 'Numpy array parameter')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramUnique('parameter1')

        RxCSObject.parameter1 = np.random.randint(1, 1e3, (1e2, 1e2))

        self.__parametersCheck_error(RxCSObject, UniqnessError, strTestName)

    def __Opt_value_depends_on_another_correct(self):
        """
            Test of value propagation onto optional parameters.
            Wanted output: Correct
        """
        strTestName = 'Test of value propagation onto optional parameters'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'Reference parameter #1')
        RxCSObject.paramAddMan('parameter2', 'Reference parameter #2')

        RxCSObject.paramAddOpt('optpar1', 'Optional parameter #1', default='$$parameter1')
        RxCSObject.paramType('optpar1', int)
        RxCSObject.paramHE('optpar1', 4)
        RxCSObject.paramLE('optpar1', 4)

        RxCSObject.paramAddOpt('optpar2', 'Optional parameter #1', default='$$parameter2')
        RxCSObject.paramType('optpar2', int)
        RxCSObject.paramHE('optpar2', 1)
        RxCSObject.paramLE('optpar2', 1)
        
        RxCSObject.parameter1 = 4
        RxCSObject.parameter2 = 1
        
        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __parametersCheck_error(self, RxCSObject, error, strTestName):
        """
            Main engine of tests on RxCS object.

            Input:
                    RxCSObject:    the object being tested
                    error          wanted error, or string 'correct'
                    strTestName:   name of the current test

            Output:
                    none

            Author:
                    Jacek Pierzchlewski

            Last modification:
                    11 June 2015

        """
        self._iNTests = self._iNTests + 1
        strTestIndex = 'Test #%d:  ' % (self._iNTests)

        # Correct output is wanted
        if isinstance(error, str):
            try:
                RxCSObject.parametersCheck()
            except:
                print(strTestIndex + strTestName + (self.iMaxCols - len(strTestName) - len(strTestIndex)) * '.' + 'Test failed!')
            else:
                print(strTestIndex + strTestName + (self.iMaxCols - len(strTestName) - len(strTestIndex)) * '.' + 'Test ok!')

        # Error is wanted
        else:
            try:
                RxCSObject.parametersCheck()
            except error:
                print(strTestIndex + strTestName + (self.iMaxCols - len(strTestName) - len(strTestIndex)) * '.' + 'Test ok!')
            except:
                print(strTestIndex + strTestName + (self.iMaxCols - len(strTestName) - len(strTestIndex)) * '.' + 'Test failed!')
            else:
                print(strTestIndex + strTestName + (self.iMaxCols - len(strTestName) - len(strTestIndex)) * '.' + 'Test failed!')


if __name__ == "__main__":
    tester = RxCS_object_tester1()
    tester.run()
