import abc


class BaseGfx(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def end(self):
        pass
