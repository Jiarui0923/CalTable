from caltable import DataUnit
from caltable import Engines
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import io
import base64

@DataUnit.register(['sasa', 'corex', 'bfactor', 'sequence_entropy', 'apl-aggregate',
                    'apl-residue-likelihood', 'apl-peptide-likelihood'])
class ProteinValuesTypeEngine(Engines.NumArrayTypeEngine):
    def __init__(self, value, iotype):
        super().__init__(value, iotype)
    
    def _plot(self, value, title=None, x_label=None, y_label=None, grid=False):
        matplotlib.use('agg')
        fig = plt.figure()
        ax = fig.subplots()
        ax.plot(list(range(len(value))), value)
        ax.set_title(self.iotype.name if title is None else title)
        if x_label is not None: ax.set_xlabel(x_label)
        if y_label is not None: ax.set_xlabel(y_label)
        if grid: ax.grid()
        return fig
        
    def _repr_markdown_(self):
        return self.view_html()
    
    def view_html(self, title=None, x_label=None, y_label=None, grid=False):
        fig = self._plot(self.value, title=title, x_label=x_label, y_label=y_label, grid=grid)
        img_stream = io.BytesIO()
        fig.savefig(img_stream, format='jpg', bbox_inches='tight')
        img_stream.seek(0)
        img_base64 = base64.b64encode(img_stream.read()).decode()
        _image_base64 = f'<img src="data:image/jpg;base64,{img_base64}">'
        fig.clear()
        plt.close(fig)
        return _image_base64
    
@DataUnit.register(['mhcii', 'apl-mhc-combined'])
class ProteinValuesTypeEngine(Engines.StringJSONTypeEngine):
    
    def _plot(self, value, title=None, x_label=None, y_label=None, grid=False):
        matplotlib.use('agg')
        fig = plt.figure()
        ax = fig.subplots()
        _df = pd.read_json(io.StringIO(value))
        _df.plot(ax=ax)
        ax.set_title(self.iotype.name if title is None else title)
        if x_label is not None: ax.set_xlabel(x_label)
        if y_label is not None: ax.set_xlabel(y_label)
        if grid: ax.grid()
        return fig
        
    def _repr_markdown_(self):
        return self.view_html()
    
    def view_html(self, title=None, x_label=None, y_label=None, grid=False):
        fig = self._plot(self.value, title=title, x_label=x_label, y_label=y_label, grid=grid)
        img_stream = io.BytesIO()
        fig.savefig(img_stream, format='jpg', bbox_inches='tight')
        img_stream.seek(0)
        img_base64 = base64.b64encode(img_stream.read()).decode()
        _image_base64 = f'<img src="data:image/jpg;base64,{img_base64}">'
        fig.clear()
        plt.close(fig)
        return _image_base64