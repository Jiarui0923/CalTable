from caltable import LocalCalBlockLib
from caltable import CalBlock
from caltable import Parameter

import pathlib
import pandas as pd

@LocalCalBlockLib.register('read-sheet')
class ReadSheet(CalBlock):
    def __init__(self, **kwargs):
        super().__init__('Read File',
                         inputs={'path': Parameter.string('path', 'The path to the target sheet file (.csv or .xlsx)'),
                                 'row_index': Parameter.string('row_index', 'Select the target row', default_value='', optional=True)},
                         outputs={},
                         desc='Read local sheet file and attach to the table.',
                         **kwargs)
    
    def forward(self, path, row_index):
        if pathlib.Path(path).suffix == '.csv':
            _table = pd.read_csv(path, index_col=0)
        elif pathlib.Path(path).suffix == '.xlsx':
            _table = pd.read_excel(path, index_col=0)
        else: raise TypeError(f'{pathlib.Path(path).suffix} Not Supported!')
        return _table.loc[row_index].to_dict()