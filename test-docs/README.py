"""
Use this document to test `blacken-docs` for Python extension types.

## Testing

To run, use the following command:

```bash
python3 blacken_docs.py test-docs/README.py
```

This command does the following:

- `blacken_docs.py` runs the script and passes the file name.
- The file is formatted and saved to the same directory.
"""
from __future__ import annotations


def f():
    """docstring here

    .. code-block:: python

        print( f"hello world")

    ```python
    print( f"hello world")
    ```
    """
    print(f'hello world')


f()
