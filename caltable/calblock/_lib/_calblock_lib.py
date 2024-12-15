"""
CalBlockLib Module
==================

This module provides a library interface for managing a collection of CalBlock algorithms.
It enables convenient access, listing, and Markdown representation of the available algorithms.

Author: Jiarui Li
Email: jli78@tulane.edu
Affiliation: Computer Science Department, Tulane University
"""

import docflow as doc


class CalBlockLib:
    """
    A class representing a library of CalBlock algorithms.
    """

    def __init__(self, source='local', **kwargs):
        """
        Initialize the CalBlockLib instance.

        Args:
            source (str): The source of the library (e.g., 'local', 'remote').
            **kwargs: Key-value pairs representing the algorithm name and its callable class.
        """
        self._lib = kwargs
        self.source = source

    def __repr__(self):
        """
        String representation of the CalBlockLib instance.

        Returns:
            str: The representation string.
        """
        return f'<Lib[{self.source}] {len(self)} Algorithms>'

    def __len__(self):
        """
        Get the number of algorithms in the library.

        Returns:
            int: Number of algorithms.
        """
        return len(self._lib)

    def __getitem__(self, name):
        """
        Access an algorithm by its name.

        Args:
            name (str): The name of the algorithm.

        Returns:
            Callable: The corresponding algorithm class or function.
        """
        return self._lib[name]

    def __contains__(self, name):
        """
        Check if an algorithm exists in the library.

        Args:
            name (str): The name of the algorithm.

        Returns:
            bool: True if the algorithm exists, False otherwise.
        """
        return name in self._lib

    @property
    def algorithms(self):
        """
        List the names of all algorithms in the library.

        Returns:
            list: A list of algorithm names.
        """
        return list(self._lib.keys())

    def _repr_markdown_(self):
        """
        Generate a Markdown representation of the library.

        Returns:
            str: The Markdown string.
        """
        _doc = doc.Document(
            doc.Title(self.source, level=3),
            doc.Sequence({key: val().desc for key, val in self._lib.items()})
        )
        return _doc.markdown
