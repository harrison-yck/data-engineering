import functools
import inspect
import logging


class Retry:
    def __init__(self, retries):
        self._retries = retries

    def __call__(self, function):
        functools.update_wrapper(self, function)
        caller_name = self.get_caller_name()

        def wrapper(*args, **kwargs):
            for i in range(self._retries):
                try:
                    return function(*args, **kwargs)
                except Exception as err:
                    self.log(caller_name, err)
                    self._retries -= 1

        return wrapper

    def log(self, caller_name, err):
        logging.info("[%s - retry left: %s]: %s" % (caller_name, self._retries, err))

    @staticmethod
    def get_caller_name() -> str:
        frm = inspect.stack()[1]
        mod = inspect.getmodule(frm[0])
        return mod.__name__
