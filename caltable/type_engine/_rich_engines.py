import re
import pandas as pd
from tabulate import tabulate

from ._meta_engines import StringTypeEngine

class StringTableTypeEngine(StringTypeEngine):
    def __init__(self, value, iotype, sep=' ', end='\n'):
        super().__init__(value=value, iotype=iotype)
        self.sep, self.end = sep, end
        self.table_value = self._build_table(value, sep=sep, end=end)
    
    def _build_table(self, value, sep=' ', end='\n'):
        return [re.split(sep, line) for line in re.split(end, value) if len(line) > 0]
    
    def __len__(self): return len(self.table_value)
    def __repr__(self): return tabulate(self.table_value)
    def _repr_markdown_(self): return pd.DataFrame(self.table_value)._repr_html_()