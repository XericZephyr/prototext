# prototext
ProtoText is a powerful python dict-like wrapper class to process google protobuf objects. 

## How to use? 

This module is written to hack the [google protobuf](https://developers.google.com/protocol-buffers/) 
python library to add several python dict-like methods. 

**If you are confused about some concepts I mentioned below, 
please read the [google protobuf language guide](https://developers.google.com/protocol-buffers/docs/overview) 
first.**

### Installation 

The newest release version is `0.3.0` even though we have some unstable development version ahead of that. 
To install the package, simply use the `pip` manager:

```bash
pip install https://github.com/XericZephyr/prototext/archive/v0.3.0.tar.gz
```

We will publish this module to PyPI as soon as we consider this module as stable. 

### Usage 

**This is the fun part!** :shipit:

Once you have successfully installed the ProtoText module, simply 
import our ProtoText module to evilly hack the protobuf module.
 
```python
import ProtoText
```
 
You don't need to anything after that. The hack will be completed automatically and
~~**currently cannot be reversed in a python session**~~ now we can safely remove our hook! 

If you want to do safely removing the prototext hook (pls don't, pls), use 

```python
ProtoText.unhook()
```

~~The unhook part is still very buggy. We are sorry for that.~~ 
(You didn't see anything in the line above.)

#### Dict-Like Operations
 
We wrap all the protobuf message with dict-like indexing and updating, i.e.
 
assume `person_obj` to be some protobuf message

 ```python
 print person_obj['name']       # print out the person_obj.name 
 person_obj['name'] = 'David'   # set the attribute 'name' to 'David'
 # again set the attribute 'name' to 'David' but in batch mode
 person_obj.update({'name': 'David'})
 print ('name' in person_obj)  # print whether the 'name' attribute is set in person_obj 
 # the 'in' operator is better than the google implementation HasField function 
 # in the sense that it won't raise Exception even if the field is not defined  
 ```
 
Ready to see something cooler? Let's go! 

We also implement a list/generator assignment for so-called repeated message/non-message field in protobuf.
 
```python
person_obj['phone'] = [Person.PhoneNumber(number="1234")]    # naive list message assignment
person_obj['phone'] = [{'number': '5678'}]                   # dict assignment
person_obj['phone'] = [{'number': '4567'}, Person.PhoneNumber(number="1234")] # mixed assignment
```

~~However, at present, the implementation for the list assignment feature is ugly, unsafe and inefficient.~~
*Again you didn't see anything in the line above.* 
 
#### Text Method
 
 The protobuf package doesn't provide the easy-to-use instance methods to **parse from** and 
  **serialize to** text-format prototxt files. For an instance, check 
  [david.prototxt](https://raw.githubusercontent.com/XericZephyr/prototext/master/tests/david.prototxt).
  
 We append a pair of text-format method to the protobuf objects, which are 
 ```python
 adr_book_obj = AddressBook()
 adr_book_obj.MergeFromText(adr_book_text)  # merge text format protobuf to adr_book_text
 adr_book_obj.ParseFromText(adr_book_text)  
 # clear the content of adr_book_obj first and then merge from the text format protobuf
 print adr_book_obj.SerializeToText()       # print out the text format protobuf from object
 ```

 
#### More Examples
 
 If you're still interested in our project, we suggest you reading our unit-test code in 
 [tests/](https://github.com/XericZephyr/prototext/tree/master/tests) folder which is intensively 
 included in this git repository. 


## Contribution

The 'we' you saw in the above text is sadly referred to 'me'. The project is now under my solo development. 
If you find this project useful and there are some places to improve, please leave your suggestions in the issues. 
 You're also welcome to contribute this project by first fork this repo. Thanks so much in advance. 