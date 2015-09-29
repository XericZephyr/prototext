import os
import unittest

try:
    from addressbook_pb2 import AddressBook, Person
except:
    print "Please make sure your protobuf 2.6.x is properly installed."
    exit()

import ProtoText

TEST_ADDRESS_BOOK = os.path.dirname(__file__) + '/david.prototxt'


class TestProtoText(unittest.TestCase):
    def test_text_method(self):
        with open(TEST_ADDRESS_BOOK, 'r') as f:
            adr_book_text = f.read()
        adr_book_obj = AddressBook()
        adr_book_obj.ParseFromText(adr_book_text)
        self.assertEqual(str(adr_book_obj), adr_book_obj.SerializeToText())

    def test_dict_method(self):
        person_obj = Person(id=28)
        # test __setitem__ for naive field
        person_obj['name'] = 'Nancy'
        # test __getitem__ for naive field
        self.assertEqual(person_obj['name'], 'Nancy')
        # test __setitem__ for repeated field
        person_obj['phone'] = [Person.PhoneNumber(number="1234")]
        print person_obj
        person_obj['phone'] = [Person.PhoneNumber(number="4567"), Person.PhoneNumber(number="1234")]
        print person_obj
        # print person_obj['phone']
