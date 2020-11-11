from typing import List
from dataclasses import dataclass

__all__ = [
    'DeclOffset',
]

# ---------------------------------------------------------
# region CONSTANTS & ENUMS

# endregion (constants)
# ---------------------------------------------------------
# region FUNCTIONS

# endregion (functions)
# ---------------------------------------------------------
# region CLASSES


@dataclass
class DeclOffset:
    """Helpper class used to facilitate structuring of data"""

    index: int
    """Zero-based order of declaration."""

    size: int = 1
    """Size in bytes of the AstNode holding an instance of this object."""


class SourceCode:

    @classmethod
    def load(cls, filepath: str, *args, **kwargs) -> 'SourceCode':
        """Loads the source file contents."""
        with open(filepath, *args, **kwargs) as src:
            source: str = src.read()

        return cls(source, filepath)

    def __init__(self, source: str, filepath: str):
        self.source: str = source
        self.filepath: str = filepath

        # scanner markers
        self.index: int = 0
        self.line_index: int = 0
        self.newlines: List[int] = []


# endregion (classes)
# ---------------------------------------------------------
