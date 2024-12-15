"""
CalBlock Core Module
=====================

This module serves as the central hub for importing core CalBlock components, including:
- CalBlock: The foundational class for creating computational blocks.
- CalBlockRemote: Extends CalBlock for remote execution capabilities.
- CalBlockLib: The base library class for managing collections of CalBlocks.
- RemoteCalBlockLib: Manages libraries of remotely accessible CalBlocks.
- LocalCalBlockLib: Manages libraries of locally defined CalBlocks.

Author: Jiarui Li  
Email: jli78@tulane.edu  
Affiliation: Computer Science Department, Tulane University
"""

from ._calblock import CalBlock
from ._calblock_remote import CalBlockRemote

from ._lib import CalBlockLib
from ._lib import RemoteCalBlockLib
from ._lib import LocalCalBlockLib
