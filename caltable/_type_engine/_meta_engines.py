from ._type_engine import TypeEngine

class _MetaTypeEngine(TypeEngine):
    _iotype_meta_id = ''

class _MetaEngineLibs(object):
    _meta_engines = {}
    @staticmethod
    def register_engine(meta_engine:_MetaTypeEngine):
        _MetaEngineLibs._meta_engines[meta_engine._iotype_meta_id] = meta_engine
    @staticmethod
    def register(engine):
        _MetaEngineLibs.register_engine(engine)
        return engine
    @staticmethod
    def build(value, iotype):
        _engine = _MetaEngineLibs._meta_engines.get(iotype.meta)
        if _engine is None: raise TypeError(f'Unknown meta type: {iotype.meta}')
        else: return _engine(value=value, iotype=iotype)

@_MetaEngineLibs.register
class StringTypeEngine(_MetaTypeEngine):
    _iotype_meta_id = 'string'
    @property
    def preview(self):
        if len(self.value) > 16: return f'{self.iotype.name}:{self.value[:16]}...({len(self.value)})'
        else: return f'{self.value}'

@_MetaEngineLibs.register
class NumberTypeEngine(_MetaTypeEngine):
    _iotype_meta_id = 'number'
    def __len__(self): return 1
    @property
    def preview(self): return f'{self.value}'

@_MetaEngineLibs.register
class NumArrayTypeEngine(_MetaTypeEngine):
    _iotype_meta_id = 'numarray'
    @property
    def preview(self):
        if len(self.value) > 3: return f'{self.iotype.name}:{self.value[:3]}...({len(self.value)})'
        else: return f'{self.value}'