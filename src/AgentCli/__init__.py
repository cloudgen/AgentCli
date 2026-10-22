# Package public surface — requirement-python-packaging / requirement-python-coding-style
# Do not re-export undefined symbols from .cli.

__version__ = "1.2.0"

from .cli import main

__all__ = ["__version__", "main"]
