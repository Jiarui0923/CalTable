from uuid import uuid4
import json
import os

from .easyapi_client import docflow as doc
from ._workflow import Workflow
from ._lib_index import CalLibIndex

class WorkBench(object):
    
    def __init__(self, index, workflows={}, name='', desc='', id=None):
        self._id = str(uuid4()) if id is None else id
        self._index = index
        self._workflows = workflows
        self._name = name
        self._desc = desc
    def __len__(self): return len(self._workflows)   
    def __repr__(self): return f'< WorkBench({self._name}) ' + ''.join([_name+', ' for _name in self._workflows])[:-2] + ' >'
    def _repr_markdown_(self):
        return doc.Document(
            doc.Title('WorkBench' if len(self._name) <= 0 else f'{self._name}', level=1),
            doc.Text(self._desc),
            doc.Title('Workflows', level=2),
            doc.Sequence({_name: f'**{_workflow.name}**: {_workflow.desc}'
                          for _name, _workflow in self._workflows.items()}),
            doc.Text(self._index._repr_markdown_()),
        ).markdown
    def __getitem__(self, name):
        if isinstance(name, (tuple, list)):
            _selected_workflows = []
            for _name in name:
                if _name in self._workflows:
                    _selected_workflows.append(self._workflows[_name])
                else: raise IndexError(f'{_name} Not Found')
            return Workflow(*_selected_workflows,
                               name='Combined Workflows',
                               desc=''.join([_workflow + '> ' for _workflow in name])[:-2])
        elif isinstance(name, str): return self._workflows[name]
        else: raise TypeError('Index Type Error')
        
    @property  
    def toolkits(self): return self._index
    @property
    def workflows(self): return list(self._workflows.keys())
    
    @staticmethod
    def load(workbench_config, force_local_credential=False):
        if isinstance(workbench_config, str):
            if os.path.isfile(workbench_config):
                with open(workbench_config, 'r') as _file:
                    workbench_config = _file.read()
            workbench_config = json.loads(workbench_config)
        else:
            workbench_config = json.load(workbench_config)
        _auth = workbench_config.get('auth')
        _name = workbench_config.get('name')
        _id = workbench_config.get('id')
        _desc = workbench_config.get('desc')
        _libs = workbench_config.get('lib')
        if _auth is not None and not force_local_credential:
            for _lib in _libs:
                if 'api_id' not in _lib or 'api_key' not in _lib:
                    _lib['api_id'] = _auth['api_id']
                    _lib['api_key'] = _auth['api_key']
        _libs = CalLibIndex(config=_libs)
        _workflows = {_name:Workflow.load(_workflow, _libs)
                      for _name, _workflow in workbench_config['workflows'].items()}
        return WorkBench(index=_libs, workflows=_workflows,
                         name=_name, desc=_desc, id=_id)