from .iotypemodel.iotype_model import IOType

class Parameter(object):
    
    def __init__(self, name, io_type, desc='', default_value=None, optional=False):
        self.name = name
        self.desc = desc
        self.optional = optional
        self.default = default_value
        self.iotype = io_type
    
    @property
    def property(self):
        return {
            'name': self.name,
            'io': self.iotype.id,
            'optional': self.optional,
            'default': self.default,
            'desc': self.desc
        }
        
meta_types = {
    'string': IOType(meta='string', id='string', name='string'),
    'number': IOType(meta='number', id='number', name='number'),
    'numarray': IOType(meta='numarray', id='numarray', name='numarray'),
}  
        
string = Parameter(name='string', io_type=meta_types['string'])
number = Parameter(name='number', io_type=meta_types['number'])
numarray = Parameter(name='numarray', io_type=meta_types['numarray'])