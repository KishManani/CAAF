from setuptools import setup, find_packages

setup(
    name="CAAF",
    version="0.0.1",
    description="Implementation of a cellular automaton model of atrial fibrillation",
    url="https://github.com/KishManani/CAAF",
    author="Kishan Manani",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    packages=find_packages(exclude=["docs", "tests"]),
    install_requires=["numpy", "matplotlib", "numba"],
)
