"""
CalBlockRemote Module
=====================

This module extends the `CalBlock` functionality to integrate with remote algorithms, 
allowing computation to be offloaded to a remote server. It wraps around a 
`remote_algorithm` and seamlessly maps its inputs and outputs for use with the `CalBlock` API.

Author: Jiarui Li
Email: jli78@tulane.edu
Affiliation: Computer Science Department, Tulane University
"""

from ._calblock import CalBlock


class CalBlockRemote(CalBlock):
    """
    A subclass of CalBlock for interfacing with remote algorithms.
    """

    def __init__(self, remote_algorithm, **kwargs):
        """
        Initialize the CalBlockRemote instance.

        Args:
            remote_algorithm: The remote algorithm object providing inputs, outputs, and description.
            **kwargs: Additional keyword arguments for column mapping.
        """
        self.remote_algorithm = remote_algorithm
        super().__init__(
            name=remote_algorithm.name,
            host=remote_algorithm._client._server_info,
            inputs=remote_algorithm.inputs,
            outputs=remote_algorithm.outputs,
            desc=remote_algorithm.description,
            **kwargs
        )

    def __repr__(self):
        """
        String representation of the CalBlockRemote instance.

        Returns:
            str: The representation string.
        """
        return f'<{self.host}[REMOTE]: {self.name}>'

    def forward(self, **inputs):
        """
        Execute the remote algorithm with the given inputs.

        Args:
            **inputs: Input parameters for the remote algorithm.

        Returns:
            dict: Output parameters returned by the remote algorithm.
        """
        return self.remote_algorithm(**inputs)
