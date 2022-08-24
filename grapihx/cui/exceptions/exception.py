class FitterException(Exception):
    pass


class CommandParseException(FitterException):
    pass


class CommandExecutionException(FitterException):
    pass
