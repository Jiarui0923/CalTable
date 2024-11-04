from .remote_algorithm import RemoteAlgorithm
from . import docflow as doc

from urllib.parse import urljoin
import requests
import json


class EasyAPIClient(object):
    
    def __init__(self, host, api_id, api_key):
        self.host = host
        self.api_id = api_id
        self.api_key = api_key
        
    def __len__(self): return len(self._get_entries())
    def __getitem__(self, entry):
        _entries = self._get_entries()
        if entry not in _entries: raise ModuleNotFoundError(f'Algorithm {entry} does not exists.')
        return RemoteAlgorithm(self, entry)
    def __repr__(self):
        return f'{self._get_server_info().get("server")}:{str(self._get_entries())}'
    def _repr_markdown_(self):
        _server_info = self._get_server_info()
        return doc.Document(
            doc.Title(_server_info.get("server"), level=3),
            doc.Text(f'Authenticated as {_server_info.get("id")}'),
            doc.Sequence({
                algo_name:self._get_entry(algo_name).get('name')
                for algo_name in self._get_entries()
            })
        ).markdown
    
    @property
    def algorithms(self): return self._get_entries()
    
    def _request(self, entry='', method='GET', data=None):
        headers = {'easyapi-id': self.api_id, 'easyapi-key': self.api_key}
        _full_url = urljoin(self.host, entry)
        if method.upper() == 'GET':
            response = requests.get(_full_url, params=data, headers=headers)
        elif method.upper() == 'POST':
            response = requests.post(_full_url, data=json.dumps(data), headers=headers)
        else: raise RuntimeError('Method Not Allowed')
        if response.status_code != 200: raise ConnectionError(f'{response.content.decode()}')
        return json.loads(response.content)
    
    def _get_server_info(self):
        data = self._request(entry='./',
                             method='GET')
        return data
    
    def _get_entries(self):
        data = self._request(entry='./entries/',
                             method='GET',
                             data={'skip':0, 'limit':-1})
        return data.get('records')
    
    def _get_entry(self, entry_name):
        data = self._request(entry=f'./entries/{entry_name}',
                             method='GET')
        return data
    
    def _get_entry_input(self, entry_name):
        data = self._request(entry=f'./entries/{entry_name}/in',
                             method='GET')
        return data
    
    def _get_entry_output(self, entry_name):
        data = self._request(entry=f'./entries/{entry_name}/out',
                             method='GET')
        return data
    
    def _get_ios(self):
        data = self._request(entry='./io/',
                             method='GET',
                             data={'skip':0, 'limit':-1})
        return data.get('records')
    
    def _get_io(self, ioname):
        data = self._request(entry=f'./io/{ioname}',
                             method='GET')
        return data
    
    def _submit_task(self, entry_name, params):
        data = self._request(entry=f'./entries/{entry_name}',
                             method='POST',
                             data=params)
        return data.get('task_id')

    def _get_task_return(self, task_id):
        data = self._request(entry=f'./tasks/{task_id}',
                             method='GET')
        return data