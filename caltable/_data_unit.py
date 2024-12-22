"""
DataUnit Module

The DataUnit module provides a framework for handling data with specific types. It integrates with the _MetaEngineLibs class to create data engines based on the input type. Each DataUnit instance can compute and manipulate data using the appropriate engine, making it flexible for a wide range of data types, such as numbers, strings, and complex structures. The module also supports operations like comparisons and rendering of data in various formats (markdown, HTML, and file generation).

Classes:
- DataUnit: A container for holding data and its corresponding engine, supporting various operations on the data.

Methods:
- __init__: Initializes the DataUnit with a given parameter and value.
- __repr__: Returns a string representation of the DataUnit.
- __len__: Returns the length of the data managed by the engine.
- Comparison operators (__eq__, __ne__, __lt__, etc.): Allow comparison operations between DataUnit instances or between a DataUnit and other values.
- _repr_markdown_: Returns the markdown representation of the DataUnit.
- view_html: Returns the HTML view of the data.
- preview: Provides a preview of the data.
- file: Allows exporting the data to a file.
- register_engine: Registers a custom engine for specific iotype IDs.
- register: A decorator function for registering engines for specific iotype IDs.
"""

from .type_engine._meta_engines import _MetaEngineLibs

class DataUnit(object):
    """
    A container for managing data and its corresponding type engine.
    
    Attributes:
        parameter: The parameter associated with the data (e.g., its type).
        value: The actual data value.
        name: The name of the parameter.
        desc: A description of the parameter.
        iotype: The input/output type of the parameter.
        _engine: The engine responsible for handling operations on the data.

    Methods:
        __repr__: Returns a string representation of the DataUnit.
        __len__: Returns the length of the data managed by the engine.
        Comparison operators (__eq__, __ne__, __lt__, etc.): Allow comparison operations on the data.
        _repr_markdown_: Returns a markdown formatted representation of the data.
        view_html: Returns the HTML view of the data.
        preview: Returns a preview of the data.
        file: Exports the data to a file.
        register_engine: Registers a custom engine for a given iotype ID.
        register: A decorator function for engine registration.
    """

    _specific_engines = {}

    def __init__(self, parameter, value):
        """
        Initializes a DataUnit instance with the provided parameter and value.
        
        Args:
            parameter: The parameter associated with the data.
            value: The data value to be handled.
        """
        self.parameter = parameter
        self.name = parameter.name
        self.desc = parameter.desc
        self.iotype = parameter.iotype
        self._engine = self._build_engine(self.iotype, value)
    
    @property
    def value(self):
        return self._engine.value
    
    @classmethod
    def _build_engine(cls, iotype, value):
        """
        Builds the appropriate engine for the data based on its iotype.
        
        Args:
            iotype: The input/output type of the parameter.
            value: The data value to be handled.
        
        Returns:
            An engine that will handle operations for this data.
        """
        if iotype.id in cls._specific_engines:
            return cls._specific_engines[iotype.id](value=value, iotype=iotype)
        return _MetaEngineLibs.build(value=value, iotype=iotype)

    def __repr__(self):
        """
        Returns a string representation of the DataUnit by using its engine's __repr__ method.
        
        Returns:
            str: A string representation of the DataUnit.
        """
        return repr(self._engine)

    def __len__(self):
        """
        Returns the length of the data handled by the engine.
        
        Returns:
            int: The length of the data.
        """
        return len(self._engine)

    def _binary_opt(self, other, func):
        """
        Helper method for performing binary operations on the data.
        
        Args:
            other: The other value (or DataUnit) to perform the operation with.
            func: The function to apply for the binary operation.
        
        Returns:
            The result of the binary operation.
        """
        if isinstance(other, DataUnit):
            return func(other._engine)
        else:
            return func(other)

    def __eq__(self, other):
        """
        Compares the DataUnit with another value or DataUnit for equality.
        
        Args:
            other: The other value or DataUnit to compare with.
        
        Returns:
            bool: True if the data is equal to the other value, otherwise False.
        """
        return self._binary_opt(other, self._engine.__eq__)

    def __ne__(self, other):
        """
        Compares the DataUnit with another value or DataUnit for inequality.
        
        Args:
            other: The other value or DataUnit to compare with.
        
        Returns:
            bool: True if the data is not equal to the other value, otherwise False.
        """
        return self._binary_opt(other, self._engine.__ne__)

    def __lt__(self, other):
        """
        Compares the DataUnit with another value or DataUnit for less than.
        
        Args:
            other: The other value or DataUnit to compare with.
        
        Returns:
            bool: True if the data is less than the other value, otherwise False.
        """
        return self._binary_opt(other, self._engine.__lt__)

    def __gt__(self, other):
        """
        Compares the DataUnit with another value or DataUnit for greater than.
        
        Args:
            other: The other value or DataUnit to compare with.
        
        Returns:
            bool: True if the data is greater than the other value, otherwise False.
        """
        return self._binary_opt(other, self._engine.__gt__)

    def __le__(self, other):
        """
        Compares the DataUnit with another value or DataUnit for less than or equal to.
        
        Args:
            other: The other value or DataUnit to compare with.
        
        Returns:
            bool: True if the data is less than or equal to the other value, otherwise False.
        """
        return self._binary_opt(other, self._engine.__le__)

    def __ge__(self, other):
        """
        Compares the DataUnit with another value or DataUnit for greater than or equal to.
        
        Args:
            other: The other value or DataUnit to compare with.
        
        Returns:
            bool: True if the data is greater than or equal to the other value, otherwise False.
        """
        return self._binary_opt(other, self._engine.__ge__)

    def __contains__(self, other):
        """
        Checks if the given value or DataUnit is contained in the data.
        
        Args:
            other: The value or DataUnit to check for containment.
        
        Returns:
            bool: True if the data contains the other value, otherwise False.
        """
        return self._binary_opt(other, self._engine.__contains__)

    def _repr_markdown_(self):
        """
        Returns the markdown formatted representation of the DataUnit.
        
        Returns:
            str: The markdown formatted representation of the data.
        """
        return self._engine._repr_markdown_()

    def view_html(self, **kwargs):
        """
        Returns the HTML view of the DataUnit.
        
        Args:
            kwargs: Additional arguments for customizing the HTML output.
        
        Returns:
            str: The HTML formatted representation of the data.
        """
        return self._engine.view_html(**kwargs)

    @property
    def preview(self):
        """
        Returns a preview of the data.
        
        Returns:
            str: A preview of the data.
        """
        return self._engine.preview

    def file(self, name=None):
        """
        Exports the data to a file.
        
        Args:
            name: The name of the file to save. If None, the default name is used.
        
        Returns:
            FileUnit: The FileUnit object representing the saved file.
        """
        return self._engine.file(name=self.name if name is None else name)

    @classmethod
    def register_engine(cls, iotype_ids, engine):
        """
        Registers a custom engine for specific iotype IDs.
        
        Args:
            iotype_ids: The iotype IDs to register the engine for.
            engine: The engine to register.
        """
        if isinstance(iotype_ids, str):
            cls._specific_engines[iotype_ids] = engine
        else:
            for iotype_id in iotype_ids:
                cls._specific_engines[iotype_id] = engine

    @classmethod
    def register(cls, iotype_ids):
        """
        A decorator function for registering engines for specific iotype IDs.
        
        Args:
            iotype_ids: The iotype IDs to register the engine for.
        
        Returns:
            function: The wrapped engine function.
        """
        def wrap(engine):
            cls.register_engine(iotype_ids, engine)
            return engine
        return wrap
