import types
import inspect
import __builtin__
import logging

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
        for x in cls.__dict__:
            if not (x in base_class.__dict__) or not (strategy == 'safe'):
                # instance method
                if isinstance(cls.__dict__[x], (types.FunctionType, classmethod, staticmethod, property)):
                    logger.debug("Wrapping [%s] %s" % (x, str(cls.__dict__[x])))
                    setattr(base_class, x, cls.__dict__[x])
                else:
                    logger.debug("Skip wrapping [%s] %s" % (x, str(cls.__dict__[x])))


def register_module_hook(class_name_list=[], allow_recursive=False, **kwargs):
    """
    Enumerate all classes in the caller module, hook all or selected classes' base
    classes with specific module
    :param class_name_list: given the class list you'd like to hook
    :return:
    """
    try:
        #
        #   Fetch the caller module
        #
        parent_frame = inspect.stack()[1][0]
        caller_module = inspect.getmodule(parent_frame)
        class_list = [v for k, v in caller_module.__dict__.iteritems()
                      if ((k in class_name_list) or not class_name_list) and
                      isinstance(v, (type, types.ClassType))]
        base_classes_list = reduce(lambda x, y: x + list(y.__bases__), class_list, [])
        if not allow_recursive:
            class_list = filter(lambda x: x not in base_classes_list, class_list)
    except Exception, e:
        logger.error("Unable to retrieve the caller module : %s" % str(e))
        return
    for c in class_list:
        try:
            #
            #   Do the class hook
            #
            register_class_hook(c, **kwargs)
        except Exception, e:
            logger.error("Unable to register class hook")
            continue
