import pandas as pd
from collections import OrderedDict
from .easyapi_client.remote_algorithm import Parameter, meta_types
from ._data_unit import DataUnit

class DataTable(object):
    
    def __init__(self, df=None):
        self.columns = OrderedDict()
        if df is None: self._table = []
        elif isinstance(df, pd.DataFrame): self._table = df.T.to_dict()
        elif isinstance(df, list): self._table = df
        else: raise TypeError
        self._infer_type(self._table)
        
    def _infer_type(self, table):
        for line in table:
            for key, val in line.items():
                if key not in self.columns:
                    if isinstance(val, str): self.columns[key] = Parameter(name=key, io_type=meta_types['string'])
                    elif isinstance(val, (int, float)): self.columns[key] = Parameter(name=key, io_type=meta_types['number'])
                    elif isinstance(val, list) and all([isinstance(i, (int, float)) for i in val]):
                        self.columns[key] = Parameter(name=key, io_type=meta_types['numarray'])
                    else: self.columns[key] = Parameter(name=key, io_type=meta_types['string'])
                    line[key] = DataUnit(value=val, parameter=self.columns[key])
                
        
    def __len__(self): return len(self._table)
    def _preview_table(self): 
        _columns = []
        for line in self._table:
            for key in line:
                if key not in _columns: _columns.append(key)
        _preview = []
        for line in self._table:
            _preview.append([])
            for key in _columns:
                if key in line: _preview[-1].append(line[key].preview)
                else: _preview[-1].append(None)
        return _preview, _columns
    def __repr__(self):
        _preview, _columns = self._preview_table()
        return pd.DataFrame(_preview, columns=_columns).__repr__()
    def _repr_html_(self):
        _preview, _columns = self._preview_table()
        return pd.DataFrame(_preview, columns=_columns)._repr_html_()
    def set_type(self, name, type_): self.columns[name] = type_
    def set_types(self, type_map):
        for key, val in type_map.items(): self.set_type(key, val)
    def __setitem__(self, keys, val):
        row, col = keys[0], keys[1]
        _param = self.columns.get(col)
        if _param is None:
            key = col
            if isinstance(val, str): self.columns[key] = Parameter(name=key, io_type=meta_types['string'])
            elif isinstance(val, (int, float)): self.columns[key] = Parameter(name=key, io_type=meta_types['number'])
            elif isinstance(val, list) and all([isinstance(i, (int, float)) for i in val]):
                self.columns[key] = Parameter(name=key, io_type=meta_types['numarray'])
            else: self.columns[key] = Parameter(name=key, io_type=meta_types['string'])
        _data = DataUnit(value=val, parameter=self.columns.get(col))
        if isinstance(row, slice):
            if row.start is None and row.stop is None:
                for i in range(len(self._table)): self._table[i][col] = _data
            else:
                for i in range(row.start, row.stop, row.step): self._table[i][col] = _data
        else: self._table[row][col] = _data
    def __getitem__(self, keys):
        col = None
        if isinstance(keys, tuple):
            if len(keys) > 1:
                row, col = keys[0], keys[1]
            else: row = keys[0]
        else: row = keys
        _data = self._table[row]
        if not isinstance(row, slice): _data = [_data]
        if col is not None:
            if isinstance(col, list): 
                _data = [{col_:line[col_] if col_ in line else None for col_ in col} for line in _data]
            else: _data = [line[col] if col in line else None for line in _data]
        if len(_data) == 1: _data = _data[0]
        return _data