class NoDefault: pass

def getlogoattr(obj, attr, default=NoDefault):
    if hasattr(obj, attr):
        return getattr(obj, attr)
    to_do = [obj] + mro(obj)
    for o in to_do:
        result = _findattr(o, attr)
        if result is not None:
            return getattr(obj, result)
    if default is NoDefault:
        raise AttributeError(
            "Attribute %s not found in %r" % (attr, obj))
    else:
        return default

def _findattr(obj, attr):
    for name, value in obj.__dict__.items():
        if name.lower() == attr.lower():
            return name
        if hasattr(value, 'aliases'):
            for alias in value.aliases:
                if alias.lower() == attr.lower():
                    return name
    return None

def _enumattr(obj):
    result = {}
    for o in [obj] + mro(obj):
        for name, value in o.__dict__.items():
            result[name] = None
            for alias in getattr(value, 'aliases', ()):
                result[alias] = None
    return sorted(result.keys())

def mro(obj):
    if hasattr(obj, '__mro__'):
        return obj.__mro__
    if not hasattr(obj, '__bases__'):
        obj = obj.__class__
    result = [obj]
    for base in obj.__bases__:
        result.extend(mro(base))
    return result

def update_logo_attrs(obj):
    if hasattr(obj, '_logo_attrs'):
        return
    attrs = {}
    to_do = [obj] + mro(obj)
    for o in to_do:
        if hasattr(o, '_logo_attrs'):
            attrs.update(o._logo_attrs)
            break
        for name, value in o.__dict__.iteritems():
            if getattr(value, 'logo_expose', False):
                if name.lower() != name:
                    attrs[name.lower()] = name
            if hasattr(value, 'aliases'):
                for alias in value.aliases:
                    attrs[alias] = name
    obj._logo_attrs = attrs
