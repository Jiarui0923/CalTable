from ._calblock._lib import CalBlockLib
from ._calblock._lib import RemoteCalBlockLib
from .easyapi_client import docflow as doc
from . import LocalCal
import json
import os
class CalLibIndex(object):
    
    def __init__(self, *args, config=None, local=True):
        self._libs = [arg for arg in args if isinstance(arg, CalBlockLib)]
        if local: self.add(LocalCal)
        if config is not None:
            self.load(config)

    def add(self, lib): self._libs.append(lib)
    def __len__(self): return sum([len(_lib) for _lib in self._libs])
    def __repr__(self): return f'< LibIndex[{len(self._libs)} libs] {len(self)} Algorithms >'
    def __getitem__(self, key):
        _sources = None
        if isinstance(key, tuple):
            _name = key[0]
            if len(key) > 1: _sources = key[1]
        elif isinstance(key, str): _name = key
        else: raise TypeError('Index type error.')
        if ':' in _name: _name, _sources = _name.split(':')
        
        if _sources is not None:
            if isinstance(_sources, str): _sources = [_source for _source in _sources.split(',') if len(_source) > 0]
        
        _blocks = [(_lib.source, _lib[_name]) for _lib in self._libs if _name in _lib]
        if len(_blocks) <= 0: raise IndexError(f'{_name} Not Found.')
        if _sources is None: return _blocks[0][1]
        for _source in _sources:
            for _block in _blocks:
                if _source == _block[0]: return _block[1]
        raise IndexError(f'{_name} exists in {[_block[0] for _block in _blocks]}')
    
    def __contains__(self, name):
        if ':' in name:
            _name, _sources = _name.split(':')
            _sources = [_source for _source in _sources.split(',') if len(_source) > 0]
            if len(_sources) <= 0: raise IndexError('Empty Source!')
            else:
                for _source in _sources:
                    for _lib in self._libs:
                        if _name in _lib and _lib.source == _source: return True
                return False
        else: return any([name in _lib for _lib in self._libs])
    
    def _repr_markdown_(self):
        _doc = doc.Document(
            doc.Title('LibIndex', level=2),
            doc.Text(f'`{len(self._libs)} libs` `{len(self)} Algorithms`\n\n'),
            *[doc.Text(_lib._repr_markdown_()+'\n\n') for _lib in self._libs]
        )
        return _doc.markdown
    
    def load(self, config):
        if isinstance(config, str):
            with open(config, 'r') as f: _config = json.loads(f.read())
        elif isinstance(config, list): _config = config
        else: _config = json.loads(config.read())
        for item in _config:
            if 'host' not in item: raise KeyError('No host in the config')
            if 'api_id' not in item:
                item['api_id'] = os.environ.get('EASYAPI_ID')
                if item['api_id'] is None: raise KeyError('API ID did not provide')
            if 'api_key' not in item:
                item['api_key'] = os.environ.get('EASYAPI_KEY')
                if item['api_key'] is None: raise KeyError('API Key did not provide')
            self.add(RemoteCalBlockLib(**item))
            
    def save(self, path=None, save_credentials=False):
        if save_credentials: UserWarning('Save crendentials is not safe!')
        _save_dict = []
        for _lib in self._libs:
            if isinstance(_lib, RemoteCalBlockLib):
                if save_credentials: _save_dict.append({'host': _lib.client.host,
                                                        'api_id': _lib.client.api_id,
                                                        'api_key': _lib.client.api_key})
                else: _save_dict.append({'host': _lib.client.host})
        _save = json.dumps(_save_dict)
        if path is None: return _save
        else:
            with open(path, 'w') as f: f.write(_save)