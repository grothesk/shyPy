from functools import wraps
import hashlib
import os


class RepititionsExcluder:
    def __init__(self, registry_file_path, parameter_list=[]):
        self.registry_file_path = registry_file_path
        self.additional_parameters = parameter_list

    def exclude_repititions(self, func):
        """
        Excludes the repeated execution of the decorated function.
        If the decorated function has not yet been registered, it is executed and
        then registered.
        If the decorated function already has been registered, it is not executed.
        """
        def wrapper(*args, **kwargs):
            if not self.exec_registered(func, *args, **kwargs):
                result = func(*args, **kwargs)
                self.register_exec(func, *args, **kwargs)
                return result

        return wrapper

    def exec_registered(self, func, *args, **kwargs):
        """
        Checks whether a certain function has already been executed with certain
        arguments for a certain version number.
        """
        registered = False

        if os.path.exists(self.registry_file_path):
            hash = self.create_hash(func, *args, **kwargs)

            with open(self.registry_file_path, 'r') as f:
                lines = f.readlines()

                for line in lines:
                    if line.replace('\n', '') == hash:
                        registered = True

        return registered

    def register_exec(self, func, *args, **kwargs):
        """
        Creates a hash and writes it to the registry file.
        """
        hash = self.create_hash(func, *args, **kwargs)
        self.append_hash_to_registry(hash)


    def create_hash(self, func, *args, **kwargs):
        """
        Creates a hash from a function's name, args, kwargs and given parameters.
        It is required that str() can be applied to the args, kwargs and parameters.
        """
        hash = hashlib.sha256()

        hash.update(func.__name__.encode('utf-8'))

        for arg in args:
            hash.update(str(type(arg)).encode('utf-8'))
            hash.update(str(arg).encode('utf-8'))

        for key in sorted(kwargs):
            hash.update(str(type(key)).encode('utf-8'))
            hash.update(str(key).encode('utf-8'))

            hash.update(str(type(kwargs[key])).encode('utf-8'))
            hash.update(str(kwargs[key]).encode('utf-8'))

        for p in self.additional_parameters:
            hash.update(str(type(p)).encode('utf-8'))
            hash.update(str(p).encode('utf-8'))

        return hash.hexdigest()


    def append_hash_to_registry(self, hash):
        with open(self.registry_file_path, 'a') as f:
            f.write('{}\n'.format(hash))


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
