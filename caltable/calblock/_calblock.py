"""
CalBlock Module
===============

This module provides the `CalBlock` class, which facilitates interaction with 
the `easyapi` through tabular data manipulation, similar to working with pandas DataFrames. 
It is designed to map inputs and outputs between a computational block and a data table, 
making it easier for users to perform computations.

Author: Jiarui Li
Email: jli78@tulane.edu
Affiliation: Computer Science Department, Tulane University
"""

import docflow as doc


class CalBlock:
    """
    A computational block class for handling input-output mappings 
    and computations with tabular data.
    """

    def __init__(self, name=None, host='local', inputs=None, outputs=None, desc='', **kwargs):
        """
        Initialize the CalBlock instance.

        Args:
            name (str): The name of the block. Defaults to the class name.
            host (str): The host identifier. Defaults to 'local'.
            inputs (dict): Input parameter definitions.
            outputs (dict): Output parameter definitions.
            desc (str): Description of the block.
            **kwargs: Additional column mapping arguments.
        """
        self.name = self.__class__.__name__ if name is None else name
        self.host = host
        self.column_map = kwargs
        self.inputs = inputs or {}
        self.outputs = outputs or {}
        self.desc = desc

    def _fetch_input(self, table, row=0, params=None):
        """
        Fetch input parameters from the table for a specific row.

        Args:
            table: The data table containing input values.
            row (int): Row index to fetch values from.
            params (dict): Parameter definitions.

        Returns:
            dict: Mapped input parameters and their values.
        """
        params = params or {}
        _inputs = {}
        for param in params.keys():
            col_name = self.column_map.get(param, param)
            if col_name in table.columns:
                _param = table[row, col_name]
                if _param is not None:
                    _inputs[param] = _param.value
        return _inputs

    def _assign_output(self, table, row=0, outputs=None, params=None):
        """
        Assign output parameters to the table for a specific row.

        Args:
            table: The data table to assign values to.
            row (int): Row index to assign values to.
            outputs (dict): Output parameter values.
            params (dict): Parameter definitions.

        Returns:
            table: The updated table with assigned values.
        """
        params = params or {}
        outputs = outputs or {}
        table.set_types(params)
        _mapped_params = {self.column_map.get(key, key): val for key, val in params.items()}
        table.set_types(_mapped_params)
        for key, val in outputs.items():
            col_name = self.column_map.get(key, key)
            table[row, col_name] = val
        return table

    def __repr__(self):
        """
        String representation of the CalBlock instance.

        Returns:
            str: The representation string.
        """
        return f'<{self.host}[LOCAL]: {self.name}>'

    def forward(self, **inputs):
        """
        Define the forward computation of the block.

        This method should be implemented in subclasses.

        Args:
            **inputs: Input parameters.

        Raises:
            NotImplementedError: If not implemented in a subclass.
        """
        raise NotImplementedError

    def forward_table(self, table):
        """
        Perform forward computation for each row in the table.

        Args:
            table: The data table to process.

        Returns:
            table: The updated table with computed values.
        """
        for row in range(len(table)):
            try:
                _inputs = self._fetch_input(table, row=row, params=self.inputs)
                _outputs = self.forward(**_inputs)
                self._assign_output(table, row=row, outputs=_outputs, params=self.outputs)
            except Exception as e:
                raise e
        return table

    def __call__(self, *args, **kwargs):
        """
        Enable the instance to be callable and perform forward table processing.

        Args:
            *args: Positional arguments for `forward_table`.
            **kwargs: Keyword arguments for `forward_table`.

        Returns:
            table: The updated table with computed values.
        """
        return self.forward_table(*args, **kwargs)

    def _repr_markdown_(self):
        """
        Generate a Markdown representation of the CalBlock instance.

        Returns:
            str: Markdown-formatted string.
        """
        _doc = doc.Document(
            doc.Title(self.name, level=3),
            doc.Text(f'\n{self.desc}  \n'),
            doc.Title('Parameters', level=4),
            doc.Sequence({
                self.column_map.get(param, param): (
                    f'({io_obj.iotype.meta}:**{io_obj.iotype.name}**)'
                    f'{"_[OPTIONAL]_" if io_obj.optional else ""}'
                    f'=`{io_obj.default}`; {io_obj.desc}; '
                    f'(`{io_obj.iotype.condition}`) {io_obj.iotype.doc}'
                )
                for param, io_obj in self.inputs.items()
            }),
            doc.Title('Returns', level=4),
            doc.Sequence({
                self.column_map.get(param, param): (
                    f'({io_obj.iotype.meta}:**{io_obj.iotype.name}**)'
                    f'{"_[OPTIONAL]_" if io_obj.optional else ""}'
                    f'=`{io_obj.default}`; {io_obj.desc}; '
                    f'(`{io_obj.iotype.condition}`) {io_obj.iotype.doc}'
                )
                for param, io_obj in self.outputs.items()
            }),
        )
        return _doc.markdown
