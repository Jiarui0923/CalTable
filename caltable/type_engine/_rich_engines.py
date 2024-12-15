"""
StringTypeEngine and Data Representation Classes
=================================================

This module defines several classes for handling different types of data representations, such as string-based tables
and JSON objects. It also includes functionality to format these representations as markdown, HTML, and other formats
for improved visualization.

Author: Jiarui Li  
Email: jli78@tulane.edu  
Affiliation: Computer Science Department, Tulane University
"""

import re
import json
import pandas as pd
from tabulate import tabulate
from .._data_unit import DataUnit
from ._meta_engines import StringTypeEngine
from ._file import FileUnit


class StringTableTypeEngine(StringTypeEngine):
    """
    A type engine for handling string-based tables. This class formats a string value as a table, splitting it based
    on a specified separator and line ending.

    Attributes:
        sep (str): The separator used to split the string into table columns (default is a space).
        end (str): The line ending used to split the string into rows (default is a newline).
        table_value (list): The parsed table as a list of rows and columns.
    """
    
    def __init__(self, value, iotype, sep=' ', end='\n'):
        """
        Initializes the StringTableTypeEngine with the string value, iotype, separator, and line-ending characters.

        Args:
            value (str): The string value to process.
            iotype: The type of the value, used for metadata.
            sep (str): The separator to use between columns (default is space).
            end (str): The line-ending character (default is newline).
        """
        super().__init__(value=value, iotype=iotype)
        self.sep, self.end = sep, end
        self.table_value = self._build_table(value, sep=sep, end=end)
    
    def _build_table(self, value, sep=' ', end='\n'):
        """
        Parses the string into a table by splitting based on the separator and line-ending characters.

        Args:
            value (str): The string value to split into a table.
            sep (str): The separator used to split columns (default is space).
            end (str): The line-ending character used to split rows (default is newline).

        Returns:
            list: The parsed table as a list of rows, each containing columns.
        """
        return [re.split(sep, line) for line in re.split(end, value) if len(line) > 0]
    
    def __len__(self):
        """
        Returns the number of rows in the table.

        Returns:
            int: The number of rows in the table.
        """
        return len(self.table_value)
    
    def __repr__(self):
        """
        Provides a string representation of the table using the `tabulate` library.

        Returns:
            str: The tabulated string representation of the table.
        """
        return tabulate(self.table_value)
    
    def _repr_markdown_(self):
        """
        Returns the table in HTML format using Pandas DataFrame.

        Returns:
            str: The HTML representation of the table.
        """
        return pd.DataFrame(self.table_value)._repr_html_()


@DataUnit.register(['json'])
class StringJSONTypeEngine(StringTypeEngine):
    """
    A type engine for handling JSON strings. It parses the string as a JSON object, formats it for readability,
    and allows for rendering the JSON as HTML.

    Attributes:
        value (str): The JSON string value, formatted with indentation for readability.
    """
    
    def __init__(self, value, iotype):
        """
        Initializes the StringJSONTypeEngine by parsing and formatting the JSON string.

        Args:
            value (str): The JSON string to process.
            iotype: The type of the value, used for metadata.
        """
        super().__init__(value=json.dumps(json.loads(value), indent=2), iotype=iotype)
    
    def _template_fold(self, title, data):
        """
        Creates an HTML `<details>` element for a foldable section of the JSON.

        Args:
            title (str): The title for the foldable section.
            data (str): The content to be displayed inside the fold.

        Returns:
            str: The HTML representation of the foldable section.
        """
        return f'<details><summary><b>{title}</b></summary><div style="margin-left:1em;">{data}</div></details>'
    
    def _template_row(self, title, data):
        """
        Creates an HTML row with the title and value for a specific key-value pair in the JSON.

        Args:
            title (str): The key in the JSON.
            data (str): The corresponding value.

        Returns:
            str: The HTML row representation of the key-value pair.
        """
        return f'<b>{title}</b>: {data}<br>'
    
    def _render_json(self, obj):
        """
        Recursively renders the JSON object as HTML.

        Args:
            obj (dict): The JSON object to render.

        Returns:
            str: The HTML representation of the JSON object.
        """
        content = ""
        for key, val in obj.items():
            if isinstance(val, dict): 
                content += self._template_fold(key, self._render_json(val))
            elif isinstance(val, (list, tuple)): 
                content += self._template_fold(key, self._render_json(dict(enumerate(val))))
            else: 
                content += self._template_row(key, val)
        return content
    
    def __len__(self):
        """
        Returns the length of the JSON string.

        Returns:
            int: The length of the JSON string.
        """
        return len(self.value)
    
    def __repr__(self):
        """
        Provides a string representation of the JSON.

        Returns:
            str: The formatted JSON string.
        """
        return self.value
    
    def _repr_markdown_(self):
        """
        Renders the JSON as markdown-compatible HTML.

        Returns:
            str: The HTML representation of the JSON for markdown.
        """
        return self._render_json(json.loads(self.value))
    
    def view_html(self, **kwargs):
        """
        Renders the JSON as HTML.

        Args:
            **kwargs: Additional keyword arguments for customization.

        Returns:
            str: The HTML representation of the JSON.
        """
        return self._render_json(json.loads(self.value))
    
    def file(self, name=None, ext='json'):
        """
        Saves the JSON data as a file.

        Args:
            name (str): The name of the file (default is None).
            ext (str): The file extension (default is 'json').

        Returns:
            FileUnit: A FileUnit object containing the JSON data.
        """
        return FileUnit(data=self.value, name=name, ext=ext)
