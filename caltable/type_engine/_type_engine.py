"""
TypeEngine Class Module
========================

This module provides the `TypeEngine` class that handles the manipulation of values and their types
with support for various operations (e.g., comparison, length checking) and provides integration
with the `FileUnit` class to save or represent data as files.

Author: Jiarui Li  
Email: jli78@tulane.edu  
Affiliation: Computer Science Department, Tulane University
"""

from ._file import FileUnit

class TypeEngine(object):
    """
    A class that represents a value associated with a specific data type, and supports various operations
    like comparisons, length checking, and file handling.

    Attributes:
        value: The value associated with the TypeEngine instance.
        iotype: The type of the value, represented as an object with metadata.
    """

    def __init__(self, value, iotype):
        """
        Initializes a TypeEngine instance.

        Args:
            value: The value associated with this instance.
            iotype: The type of the value, which provides metadata and type-specific behavior.
        """
        self.value, self.iotype = value, iotype

    def __repr__(self):
        """
        Returns a string representation of the TypeEngine instance.

        Returns:
            str: The string representation, showing the type metadata and the value.
        """
        return f'< {self.iotype.meta}:{self.iotype.name} >\n{self.value}'

    def __len__(self):
        """
        Returns the length of the value.

        Returns:
            int: The length of the value (if applicable).
        """
        return len(self.value)

    def _binary_opt(self, other, func):
        """
        A helper function to perform binary operations on the value and another object.

        Args:
            other: The other object to operate on.
            func: The binary operation function to apply.

        Returns:
            The result of the binary operation.
        """
        if isinstance(other, TypeEngine):
            return func(self.value, other.value)
        else:
            return func(self.value, other)

    def __eq__(self, other):
        """
        Checks if the value is equal to another value.

        Args:
            other: The other object to compare with.

        Returns:
            bool: `True` if the values are equal, `False` otherwise.
        """
        return self._binary_opt(other, lambda a, b: a == b)

    def __ne__(self, other):
        """
        Checks if the value is not equal to another value.

        Args:
            other: The other object to compare with.

        Returns:
            bool: `True` if the values are not equal, `False` otherwise.
        """
        return self._binary_opt(other, lambda a, b: a != b)

    def __lt__(self, other):
        """
        Checks if the value is less than another value.

        Args:
            other: The other object to compare with.

        Returns:
            bool: `True` if the value is less than the other, `False` otherwise.
        """
        return self._binary_opt(other, lambda a, b: a < b)

    def __gt__(self, other):
        """
        Checks if the value is greater than another value.

        Args:
            other: The other object to compare with.

        Returns:
            bool: `True` if the value is greater than the other, `False` otherwise.
        """
        return self._binary_opt(other, lambda a, b: a > b)

    def __le__(self, other):
        """
        Checks if the value is less than or equal to another value.

        Args:
            other: The other object to compare with.

        Returns:
            bool: `True` if the value is less than or equal to the other, `False` otherwise.
        """
        return self._binary_opt(other, lambda a, b: a <= b)

    def __ge__(self, other):
        """
        Checks if the value is greater than or equal to another value.

        Args:
            other: The other object to compare with.

        Returns:
            bool: `True` if the value is greater than or equal to the other, `False` otherwise.
        """
        return self._binary_opt(other, lambda a, b: a >= b)

    def __contains__(self, other):
        """
        Checks if the value contains the other object.

        Args:
            other: The object to check for containment.

        Returns:
            bool: `True` if the value contains the object, `False` otherwise.
        """
        return self._binary_opt(other, lambda a, b: b in a)

    def _repr_markdown_(self):
        """
        Returns a Markdown representation of the TypeEngine instance.

        Returns:
            str: The Markdown representation.
        """
        return f'< `{self.iotype.meta}`:{self.iotype.name} >  \n{self.value}'

    @property
    def preview(self):
        """
        Provides a preview of the value.

        Returns:
            The value associated with the TypeEngine instance.
        """
        return self.value

    def view_html(self, **kwargs):
        """
        Returns an HTML representation of the value.

        Args:
            **kwargs: Additional keyword arguments to modify the behavior.

        Returns:
            The value rendered as an HTML string.
        """
        return self.value

    def file(self, name=None, ext='txt'):
        """
        Converts the value into a `FileUnit` object, allowing the data to be saved as a file.

        Args:
            name (str, optional): The name of the file. Defaults to a randomly generated UUID if not provided.
            ext (str, optional): The file extension. Defaults to 'txt'.

        Returns:
            FileUnit: A `FileUnit` object representing the value as a file.
        """
        return FileUnit(data=self.value, name=name, ext=ext)
