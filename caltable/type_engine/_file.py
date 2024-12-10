from uuid import uuid4
from pathlib import Path
import os
import io

class FileUnit(object):
    
    def __init__(self, data, name=None, ext='txt'):
        self.binary_file = isinstance(data, bytes)
        if self.binary_file: self.data = data
        else: self.data = str(data)
        self.name = str(uuid4()) if name is None else name
        self.ext = ext
    def __len__(self):
        if self.binary_file: return len(self.data)
        else: return len(self.data.encode())
    def _parse_size(self, size_bytes):
        _units = ['Bytes', 'KB', 'MB', 'GB', 'TB']
        for _unit in _units:
            if size_bytes < 1024: return f'{size_bytes:.1f} {_unit}'
            else: size_bytes /= 1024
    def __repr__(self):
        return f'< {"Binary" if self.binary_file else "Text"} File {self.name}.{self.ext} ({self._parse_size(len(self))}) >'
    def save(self, path, prefix=''):
        _path = os.path.join(path, f'{prefix}{self.name}.{self.ext}')
        _mode = 'wb' if self.binary_file else 'w'
        with open(_path, _mode) as f_handle_: f_handle_.write(self.data)
        return Path(_path)
    
    def write(self, buffer:io.BytesIO):
        buffer.write(self.data)
        return buffer
    
    @property
    def filename(self): return f'{self.name}.{self.ext}'