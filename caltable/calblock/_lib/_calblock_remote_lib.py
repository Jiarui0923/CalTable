"""
RemoteCalBlockLib Module
========================

This module defines a specialized `CalBlockLib` for managing remotely accessible CalBlock algorithms.
It integrates with the EasyAccess client to fetch and utilize remote algorithms.

Author: Jiarui Li
Email: jli78@tulane.edu
Affiliation: Computer Science Department, Tulane University
"""

from ._calblock_lib import CalBlockLib
from .._calblock_remote import CalBlockRemote
import docflow as doc
from easyaccess import EasyAccess


class RemoteCalBlockLib(CalBlockLib):
    """
    A library for managing remotely accessible CalBlock algorithms.
    """

    def __init__(self, client=None, host=None, api_id=None, api_key=None):
        """
        Initialize the RemoteCalBlockLib with an EasyAccess client.

        Args:
            client (EasyAccess, optional): The EasyAccess client to connect to the remote server. If None, a new client is created.
            host (str, optional): The host URL for the remote server.
            api_id (str, optional): The API ID for authentication.
            api_key (str, optional): The API key for authentication.
        """
        if client is None:
            client = EasyAccess(host=host, api_id=api_id, api_key=api_key)

        self.client = client
        _host = client._server_info
        self.host = _host

        _blocks = {algo_name: algorithm for algo_name, algorithm in client[client.algorithms].items()}
        super().__init__(source=_host, **_blocks)

    def __getitem__(self, name):
        """
        Retrieve a CalBlockRemote instance for the specified algorithm.

        Args:
            name (str): The name of the remote algorithm.

        Returns:
            function: A callable that creates a `CalBlockRemote` instance with the specified name.
        """
        return lambda **kwargs: CalBlockRemote(self._lib[name], **kwargs)

    def _repr_markdown_(self):
        """
        Generate a Markdown representation of the remote library.

        Returns:
            str: A Markdown-formatted string of the library's contents.
        """
        _doc = doc.Document(
            doc.Title(self.source, level=3),
            doc.Sequence({key: val.description for key, val in self._lib.items()})
        )
        return _doc.markdown
