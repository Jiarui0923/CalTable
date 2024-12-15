"""
Type Engine Module

This module is part of the CalTable project.
The module defines a variety of type engines for handling different data types, including numbers, strings, numeric arrays, and more complex structures like JSON and tables.

Imports:
- TypeEngine: A base class for handling various types of data.
- NumberTypeEngine, StringTypeEngine, NumArrayTypeEngine: Specialized type engines for handling specific types of data.
- StringTableTypeEngine, StringJSONTypeEngine: Rich engines for rendering string-based tables and formatted JSON data.
- FileUnit: A utility for saving and working with data files.
"""

from ._type_engine import TypeEngine
from ._meta_engines import NumberTypeEngine
from ._meta_engines import StringTypeEngine
from ._meta_engines import NumArrayTypeEngine
from ._rich_engines import StringTableTypeEngine
from ._rich_engines import StringJSONTypeEngine
from ._file import FileUnit