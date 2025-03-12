from setuptools import setup, find_packages
import os


LONG_DESCRIPTION = '''
The `CalTable` package provides tools to facilitate reading, processing, and manipulating data within 
computational workflows. It integrates with `easyapi` and `easyaccess` to allow seamless interaction 
with APIs and local data files, enabling users to compute data as if they were working with pandas 
DataFrames.

If there is any issue, please put up with an issue or contact Jiarui Li (jli78@tulane.edu)
'''
VERSION = '2.0.8'
NAME = 'CalTable'

install_requires = [
    "pandas",
    "tabulate",
    "easyaccess @ git+https://github.com/Jiarui0923/EasyAccess",
    "docflow @ git+https://github.com/Jiarui0923/DocFlow",
]


setup(
    name=NAME,
    description="Calculate Table (CalTable) for computation work with EasyAPI.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    version=VERSION,
    packages=find_packages(),
    install_requires=install_requires,
    url="https://github.com/Jiarui0923/CalTable",
    author='Jiarui Li, Marco K. Carbullido, Jai Bansal, Samuel J. Landry, Ramgopal R. Mettu',
    author_email=('jli78@tulane.edu'),
    maintainer=("Jiarui Li"),
    maintainer_email="jli78@tulane.edu",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Build Tools",
    ],
    zip_safe=True,
    platforms=["any"],
    entry_points={
        'caltable.extensions': [],
    },
)
