from __future__ import unicode_literals
'''
Inspired by http://www.thescripts.com/forum/thread46361.html

Derived from github.com/esss/ben10.
'''
import six
import locale



#===================================================================================================
# reraiseit
#===================================================================================================
def reraise(exception, message, separator='\n'):
    '''
    Raised the same exception given, with an additional message.

    :param Exception exception:
        Original exception being raised with additional messages

    :param unicode message:
        Message to be added to the given exception

    :param unicode separator:
        String separating `message` from the `exception`'s original message.

    e.g.
        try:
            raise RuntimeError('original message')
        except Exception, e:
            Reraise(e, 'message')

        >>> RuntimeError:
        >>> message
        >>> original message

        try:
            raise RuntimeError('original message')
        except Exception, e:
            Reraise(e, '[message]', separator=' ')

        >>> RuntimeError:
        >>> [message] original message
    '''
    import sys

    # IMPORTANT: Do NOT use try/except mechanisms in this method or the sys.exc_info()[-1] will be invalid

    if hasattr(exception, 'reraised_message'):
        current_message = exception.reraised_message
    else:
        current_message = exception_to_unicode(exception)

    # Build the new message
    if not current_message.startswith(separator):
        current_message = separator + current_message
    message = '\n' + message + current_message

    if exception.__class__ in _SPECIAL_EXCEPTION_MAP:
        # Handling for special case, some exceptions have different behaviors.
        exception = _SPECIAL_EXCEPTION_MAP[exception.__class__](*exception.args)

    elif exception.__class__ not in _SPECIAL_EXCEPTION_MAP.values():
        # In Python 2.5 overriding the exception "__str__" has no effect in "unicode()". Instead, we
        # must change the "args" attribute which is used to build the string representation.
        # Even though the documentation says "args" will be deprecated, it uses its first argument
        # in unicode() implementation and not "message".
        exception.args = (message,)

    exception.message = message
    # keep the already decoded message in the object in case this exception is reraised again
    exception.reraised_message = message

    # Reraise the exception with the EXTRA message information
    if six.PY2:
        six.reraise(exception, None, sys.exc_info()[-1])
    else:
        raise exception.with_traceback(sys.exc_info()[-1])


#===================================================================================================
# exception_to_unicode
#===================================================================================================
def exception_to_unicode(exception):
    '''
    Obtains unicode representation of an Exception.

    This wrapper is used to circumvent Python 2.7 problems with built-in exceptions with unicode
    messages.

    Steps used:
        * Try to obtain Exception.__unicode__
        * Try to obtain Exception.__str__ and decode with utf-8
        * Try to obtain Exception.__str__ and decode with locale.getpreferredencoding
        * If all fails, return Exception.__str__ and decode with (ascii, errors='replace')

    :param Exception exception:

    :return unicode:
        Unicode representation of an Exception.
    '''
    if six.PY2:
        try:
            # First, try to obtain __unicode__ as defined by the Exception
            return six.text_type(exception)
        except UnicodeDecodeError:
            try:
                # If that fails, try decoding with utf-8 which is the strictest and will complain loudly.
                return bytes(exception).decode('utf-8')
            except UnicodeDecodeError:
                try:
                    # If that fails, try obtaining bytes repr and decoding with locale
                    return bytes(exception).decode(locale.getpreferredencoding())
                except UnicodeDecodeError:
                    # If all failed, give up and decode with ascii replacing errors.
                    return bytes(exception).decode(errors='replace')
        except UnicodeEncodeError:
            # Some exception contain unicode messages, but try to convert them to bytes when calling
            # unicode() (such as IOError). In these cases, we do our best to fix Python 2.7's poor
            # handling of unicode exceptions.
            assert type(exception.message) == six.text_type  # This should be true if code got here.
            return exception.message
    else:
        return str(exception)


#===================================================================================================
# SPECIAL_EXCEPTIONS
#===================================================================================================
# [[[cog
# SPECIAL_EXCEPTIONS = [
#     KeyError,
#     OSError,
#     IOError,
#     SyntaxError,
#     UnicodeDecodeError,
#     UnicodeEncodeError,
# ]
# from ben10.foundation.string import Dedent
# exception_map = []
# for exception_class in SPECIAL_EXCEPTIONS:
#     superclass_name = exception_class.__name__
#     exception_map.append('\n        ' + superclass_name + ' : Reraised' + superclass_name + ',')
#     cog.out(Dedent(
#         '''
#         class Reraised%(superclass_name)s(%(superclass_name)s):
#             def __init__(self, *args):
#                 %(superclass_name)s.__init__(self, *args)
#                 self.message = None
#
#             def __str__(self):
#                 return self.message
#
#
#         '''% locals()
#     ))
# cog.out(Dedent(
#     '''
#     _SPECIAL_EXCEPTION_MAP = {%s
#     }
#     ''' % ''.join(exception_map)
# ))
# ]]]
class ReraisedKeyError(KeyError):
    def __init__(self, *args):
        KeyError.__init__(self, *args)
        self.message = None

    def __str__(self):
        return self.message

class ReraisedOSError(OSError):
    def __init__(self, *args):
        OSError.__init__(self, *args)
        self.message = None

    def __str__(self):
        return self.message

class ReraisedOSError(OSError):
    def __init__(self, *args):
        OSError.__init__(self, *args)
        self.message = None

    def __str__(self):
        return self.message

class ReraisedSyntaxError(SyntaxError):
    def __init__(self, *args):
        SyntaxError.__init__(self, *args)
        self.message = None

    def __str__(self):
        return self.message

class ReraisedUnicodeDecodeError(UnicodeDecodeError):
    def __init__(self, *args):
        UnicodeDecodeError.__init__(self, *args)
        self.message = None

    def __str__(self):
        return self.message

class ReraisedUnicodeEncodeError(UnicodeEncodeError):
    def __init__(self, *args):
        UnicodeEncodeError.__init__(self, *args)
        self.message = None

    def __str__(self):
        return self.message

_SPECIAL_EXCEPTION_MAP = {
    KeyError : ReraisedKeyError,
    OSError : ReraisedOSError,
    OSError : ReraisedOSError,
    SyntaxError : ReraisedSyntaxError,
    UnicodeDecodeError : ReraisedUnicodeDecodeError,
    UnicodeEncodeError : ReraisedUnicodeEncodeError,
}
# [[[end]]] (checksum: 896c3faa794c9a17cbe89209d38816dc)


if six.PY3:
    class ReraisedFileNotFoundError(FileNotFoundError):
        def __init__(self, *args):
            FileNotFoundError.__init__(self, *args)
            self.message = None

        def __str__(self):
            return self.message

    _SPECIAL_EXCEPTION_MAP[FileNotFoundError] = ReraisedFileNotFoundError
