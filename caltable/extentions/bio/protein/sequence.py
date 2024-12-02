import re
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from caltable import DataUnit
from caltable import Engines

@DataUnit.register(['fasta'])
class SequenceAlignmentTypeEngine(Engines.StringTypeEngine):
    def __init__(self, value, iotype):
        super().__init__(value, iotype)
    
    def _fetch_sequences(self, _alignment):
        return dict(re.findall(r">(.*?)\n([^>]+)\n", _alignment))
    def _generate_heatmap_data(self, sequences):
        """Converts sequences into numerical matrix for visualization."""
        residues = sorted(set("".join(sequences.values())))  # Unique residues
        residue_to_int = {res: i for i, res in enumerate(residues)}  # Map residue to int
        _max_len = max([len(sequence) for sequence in sequences.values()])
        # Convert sequences to a numerical matrix
        alignment_matrix = [
            [residue_to_int[res] for res in seq] + [-1] *(_max_len - len(seq))
            for seq in sequences.values()
        ]
        residues.insert(0, "*")
        return np.array(alignment_matrix), list(sequences.keys()), residues
    def _plot_sequences(self, sequences):
        alignment_matrix, sequence_names, residues = self._generate_heatmap_data(sequences)
        fig = go.Figure(
            data=go.Heatmap(
                z=alignment_matrix, 
                x=list(range(alignment_matrix.shape[1])),  # Columns represent positions
                y=sequence_names,  # Rows are sequence names
                colorscale="Viridis",  # Color scheme
                colorbar=dict(
                    title="Residues",
                    tickvals=list(range(len(residues))),
                    ticktext=residues,
                )
            )
        )
        # Update layout for better readability
        fig.update_layout(
            title="FASTA Alignment Visualization",
            xaxis_title="Position",
            yaxis_title="Sequences",
            yaxis=dict(showgrid=False, automargin=True),
            xaxis=dict(
                title="Position",
                tickmode="array",
                showgrid=False,
                scaleanchor="y",  # Lock x and y axis scales to make squares
                scaleratio=1
            ),
        )

        return fig
    def _plot(self, value):
        _sequences = self._fetch_sequences(value)
        fig = self._plot_sequences(_sequences)
        return fig
        
    def _repr_markdown_(self):
        self._plot(self.value).show()
        return f'{pd.DataFrame(list(self._fetch_sequences(self.value).items()), columns=["ID", "Sequence"])._repr_html_()}'
    
    def view_html(self, **kwargs):
        return self._plot(self.value).to_html()