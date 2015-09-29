__author__ = 'zhengxu'

from google.protobuf.text_format import Merge
from google.protobuf.message import Message
import types
import tempfile
import os.path
from UserDict import UserDict


#
#   protobuf Message dict function
#
def dict__contains__(self, item):
    try:
        return self.HasField(item)
    except ValueError:
        return False


def dict__getitem__(self, key):
    return getattr(self, key)


def dict__setitem__(self, key, value):
    if isinstance(value, list):
        # TODO: Check if it's a repeated message field,
        # if so, allow user to pass dict list
        del self[key]
        getattr(self, key).extend(value)
    else:
        setattr(self, key, value)


def dict__delitem__(self, key):
    self.ClearField(key)


#
#   TODO:
#       1. Add update function
#       2. Add iter serious function [But not very useful]
#       3. [Difficult] Try to override the __init__ function in Message
#


MESSAGE_DICT_METHODS = {
    '__getitem__': dict__getitem__,
    '__setitem__': dict__setitem__,
    '__delitem__': dict__delitem__,
    '__contains__': dict__contains__
}


def append_dict_methods(message_class):
    for (method_name, method_pointer) in MESSAGE_DICT_METHODS.iteritems():
        if not hasattr(message_class, method_name):
            setattr(message_class, method_name, method_pointer)


#
#   Text Format Functions
#

def message_ParseFromText(self, proto_text_string):
    self.Clear()
    return Merge(proto_text_string, self)


def message_MergeFromText(self, proto_text_string):
    return Merge(proto_text_string, self)


def message_SerializeToText(self):
    return str(self)


MESSAGE_TEXT_METHODS = {
    'ParseFromText': message_ParseFromText,
    'MergeFromText': message_MergeFromText,
    'SerializeToText': message_SerializeToText
}


def append_text_methods(message_class):
    for (method_name, method_pointer) in MESSAGE_TEXT_METHODS.iteritems():
        if not hasattr(message_class, method_name):
            setattr(message_class, method_name, method_pointer)


def global_module_init():
    append_dict_methods(Message)
    append_text_methods(Message)

"""
    Deprecated Code
"""


class ProtoText(object):
    MESSAGE_DICT_METHODS = {
        '__getitem__': dict__getitem__,
        '__setitem__': dict__setitem__,
        '__delitem__': dict__delitem__,
        '__contains__': dict__contains__
    }

    def __init__(self, pb_class_or_instance, prototxt=None):
        """
        :param pb_class_or_instance: a protobuf prototype class or instance
        :param prototxt:
        :return:
        """
        if isinstance(pb_class_or_instance, (type, types.ClassType)):
            self._pb_obj = pb_class_or_instance()
        else:
            self._pb_obj = type(pb_class_or_instance)()
            self._pb_obj.MergeFrom(pb_class_or_instance)
        self.merge_from_prototxt(prototxt)

    @property
    def pb_obj(self):
        return self._pb_obj

    def merge_from_prototxt(self, prototxt):
        """
        Merge current message with given prototxt buffer or file
        :param prototxt: can be either proto text string or file path
        :return:
        """
        if isinstance(prototxt, str):
            if os.path.exists(prototxt):
                with open(prototxt, 'r') as f:
                    prototxt = f.read()
            Merge(prototxt, self._pb_obj)

    @property
    def temp_file(self):
        self._tmp_file.seek(0)
        self._tmp_file.write(str(self._pb_obj))
        self._tmp_file.flush()
        return self._tmp_file

    def __str__(self):
        return self._pb_obj.__str__()

    def __enter__(self):
        self._tmp_file = tempfile.NamedTemporaryFile(mode='w')
        self.__append_dict_method()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__cleanup_dict_method()
        if self._tmp_file:
            self._tmp_file.close()

    def __append_dict_method(self):
        #
        #   This is a safe strategy, will only set message function when it's unset
        #
        for (method_name, method_pointer) in self.MESSAGE_DICT_METHODS.iteritems():
            if not hasattr(Message, method_name):
                setattr(Message, method_name, method_pointer)

    def __cleanup_dict_method(self):
        #
        #   This is a safe strategy, remove only the method set by this class
        #
        for (method_name, method_pointer) in self.MESSAGE_DICT_METHODS.iteritems():
            if hasattr(Message, method_name) and getattr(Message, method_name) == method_pointer:
                delattr(Message, method_pointer)
