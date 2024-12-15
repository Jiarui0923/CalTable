"""
ReadFile Class
==============

This module defines the `ReadFile` class, a computational block for reading files from a local 
system. It inherits from `CalBlock` and is registered with the `LocalCalBlockLib` for use in 
computational workflows. The block reads the content of a specified file, either in binary or 
text format, and outputs the file data and its name.

Class:
------
- `ReadFile`: A computational block that reads a file from a specified path.

Methods:
--------
- `__init__(self, is_binary=False, encoding=None, **kwargs)`: Initializes the `ReadFile` block with 
  optional parameters for binary reading and file encoding.
- `forward(self, path)`: Reads the file from the specified path and returns the file's data 
  along with its name.
"""

from ..calblock import LocalCalBlockLib  # Import LocalCalBlockLib for registering computational blocks
from ..calblock import CalBlock  # Import CalBlock as the base class for creating computational blocks
from easyaccess.parameter import Parameter  # Import Parameter to define input/output parameters

import pathlib  # Import pathlib to handle file path operations

@LocalCalBlockLib.register('read_file')
class ReadFile(CalBlock):
    """
    ReadFile Class
    --------------
    A computational block that reads the contents of a file from a given path. The file can be read 
    in binary or text format, depending on the specified configuration.

    Attributes:
    -----------
    is_binary (bool): A flag to determine whether to read the file in binary mode (default: False).
    encoding (str or None): The encoding to use when reading the file (default: None, i.e., system default).
    
    Methods:
    --------
    forward(path): Reads the file from the given path and returns the file data and its name.
    """
    
    def __init__(self, is_binary=False, encoding=None, **kwargs):
        """
        Initializes the ReadFile computational block with the given parameters.

        Parameters:
        -----------
        is_binary (bool): If True, the file is read in binary mode; default is False (text mode).
        encoding (str or None): The encoding to use when reading the file. If None, the default system encoding is used.
        kwargs: Additional keyword arguments passed to the parent `CalBlock` class for further customization.
        """
        self.is_binary = is_binary  # Set the binary flag
        self.encoding = encoding  # Set the encoding
        super().__init__('Read File',
                         inputs={'path': Parameter.string('path', 'The path to the target file')},
                         outputs={'file': Parameter.string('file', 'The file data'),
                                  'filename': Parameter.string('filename', 'The file name')},
                         desc='Read local files from the given path.',
                         **kwargs)
    
    def forward(self, path):
        """
        Reads the file from the specified path and returns the file data along with the file name.

        Parameters:
        -----------
        path (str): The path to the file to be read.

        Returns:
        --------
        dict: A dictionary containing the 'filename' (file name without extension) and 'file' (file contents).
        """
        _flag = 'rb' if self.is_binary else 'r'  # Determine the mode to open the file based on binary flag
        with open(path, _flag, encoding=self.encoding) as _file: 
            _data = _file.read()  # Read the file content
        _name = pathlib.Path(path).stem  # Extract the file name without extension
        return dict(filename=_name, file=_data)  # Return the file name and content
