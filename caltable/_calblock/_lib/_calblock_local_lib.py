import warnings
from ._calblock_lib import CalBlockLib

class LocalCalBlockLib(CalBlockLib):
    
    _type = 'local'
    _blocks = {}
    def __init__(self):
        super().__init__(source='local', **self._blocks)
    
    @staticmethod
    def register_block(block, name=None):
        if name is None: name = block.name
        if name in LocalCalBlockLib._blocks: warnings.warn(f'Local block conflicts. {name} exists.')
        LocalCalBlockLib._blocks[name] = block
    @staticmethod
    def register(name):
        def wrap(block):
            LocalCalBlockLib.register_block(block, name=name)
            return block
        return wrap