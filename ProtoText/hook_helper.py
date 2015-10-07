import types
import __builtin__
import logging

HOOK_TABLE_NAME = '__ZX_PY_HOOK_TABLE__'

logger = logging.getLogger(__name__)


def register_class_hook(cls, strategy='safe', skip_buildin=True):
    """
    :param cls:  the class object of the class hook
    :param strategy:  'safe' or 'override'
    :param skip_buildin: determine if we skip the build in object
    :return:
    """
    assert isinstance(cls, (type, types.ClassType)), \
        "The input object must be a class object"
    base_classes = cls.__bases__
    for base_class in base_classes:
        if skip_buildin and base_class.__name__ in __builtin__.__dict__:
            logger.warn("Skip hooking build-in base class '%s' in sub-class '%s' ..." %
                        (base_class.__name__, cls.__name__))
            continue
        if HOOK_TABLE_NAME in base_class.__dict__:
            logger.warn("Skip hooking the base class %s to avoid multi-hook conflict ..." %
                        base_class.__name__)
            continue
        else:
            # build HOOK_TABLE
            setattr(base_class, HOOK_TABLE_NAME, {})
            assert HOOK_TABLE_NAME in base_class.__dict__, "Unable to append hook table to target class"
        for x in cls.__dict__:
            if not (x in base_class.__dict__ and strategy == 'safe'):
                # instance method
                if isinstance(cls.__dict__[x], (types.FunctionType, classmethod, staticmethod, property)):
                    logger.debug("Wrapping [%s] %s" % (x, str(cls.__dict__[x])))
                    # Append hook table
                    base_class.__dict__[HOOK_TABLE_NAME][x] = base_class.__dict__[x] \
                        if x in base_class.__dict__ else None
                    # Set hook
                    setattr(base_class, x, cls.__dict__[x])
            else:
                logger.debug("Skip wrapping [%s] %s for security consideration" % (x, str(cls.__dict__[x])))


def deregister_class_hook(cls):
    """
    :param cls:  the class object of the class to unhook
    :return:
    """
    assert isinstance(cls, (type, types.ClassType)), \
        "The input object must be a class object"
    base_classes = cls.__bases__
    for base_class in base_classes:
        if HOOK_TABLE_NAME not in base_class.__dict__:
            logger.warn("Unable to find Hook Table for class '%s', "
                        "probably it's not properly hooked." % base_class.__name__)
            continue
        _hook_table = base_class.__dict__[HOOK_TABLE_NAME]
        for x in _hook_table:
            if _hook_table[x]:
                setattr(base_class, x, _hook_table[x])
            else:
                delattr(base_class, x)
        delattr(base_class, HOOK_TABLE_NAME)