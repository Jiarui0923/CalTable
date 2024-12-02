import re
import json
import pandas as pd
from tabulate import tabulate
from .._data_unit import DataUnit

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
    
@DataUnit.register(['json'])
class StringJSONTypeEngine(StringTypeEngine):
    def __init__(self, value, iotype):
        super().__init__(value=json.dumps(json.loads(value), indent=2), iotype=iotype)
    
    def _template_fold(self, title, data):
        return f'<details><summary><b>{title}</b></summary><div style="margin-left:1em;">{data}</div></details>'
    def _template_row(self, title, data):
        return f'<b>{title}</b>: {data}<br>'
    def _render_json(self, obj):
        content = ""
        for key, val in obj.items():
            if isinstance(val, dict): content += self._template_fold(key, self._render_json(val))
            elif isinstance(val, (list, tuple)): content += self._template_fold(key, self._render_json(dict(enumerate(val))))
            else: content += self._template_row(key, val)
        return content
    
    def __len__(self): return len(self.value)
    def __repr__(self): return self.value
    def _repr_markdown_(self): return self._render_json(json.loads(self.value))
    def view_html(self, **kwargs):
        return self._render_json(json.loads(self.value))