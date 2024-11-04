from .type_engine._meta_engines import _MetaEngineLibs

class DataUnit(object):
    _specific_engines = {}
    def __init__(self, parameter, value):
        self.parameter = parameter
        self.value = value
        self.name = parameter.name
        self.desc = parameter.desc
        self.iotype = parameter.iotype
        self._engine = self._build_engine(self.iotype, self.value)
    
    def _build_engine(self, iotype, value):
        if iotype.id in DataUnit._specific_engines:
            return DataUnit._specific_engines[iotype.id](value=value, iotype=iotype)
        return _MetaEngineLibs.build(value=value, iotype=iotype)
    
    def __repr__(self): return repr(self._engine)
    def __len__(self): return len(self._engine)
    def _binary_opt(self, other, func):
        if isinstance(other, DataUnit): return func(other._engine)
        else: return func(other)
    def __eq__(self, other): return self._binary_opt(other, self._engine.__eq__)
    def __ne__(self, other): return self._binary_opt(other, self._engine.__ne__)
    def __lt__(self, other): return self._binary_opt(other, self._engine.__lt__)
    def __gt__(self, other): return self._binary_opt(other, self._engine.__gt__)
    def __le__(self, other): return self._binary_opt(other, self._engine.__le__)
    def __ge__(self, other): return self._binary_opt(other, self._engine.__ge__)
    def __contains__(self, other): return self._binary_opt(other, self._engine.__contains__)
    def _repr_markdown_(self): return self._engine._repr_markdown_()
    @property
    def preview(self): return self._engine.preview
    @staticmethod
    def register_engine(iotype_ids, engine):
        if isinstance(iotype_ids, str): DataUnit._specific_engines[iotype_ids] = engine
        else:
            for iotype_id in iotype_ids: DataUnit._specific_engines[iotype_id] = engine
    @staticmethod
    def register(iotype_ids):
        def wrap(engine):
            DataUnit.register_engine(iotype_ids, engine)
            return engine
        return wrap