from functools import wraps
import time


class CheckRaiseDecorator:
    """
    This class can be used to create decorators for checking input arguments of
    the decorated functions for certain conditions.
    For each decorator, a condition is linked to an exception that is raised if
    the associated condition is not met.

    A condition is a Boolean function, an exception inherits from Exception.
    The arguments are selected by their position. This is done by passing
    indices to __call__.
    """
    def __init__(self, condition, exception):
        self.condition = condition
        self.exception = exception

    def __call__(self, *call_args):
        def check_decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                for n in call_args:
                    if not self.condition(args[n]):
                        raise self.exception('arg number {} of function \'{}\''
                                             ' did not met condition.'.
                                             format(n, func.__name__))
                return func(*args, **kwargs)
            return wrapper
        return check_decorator


def log_execution_time(log_func):
    """
    Returns a decorator for logging execution time of the decorated function.
    The way of logging the execution time is defined by log_func. log_func is
    any function that takes the following 3 arguments:
    - func_name
    - start_time
    - end_time.

    Various log mechanisms are conceivable, e.g.:
    - writing the execution time to a csv
    - writing the execution time to a database
    - ...

    Among other things, the decorator is suitable for observing the processing
    of growing data sets.
    """
    def log_execution_time_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            log_func(func.__name__, start_time, end_time)
            return result
        return wrapper
    return log_execution_time_decorator
