"""
CalBlock Library Module
========================

This module provides unified access to CalBlock libraries, including:
- LocalCalBlockLib: A library of locally defined CalBlocks.
- RemoteCalBlockLib: A library of remotely accessible CalBlocks integrated with EasyAccess.

Author: Jiarui Li  
Email: jli78@tulane.edu  
Affiliation: Computer Science Department, Tulane University
"""

from ._calblock_lib import CalBlockLib
from ._calblock_remote_lib import RemoteCalBlockLib
from ._calblock_local_lib import LocalCalBlockLib
