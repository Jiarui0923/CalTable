"""
Workflow Module
===============

This module defines the `Workflow` class, which is a subclass of `CalBlock`. It is used to 
define and execute a sequence of `CalBlock` operations, also known as a workflow. The class 
provides methods for managing inputs and outputs, analyzing blocks, and forwarding data 
through the sequence. Workflows can be loaded from a configuration and executed on tables 
or data frames.

Modules:
--------
- `Workflow`: A class to define and manage workflows, which are sequences of `CalBlock` operations.
"""

from .calblock import CalBlock
from . import IndexCal


class Workflow(CalBlock):
    """
    A class representing a sequence of `CalBlock` operations, also known as a workflow.

    Attributes:
    -----------
    _blocks : list
        A list of `CalBlock` objects that represent the operations in the workflow.

    Methods:
    --------
    __init__(*args, name=None, desc=None):
        Initializes the Workflow with the given blocks, name, and description.
    _inputs_analysis():
        Analyzes and returns the inputs required by the workflow.
    _outputs_analysis():
        Analyzes and returns the outputs produced by the workflow.
    __len__():
        Returns the number of blocks in the workflow.
    __repr__():
        Returns a string representation of the workflow.
    forward_table(table):
        Forwards the input table through all blocks in the workflow.
    load(workflow, index=IndexCal):
        Loads a workflow from a configuration and returns a `Workflow` object.
    """

    def __init__(self, *args, name=None, desc=None):
        """
        Initializes the Workflow with the given blocks, name, and description.

        Parameters:
        -----------
        *args : CalBlock
            One or more `CalBlock` instances to be included in the workflow.
        name : str, optional
            The name of the workflow. Defaults to the class name.
        desc : str, optional
            A description of the workflow. Defaults to a generated description.
        """
        self._blocks = args
        name = self.__name__ if name is None else name
        desc = f'{name} Workflow(blocks={len(args)})' if desc is None else desc
        super().__init__(name=name,
                         inputs=self._inputs_analysis(),
                         outputs=self._outputs_analysis(),
                         desc=desc)

    def _inputs_analysis(self):
        """
        Analyzes and returns the inputs required by the workflow.

        Returns:
        --------
        dict
            A dictionary of input names and their corresponding values.
        """
        _existed_inputs = [self._blocks[0].column_map.get(key, key)
                           for key in self._blocks[0].outputs]
        _inputs = {self._blocks[0].column_map.get(key, key): val
                   for key, val in self._blocks[0].inputs.items()}
        for block_ in self._blocks[1:]:
            for key, val in block_.inputs.items():
                key = block_.column_map.get(key, key)
                if key not in _inputs and key not in _existed_inputs:
                    _inputs[key] = val
            for key in block_.outputs:
                key = block_.column_map.get(key, key)
                if key not in _existed_inputs:
                    _existed_inputs.append(key)
        return _inputs

    def _outputs_analysis(self):
        """
        Analyzes and returns the outputs produced by the workflow.

        Returns:
        --------
        dict
            A dictionary of output names and their corresponding values.
        """
        _outputs = {}
        for block_ in self._blocks:
            for key, val in block_.outputs.items():
                _outputs[block_.column_map.get(key, key)] = val
        return _outputs

    def __len__(self):
        """
        Returns the number of blocks in the workflow.

        Returns:
        --------
        int
            The number of blocks in the workflow.
        """
        return len(self._blocks)

    def __repr__(self):
        """
        Returns a string representation of the workflow.

        Returns:
        --------
        str
            A string representation of the workflow.
        """
        return f'< {self.host}[LOCAL]: {self.name} Blocks={len(self)} >'

    def forward_table(self, table):
        """
        Forwards the input table through all blocks in the workflow.

        Parameters:
        -----------
        table : DataFrame
            The input table to be processed by the workflow.

        Returns:
        --------
        DataFrame
            The processed table after passing through all blocks.
        """
        for _block in self._blocks:
            table = _block(table)
        return table

    @classmethod
    def load(cls, workflow, index=IndexCal):
        """
        Loads a workflow from a configuration and returns a `Workflow` object.

        Parameters:
        -----------
        workflow : dict
            A dictionary containing the workflow configuration.
        index : IndexCal, optional
            An index to map workflow units to `CalBlock` instances. Defaults to `IndexCal`.

        Returns:
        --------
        Workflow
            A `Workflow` instance created from the provided configuration.

        Raises:
        -------
        TypeError
            If the configuration format is invalid.
        """
        _name = workflow.get('name', None)
        _desc = workflow.get('desc', None)
        workflow = workflow['workflow']
        _workflow_blocks = []
        for _unit in workflow:
            if isinstance(_unit, str):
                _workflow_blocks.append(index[_unit]())
            elif isinstance(_unit, (list, tuple)):
                if len(_unit) >= 2:
                    _unit, _param = _unit[0], _unit[1]
                elif len(_unit) == 1:
                    _unit, _param = _unit[0], {}
                else:
                    raise TypeError
                _workflow_blocks.append(index[_unit](**_param))
        return cls(*_workflow_blocks, name=_name, desc=_desc)
