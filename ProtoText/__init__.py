__author__ = 'zhengxu'
__version__ = '0.2.5'

try:
    from google.protobuf.message import Message
except:
    raise Exception("Unable to import protobuf Message class. " \
                    "Please make sure your protobuf python library is properly installed.")

from .models import global_module_init

global_module_init()
