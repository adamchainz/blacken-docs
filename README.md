[![Build Status](https://dev.azure.com/asottile/asottile/_apis/build/status/asottile.blacken-docs?branchName=main)](https://dev.azure.com/asottile/asottile/_build/latest?definitionId=36&branchName=main)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/asottile/blacken-docs/main.svg)](https://results.pre-commit.ci/latest/github/asottile/blacken-docs/main)

blacken-docs
============

Run `black` on python code blocks in documentation files.

## install

```bash
pip install blacken-docs
```

## usage

`blacken-docs` provides a single executable (`blacken-docs`) which will modify
`.rst` / `.md` / `.tex` files in place.

If a file is modified, `blacken-docs` exits nonzero.

It currently supports the following [`black`](https://github.com/psf/black)
options:

- `-l` / `--line-length`
- `-t` / `--target-version`
- `-S` / `--skip-string-normalization`

Following additional parameters can be used:

 - `-E` / `--skip-errors`
 - `--rst-literal-blocks`

`blacken-docs` will format code in the following block types:

(markdown)
```markdown
    ```python
    def hello():
        print("hello world")
    ```
```

(markdown `pycon`)
```markdown
    ```pycon

    >>> def hello():
    ...     print("hello world")
    ...

    ```
```

(rst)
```rst
    .. code-block:: python

        def hello():
            print("hello world")
```

This style is enabled with the `--use-sphinx-default` option.

(rst `pycon`)
```rst
    .. code-block:: pycon

        >>> def hello():
        ...     print("hello world")
        ...
```

(rst literal blocks - activated with ``--rst-literal-blocks``)

reStructuredText [literal blocks](https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#literal-blocks) are marked with `::` and can be any monospaced text by default.
However Sphinx interprets them as Python code [by default](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html#rst-literal-blocks).
If your project uses Sphinx and such a configuration, add `--rst-literal-blocks` to also format such blocks.

``rst
    An example::

        def hello():
            print("hello world")
```

(latex)
```latex
\begin{minted}{python}
def hello():
    print("hello world")
\end{minted}
```

(latex `pycon`)
```latex
\begin{minted}{pycon}
>>> def hello():
...     print("hello world")
...
\end{minted}
```

(latex with pythontex)
```latex
\begin{pycode}
def hello():
    print("hello world")
\end{pycode}
```

(markdown/rst in python docstrings)
```python
def f():
    """docstring here

    .. code-block:: python

        print("hello world")

    ```python
    print("hello world")
    ```
    """
```

## usage with pre-commit

See [pre-commit](https://pre-commit.com) for instructions

Sample `.pre-commit-config.yaml`:


```yaml
-   repo: https://github.com/adamchainz/blacken-docs
    rev: v1.12.1
    hooks:
    -   id: blacken-docs
        additional_dependencies: [black==...]
```

Since `black` is currently a moving target, it is suggested to pin `black`
to a specific version using `additional_dependencies`.
