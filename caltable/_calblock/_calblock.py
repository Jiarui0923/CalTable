from ..easyapi_client import docflow as doc

class CalBlock(object):
    def __init__(self, name=None, host='local', inputs={}, outputs={}, desc='', **kwargs):
        self.name = self.__name__ if name is None else name
        self.host = host
        self.column_map = kwargs
        self.inputs = {self.column_map.get(key, key):val
                       for key, val in inputs.items()}
        self.outputs = {self.column_map.get(key, key):val
                        for key, val in outputs.items()}
        self.desc = desc
        
    def _fetch_input(self, table, row=0, params={}):
        _inputs = {}
        table.set_types(params)
        for param in params.keys():
            if param in self.column_map: col_name = self.column_map[param]
            else: col_name = param
            if col_name in table.columns:
                _param = table[row, col_name]
                if _param is not None: _inputs[param] = _param.value
        return _inputs
    def _assign_output(self, table, row=0, outputs={}, params={}):
        table.set_types(params)
        for key, val in outputs.items():
            col_name = key if key not in self.column_map else self.column_map[key]
            table[row, col_name] = val
        return table
    def __repr__(self): return f'< {self.host}[LOCAL]: {self.name} >'
    def forward(self, **inputs): raise NotImplemented
    def forward_table(self, table):
        for row in range(len(table)):
            _inputs = self._fetch_input(table, row=row,
                                        params=self.remote_algorithm.inputs)
            _outputs = self.forward(**_inputs)
            self._assign_output(table, row=row, outputs=_outputs,
                                params=self.remote_algorithm.outputs)
        return table
    def __call__(self, *args, **kwargs): return self.forward_table(*args, **kwargs)
    def _repr_markdown_(self):
        _doc = doc.Document(
            doc.Title(self.name, level=3),
            doc.Text(f'\n{self.desc}  \n'),
            doc.Title('Parameters', level=4),
            doc.Sequence({param:f'({io_obj.iotype.meta}:**{io_obj.iotype.name}**){"_[OPTIONAL]_" if io_obj.optional else ""}=`{io_obj.default}`; {io_obj.desc}; (`{io_obj.iotype.condition}`) {io_obj.iotype.doc}'
                          for param, io_obj
                          in self.inputs.items()}),
            doc.Title('Returns', level=4),
            doc.Sequence({param:f'({io_obj.iotype.meta}:**{io_obj.iotype.name}**){"_[OPTIONAL]_" if io_obj.optional else ""}=`{io_obj.default}`; {io_obj.desc}; (`{io_obj.iotype.condition}`) {io_obj.iotype.doc}'
                          for param, io_obj
                          in self.outputs.items()}),
        )
        return _doc.markdown