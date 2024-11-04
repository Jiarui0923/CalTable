from caltable import LocalCalBlockLib
from caltable import CalBlock
from caltable import Parameter

import pathlib

@LocalCalBlockLib.register('read-file')
class ReadFile(CalBlock):
    def __init__(self, is_binary=False, encoding=None, **kwargs):
        self.is_binary = is_binary
        self.encoding = encoding
        super().__init__('Read File',
                         inputs={'path': Parameter.string('path', 'The path to the target file')},
                         outputs={'file': Parameter.string('file', 'The file data'),
                                  'filename': Parameter.string('filename', 'The file name')},
                         desc='Read local files from the given path.',
                         **kwargs)
    
    def forward(self, path):
        _flag = 'rb' if self.is_binary else 'r'
        with open(path, _flag, encoding=self.encoding) as _file: _data = _file.read()
        _name = pathlib.Path(path).stem
        return dict(filename=_name, file=_data)