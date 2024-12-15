"""
FileUnit Class Module
======================

This module provides the `FileUnit` class, which represents a file object (binary or text).
It supports saving the file to disk, writing to a buffer, and getting file size and metadata.

Author: Jiarui Li  
Email: jli78@tulane.edu  
Affiliation: Computer Science Department, Tulane University
"""

from uuid import uuid4
from pathlib import Path
import os
import io

class FileUnit(object):
    """
    Represents a file, either binary or text, with methods to handle file operations
    like saving to disk and writing to a buffer.

    Attributes:
        data: The file's data (either bytes or string).
        name: The name of the file.
        ext: The file's extension.
        binary_file: A flag indicating if the file is binary.
    """
    
    def __init__(self, data, name=None, ext='txt'):
        """
        Initializes the FileUnit instance.

        Args:
            data (bytes or str): The content of the file.
            name (str, optional): The name of the file. Defaults to a random UUID if not provided.
            ext (str, optional): The extension of the file. Defaults to 'txt'.
        """
        self.binary_file = isinstance(data, bytes)
        if self.binary_file:
            self.data = data
        else:
            self.data = str(data)
        self.name = str(uuid4()) if name is None else name
        self.ext = ext

    def __len__(self):
        """
        Returns the length of the file data.

        Returns:
            int: The length of the file data in bytes.
        """
        if self.binary_file:
            return len(self.data)
        else:
            return len(self.data.encode())

    def _parse_size(self, size_bytes):
        """
        Converts the file size in bytes to a human-readable format.

        Args:
            size_bytes (int): The size of the file in bytes.

        Returns:
            str: A string representing the size of the file in a human-readable format.
        """
        _units = ['Bytes', 'KB', 'MB', 'GB', 'TB']
        for _unit in _units:
            if size_bytes < 1024:
                return f'{size_bytes:.1f} {_unit}'
            else:
                size_bytes /= 1024

    def __repr__(self):
        """
        Returns a string representation of the file, including its type, name, extension, and size.

        Returns:
            str: The string representation of the file.
        """
        return f'< {"Binary" if self.binary_file else "Text"} File {self.name}.{self.ext} ({self._parse_size(len(self))}) >'

    def save(self, path, prefix=''):
        """
        Saves the file to disk at the specified path.

        Args:
            path (str): The directory path where the file will be saved.
            prefix (str, optional): A prefix to add to the file name. Defaults to ''.

        Returns:
            Path: The path to the saved file.
        """
        _path = os.path.join(path, f'{prefix}{self.name}.{self.ext}')
        _mode = 'wb' if self.binary_file else 'w'
        with open(_path, _mode) as f_handle_:
            f_handle_.write(self.data)
        return Path(_path)

    def write(self, buffer: io.BytesIO):
        """
        Writes the file's data to the provided buffer.

        Args:
            buffer (io.BytesIO): The buffer to write the data to.

        Returns:
            io.BytesIO: The buffer containing the file's data.
        """
        buffer.write(self.data)
        return buffer

    @property
    def filename(self):
        """
        Returns the full file name, including extension.

        Returns:
            str: The file name with extension.
        """
        return f'{self.name}.{self.ext}'
