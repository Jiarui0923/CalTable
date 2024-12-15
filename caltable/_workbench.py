"""
WorkBench Module
================

This module defines the `WorkBench` class, which serves as a container for multiple workflows 
and provides functionality to manage and load them. The class supports adding workflows, 
retrieving them by name, and rendering information about them. It also provides functionality 
to load a workbench from a configuration file.

Modules:
--------
- `WorkBench`: A class that manages a collection of workflows and their associated toolkits.
"""

from uuid import uuid4
import json
import os
import docflow as doc

from ._workflow import Workflow
from ._lib_index import CalLibIndex


class WorkBench(object):
    """
    A class representing a workbench containing multiple workflows and their associated toolkits.

    Attributes:
    -----------
    _id : str
        A unique identifier for the workbench.
    _index : CalLibIndex
        An index of libraries used in the workflows.
    _workflows : dict
        A dictionary of workflows, keyed by their names.
    _name : str
        The name of the workbench.
    _desc : str
        A description of the workbench.

    Methods:
    --------
    __len__():
        Returns the number of workflows in the workbench.
    __repr__():
        Returns a string representation of the workbench.
    _repr_markdown_():
        Returns a markdown string representing the workbench.
    __getitem__(name):
        Retrieves a workflow or a combination of workflows by name.
    toolkits:
        A property that returns the toolkit index.
    workflows:
        A property that returns a list of the workflow names.
    load(workbench_config, force_local_credential=False):
        Loads a workbench from a configuration and returns a `WorkBench` instance.
    """

    def __init__(self, index, workflows={}, name='', desc='', id=None):
        """
        Initializes the WorkBench with the given toolkits, workflows, name, description, and ID.

        Parameters:
        -----------
        index : CalLibIndex
            An index of libraries used in the workflows.
        workflows : dict, optional
            A dictionary of workflows. Defaults to an empty dictionary.
        name : str, optional
            The name of the workbench. Defaults to an empty string.
        desc : str, optional
            A description of the workbench. Defaults to an empty string.
        id : str, optional
            A unique identifier for the workbench. If not provided, a new UUID is generated.
        """
        self._id = str(uuid4()) if id is None else id
        self._index = index
        self._workflows = workflows
        self._name = name
        self._desc = desc

    def __len__(self):
        """
        Returns the number of workflows in the workbench.

        Returns:
        --------
        int
            The number of workflows in the workbench.
        """
        return len(self._workflows)

    def __repr__(self):
        """
        Returns a string representation of the workbench.

        Returns:
        --------
        str
            A string representation of the workbench with workflow names.
        """
        return f'< WorkBench({self._name}) ' + ''.join([_name + ', ' for _name in self._workflows])[:-2] + ' >'

    def _repr_markdown_(self):
        """
        Returns a markdown string representing the workbench.

        Returns:
        --------
        str
            A markdown string describing the workbench and its workflows.
        """
        return doc.Document(
            doc.Title('WorkBench' if len(self._name) <= 0 else f'{self._name}', level=1),
            doc.Text(self._desc),
            doc.Title('Workflows', level=2),
            doc.Sequence({_name: f'**{_workflow.name}**: {_workflow.desc}'
                          for _name, _workflow in self._workflows.items()}),
            doc.Text(self._index._repr_markdown_()),
        ).markdown

    def __getitem__(self, name):
        """
        Retrieves a workflow or a combination of workflows by name.

        Parameters:
        -----------
        name : str or list/tuple
            The name of the workflow or a list/tuple of workflow names.

        Returns:
        --------
        Workflow
            A `Workflow` instance corresponding to the specified name(s).

        Raises:
        -------
        IndexError
            If the specified workflow name is not found.
        TypeError
            If the provided index is neither a string nor a list/tuple.
        """
        if isinstance(name, (tuple, list)):
            _selected_workflows = []
            for _name in name:
                if _name in self._workflows:
                    _selected_workflows.append(self._workflows[_name])
                else:
                    raise IndexError(f'{_name} Not Found')
            return Workflow(*_selected_workflows,
                            name='Combined Workflows',
                            desc=''.join([_workflow + '> ' for _workflow in name])[:-2])
        elif isinstance(name, str):
            return self._workflows[name]
        else:
            raise TypeError('Index Type Error')

    @property  
    def toolkits(self):
        """
        A property that returns the toolkit index.

        Returns:
        --------
        CalLibIndex
            The index of libraries used in the workflows.
        """
        return self._index

    @property
    def workflows(self):
        """
        A property that returns a list of the workflow names.

        Returns:
        --------
        list
            A list of the names of the workflows.
        """
        return list(self._workflows.keys())

    @staticmethod
    def load(workbench_config, force_local_credential=False):
        """
        Loads a workbench from a configuration and returns a `WorkBench` instance.

        Parameters:
        -----------
        workbench_config : str or dict
            The configuration of the workbench, either as a file path or a dictionary.
        force_local_credential : bool, optional
            If True, forces the use of local credentials. Defaults to False.

        Returns:
        --------
        WorkBench
            A `WorkBench` instance created from the provided configuration.

        Raises:
        -------
        FileNotFoundError
            If the provided file path is invalid.
        """
        if isinstance(workbench_config, str):
            if os.path.isfile(workbench_config):
                with open(workbench_config, 'r') as _file:
                    workbench_config = _file.read()
            workbench_config = json.loads(workbench_config)
        else:
            workbench_config = json.load(workbench_config)

        _auth = workbench_config.get('auth')
        _name = workbench_config.get('name')
        _id = workbench_config.get('id')
        _desc = workbench_config.get('desc')
        _libs = workbench_config.get('lib')

        if _auth is not None and not force_local_credential:
            for _lib in _libs:
                if 'api_id' not in _lib or 'api_key' not in _lib:
                    _lib['api_id'] = _auth['api_id']
                    _lib['api_key'] = _auth['api_key']

        _libs = CalLibIndex(config=_libs)
        _workflows = {_name: Workflow.load(_workflow, _libs)
                      for _name, _workflow in workbench_config['workflows'].items()}

        return WorkBench(index=_libs, workflows=_workflows,
                         name=_name, desc=_desc, id=_id)
