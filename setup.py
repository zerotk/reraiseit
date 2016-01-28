#!/bin/env python
from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand
import sys


class PyTest(TestCommand):

    user_options = [('pytest-args=', 'a', 'Arguments to pass to py.test')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(['reraiseit'] + self.pytest_args)
        sys.exit(errno)


setup(
    name='reraiseit',
    version='0.1.0',

    author='Alexandre Andrade',
    author_email='kaniabi@gmail.com',

    url='https://github.com/zerotk/reraiseit',

    description = 'Reraise exceptions.',
    long_description = '''A function to re-raise exceptions adding information to the traceback and with unicode support.''',

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: LGPL License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],

    include_package_data=True,

    #package_dir = {'' : 'source/python'},
    #packages=find_packages('source/python'),

    install_requires=[
        'six',
        # DEVELOPMENT
        'coverage',
    ],
    cmdclass={'test': PyTest},
)
