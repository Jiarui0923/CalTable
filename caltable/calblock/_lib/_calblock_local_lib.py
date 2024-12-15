"""
LocalCalBlockLib Module
=======================

This module defines a specialized `CalBlockLib` for managing locally registered CalBlock algorithms.
It provides static methods for registering blocks with unique names and resolving conflicts.

Author: Jiarui Li
Email: jli78@tulane.edu
Affiliation: Computer Science Department, Tulane University
"""

import warnings
from ._calblock_lib import CalBlockLib


class LocalCalBlockLib(CalBlockLib):
    """
    A library for managing local CalBlock algorithms.
    """

    _type = 'local'
    _blocks = {}

    def __init__(self):
        """
        Initialize the LocalCalBlockLib instance using the locally registered blocks.
        """
        super().__init__(source=self._type, **self._blocks)

    @classmethod
    def register_block(cls, block, name=None):
        """
        Register a CalBlock algorithm locally.

        Args:
            block: The CalBlock class or instance to be registered.
            name (str, optional): The unique name for the block. If None, defaults to `block.name`.

        Warnings:
            Issues a warning if a block with the same name already exists.
        """
        if name is None:
            name = block.name
        if name in cls._blocks:
            warnings.warn(f'Local block conflict: {name} already exists.')
        cls._blocks[name] = block

    @classmethod
    def register(cls, name):
        """
        Decorator to register a CalBlock algorithm by wrapping its definition.

        Args:
            name (str): The unique name for the block.

        Returns:
            function: A decorator function for wrapping the CalBlock definition.
        """
        def wrap(block):
            cls.register_block(block, name=name)
            return block
        return wrap
