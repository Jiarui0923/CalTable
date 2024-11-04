from caltable import DataUnit
from caltable import Engines
from caltable import LocalCalBlockLib
from caltable import CalBlock
from caltable import DataTable
from caltable import string
import pandas as pd
import py3Dmol
import os
import pathlib


@DataUnit.register('pdb')
class ProteinPDBTypeEngine(Engines.StringTableTypeEngine):
    def __init__(self, value, iotype):
        super().__init__(value, iotype, sep=' +', end='\n')
    @property
    def preview(self): return f'PDB:{len(self)} lines'
    
    def _plot(self, value, width=400, height=300):
        view = py3Dmol.view(width=width, height=height)
        view.addModelsAsFrames(value)
        view.setStyle({'model': -1}, {"cartoon": {'color': 'spectrum'}})
        view.zoomTo()
        return view
        
    def _repr_markdown_(self):
        self._plot(self.value, width=400, height=300).show()
        return f'{pd.DataFrame(self.table_value)._repr_html_()}'
    
    def view_html(self, width=400, height=300, **kwargs):
        return self._plot(self.value, width=width, height=height).write_html()
    
@LocalCalBlockLib.register('read-pdbs')
class ReadLocalPDBs(CalBlock):
    def __init__(self, pdb_exts=['.pdb'], **kwargs):
        self.pdb_exts = pdb_exts
        super().__init__('Read PDB Files',
                         inputs={'path': string},
                         outputs={'pdb': string, 'pdb_id': string},
                         desc='Read local PDB files from given path',
                         **kwargs)
    
    def _fetch_one(self, path):
        with open(path, 'r') as f: _pdb = f.read()
        _pdb_id = pathlib.Path(path).stem
        return {self.column_map.get('pdb', 'pdb'): _pdb,
                self.column_map.get('pdb_id', 'pdb_id'): _pdb_id,}
    
    def forward_table(self, path:str):
        _data = []
        if os.path.isfile(path): _data.append(self._fetch_one(path))
        else:
            for root, _, files in os.walk(path):
                for file in files:
                    if pathlib.Path(file).suffix in self.pdb_exts:
                        _data.append(self._fetch_one(os.path.join(root, file)))
        return DataTable(_data)