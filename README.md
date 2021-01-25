[![Build Status](https://dev.azure.com/asottile/asottile/_apis/build/status/asottile.blacken-docs?branchName=master)](https://dev.azure.com/asottile/asottile/_build/latest?definitionId=36&branchName=master)
[![Azure DevOps coverage](https://img.shields.io/azure-devops/coverage/asottile/asottile/36/master.svg)](https://dev.azure.com/asottile/asottile/_build/latest?definitionId=36&branchName=master)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/asottile/blacken-docs/master.svg)](https://results.pre-commit.ci/latest/github/asottile/blacken-docs/master)

blacken-docs
============

Run `black` on python code blocks in documentation files.

## install

`pip install blacken-docs`

## usage

`blacken-docs` provides a single executable (`blacken-docs`) which will modify
`.rst` / `.md` / `.tex` files in place.

It currently supports the following [`black`](https://github.com/psf/black)
options:

- `-l` / `--line-length`
- `-t` / `--target-version`
- `-S` / `--skip-string-normalization`

Following additional parameters can be used:

 - `-E` / `--skip-errors`

`blacken-docs` will format code in the following block types:

(markdown)
```markdown
    ```python
    def hello():
        print("hello world")
    ```
```

(rst)
```rst
    .. code-block:: python

        def hello():
            print("hello world")
```

(rst `pycon`)
```rst
    .. code-block:: pycon

        >>> def hello():
        ...     print("hello world")
        ...
```

(latex)
```latex
\begin{minted}{python}
def hello():
    print("hello world")
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
-   repo: https://github.com/asottile/blacken-docs
    rev: v1.9.2
    hooks:
    -   id: blacken-docs
        additional_dependencies: [black==...]
```

Since `black` is currently a moving target, it is suggested to pin `black`
to a specific version using `additional_dependencies`.
