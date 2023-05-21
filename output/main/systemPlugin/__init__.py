"""
$SystemPlugin

Import all the sytem plugin files. You can import a unique package, for that use::
>>> from systemPlugin import module
"""


__all__ = ["log"]

from .log import Log, ReadLog, ClearLog
