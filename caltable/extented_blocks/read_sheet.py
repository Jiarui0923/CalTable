"""
ReadSheet Class
===============

This module defines the `ReadSheet` class, a computational block for reading data from a local sheet 
file (either `.csv` or `.xlsx` format) and extracting a specific row of data based on the `row_index`. 
The block is registered with the `LocalCalBlockLib` for use in computational workflows.

Class:
------
- `ReadSheet`: A computational block that reads a specified row from a sheet file and returns it as a dictionary.

Methods:
--------
- `__init__(self, **kwargs)`: Initializes the `ReadSheet` block with optional parameters.
- `forward(self, path, row_index)`: Reads the sheet file from the given path, extracts the row data specified by `row_index`, 
  and returns the data as a dictionary with non-null values.
"""

from ..calblock import LocalCalBlockLib  # Import LocalCalBlockLib for registering computational blocks
from ..calblock import CalBlock  # Import CalBlock as the base class for creating computational blocks
from easyaccess.parameter import Parameter  # Import Parameter to define input/output parameters

import pathlib  # Import pathlib to handle file path operations
import pandas as pd  # Import pandas for reading sheet files (.csv and .xlsx)

@LocalCalBlockLib.register('read_sheet')
class ReadSheet(CalBlock):
    """
    ReadSheet Class
    ---------------
    A computational block that reads a sheet file (either `.csv` or `.xlsx`) from a given path and 
    extracts a specified row of data. The row is returned as a dictionary with column names as keys 
    and row values as corresponding values.

    Attributes:
    -----------
    None directly defined in this class (inherits from CalBlock).
    
    Methods:
    --------
    forward(path, row_index): Reads the sheet from the given path, extracts the row identified by `row_index`, 
                               and returns the row data as a dictionary.
    """
    
    def __init__(self, **kwargs):
        """
        Initializes the ReadSheet computational block with the given parameters.

        Parameters:
        -----------
        kwargs: Additional keyword arguments passed to the parent `CalBlock` class for further customization.
        """
        super().__init__('Read File',
                         inputs={'path': Parameter.string('path', 'The path to the target sheet file (.csv or .xlsx)'),
                                 'row_index': Parameter.string('row_index', 'Select the target row', default_value='', optional=True)},
                         outputs={},
                         desc='Read local sheet file and attach to the table.',
                         **kwargs)
    
    def forward(self, path, row_index):
        """
        Reads the sheet file from the specified path, extracts the row identified by `row_index`, 
        and returns the data as a dictionary with non-null values.

        Parameters:
        -----------
        path (str): The path to the sheet file (either `.csv` or `.xlsx`).
        row_index (str): The index (or label) of the row to extract from the sheet.

        Returns:
        --------
        dict: A dictionary containing the row data where keys are the column names and values are the corresponding row values.
              Only non-null values are included.
        
        Raises:
        -------
        TypeError: If the file extension is not supported (i.e., not `.csv` or `.xlsx`).
        """
        if pathlib.Path(path).suffix == '.csv':
            _table = pd.read_csv(path, index_col=0)  # Read the CSV file
        elif pathlib.Path(path).suffix == '.xlsx':
            _table = pd.read_excel(path, index_col=0)  # Read the Excel file
        else:
            raise TypeError(f'{pathlib.Path(path).suffix} Not Supported!')  # Raise error for unsupported file types

        _data = _table.loc[row_index].to_dict()  # Extract the specified row as a dictionary
        _data = {_k: _v for _k, _v in _data.items() if _v is not None}  # Remove any None values
        return _data  # Return the cleaned dictionary
