"""
CalLibIndex Module
==================

This module defines the `CalLibIndex` class, which is used to manage and interact with 
multiple instances of `CalBlockLib` libraries (both local and remote). It provides methods 
to add libraries, retrieve algorithms, load and save configurations, and generate markdown 
documentation for the libraries.

The `CalLibIndex` class allows users to work with a collection of algorithm libraries that 
can be accessed either locally or remotely via an API. It supports loading configurations 
from JSON files and saving them for later use.

Modules:
--------
- `CalLibIndex`: A class to manage `CalBlockLib` libraries.
"""

from .calblock._lib import CalBlockLib
from .calblock._lib import RemoteCalBlockLib
import docflow as doc
from . import LocalCal
import json
import os


class CalLibIndex(object):
    """
    Class to manage and interact with multiple instances of `CalBlockLib` libraries, both local and remote.

    Attributes:
    -----------
    _libs : list
        A list containing instances of `CalBlockLib` and `LocalCal` libraries.
    """

    def __init__(self, *args, config=None, local=True):
        """
        Initializes the CalLibIndex with the provided libraries and configuration.

        Parameters:
        -----------
        *args : CalBlockLib
            One or more `CalBlockLib` instances to be added to the library index.
        config : str or list, optional
            Configuration for remote libraries, either as a JSON file path or a list of configurations.
        local : bool, optional
            If True, adds the `LocalCal` library to the index (default is True).
        """
        self._libs = [arg for arg in args if isinstance(arg, CalBlockLib)]
        if local:
            self.add(LocalCal)
        if config is not None:
            self.load(config)

    def add(self, lib):
        """
        Adds a library to the index.

        Parameters:
        -----------
        lib : CalBlockLib
            A library to add to the library index.
        """
        self._libs.append(lib)

    def __len__(self):
        """
        Returns the total number of algorithms across all libraries in the index.

        Returns:
        --------
        int
            The total number of algorithms in the index.
        """
        return sum([len(_lib) for _lib in self._libs])

    def __repr__(self):
        """
        Returns a string representation of the CalLibIndex.

        Returns:
        --------
        str
            A string representation of the library index.
        """
        return f'< LibIndex[{len(self._libs)} libs] {len(self)} Algorithms >'

    def __getitem__(self, key):
        """
        Retrieves an algorithm by name, optionally filtering by source.

        Parameters:
        -----------
        key : str or tuple
            The name of the algorithm to retrieve. Can be a tuple containing the algorithm name 
            and a list of sources (optional).

        Returns:
        --------
        object
            The requested algorithm.

        Raises:
        -------
        TypeError
            If the key is not a string or tuple.
        IndexError
            If the algorithm is not found.
        """
        _sources = None
        if isinstance(key, tuple):
            _name = key[0]
            if len(key) > 1:
                _sources = key[1]
        elif isinstance(key, str):
            _name = key
        else:
            raise TypeError('Index type error.')

        if ':' in _name:
            _name, _sources = _name.split(':')

        if _sources is not None:
            if isinstance(_sources, str):
                _sources = [_source for _source in _sources.split(',') if len(_source) > 0]

        _blocks = [(_lib.source, _lib[_name]) for _lib in self._libs if _name in _lib]
        if len(_blocks) <= 0:
            raise IndexError(f'{_name} Not Found.')
        if _sources is None:
            return _blocks[0][1]
        for _source in _sources:
            for _block in _blocks:
                if _source == _block[0]:
                    return _block[1]
        raise IndexError(f'{_name} exists in {[_block[0] for _block in _blocks]}')

    def __contains__(self, name):
        """
        Checks if an algorithm exists in any of the libraries or specific sources.

        Parameters:
        -----------
        name : str
            The name of the algorithm to check.

        Returns:
        --------
        bool
            True if the algorithm exists, False otherwise.

        Raises:
        -------
        IndexError
            If the algorithm name or source is invalid.
        """
        if ':' in name:
            _name, _sources = name.split(':')
            _sources = [_source for _source in _sources.split(',') if len(_source) > 0]
            if len(_sources) <= 0:
                raise IndexError('Empty Source!')
            else:
                for _source in _sources:
                    for _lib in self._libs:
                        if _name in _lib and _lib.source == _source:
                            return True
                return False
        else:
            return any([name in _lib for _lib in self._libs])

    def _repr_markdown_(self):
        """
        Generates a markdown representation of the CalLibIndex, including details of the libraries.

        Returns:
        --------
        str
            A markdown formatted string representing the library index.
        """
        _doc = doc.Document(
            doc.Title('LibIndex', level=2),
            doc.Text(f'`{len(self._libs)} libs` `{len(self)} Algorithms`\n\n'),
            *[doc.Text(_lib._repr_markdown_() + '\n\n') for _lib in self._libs]
        )
        return _doc.markdown

    def load(self, config):
        """
        Loads the configuration for remote libraries from a file or list.

        Parameters:
        -----------
        config : str, list, or file-like object
            The configuration to load, either as a JSON file path or a list of configurations.

        Raises:
        -------
        KeyError
            If the required keys (`host`, `api_id`, `api_key`) are not found in the configuration.
        """
        if isinstance(config, str):
            with open(config, 'r') as f:
                _config = json.loads(f.read())
        elif isinstance(config, list):
            _config = config
        else:
            _config = json.loads(config.read())

        for item in _config:
            if 'host' not in item:
                raise KeyError('No host in the config')
            if 'api_id' not in item:
                item['api_id'] = os.environ.get('EASYAPI_ID')
                if item['api_id'] is None:
                    raise KeyError('API ID did not provide')
            if 'api_key' not in item:
                item['api_key'] = os.environ.get('EASYAPI_KEY')
                if item['api_key'] is None:
                    raise KeyError('API Key did not provide')
            self.add(RemoteCalBlockLib(**item))

    def save(self, path=None, save_credentials=False):
        """
        Saves the current library configurations to a file or returns them as a JSON string.

        Parameters:
        -----------
        path : str, optional
            The path to save the configuration file. If None, the configuration is returned as a string.
        save_credentials : bool, optional
            If True, saves credentials (API keys). Default is False.

        Returns:
        --------
        str
            The JSON string representation of the configuration, if `path` is None.

        Raises:
        -------
        UserWarning
            If `save_credentials` is True, a warning is raised about saving sensitive information.
        """
        if save_credentials:
            UserWarning('Save credentials is not safe!')
        _save_dict = []
        for _lib in self._libs:
            if isinstance(_lib, RemoteCalBlockLib):
                if save_credentials:
                    _save_dict.append({'host': _lib.client.host,
                                        'api_id': _lib.client.api_id,
                                        'api_key': _lib.client.api_key})
                else:
                    _save_dict.append({'host': _lib.client.host})
        _save = json.dumps(_save_dict)
        if path is None:
            return _save
        else:
            with open(path, 'w') as f:
                f.write(_save)
