from .models import MessageWrapper
from .hook_helper import register_class_hook

__author__ = 'zhengxu'
__version__ = '0.3.0'

try:
    from google.protobuf.message import Message
except:
    raise Exception("Unable to import protobuf Message class. "
                    "Please make sure your protobuf python library is properly installed.")


#
#   Hook Message class by MessageWrapper
#
register_class_hook(MessageWrapper)
