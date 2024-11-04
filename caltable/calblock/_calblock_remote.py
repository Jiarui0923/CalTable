from ._calblock import CalBlock

class CalBlockRemote(CalBlock):
    def __init__(self, remote_algorithm, **kwargs):
        self.remote_algorithm = remote_algorithm
        super().__init__(name=remote_algorithm.name,
                         host=remote_algorithm._client._get_server_info()['server'],
                         inputs=remote_algorithm.inputs,
                         outputs=remote_algorithm.outputs,
                         desc=remote_algorithm.description,
                         **kwargs)
        
    def __repr__(self): return f'< {self.host}[REMOTE]: {self.name} >'
    def forward(self, **inputs):
        return self.remote_algorithm(**inputs)