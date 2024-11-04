from caltable import DataUnit
from caltable import Engines
import plotly.express as px
import pandas as pd

@DataUnit.register(['sasa', 'corex', 'bfactor'])
class ProteinValuesTypeEngine(Engines.NumArrayTypeEngine):
    def __init__(self, value, iotype):
        super().__init__(value, iotype)
    
    def _plot(self, value):
        fig = px.line(x=list(range(len(value))), y=value, title=self.iotype.name)
        return fig
        
    def _repr_markdown_(self):
        self._plot(self.value).show()
        return f'{pd.DataFrame(self.value).T._repr_html_()}'
    
    def view_html(self, **kwargs):
        return self._plot(self.value).to_html()