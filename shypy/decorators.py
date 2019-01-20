from functools import wraps


class CheckRaiser:
    '''
    This class can be used to create decorators for checking input arguments of
    the decorated functions for certain conditions.
    For each decorator, a condition is linked to an exception that is raised if
    the associated condition is not met.

    A condition is a Boolean function, an exception inherits from Exception.
    The arguments are selected by their position. This is done by passing
    indices to __call__.
    '''
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
