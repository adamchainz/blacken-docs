[![Build Status](https://travis-ci.org/asottile/blacken-docs.svg?branch=master)](https://travis-ci.org/asottile/blacken-docs)
[![Coverage Status](https://coveralls.io/repos/github/asottile/blacken-docs/badge.svg?branch=master)](https://coveralls.io/github/asottile/blacken-docs?branch=master)

blacken-docs
============

Run `black` on python code blocks in documentation files.

## install

`pip install blacken-docs`

## usage

TODO

## usage with pre-commit

This works especially well when integrated with [`pre-commit`][pre-commit].


```yaml
-   repo: https://github.com/asottile/blacken-docs
    rev: v0.0.0
    hooks:
    -   id: blacken-markdown
    -   id: blacken-rst
```

### supported [`black`](https://github.com/ambv/black) options

Currently the following black options are supported:

- `--line-length`
- `--py36`
- `-S` / `--skip-string-normalization`
