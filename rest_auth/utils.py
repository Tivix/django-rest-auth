from six import string_types
import sys
if sys.version_info < (2, 7):
    from django.utils.importlib import import_module
else:
    from importlib import import_module


def import_callable(path_or_callable):
    if hasattr(path_or_callable, '__call__'):
        return path_or_callable
    else:
        assert isinstance(path_or_callable, string_types)
        package, attr = path_or_callable.rsplit('.', 1)
        return getattr(import_module(package), attr)
