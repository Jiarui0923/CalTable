from .calblock import CalBlock
from . import IndexCal

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
        _existed_inputs = [self._blocks[0].column_map.get(key, key)
                           for key in self._blocks[0].outputs]
        _inputs = {self._blocks[0].column_map.get(key, key):val
                   for key, val in self._blocks[0].inputs.items()}
        for block_ in self._blocks[1:]:
            for key, val in block_.inputs.items():
                key = block_.column_map.get(key, key)
                if key not in _inputs and key not in _existed_inputs:
                    _inputs[key] = val
            for key in block_.outputs:
                key = block_.column_map.get(key, key)
                if key not in _existed_inputs: _existed_inputs.append(key)
        return _inputs
    def _outputs_analysis(self):
        _outputs = {}
        for block_ in self._blocks:
            for key, val in block_.outputs.items(): _outputs[block_.column_map.get(key, key)] = val
        return _outputs
    
    def __len__(self): return len(self._blocks)
    def __repr__(self): return f'< {self.host}[LOCAL]: {self.name} Blocks={len(self)} >'
    def forward_table(self, table):
        for _block in self._blocks: table = _block(table)
        return table
    
    @staticmethod
    def load(workflow, index=IndexCal):
        _name = workflow.get('name', None)
        _desc = workflow.get('desc', None)
        workflow = workflow['workflow']
        _workflow_blocks = []
        for _unit in workflow:
            if isinstance(_unit, str):
                _workflow_blocks.append(index[_unit]())
            elif isinstance(_unit, (list, tuple)):
                if len(_unit) >= 2: _unit, _param = _unit[0], _unit[1]
                elif len(_unit) == 1: _unit, _param = _unit[0], {}
                else: raise TypeError
                _workflow_blocks.append(index[_unit](**_param))
        return Workflow(*_workflow_blocks, name=_name, desc=_desc)