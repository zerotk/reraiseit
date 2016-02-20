# coding=utf-8
from __future__ import unicode_literals, print_function

import locale  # Used by code inside a string.
import pytest
import six
import traceback

from zerotk.reraiseit import reraise, exception_to_unicode

MESSAGE_TYPE = bytes if six.PY2 else str

#===================================================================================================
# ExecutePythonCode
#===================================================================================================
def execute_python_code(code):
    try:
        c = compile(code, '<string>', 'exec')
    except Exception as e:
        print('On execute_python_code with code=\n{}'.format(code))
        raise
    six.exec_(c)


#===================================================================================================
# MessageAttributeIsBytesException
#===================================================================================================
class MessageAttributeIsBytesException(Exception):
    '''
    Simulate a 'message' attribute with the bytes type

    :ivar bytes message:
    '''
    def __init__(self):
        self.message = b'My ascii message'

    def __str__(self):
        return bytes('исключение')


#===================================================================================================
# ExceptionTestConfiguration
#===================================================================================================
class ExceptionTestConfiguration():

    def __init__(self, exception_type, string_statement, expected_inner_exception_message='', expected_traceback_message=None, raised_exception=None):
        self.exception_type = exception_type
        if raised_exception is not None:
            self.raised_exception = raised_exception
        else:
            self.raised_exception = exception_type
        self.string_statement = string_statement
        self.expected_inner_exception_message = expected_inner_exception_message
        self.expected_traceback_message = expected_traceback_message


    def RaiseExceptionUsingReraise(self):

        def raise_exception():
            execute_python_code(self.string_statement)
            pytest.fail('Should not reach here')

        def reraise_exception():
            try:
                raise_exception()
            except self.raised_exception as e:
                reraise(e, "While doing 'bar'")

        try:
            try:
                reraise_exception()
            except self.raised_exception as e1:
                reraise(e1, "While doing x:")
        except self.raised_exception as e2:
            reraise(e2, "While doing y:")


    def get_expected_exception_message(self):
        return "\nWhile doing y:\nWhile doing x:\nWhile doing 'bar'\n" + self.expected_inner_exception_message


    def get_expected_traceback_message(self, actual_exception):
        # Getting the type of the "actual exception" because its type might be different than self.exception_type
        reraised_exception_name = type(actual_exception).__name__
        if six.PY3 and reraised_exception_name.startswith('Reraised'):
            reraised_exception_name = 'zerotk.reraiseit._reraiseit.' + reraised_exception_name
        exception_message = self.get_expected_exception_message()

        if self.expected_traceback_message is not None:
            exception_message = self.expected_traceback_message
        else:
            exception_message = reraised_exception_name + ": " + exception_message + "\n"

        # HACK [muenz]: the 'traceback' module does this, so in order to be able to compare strings we need this workaround
        # notice that if the exception "leaks" the Python console handles the unicode symbols properly
        exception_message = traceback._some_str(exception_message)
        assert type(exception_message) == MESSAGE_TYPE

        return exception_message


if six.PY2:
    parametrized_exceptions = pytest.mark.parametrize(
        'exception_configuration',
        [
            ExceptionTestConfiguration(ValueError, "raise ValueError('message')", 'message'),
            ExceptionTestConfiguration(KeyError, "raise KeyError('message')", "u'message'"),
            ExceptionTestConfiguration(OSError, "raise OSError(2, 'message')", '[Errno 2] message'),
            ExceptionTestConfiguration(IOError, "raise IOError('message')", 'message'),
            ExceptionTestConfiguration(
                SyntaxError,
                "in valid syntax",
                expected_inner_exception_message='invalid syntax (<string>, line 1)',
                expected_traceback_message=(
                    '  File "<string>", line 1\n'
                    '    in valid syntax\n'
                    '     ^\n'
                    'ReraisedSyntaxError: invalid syntax\n'
                )
            ),
            ExceptionTestConfiguration(
                UnicodeDecodeError,
                "u'£'.encode('utf-8').decode('ascii')",
                "'ascii' codec can't decode byte 0xc2 in position 0: ordinal not in range(128)"
            ),
            ExceptionTestConfiguration(
                UnicodeEncodeError,
                "u'£'.encode('ascii')",
                "'ascii' codec can't encode character u'\\xa3' in position 0: ordinal not in range(128)"
            ),
            ExceptionTestConfiguration(AttributeError, "raise AttributeError('message')", 'message'),

            ExceptionTestConfiguration(OSError, "raise OSError()"),
            ExceptionTestConfiguration(OSError, "raise OSError(1)", '1'),
            ExceptionTestConfiguration(OSError, "raise OSError(2, '£ message')", '[Errno 2] £ message'),
            ExceptionTestConfiguration(IOError, "raise IOError('исключение')", "исключение", expected_traceback_message='IOError: <unprintable IOError object>\n'),
            pytest.mark.xfail(raises=AssertionError, reason="ExceptionToUnicode() assumes that the 'message' attribute is 'unicode'")(
               ExceptionTestConfiguration(MessageAttributeIsBytesException, 'raise MessageAttributeIsBytesException()', '')
            ),
            ExceptionTestConfiguration(OSError, "raise OSError(2, '£ message'.encode(locale.getpreferredencoding()))", '[Errno 2] £ message'),
            ExceptionTestConfiguration(OSError, "raise OSError(2, b'£ message')", '[Errno 2] £ message'),
            ExceptionTestConfiguration(IOError, "raise IOError(b'£ message')", '£ message', expected_traceback_message='IOError: <unprintable IOError object>\n'),
            ExceptionTestConfiguration(Exception, "raise Exception(b'£ message')", '£ message'),
        ], ids=[
            'ValueError',
            'KeyError',
            'OSError',
            'IOError',
            'SyntaxError',
            'UnicodeDecodeError',
            'UnicodeEncodeError',
            'AttributeError',

            'OSError - empty',
            'OSError - ErrorNo, empty message',
            'OSError - ErrorNo, unicode message',
            'IOError - unicode message',
            'MessageAttributeIsBytesException',

            'OSError - bytes message in UTF-8',
            'OSError - bytes message in locale.getpreferredencoding()',
            'IOError - bytes message',
            'Exception - bytes message',
        ]
    )
else:
    parametrized_exceptions = pytest.mark.parametrize(
        'exception_configuration',
        [
            ExceptionTestConfiguration(ValueError, "raise ValueError('message')", 'message'),
            ExceptionTestConfiguration(KeyError, "raise KeyError('message')", "'message'"),
            ExceptionTestConfiguration(
                OSError,
                "raise OSError(2, 'message')",
                '[Errno 2] message',
            ),
            ExceptionTestConfiguration(IOError, "raise IOError('message')", 'message'),
            ExceptionTestConfiguration(
                SyntaxError,
                "in valid syntax",
                expected_inner_exception_message='invalid syntax (<string>, line 1)',
                expected_traceback_message=(
                    '  File "<string>", line 1\n'
                    '    in valid syntax\n'
                    '     ^\n'
                    'zerotk.reraiseit._reraiseit.ReraisedSyntaxError: invalid syntax\n'
                )
            ),
            ExceptionTestConfiguration(
                UnicodeDecodeError,
                "'£'.encode('utf-8').decode('ascii')",
                "'ascii' codec can't decode byte 0xc2 in position 0: ordinal not in range(128)"
            ),
            ExceptionTestConfiguration(
                UnicodeEncodeError,
                "'£'.encode('ascii')",
                "'ascii' codec can't encode character '\\xa3' in position 0: ordinal not in range(128)"
            ),
            ExceptionTestConfiguration(AttributeError, "raise AttributeError('message')", 'message'),

            # On Python 3 (Windows) raising OSError actually raises a FileNotFoundError.
            ExceptionTestConfiguration(OSError, "raise OSError()"),
            ExceptionTestConfiguration(OSError, "raise OSError(1)", '1'),
        ], ids=[
            'ValueError',
            'KeyError',
            'OSError',
            'IOError',
            'SyntaxError',
            'UnicodeDecodeError',
            'UnicodeEncodeError',
            'AttributeError',

            'OSError - empty',
            'OSError - ErrorNo, empty message',
        ]
    )


@parametrized_exceptions
def testReraiseKeepsTraceback(exception_configuration):
    with pytest.raises(exception_configuration.exception_type) as e:
        exception_configuration.RaiseExceptionUsingReraise()

    # reraiseit() should not appear in the traceback
    traceback_filenames = []
    for traceback_entry in e.traceback:
        try:
            traceback_filenames.append(traceback_entry.path.basename)
        except AttributeError:
            # traceback_entry.path will be a string when the code was run using "exec compile('code')".
            # However this does not hold true if 'code' contains a SyntaxError, which in that case 'traceback_entry.path'
            # will be a LocalPath
            traceback_filenames.append(traceback_entry.path)

    crash_entry = e.traceback.getcrashentry()
    expected_filenames = [
        'reraiseit_test.py',
        'reraiseit_test.py',
        '_reraiseit.py',
        'reraiseit_test.py',
        '_reraiseit.py',
        'reraiseit_test.py',
        'reraiseit_test.py',
        '_reraiseit.py',
        'reraiseit_test.py',
        'reraiseit_test.py',
        'reraiseit_test.py',
    ]
    if isinstance(crash_entry.path, MESSAGE_TYPE):
        if six.PY2:
            expected_filenames += ['six.py', '<string>']
        expected_filenames += ['<string>']
    if six.PY2:
        expected_filenames = map(six.binary_type, expected_filenames)
    assert traceback_filenames == expected_filenames

    assert crash_entry.locals['code'] == exception_configuration.string_statement


@parametrized_exceptions
def testReraiseAddsMessagesCorrectly(exception_configuration):
    with pytest.raises(exception_configuration.exception_type) as e:
        exception_configuration.RaiseExceptionUsingReraise()

    assert isinstance(e.value, exception_configuration.exception_type)
    assert exception_to_unicode(e.value) == exception_configuration.get_expected_exception_message()

    traceback_message = traceback.format_exception_only(type(e.value), e.value)
    traceback_message = ''.join(traceback_message)

    assert traceback_message == exception_configuration.get_expected_traceback_message(e.value)


@parametrized_exceptions
def testPickle(exception_configuration):
    try:
        exception_configuration.RaiseExceptionUsingReraise()
    except exception_configuration.exception_type as reraised_exception:
        from six.moves.cPickle import dumps, loads
        dumped_exception = dumps(reraised_exception)
        pickled_exception = loads(dumped_exception)
        assert exception_to_unicode(pickled_exception) == exception_to_unicode(reraised_exception)
        assert exception_to_unicode(pickled_exception) != ''
        assert exception_to_unicode(reraised_exception) != ''
