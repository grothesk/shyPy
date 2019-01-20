import hashlib
import os
import inspect
from joblib import Memory


HERE = os.path.dirname(__file__)


class NeoCache:
    def __init__(self, context, cache_dir=None):
        self.registry = {}
        self.context = context
        if cache_dir:
            self.cache_dir = cache_dir
        else:
            self.cache_dir = os.path.join(HERE, context)
        self.memory = Memory(self.cache_dir, verbose=0)

    def register(self):
        """
        Returns a decorator. The decorator ensures that the function name is
        registered and that the function is handled as a MemorizedFunc.
        """
        def decorator(func):
            if len(inspect.signature(func).parameters) > 0:
                raise TypeError(
                    'The signature of \'{}\' contains input arguments. '
                    'NeoCache only supports registering functions without '
                    'any input arguments.'.format(func.__name__)
                )
            func = self.memory.cache(func)
            self.registry[func.__name__] = func
            return func
        return decorator

    def clear_cache(self):
        """
        Clears the cache by deleting all the files in the cache directory.
        """
        self.memory.clear()

    def update(self):
        """
        Clears the cache and executes all of the registered functions, so that
        the cache contains the latest return values.
        """
        self.clear_cache()
        for f in self.registry.values():
            f()


class RepititionsExcluder:
    def __init__(self, registry_file_path, parameter_list=[]):
        self.registry_file_path = registry_file_path
        self.additional_parameters = parameter_list

    def exclude_repititions(self, func):
        """
        Excludes the repeated execution of the decorated function.
        If the decorated function has not yet been registered, it is executed
        and then registered.
        If the decorated function already has been registered, it is not
        executed.
        """
        def wrapper(*args, **kwargs):
            if not self.exec_registered(func, *args, **kwargs):
                result = func(*args, **kwargs)
                self.register_exec(func, *args, **kwargs)
                return result

        return wrapper

    def exec_registered(self, func, *args, **kwargs):
        """
        Checks whether a certain function has already been executed with
        certain arguments for a certain version number.
        """
        registered = False

        if os.path.exists(self.registry_file_path):
            hash_str = self.create_hash(func, *args, **kwargs)

            with open(self.registry_file_path, 'r') as f:
                lines = f.readlines()

                for line in lines:
                    if line.replace('\n', '') == hash_str:
                        registered = True

        return registered

    def register_exec(self, func, *args, **kwargs):
        """
        Creates a hash and writes it to the registry file.
        """
        hash_str = self.create_hash(func, *args, **kwargs)
        self.append_hash_to_registry(hash_str)

    def create_hash(self, func, *args, **kwargs):
        """
        Creates a hash from a function's name, args, kwargs and given
        parameters.
        It is required that str() can be applied to the args, kwargs and
        parameters.
        """
        hash_str = hashlib.sha256()

        hash_str.update(func.__name__.encode('utf-8'))

        for arg in args:
            hash_str.update(str(type(arg)).encode('utf-8'))
            hash_str.update(str(arg).encode('utf-8'))

        for key in sorted(kwargs):
            hash_str.update(str(type(key)).encode('utf-8'))
            hash_str.update(str(key).encode('utf-8'))

            hash_str.update(str(type(kwargs[key])).encode('utf-8'))
            hash_str.update(str(kwargs[key]).encode('utf-8'))

        for p in self.additional_parameters:
            hash_str.update(str(type(p)).encode('utf-8'))
            hash_str.update(str(p).encode('utf-8'))

        return hash_str.hexdigest()

    def append_hash_to_registry(self, hash):
        with open(self.registry_file_path, 'a') as f:
            f.write('{}\n'.format(hash))
