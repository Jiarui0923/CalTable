"""
CalTable Package
================

This package defines the core components of the CalTable project, which allows users to access 
and compute data using EasyAPI, providing functionality similar to pandas DataFrame operations. 
It includes several modules for managing data units, tables, workflows, and toolkits, and supports 
working with remote and local computing resources.

Modules:
--------
- `type_engine`: Defines the type engines used in the computation process.
- `DataUnit`: Represents a data unit used for computation.
- `DataTable`: Defines a data table structure to hold and manage data.
- `CalBlock`: Defines the basic block of a computational workflow.
- `CalBlockRemote`: Defines a remote version of the `CalBlock` for distributed computation.
- `CalBlockLib`: Contains the libraries for working with `CalBlock` units.
- `RemoteCalBlockLib`: Defines remote computation blocks for API interaction.
- `LocalCalBlockLib`: Defines local computation blocks for API interaction.
- `meta_types`, `Parameter`, `IOType`: Components from `easyaccess.parameter` for handling metadata and parameters.
- `CalLibIndex`: An index for managing computational libraries.
- `Workflow`: Defines a computational workflow.
- `WorkBench`: Manages and loads workflows and toolkits.

"""

from . import type_engine as Engines  # Import type engine definitions
from .type_engine import FileUnit  # Import FileUnit class from type_engine

from ._data_unit import DataUnit  # Import DataUnit class for data computation
from ._data_table import DataTable  # Import DataTable class to manage tables

from .calblock import CalBlock  # Import CalBlock class for computational blocks
from .calblock import CalBlockRemote  # Import CalBlockRemote for remote computation blocks

from .calblock._lib import CalBlockLib  # Import CalBlockLib for block library management
from .calblock._lib import RemoteCalBlockLib  # Import RemoteCalBlockLib for remote computation blocks
from .calblock._lib import LocalCalBlockLib  # Import LocalCalBlockLib for local computation blocks

from easyaccess.parameter import meta_types  # Import meta_types for handling metadata in parameters
from easyaccess.parameter import Parameter  # Import Parameter for managing parameters
from easyaccess.parameter import IOType  # Import IOType for input/output type definitions

from .extented_blocks import *
# main_package/__init__.py

import pkg_resources

def load_extensions():
    """
    Automatically load all registered extensions for the main package.
    Extensions must declare themselves in the entry point `caltable.extensions`.
    """
    for entry_point in pkg_resources.iter_entry_points('caltable.extensions'):
        try: entry_point.load()
        except Exception as e:
            import warnings
            warnings.warn(f"Failed to load extension {entry_point.name}: {e}")

# Load extensions automatically when the main package is imported
load_extensions()

LocalCal = LocalCalBlockLib()  # Instantiate a LocalCalBlockLib object

from ._lib_index import CalLibIndex  # Import CalLibIndex for library indexing

IndexCal = CalLibIndex()  # Instantiate a CalLibIndex for managing computational libraries

from ._workflow import Workflow  # Import Workflow class for managing computational workflows
from ._workbench import WorkBench  # Import WorkBench class for managing workflows and toolkits