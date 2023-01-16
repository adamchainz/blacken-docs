============
blacken-docs
============

.. image:: https://img.shields.io/github/actions/workflow/status/adamchainz/blacken-docs/main.yml?branch=main&style=for-the-badge
   :target: https://github.com/adamchainz/blacken-docs/actions?workflow=CI

.. image:: https://img.shields.io/badge/Coverage-100%25-success?style=for-the-badge
  :target: https://github.com/adamchainz/blacken-docs/actions?workflow=CI

.. image:: https://img.shields.io/pypi/v/blacken-docs.svg?style=for-the-badge
   :target: https://pypi.org/project/blacken-docs/

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge
   :target: https://github.com/psf/black

.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=for-the-badge
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit

Run `Black <https://pypi.org/project/black/>`__ on Python code blocks in documentation files.

Installation
============

Use **pip**:

.. code-block:: sh

    python -m pip install blacken-docs

Python 3.7 to 3.11 supported.

Black 22.1.0+ supported.

pre-commit hook
---------------

You can also install blacken-docs as a `pre-commit <https://pre-commit.com/>`__ hook.
Add the following to the ``repos`` section of your ``.pre-commit-config.yaml`` file (`docs <https://pre-commit.com/#plugins>`__):

.. code-block:: yaml

    -   repo: https://github.com/adamchainz/blacken-docs
        rev: ""  # replace with latest tag on GitHub
        hooks:
        -   id: blacken-docs
            additional_dependencies:
            - black==22.12.0

Then, reformat your entire project:

.. code-block:: sh

    pre-commit run blacken-docs --all-files

Since Black is a moving target, it’s best to pin it in ``additional_dependencies``.
Upgrade as appropriate.

Usage
=====

blacken-docs is a commandline tool that rewrites documentation files in place.
It supports Markdown, reStructuredText, and LaTex files.
Additionally, you can run it on Python files to reformat Markdown and reStructuredText within docstrings.

Run ``blacken-docs`` with the filenames to rewrite:

.. code-block:: sh

    blacken-docs README.rst

If any file is modified, ``blacken-docs`` exits nonzero.

blacken-docs currently passes the following options through to Black:

* ``-l`` / ``--line-length``
* ``-t`` / ``--target-version``
* ``-S`` / ``--skip-string-normalization``

It also has the below extra options:

* ``-E`` / ``--skip-errors`` - Don’t exit non-zero for errors from Black (normally syntax errors).
* ``--rst-literal-blocks`` - Also format literal blocks in reStructuredText files (more below).

History
=======

blacken-docs was created by `Anthony Sottile <https://github.com/asottile/>`__ in 2018.
At the end of 2022, Adam Johnson took over maintenance.

Supported code block formats
============================

blacken-docs formats code blocks matching the following patterns.

Markdown
--------

In “python” blocks:

.. code-block:: markdown

    ```python
    def hello():
        print("hello world")
    ```

And “pycon” blocks:

.. code-block:: markdown

    ```pycon

    >>> def hello():
    ...     print("hello world")
    ...

    ```

Within Python files, docstrings that contain Markdown code blocks may be reformatted:

.. code-block:: python

    def f():
        """docstring here

        ```python
        print("hello world")
        ```
        """

reStructuredText
----------------

In “python” blocks:

.. code-block:: rst

    .. code-block:: python

        def hello():
            print("hello world")

In “pycon” blocks:

.. code-block:: rst

    .. code-block:: pycon

        >>> def hello():
        ...     print("hello world")
        ...

Use ``--rst-literal-blocks`` to also format `literal blocks <https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#literal-blocks>`__:

.. code-block:: rst

    An example::

        def hello():
            print("hello world")

Literal blocks are marked with ``::`` and can be any monospaced text by default.
However Sphinx interprets them as Python code `by default <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html#rst-literal-blocks>`__.
If your project uses Sphinx and such a configuration, add ``--rst-literal-blocks`` to also format such blocks.

Within Python files, docstrings that contain reStructuredText code blocks may be reformatted:

.. code-block:: python

    def f():
        """docstring here

        .. code-block:: python

            print("hello world")
        """

LaTeX
-----

In minted “python” blocks:

.. code-block:: latex

    \begin{minted}{python}
    def hello():
        print("hello world")
    \end{minted}

In minted “pycon” blocks:

.. code-block:: latex

    \begin{minted}{pycon}
    >>> def hello():
    ...     print("hello world")
    ...
    \end{minted}

In PythonTeX blocks:

.. code-block:: latex

    \begin{pycode}
    def hello():
        print("hello world")
    \end{pycode}
