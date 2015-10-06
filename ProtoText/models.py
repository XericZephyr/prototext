import types

from google.protobuf.text_format import Merge
from google.protobuf.message import Message

__author__ = 'zhengxu'

"""
    TODO:
        - Add iter serious function [But not very useful]
        - [Difficult] Try to override the __init__ function in Message
"""


class MessageWrapper(Message):
    #
    #   Dictionary Methods
    #
    def __contains__(self, item):
        try:
            return item in [x.name for x, y in self.ListFields()]
        except ValueError:
            return False

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        if isinstance(value, list) or isinstance(value, types.GeneratorType):
            # set repeated non-message/message field
            del self[key]
            # this algorithm is inefficient, but allow the mixture of dict and Message in list
            f = getattr(self, key)
            for v in value:
                if isinstance(v, dict):
                    f.add().update(v)
                elif issubclass(v.__class__, Message):
                    f.add().CopyFrom(v)
                else:
                    f.append(v)
        elif isinstance(value, dict):
            # set singular message field
            del self[key]
            self.update(value)
        else:
            setattr(self, key, value)

    def __delitem__(self, key):
        self.ClearField(key)

    def update(self, reference_dict):
        assert isinstance(reference_dict, dict), "Argument must be Python dictionary."
        for k, v in reference_dict.iteritems():
            self[k] = v

    #
    #   Text Format Methods
    #
    def ParseFromText(self, proto_text_string):
        self.Clear()
        return Merge(proto_text_string, self)

    def MergeFromText(self, proto_text_string):
        return Merge(proto_text_string, self)

    def SerializeToText(self):
        return str(self)
