import base_exceptions as base_exception


class QuitException(base_exception.FitterException):
    pass


class CommandParseException(base_exception.FitterException):
    pass


class CommandExecutionException(base_exception.FitterException):
    pass
