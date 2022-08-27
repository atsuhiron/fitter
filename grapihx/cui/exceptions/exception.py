class FitterException(Exception):
    pass


class QuitException(FitterException):
    pass


class CommandParseException(FitterException):
    pass


class CommandExecutionException(FitterException):
    pass
