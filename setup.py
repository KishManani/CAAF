from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='CAAF',  # Required
    version='0.0.1',  # Required
    description='A Python implementation of a cellular automaton model of atrial fibrillation',  # Required
    url='https://github.com/KishManani/CAAF',
    author='Kishan Manani',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['numpy', 'matplotlib', 'numba']
)
