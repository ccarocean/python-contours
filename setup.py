# -* coding: utf-8 -*-
# pylint: disable=invalid-name
"""Build, test, and install contours."""

import re
from setuptools import setup

version = re.search(
    r"^__version__\s*=\s*'(.*)'",
    open('contours/__init__.py').read(),
    re.M).group(1)

with open('README.rst', 'r') as f:
    long_desc = f.read()

setup(
    name='contours',
    version=version,
    description='Contour calculation with Matplotlib.',
    author='Michael R. Shannon',
    author_email='mrshannon.aerospace@gmail.com',
    license='MIT',
    url='https://github.com/ccarocean/python-contours',
    download_url=('https://github.com/ccarocean/python-contours/'
                  'archive/v0.0.2.zip'),
    long_description=long_desc,
    packages=['contours'],
    platforms=['any'],
    keywords=['math', 'plotting', 'matplotlib'],
    install_requires=[
        'numpy>=1.4.0',
        'matplotlib>=1.5.0',
        'future'],
    extras_require={
        'shapely': ['shapely>=1.2.10']
    },
    test_suite='tests',
    tests_require=[
        'coverage',
        'testfixtures'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development',
    ],
    zip_safe=True
)
