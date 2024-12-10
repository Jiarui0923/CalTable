from ._file import FileUnit

class TypeEngine(object):
    def __init__(self, value, iotype): self.value, self.iotype = value, iotype
    def __repr__(self): return f'< {self.iotype.meta}:{self.iotype.name} >\n{self.value}'
    def __len__(self): return len(self.value)
    def _binary_opt(self, other, func):
        if isinstance(other, TypeEngine): return func(self.value, other.value)
        else: return func(self.value, other)
    def __eq__(self, other): return self._binary_opt(other, lambda a, b: a == b)
    def __ne__(self, other): return self._binary_opt(other, lambda a, b: a != b)
    def __lt__(self, other): return self._binary_opt(other, lambda a, b: a <  b)
    def __gt__(self, other): return self._binary_opt(other, lambda a, b: a >  b)
    def __le__(self, other): return self._binary_opt(other, lambda a, b: a <= b)
    def __ge__(self, other): return self._binary_opt(other, lambda a, b: a >= b)
    def __contains__(self, other): return self._binary_opt(other, lambda a, b: b in a)
    def _repr_markdown_(self): return f'< `{self.iotype.meta}`:{self.iotype.name} >  \n{self.value}'
    @property
    def preview(self): return self.value
    def view_html(self, **kwargs): return self.value
    
    def file(self, name=None, ext='txt'): return FileUnit(data=self.value, name=name, ext=ext)