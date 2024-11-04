from ...easyapi_client import docflow as doc

class CalBlockLib(object):
    
    def __init__(self, source='local', **kwargs):
        
        self._lib = kwargs
        self.source = source
    def __repr__(self): return f'< Lib[{self.source}] {len(self)} Algorithms >'
    def __len__(self): return len(self._lib)
    def __getitem__(self, name): return self._lib[name]
    def __contains__(self, name): return name in self._lib
    @property
    def algorithms(self): return list(self._lib.keys())
    def _repr_markdown_(self):
        _doc = doc.Document(
            doc.Title(self.source, level=3),
            doc.Sequence({key:val().desc for key, val in self._lib.items()})
        )
        return _doc.markdown