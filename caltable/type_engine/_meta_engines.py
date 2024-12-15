"""
MetaEngineLibs and TypeEngine Classes Module
===========================================

This module defines a system for managing different types of engines associated with values, providing
various previews and visualizations (e.g., plots for numerical arrays). The system is extensible, 
allowing different types to be registered and processed dynamically. The module also integrates with
Plotly and Pandas for plotting and displaying data.

Author: Jiarui Li  
Email: jli78@tulane.edu  
Affiliation: Computer Science Department, Tulane University
"""

from ._type_engine import TypeEngine
import plotly.express as px
import pandas as pd

class _MetaTypeEngine(TypeEngine):
    """
    A subclass of TypeEngine representing a meta engine type that associates a specific type of value
    with metadata. This serves as a base class for all other type engines.

    Attributes:
        _iotype_meta_id (str): A unique identifier for the engine's metadata type.
    """
    _iotype_meta_id = ''


class _MetaEngineLibs(object):
    """
    A library class that manages the registration and creation of various MetaTypeEngine instances.
    This class supports engine registration and building of specific type engines based on metadata.

    Methods:
        register_engine(meta_engine: _MetaTypeEngine): Registers a given engine.
        register(engine): A decorator method to register an engine.
        build(value, iotype): Builds an engine instance based on the provided value and iotype.
    """
    
    _meta_engines = {}

    @classmethod
    def register_engine(cls, meta_engine: _MetaTypeEngine):
        """
        Registers a meta engine by associating its meta ID with the engine class.

        Args:
            meta_engine (_MetaTypeEngine): The engine class to register.
        """
        cls._meta_engines[meta_engine._iotype_meta_id] = meta_engine

    @classmethod
    def register(cls, engine):
        """
        A decorator to register a specific engine class.

        Args:
            engine: The engine class to be registered.

        Returns:
            The registered engine class.
        """
        cls.register_engine(engine)
        return engine

    @classmethod
    def build(cls, value, iotype):
        """
        Builds an engine instance based on the provided value and iotype.

        Args:
            value: The value to associate with the engine.
            iotype: The type of the value, providing metadata for engine creation.

        Returns:
            TypeEngine: An instance of the engine corresponding to the given iotype.
        
        Raises:
            TypeError: If the meta type is unknown or unsupported.
        """
        _engine = cls._meta_engines.get(iotype.meta)
        if _engine is None:
            raise TypeError(f'Unknown meta type: {iotype.meta}')
        else:
            return _engine(value=value, iotype=iotype)


@_MetaEngineLibs.register
class StringTypeEngine(_MetaTypeEngine):
    """
    A type engine for string values that provides a preview of the string.

    Attributes:
        preview (str): A preview of the string, truncated if too long.
    """
    _iotype_meta_id = 'string'

    @property
    def preview(self):
        """
        Provides a preview of the string value.

        Returns:
            str: The preview, truncated if the string length exceeds 16 characters.
        """
        if len(self.value) > 16:
            return f'{self.iotype.name}:{self.value[:16]}...({len(self.value)})'
        else:
            return f'{self.value}'


@_MetaEngineLibs.register
class NumberTypeEngine(_MetaTypeEngine):
    """
    A type engine for numeric values.

    Attributes:
        preview (str): The string representation of the numeric value.
    """
    _iotype_meta_id = 'number'

    def __len__(self):
        """
        Returns the length of the number, which is always 1.

        Returns:
            int: The length of the number (1).
        """
        return 1

    @property
    def preview(self):
        """
        Provides a preview of the numeric value.

        Returns:
            str: The string representation of the value.
        """
        return f'{self.value}'


@_MetaEngineLibs.register
class NumArrayTypeEngine(_MetaTypeEngine):
    """
    A type engine for numeric array values, which allows for plotting and visualization.

    Attributes:
        preview (str): A preview of the numeric array, truncated if too long.
    """
    _iotype_meta_id = 'numarray'

    @property
    def preview(self):
        """
        Provides a preview of the numeric array.

        Returns:
            str: The preview, truncated if the array length exceeds 3 elements.
        """
        if len(self.value) > 3:
            return f'{self.iotype.name}:{self.value[:3]}...({len(self.value)})'
        else:
            return f'{self.value}'

    def _plot(self, value):
        """
        Creates a plotly line plot for the given numeric array.

        Args:
            value: The numeric array to plot.

        Returns:
            plotly.graph_objects.Figure: A Plotly figure representing the line plot.
        """
        fig = px.line(x=list(range(len(value))), y=value, title=self.iotype.name)
        return fig

    def _repr_markdown_(self):
        """
        Returns a markdown representation of the numeric array, including a plot.

        Returns:
            str: The markdown representation, including the plot and HTML table.
        """
        self._plot(self.value).show()
        return f'{pd.DataFrame(self.value).T._repr_html_()}'

    def view_html(self, **kwargs):
        """
        Returns an HTML representation of the numeric array as a Plotly plot.

        Args:
            **kwargs: Additional keyword arguments for customizing the plot.

        Returns:
            str: The HTML representation of the plot.
        """
        return self._plot(self.value).to_html()
