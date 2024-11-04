from ._calblock import CalBlock

class Workflow(CalBlock):
    def __init__(self, *args, name=None, desc=None):
        self._blocks = args
        name = self.__name__ if name is None else name
        desc = f'{name} Workflow(blocks={len(args)})' if desc is None else desc
        super().__init__(name=name,
                         inputs=self._inputs_analysis(),
                         outputs=self._outputs_analysis(),
                         desc=desc)
    def _inputs_analysis(self):
        _existed_inputs = [key for key in self._blocks[0].outputs]
        _inputs = {key:val for key, val in self._blocks[0].inputs.items()}
        for block_ in self._blocks[1:]:
            for key, val in block_.inputs.items():
                if key not in _inputs and key not in _existed_inputs:
                    _inputs[key] = val
            for key in block_.outputs:
                if key not in _existed_inputs: _existed_inputs.append(key)
        return _inputs
    def _outputs_analysis(self):
        _outputs = {}
        for block_ in self._blocks:
            for key, val in block_.outputs.items():
                if key not in _outputs: _outputs[key] = val
        return _outputs
    
    def __len__(self): return len(self._blocks)
    def __repr__(self): return f'< {self.host}[LOCAL]: {self.name} Blocks={len(self)} >'
    def forward_table(self, table):
        for _block in self._blocks: table = _block(table)
        return table