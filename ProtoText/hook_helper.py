import types
import inspect
import __builtin__
import logging

logger = logging.getLogger(__name__)

"""
    TODO:
        - Add ModuleHookHelper and remove the deprecated code
        - Append the old function pointer to the original message object.
        - Try to avoid multiple hook at the same time.
"""


class ClassHookHelper(object):
    def __init__(self, cls, **kwargs):
        """
        :param cls:  the class object of the class hook
        :param strategy:  'safe' or 'override' default: safe
        :param skip_buildin: determine if we skip the build in object default: True
        :return:
        """
        # TODO: Add more strict check for eligible class
        assert isinstance(cls, (type, types.ClassType)), \
            "The input object must be a class object"
        self._hook_class = cls
        self._hook_table = {}
        self._strategy = kwargs.get('strategy', 'safe')
        self._skip_buildin_class = kwargs.get('skip_buildin_class', True)

    def hook(self, strategy=None, skip_buildin=None):
        strategy = strategy or self._strategy
        skip_buildin = skip_buildin or self._skip_buildin_class
        cls = self._hook_class
        base_classes = cls.__bases__
        for base_class in base_classes:
            if skip_buildin and base_class.__name__ in __builtin__.__dict__:
                logger.warn("Skip hooking build-in base class '%s' in sub-class '%s' ..." %
                            (base_class.__name__, cls.__name__))
                continue
            for x in cls.__dict__:
                if not (x in base_class.__dict__ and strategy == 'safe'):
                    # instance method
                    if isinstance(cls.__dict__[x], (types.FunctionType, classmethod, staticmethod, property)):
                        # build hook table
                        if not (base_class.__name__ in self._hook_table and
                                    isinstance(self._hook_table[base_class.__name__], dict)):
                            self._hook_table[base_class.__name__] = {}
                        self._hook_table[base_class.__name__][x] = \
                            (base_class.__dict__[x] if base_class.__dict__.has_key(x) else None, cls.__dict__[x])
                        logger.debug("Wrapping [%s] %s" % (x, str(cls.__dict__[x])))
                        setattr(base_class, x, cls.__dict__[x])
                else:
                    logger.debug("Skip wrapping [%s] %s for security consideration" % (x, str(cls.__dict__[x])))

    def unhook(self):
        cls = self._hook_class
        base_classes = cls.__bases__
        for base_class in base_classes:
            if base_class.__name__ in self._hook_table:
                _sub_hook_table = self._hook_table[base_class.__name__]
                for x in cls.__dict__:
                    if x in _sub_hook_table:
                        if _sub_hook_table[x][1] != cls.__dict__[x]:
                            logger.error("Error! This hook is not installed by this helper. [%s] %s != %s " %
                                         (x, _sub_hook_table[x][1], str(cls.__dict__[x])))
                            continue
                        if _sub_hook_table[x][0] is None:
                            logger.debug("Delete [%s] %s for unhooking" % (x, str(cls.__dict__[x])))
                            delattr(base_class, x)
                        else:
                            logger.debug("Recover [%s] %s to %s for unhooking" %
                                         (x, str(cls.__dict__[x]), str(_sub_hook_table[x][0])))
                            setattr(base_class, x, _sub_hook_table[x][0])


"""
    Deprecated Code, subject to elimination in the near future.
"""


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
            if not (x in base_class.__dict__ and strategy == 'safe'):
                # instance method
                if isinstance(cls.__dict__[x], (types.FunctionType, classmethod, staticmethod, property)):
                    logger.debug("Wrapping [%s] %s" % (x, str(cls.__dict__[x])))
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
        for x in cls.__dict__:
            if x in base_class.__dict__:
                # instance method
                if cls.__dict__[x] == base_class.__dict__[x] and \
                        isinstance(cls.__dict__[x], (types.FunctionType, classmethod, staticmethod, property)):
                    logger.debug("Remove warping [%s] %s" % (x, str(cls.__dict__[x])))
                    delattr(base_class, x)


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
