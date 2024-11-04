#! /usr/bin/env python3

import re
from pathlib import Path

from setuptools import setup

tests_require = [
    "pytest>=2.3",
    "tox",
    "twine",
    "passlib>=1.6",
    "webtest",
    "build>=1.2.0;python_version>='3.8'",
    "markdown",
]

setup_requires = [
    "setuptools",
    "setuptools-git>=0.3",
    "wheel>=0.25.0",
    "markdown",
    "pandas",
    "numpy",
    "plotly",
    "py3Dmol",
    "openpyxl",
]
install_requires = [
    "pip>=7",
    "packaging>=23.2",
    "importlib_resources;python_version>='3.8' and python_version<='3.12'",
    "markdown",
    "markdown",
    "pandas",
    "numpy",
    "plotly",
    "py3Dmol",
    "openpyxl",
]


def read_file(rel_path: str):
    return Path(__file__).parent.joinpath(rel_path).read_text()


def get_version():
    return '1.0.0'


setup(
    name="CalTable",
    description="Calculate Table (CalTable) for interdisciplinary computation work with EasyAPI.",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    version=get_version(),
    packages=["caltable"],
    python_requires=">=3.9",
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    url="https://git.tulane.edu/apl/caltable",
    maintainer=(
        "Jiarui Li",
        "Ramgopal Mettu"
    ),
    maintainer_email="jli78@tulane.edu",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        "License :: OSI Approved :: zlib/libpng License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Build Tools",
        "Topic :: System :: Software Distribution",
    ],
    zip_safe=True,
    options={"bdist_wheel": {"universal": True}},
    platforms=["any"],
)
