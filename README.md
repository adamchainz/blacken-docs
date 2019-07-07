[![Build Status](https://travis-ci.org/asottile/blacken-docs.svg?branch=master)](https://travis-ci.org/asottile/blacken-docs)
[![Coverage Status](https://coveralls.io/repos/github/asottile/blacken-docs/badge.svg?branch=master)](https://coveralls.io/github/asottile/blacken-docs?branch=master)

blacken-docs
============

Run `black` on python code blocks in documentation files.

## install

`pip install blacken-docs`

## usage

`blacken-docs` provides a single executable (`blacken-docs`) which will modify
`.rst` / `.md` files in place.

It currently supports the following [`black`](https://github.com/ambv/black)
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

## usage with pre-commit

See [pre-commit](https://pre-commit.com) for instructions

Sample `.pre-commit-config.yaml`:


```yaml
-   repo: https://github.com/asottile/blacken-docs
    rev: v1.2.0
    hooks:
    -   id: blacken-docs
        additional_dependencies: [black==...]
```

Since `black` is currently a moving target, it is suggested to pin `black`
to a specific version using `additional_dependencies`.
