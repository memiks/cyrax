import os
from imp import load_source
from jinja2 import Environment, FileSystemLoader, Undefined, ext

from cyrax.template import (typogrify, templatefilters, templatetags,
                            templatefunctions)


class LoyalUndefined(Undefined):
    def __getattr__(self, name):
        return self

    __getitem__ = __getattr__

    def __call__(self, *args, **kwargs):
        return self


def initialize_env(source):
    '''
    Initialize environment.
    '''
    loader = FileSystemLoader(source)

    env = Environment(loader=loader, undefined=LoyalUndefined,
                      extensions=[templatetags.MetaInfoExtension,
                                  templatetags.MarkExtension,
                                  ext.do,
                                  ext.with_],
                      cache_size=-1)

    filters = dict((f.__name__, f) for f in typogrify.filters)
    env.filters.update(filters)

    filters = dict((f.__name__, f) for f in templatefilters.filters)
    env.filters.update(filters)

    path = os.path.join(source, 'utils', 'filters.py')
    if os.path.exists(path):
        customfilters = load_source('filters', path)
        filters = dict((f.__name__, f) for f in customfilters.filters)
        env.filters.update(filters)

    functions = dict((f.__name__, f) for f in templatefunctions.functions)
    env.globals.update(functions)

    path = os.path.join(source, 'utils', 'functions.py')
    if os.path.exists(path):
        customfilters = load_source('functions', path)
        filters = dict((f.__name__, f) for f in customfilters.filters)
        env.filters.update(filters)

    return env
