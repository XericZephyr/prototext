from .models import MessageWrapper
from .hook_helper import register_class_hook, deregister_class_hook

__author__ = 'zhengxu'
__version__ = '0.3.3'

try:
    from google.protobuf.message import Message
except:
    raise Exception("Unable to import protobuf Message class. "
                    "Please make sure your protobuf python library is properly installed.")


#
#   Hook Message class by MessageWrapper
#
MESSAGE_WRAPPER_CLASS = [MessageWrapper]


def prototext_hook():
    for mwc in MESSAGE_WRAPPER_CLASS:
        register_class_hook(mwc)


def prototext_unhook():
    for mwc in MESSAGE_WRAPPER_CLASS:
        deregister_class_hook(mwc)

prototext_hook()
