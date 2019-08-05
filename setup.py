# -*- coding: utf-8 -*-
# Author: pistonyang@gmail.com

from setuptools import setup, find_packages

VERSION = '0.0.3'

setup(
    name='torchtoolbox',
    version=VERSION,
    author='X.Yang',
    author_email='pistonyang@gmail.com',
    url='https://github.com/deeplearningforfun/torch-toolbox',
    description='Collect and write useful tools for Pytorch.',
    long_description=open('README.md').read(),
    license='BSD 3-Clause',
    packages=find_packages(exclude=('*tests*',)),
    zip_safe=True,
    classifiers=[
        'Programming Language :: Python :: 3',
    ], install_requires=['numpy']
)
