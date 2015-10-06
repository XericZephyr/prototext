from .models import MessageWrapper
from .hook_helper import register_class_hook, ClassHookHelper

__author__ = 'zhengxu'
__version__ = '0.3.2'

try:
    from google.protobuf.message import Message
except:
    raise Exception("Unable to import protobuf Message class. "
                    "Please make sure your protobuf python library is properly installed.")


#
#   Hook Message class by MessageWrapper
#
MESSAGE_WRAPPER_CLASS = [MessageWrapper]
HOOK_HELPER_CLASS = []


def prototext_hook():
    global HOOK_HELPER_CLASS
    HOOK_HELPER_CLASS = [ClassHookHelper(x) for x in MESSAGE_WRAPPER_CLASS]
    for hhc in HOOK_HELPER_CLASS:
        hhc.hook()


def prototext_unhook():
    for hhc in HOOK_HELPER_CLASS:
        hhc.unhook()


prototext_hook()
