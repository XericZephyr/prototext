from ProtoText import __version__
from setuptools import setup, find_packages

__author__ = 'zhengxu'

setup(
    name="ProtoText",
    version=__version__,
    packages=find_packages(exclude=['tests']),

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=['protobuf>=2.6'],

    package_data={},

    # metadata for upload to PyPI
    author="Zheng Xu",
    author_email="xuzheng1111@gmail.com",
    description="ProtoText is a powerful python dict-like wrapper class to process google protobuf objects.",
    license="MIT",
    keywords="protobuf, dict",
    url="https://github.com/XericZephyr/prototext",  # project home page, if any

    # could also include long_description, download_url, classifiers, etc.
)
