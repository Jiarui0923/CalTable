from ._calblock_lib import CalBlockLib
from .._calblock_remote import CalBlockRemote
from ...easyapi_client import docflow as doc
from ...easyapi_client import EasyAccess

class RemoteCalBlockLib(CalBlockLib):
    
    def __init__(self, client=None, host=None, api_id=None, api_key=None):
        if client is None: client = EasyAccess(host=host, api_id=api_id, api_key=api_key)
        self.client = client
        _host = client._get_server_info()['server']
        _blocks = {}
        for algorithm in client.algorithms:
            _blocks[algorithm] = client[algorithm]
        
        super().__init__(source=_host,
                         **_blocks)
        
    def __getitem__(self, name): return lambda **kwargs: CalBlockRemote(self._lib[name], **kwargs)
    
    def _repr_markdown_(self):
        _doc = doc.Document(
            doc.Title(self.source, level=3),
            doc.Sequence({key:val.description for key, val in self._lib.items()})
        )
        return _doc.markdown