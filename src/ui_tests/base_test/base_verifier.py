import re
from pprint import pformat
from decimal import Decimal
from utils import log_util
from deepdiff import DeepDiff


class BaseVerifier:
    """
    Base class to verify stuff in your tests
    """

    def __init__(self, name='Verifier'):
        """VerifierBase init
        """
        self.logger = log_util.logger

    def fail(self, msg=''):
        '''Fail this test.

        :type msg: string
        :param msg: The message to fail with.

        >>> v = VerifierBase()
        >>> v.fail('test failed')
        Traceback (most recent call last):
        AssertionError: test failed
        '''
        self.logger.error(f"{msg} ==> FAIL")
        raise AssertionError(msg)

    def verify_true(self, expression, msg='', verbose=True):
        '''
        Verify the expression evaluates to true.
        Fails the test if it does not.

        :type expression: bool
        :param expression: The expression to evaluate
        :type msg: string
        :param msg: A message describing this verification

        >>> v = VerifierBase()
        >>> v.verify_true(False, 'test failed')
        Traceback (most recent call last):
        AssertionError: test failed
        '''
        if not expression:
            self.fail(msg)
        if verbose:
            self.logger.debug(f'{msg} ==> PASS')
        return True

    def verify_false(self, expression, msg='', verbose=True):
        '''
        Verify the expression evaluates to false.
        Fails the test if it does not.

        :type expression: bool
        :param expression: The expression to evaluate
        :type msg: string
        :param msg: A message describing this verification

        >>> v = VerifierBase()
        >>> v.verify_false(True, 'test failed')
        Traceback (most recent call last):
        AssertionError: test failed
        '''
        if expression:
            self.fail(msg)
        if verbose:
            self.logger.debug(f'{msg} ==> PASS')
        return True

    def verify_equals(self, actual, expected, msg='', verbose=True, ignore_order=False, **kwargs):
        '''
        Verify that 2 objects are equal

        :type actual: object
        :param actual: One object to evaluate against
        :type expected: object
        :param expected: The other object to evaluate against
        :type msg: string
        :param msg: A message describing this verification
        **kwargs:
            check options in DeepDiff https://zepworks.com/deepdiff/5.8.2/diff.html

        >>> v = VerifierBase()
        >>> v.verify_equals(1, 2, 'test failed')
        Traceback (most recent call last):
        AssertionError: Verify: <1> = <2> (test failed)
        '''
        diff = None
        logmsg = f'Verify actual = expected: {actual} = {expected}'
        if msg:
            logmsg += f' ({msg})'

        if actual != expected:
            # get object diff
            diff = DeepDiff(actual, expected, ignore_order=ignore_order, **kwargs)

        if diff:
            logmsg += "\n" + pformat(diff)
            self.logger.info(diff)
            self.fail(logmsg)

        if verbose:
            logmsg += ' ==> PASS'
            self.logger.debug(logmsg)
        return True

    def verify_numbers_equal(
            self, actual, expected, msg='', margin_of_error=0, verbose=True):
        '''
        Verify that 2 numbers are equal

        :type actual: number(int, long, float or Decimal)
        :param actual: One number to evaluate against
        :type expected: number(int, long, float or Decimal)
        :param expected: The other number to evaluate against
        :type msg: string
        :param msg: A message describing this verification
        :type margin_of_error: number(int, long, float or Decimal)
        :param actual: The margin of error for the verify

        >>> v = VerifierBase()
        >>> v.verify_numbers_equal(7, 7, 'test passed')
        True
        >>> v.verify_numbers_equal(2, 2.00000000001, 'test failed')
        Traceback (most recent call last):
        AssertionError: Verify: <2> = <2.00000000001> (test failed)
        >>> v.verify_numbers_equal(
                -10, -10.01, 'test passed', margin_of_error=0.01)
        True
        >>> v.verify_numbers_equal(
                1000000000001.12334253, 1000000000002,
                'test passed', margin_of_error=1)
        True
        >>> v.verify_numbers_equal(
                1, 0.9, 'test failed', margin_of_error=0.09999)
        Traceback (most recent call last):
        AssertionError: Verify: <1> = <0.9>, margin_of_error=0.09999 \
        (test failed)
        >>> from decimal import Decimal
        >>> v.verify_numbers_equal(
            Decimal(3.14), Decimal(3.1415), margin_of_error=0.01)
        True
        >>> v.verify_numbers_equal(
            Decimal(3.14), Decimal(3.1415), margin_of_error=0.001)
        Traceback (most recent call last):
        AssertionError: Verify: <3.140000000000000124344978758017532527446 \
        746826171875> = <3.14150000000000018118839761882554739713668823242 \
        1875>, margin_of_error=0.001
        '''

        actual_decimal = Decimal(actual)
        expected_decimal = Decimal(expected)
        margin_of_error_decimal = Decimal(margin_of_error)

        if margin_of_error_decimal == 0:
            logmsg = f'Verify actual = expected: {actual} = {expected}'
            if msg:
                logmsg += f' ({msg})'
            if actual_decimal != expected_decimal:
                self.fail(logmsg)
        else:
            logmsg = f'Verify actual = expected: {actual} = {expected}, margin_of_error={margin_of_error}'
            if msg:
                logmsg += f' ({msg})'
            if (not expected_decimal - margin_of_error_decimal <=
                    actual_decimal <=
                    expected_decimal + margin_of_error_decimal):
                self.fail(logmsg)

        if verbose:
            logmsg += ' ==> PASS'
            self.logger.debug(logmsg)
        return True

    def verify_not_equals(self, actual, expected, msg='', verbose=True):
        '''
        Verify that 2 objects are not equal

        :type actual: object
        :param actual: One object to evaluate against
        :type expected: object
        :param expected: The other object to evaluate against
        :type msg: string
        :param msg: A message describing this verification

        >>> v = VerifierBase()
        >>> v.verify_not_equals(1, 1, 'test failed')
        Traceback (most recent call last):
        AssertionError: Verify: <1> != <1> (test failed)
        '''

        logmsg = f'Verify actual != expected: {actual} != {expected}'
        if msg:
            logmsg += f' ({msg})'
        if actual == expected:
            self.fail(logmsg)
        if verbose:
            logmsg += ' ==> PASS'
            self.logger.debug(logmsg)
        return True

    def verify_in(self, obj1, obj2, msg='', verbose=True):
        '''
        Verify that the obj1 is in the obj2.
        equivalent to: return bool(<obj1> in <obj2>)

        :type obj1: object
        :param obj1: One object to evaluate if it's in another
        :type obj2: object
        :param obj2: The other object to evaluate if it contains the other
        :type msg: string
        :param msg: A message describing this verification

        >>> veribase = VerifierBase()
        >>> veribase.verify_in('a', 'abc', )
        >>> veribase.verify_in('abc', 'fooabdbar', 'test failed')
        >>> veribase.verify_in([1,2], [1,2,3])
        >>> veribase.verify_in(set([1,2]), set([1,2,3]))
        Traceback (most recent call last):
        AssertionError: Verify: <abc> in <fooabdbar> (test failed)
        '''
        logmsg = f"Verify: <{obj1}> in <{obj2}>"
        if msg:
            logmsg += f' ({msg})'
        if obj1 not in obj2:
            if isinstance(obj1, (list, set)) and isinstance(obj2, (list, set)):
                for o1 in obj1:
                    if o1 not in obj2:
                        self.fail(logmsg)
            else:
                self.fail(logmsg)
        if verbose:
            logmsg += ' ==> PASS'
            self.logger.debug(logmsg)
        return True

    def verify_dict_in(self, expected: dict, actual: dict, msg: str = '', verbose: bool = True):
        '''
        Verify that the dict_expected is in the dict_actual.
        :param expected: dict
        :param actual: dict
        :param msg: verify string
        :param verbose:
        :return:
        >>> veribase = VerifierBase()
        >>> veribase.verify_in({'a':1}, {'a':1,'b':2} )
        >>> veribase.verify_in({'a':1}, {'a':2,'b':2} ,'test failed')

        '''
        logmsg = f"Verify: <{expected}> in <{actual}>"
        if msg:
            logmsg += f' ({msg})'
        for k in expected:
            if k in actual:
                if isinstance(expected[k], dict):
                    self.verify_dict_in(expected[k], actual[k], msg=msg, verbose=verbose)
                else:
                    try:
                        self.verify_equals(actual[k], expected[k], msg=msg, verbose=verbose)
                    except AssertionError as e:
                        self.logger.error(f"failed in verifying {k}")
                        raise e
            else:
                self.fail(f"{logmsg}\n expected key {k} not in the target dict")
        if verbose:
            logmsg += ' ==> PASS'
            self.logger.debug(logmsg)
        return True

    def verify_not_in(self, obj1, obj2, msg='', verbose=True):
        '''
        Verify that the obj1 is not in the obj2.
        equivalent to: return bool(<obj1> in <obj2>)

        :type obj1: object
        :param obj1: One object to evaluate if it's in another
        :type obj2: object
        :param obj2: The other object to evaluate if it contains the other
        :type msg: string
        :param msg: A message describing this verification

        >>> veribase = VerifierBase()
        >>> veribase.verify_not_in('d', 'abc', )
        >>> veribase.verify_not_in('foo', 'fooabdbar', 'test failed')
        Traceback (most recent call last):
        AssertionError: Verify: <abc> not in <fooabdbar> (test failed)
        '''
        logmsg = f"Verify: <{obj1}> not in <{obj2}>"
        if msg:
            logmsg += f' ({msg})'
        if obj1 in obj2:
            self.fail(logmsg)
        if verbose:
            logmsg += ' ==> PASS'
            self.logger.debug(logmsg)
        return True

    def verify_openapi_call_failed(
            self, func, func_args=None, func_kwargs=None,
            expected_exception=Exception, expected_status=None, expected_msg=None, msg=''):
        """

        Args:
            func: function that will be called, other functions can also be passed as parameter besides open_api call
            func_args: list arguments of this function
            func_kwargs: dict arguments of this function
            expected_exception: expected exceptions
            expected_status: expected error status
            expected_msg: expected message
            msg: assertion error message if this function fails

        Returns:

        """
        func_args = func_args or []
        func_kwargs = func_kwargs or {}
        try:
            func(*func_args, **func_kwargs)
        #     pylint: disable=broad-except
        except expected_exception as ex:
            if expected_status is not None:
                self.verify_equals(ex.status, expected_status)
            if expected_msg is not None:
                error_msg = getattr(ex, 'body', str(ex))
                self.verify_in(expected_msg, error_msg)
        else:
            self.fail(msg)

    def verify_string_match(self, expected_pattern, actual_str, msg='', verbose=True):
        '''
        Verify that the actual_str matches the expected pattern


        :type expected_pattern: str
        :param expected_pattern: The expected regex pattern
        :type actual_str: str
        :param actual_str: The actual string
        :type msg: string
        :param msg: A message describing this verification

        >>> veribase = VerifierBase()
        >>> veribase.verify_string_match('\\d+', "1abc" )
        >>> veribase.verify_string_match('\\d+', "abc" ,'test failed')

        '''
        logmsg = f"Verify: the string <{actual_str}> matches the pattern <{expected_pattern}>"
        if msg:
            logmsg += f' ({msg})'
        if not re.match(expected_pattern, actual_str):
            self.fail(logmsg)
        if verbose:
            logmsg += ' ==> PASS'
            self.logger.debug(logmsg)
        return True
