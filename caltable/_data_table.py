"""
DataTable Module

The DataTable module provides a structure for handling tables of data. It supports operations for manipulating, accessing, and exporting data in a tabular format, leveraging Pandas for its internal representation. Data in the table is processed using the DataUnit class, which wraps the actual data with additional metadata and engine functionality. The module allows for flexible column type handling, indexing, and exporting of data in different formats.

Classes:
- DataTable: A container for tabular data with support for adding, accessing, and manipulating rows and columns. It also supports exporting and reporting.

Methods:
- __init__: Initializes a DataTable from a DataFrame or a list.
- _infer_type: Infers the data type for each column in the table.
- __len__: Returns the number of rows in the table.
- _preview_table: Previews the table data in a list format.
- __repr__: Returns a string representation of the table.
- _repr_html_: Returns the HTML representation of the table.
- set_type: Sets the type for a specific column.
- set_types: Sets types for multiple columns.
- __setitem__: Allows setting values in the table using indexing.
- __getitem__: Allows accessing values in the table using indexing.
- export: Exports the table data to a zip archive of files.
- report: Generates a report in the form of a document.
"""

import pandas as pd
import tempfile
import os
import shutil
from collections import OrderedDict
from easyaccess.parameter import Parameter, meta_types

import docflow as doc
from ._data_unit import DataUnit


class DataTable(object):
    """
    A class that represents a table of data with support for flexible type handling, 
    data access, manipulation, and export functionality.

    Attributes:
        columns (OrderedDict): A dictionary that holds the column names and their associated Parameter objects.
        _table (list): The internal representation of the table, either as a list of rows or a DataFrame.
        
    Methods:
        __len__: Returns the number of rows in the table.
        __repr__: Returns a string representation of the DataTable.
        _repr_html_: Returns the HTML representation of the DataTable.
        set_type: Sets the type for a specific column.
        set_types: Sets types for multiple columns.
        __setitem__: Sets values for a given cell in the table.
        __getitem__: Gets values for a given cell or row in the table.
        export: Exports the table as a zip archive of files.
        report: Generates a report of the table in document form.
    """

    def __init__(self, df=None):
        """
        Initializes a DataTable instance.

        Args:
            df (pd.DataFrame or list, optional): If provided, initializes the table with the given DataFrame or list.
        """
        self.columns = OrderedDict()
        if df is None:
            self._table = []
        elif isinstance(df, pd.DataFrame):
            self._table = list(df.T.to_dict().values())
            for row_index, row in enumerate(self._table):
                for col_index, val in row.items(): self[row_index, col_index] = val
        elif isinstance(df, list):
            self._table = df
            for row_index, row in enumerate(self._table):
                for col_index, val in row.items(): self[row_index, col_index] = val
        else:
            raise TypeError("Input must be a DataFrame or a list.")
        self._infer_type(self._table)

    def _infer_type(self, table):
        """
        Infers the type for each column based on the data values in the table.

        Args:
            table (list): The table data, where each row is a dictionary of column names to values.
        """
        for line in table:
            for key, val in line.items():
                if key not in self.columns:
                    if isinstance(val, str):
                        self.columns[key] = Parameter(name=key, io_type=meta_types['string'])
                    elif isinstance(val, (int, float)):
                        self.columns[key] = Parameter(name=key, io_type=meta_types['number'])
                    elif isinstance(val, list) and all([isinstance(i, (int, float)) for i in val]):
                        self.columns[key] = Parameter(name=key, io_type=meta_types['numarray'])
                    else:
                        self.columns[key] = Parameter(name=key, io_type=meta_types['string'])
                    line[key] = DataUnit(value=val, parameter=self.columns[key])

    def __len__(self):
        """
        Returns the number of rows in the table.

        Returns:
            int: The number of rows in the table.
        """
        return len(self._table)

    def _preview_table(self):
        """
        Previews the table data as a list of lists, with column headers.

        Returns:
            tuple: A tuple containing two lists: the table data and the column names.
        """
        _columns = []
        for line in self._table:
            for key in line:
                if key not in _columns:
                    _columns.append(key)
        _preview = []
        for line in self._table:
            _preview.append([])
            for key in _columns:
                if key in line:
                    _preview[-1].append(line[key].preview)
                else:
                    _preview[-1].append(None)
        return _preview, _columns

    def __repr__(self):
        """
        Returns a string representation of the DataTable.

        Returns:
            str: A string representation of the DataTable.
        """
        _preview, _columns = self._preview_table()
        return pd.DataFrame(_preview, columns=_columns).__repr__()

    def _repr_html_(self):
        """
        Returns the HTML representation of the DataTable.

        Returns:
            str: The HTML representation of the DataTable.
        """
        _preview, _columns = self._preview_table()
        return pd.DataFrame(_preview, columns=_columns)._repr_html_()

    def set_type(self, name, type_):
        """
        Sets the type for a specific column.

        Args:
            name (str): The column name.
            type_ (Parameter): The Parameter object representing the new type for the column.
        """
        self.columns[name] = type_

    def set_types(self, type_map):
        """
        Sets types for multiple columns.

        Args:
            type_map (dict): A dictionary mapping column names to their corresponding Parameter objects.
        """
        for key, val in type_map.items():
            self.set_type(key, val)

    def __setitem__(self, keys, val):
        """
        Sets a value in the table using indexing.

        Args:
            keys (tuple): A tuple containing the row index and column name.
            val (any): The value to set in the table.
        """
        row, col = keys[0], keys[1]
        _param = self.columns.get(col)
        if _param is None:
            key = col
            if isinstance(val, str):
                self.columns[key] = Parameter(name=key, io_type=meta_types['string'])
            elif isinstance(val, (int, float)):
                self.columns[key] = Parameter(name=key, io_type=meta_types['number'])
            elif isinstance(val, list) and all([isinstance(i, (int, float)) for i in val]):
                self.columns[key] = Parameter(name=key, io_type=meta_types['numarray'])
            else:
                self.columns[key] = Parameter(name=key, io_type=meta_types['string'])
        _data = DataUnit(value=val, parameter=self.columns.get(col))
        if isinstance(row, slice):
            if row.start is None and row.stop is None:
                for i in range(len(self._table)):
                    self._table[i][col] = _data
            else:
                for i in range(row.start, row.stop, row.step):
                    self._table[i][col] = _data
        else:
            self._table[row][col] = _data

    def __getitem__(self, keys):
        """
        Gets a value from the table using indexing.

        Args:
            keys (tuple): A tuple containing the row index and column name, or just the row index.
        
        Returns:
            any: The data corresponding to the given row and column, or the entire row.
        """
        col = None
        if isinstance(keys, tuple):
            if len(keys) > 1:
                row, col = keys[0], keys[1]
            else:
                row = keys[0]
        else:
            row = keys
        _data = self._table[row]
        if not isinstance(row, slice):
            _data = [_data]
        if col is not None:
            if isinstance(col, list):
                _data = [{col_: line[col_] if col_ in line else None for col_ in col} for line in _data]
            else:
                _data = [line[col] if col in line else None for line in _data]
        if len(_data) == 1:
            _data = _data[0]
        return _data

    def export(self, path='./', file_name='package', format='zip', index_col=None):
        """
        Exports the table data to a zip archive of files.

        Args:
            path (str, optional): The path where the files will be saved. Defaults to the current directory.
            file_name (str, optional): The name of the zip file. Defaults to 'package'.
            format (str, optional): The format of the archive. Defaults to 'zip'.
            index_col (str, optional): The column to use as the index for directories. Defaults to None.

        Returns:
            int: The number of files exported.
        """
        _file_counts = 0
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=False) as temp_dir:
            for row in range(len(self)):
                _index = str(self[row, index_col].preview if index_col is not None else row)
                _case_path = os.path.join(temp_dir, _index)
                os.makedirs(_case_path, exist_ok=True)
                for cell in self[row].values():
                    cell.file().save(path=_case_path)
                    _file_counts += 1
            shutil.make_archive(os.path.join(path, file_name), format=format, root_dir=temp_dir)
        return _file_counts

    def report(self, title=None, index_col=None):
        """
        Generates a report of the table data in document form.

        Args:
            title (str, optional): The title of the report. Defaults to 'Report'.
            index_col (str, optional): The column to use as the index in the report. Defaults to None.

        Returns:
            doc.Document: The generated document report.
        """
        doc_blocks = []
        for row in range(len(self)):
            _index = str(self[row, index_col].preview if index_col is not None else row)
            doc_blocks_row = []
            doc_blocks_row.append(doc.Title(_index, level=3))
            for cell in self[row].values():
                _doc_unit = doc.Document(
                    doc.Title(cell.name, level=4),
                    doc.Text(cell.view_html()),
                    doc.Text('\n\n'),
                )
                doc_blocks_row.append(_doc_unit)
            doc_blocks.append(doc.Expander(doc.Document(*doc_blocks_row), _index))
        return doc.Document(
            doc.Title('Report' if title is None else title, level=1),
            doc.IdenticalBadge(),
            doc.UUIDStamp(),
            doc.DateTimeStamp(timefmt='%d-%m-%Y %H:%M:%S'),
            *doc_blocks
        )
