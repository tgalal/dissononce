# -*- coding: utf-8 -*-
import dissononce
from setuptools import find_packages, setup

setup(
    name='dissononce',
    version=dissononce.__version__,
    packages=find_packages(exclude=['tests', 'examples']),
    install_requires=['cryptography>=2.5'],
    extras_require={
        'GuardedHandshakeState': ['transitions']
    },
    test_requires=['pytest'],
    license='MIT',
    author='Tarek Galal',
    author_email='tare2.galal@gmail.com',
    description="Noise Protocol Framework Implementation for Python2-3.x",
    long_description="Dissononce is a python implementation for Noise Protocol Framework. A main goal of this project "
                     "is to provide a simple, easy to read and understand practical reference for Noise enthusiasts, "
                     "implementers and users.",
    platforms='any',
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: MIT License',
                 'Natural Language :: English',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.5',
                 'Programming Language :: Python :: 2.6',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Operating System :: MacOS :: MacOS X',
                 'Operating System :: Microsoft :: Windows',
                 'Operating System :: POSIX :: Linux',
                 'Topic :: Security :: Cryptography',
                 'Topic :: Software Development :: Libraries :: Python Modules']
)
