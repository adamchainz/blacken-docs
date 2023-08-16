from __future__ import annotations

from textwrap import dedent

import black
from black.const import DEFAULT_LINE_LENGTH

import blacken_docs
from blacken_docs import __main__  # noqa: F401


BLACK_MODE = black.FileMode(line_length=DEFAULT_LINE_LENGTH)


def test_format_src_trivial():
    after, _ = blacken_docs.format_str("", BLACK_MODE)
    assert after == ""


def test_format_src_markdown_simple():
    before = dedent(
        """\
        ```python
        f(1,2,3)
        ```
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == dedent(
        """\
        ```python
        f(1, 2, 3)
        ```
        """
    )


def test_format_src_markdown_leading_whitespace():
    before = dedent(
        """\
        ```   python
        f(1,2,3)
        ```
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == dedent(
        """\
        ```   python
        f(1, 2, 3)
        ```
        """
    )


def test_format_src_markdown_short_name():
    before = dedent(
        """\
        ```   py
        f(1,2,3)
        ```
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == dedent(
        """\
        ```   py
        f(1, 2, 3)
        ```
        """
    )


def test_format_src_markdown_options():
    before = dedent(
        """\
        ```python title='example.py'
        f(1,2,3)
        ```
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == dedent(
        """\
        ```python title='example.py'
        f(1, 2, 3)
        ```
        """
    )


def test_format_src_markdown_trailing_whitespace():
    before = dedent(
        """\
        ```python
        f(1,2,3)
        ```    \n"""
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == dedent(
        """\
        ```python
        f(1, 2, 3)
        ```    \n"""
    )


def test_format_src_indented_markdown():
    before = dedent(
        """\
        - do this pls:
          ```python
          f(1,2,3)
          ```
        - also this
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == dedent(
        """\
        - do this pls:
          ```python
          f(1, 2, 3)
          ```
        - also this
        """
    )


def test_format_src_markdown_pycon():
    before = (
        "hello\n"
        "\n"
        "```pycon\n"
        "\n"
        "    >>> f(1,2,3)\n"
        "    output\n"
        "```\n"
        "world\n"
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == (
        "hello\n" "\n" "```pycon\n" "\n" ">>> f(1, 2, 3)\n" "output\n" "```\n" "world\n"
    )


def test_format_src_markdown_pycon_options():
    before = (
        "hello\n"
        "\n"
        "```pycon title='Session 1'\n"
        "\n"
        "    >>> f(1,2,3)\n"
        "    output\n"
        "```\n"
        "world\n"
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == (
        "hello\n"
        "\n"
        "```pycon title='Session 1'\n"
        "\n"
        ">>> f(1, 2, 3)\n"
        "output\n"
        "```\n"
        "world\n"
    )


def test_format_src_latex_minted():
    before = (
        "hello\n" "\\begin{minted}{python}\n" "f(1,2,3)\n" "\\end{minted}\n" "world!"
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == (
        "hello\n" "\\begin{minted}{python}\n" "f(1, 2, 3)\n" "\\end{minted}\n" "world!"
    )


def test_format_src_latex_minted_indented():
    # Personaly I would have minted python code all flush left,
    # with only the Python code's own four space indentation:
    before = (
        "hello\n"
        "  \\begin{minted}{python}\n"
        "    if True:\n"
        "      f(1,2,3)\n"
        "  \\end{minted}\n"
        "world!"
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == (
        "hello\n"
        "  \\begin{minted}{python}\n"
        "  if True:\n"
        "      f(1, 2, 3)\n"
        "  \\end{minted}\n"
        "world!"
    )


def test_format_src_latex_minted_pycon():
    before = (
        "Preceeding text\n"
        "\\begin{minted}{pycon}\n"
        ">>> print( 'Hello World' )\n"
        "Hello World\n"
        "\\end{minted}\n"
        "Following text."
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == (
        "Preceeding text\n"
        "\\begin{minted}{pycon}\n"
        '>>> print("Hello World")\n'
        "Hello World\n"
        "\\end{minted}\n"
        "Following text."
    )


def test_format_src_latex_minted_pycon_indented():
    # Nicer style to put the \begin and \end on new lines,
    # but not actually required for the begin line
    before = (
        "Preceeding text\n"
        "  \\begin{minted}{pycon}\n"
        "    >>> print( 'Hello World' )\n"
        "    Hello World\n"
        "  \\end{minted}\n"
        "Following text."
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == (
        "Preceeding text\n"
        "  \\begin{minted}{pycon}\n"
        '  >>> print("Hello World")\n'
        "  Hello World\n"
        "  \\end{minted}\n"
        "Following text."
    )


def test_src_pythontex():
    before = "hello\n" "\\begin{pyblock}\n" "f(1,2,3)\n" "\\end{pyblock}\n" "world!"
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == (
        "hello\n" "\\begin{pyblock}\n" "f(1, 2, 3)\n" "\\end{pyblock}\n" "world!"
    )


def test_format_src_rst():
    before = (
        "hello\n" "\n" ".. code-block:: python\n" "\n" "    f(1,2,3)\n" "\n" "world\n"
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == (
        "hello\n" "\n" ".. code-block:: python\n" "\n" "    f(1, 2, 3)\n" "\n" "world\n"
    )


def test_format_src_rst_literal_blocks():
    before = "hello::\n" "\n" "    f(1,2,3)\n" "\n" "world\n"
    after, _ = blacken_docs.format_str(
        before,
        BLACK_MODE,
        rst_literal_blocks=True,
    )
    assert after == ("hello::\n" "\n" "    f(1, 2, 3)\n" "\n" "world\n")


def test_format_src_rst_literal_blocks_nested():
    before = dedent(
        """
        * hello

          .. warning::

            don't hello too much
        """,
    )
    after, errors = blacken_docs.format_str(
        before,
        BLACK_MODE,
        rst_literal_blocks=True,
    )
    assert after == before
    assert errors == []


def test_format_src_rst_literal_blocks_empty():
    before = dedent(
        """
        Example::

        .. warning::

            There was no example.
        """,
    )
    after, errors = blacken_docs.format_str(
        before,
        BLACK_MODE,
        rst_literal_blocks=True,
    )
    assert after == before
    assert errors == []


def test_format_src_rst_sphinx_doctest():
    before = (
        ".. testsetup:: group1\n"
        "\n"
        "   import parrot  \n"
        "   mock = SomeMock( )\n"
        "\n"
        ".. testcleanup:: group1\n"
        "\n"
        "   mock.stop( )\n"
        "\n"
        ".. doctest:: group1\n"
        "\n"
        "   >>> parrot.voom( 3000 )\n"
        "   This parrot wouldn't voom if you put 3000 volts through it!\n"
        "\n"
        ".. testcode::\n"
        "\n"
        "   parrot.voom( 3000 )\n"
        "\n"
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == (
        ".. testsetup:: group1\n"
        "\n"
        "   import parrot\n"
        "\n"
        "   mock = SomeMock()\n"
        "\n"
        ".. testcleanup:: group1\n"
        "\n"
        "   mock.stop()\n"
        "\n"
        ".. doctest:: group1\n"
        "\n"
        "   >>> parrot.voom(3000)\n"
        "   This parrot wouldn't voom if you put 3000 volts through it!\n"
        "\n"
        ".. testcode::\n"
        "\n"
        "   parrot.voom(3000)\n"
        "\n"
    )


def test_format_src_rst_indented():
    before = (
        ".. versionadded:: 3.1\n"
        "\n"
        "    hello\n"
        "\n"
        "    .. code-block:: python\n"
        "\n"
        "        def hi():\n"
        "            f(1,2,3)\n"
        "\n"
        "    world\n"
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == (
        ".. versionadded:: 3.1\n"
        "\n"
        "    hello\n"
        "\n"
        "    .. code-block:: python\n"
        "\n"
        "        def hi():\n"
        "            f(1, 2, 3)\n"
        "\n"
        "    world\n"
    )


def test_format_src_rst_code_block_indent():
    before = "\n".join(
        [
            ".. code-block:: python",
            "   ",
            "   f(1,2,3)\n",
        ]
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == "\n".join(
        [
            ".. code-block:: python",
            "   ",
            "   f(1, 2, 3)\n",
        ]
    )


def test_format_src_rst_with_highlight_directives():
    before = (
        ".. code-block:: python\n"
        "    :lineno-start: 10\n"
        "    :emphasize-lines: 11\n"
        "\n"
        "    def foo():\n"
        "        bar(1,2,3)\n"
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == (
        ".. code-block:: python\n"
        "    :lineno-start: 10\n"
        "    :emphasize-lines: 11\n"
        "\n"
        "    def foo():\n"
        "        bar(1, 2, 3)\n"
    )


def test_format_src_rst_python_inside_non_python_code_block():
    before = (
        "blacken-docs does changes like:\n"
        "\n"
        ".. code-block:: diff\n"
        "\n"
        "     .. code-block:: python\n"
        "\n"
        "    -    'Hello World'\n"
        '    +    "Hello World"\n'
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == before


def test_integration_ok(tmp_path, capsys):
    f = tmp_path / "f.md"
    f.write_text(
        "```python\n" "f(1, 2, 3)\n" "```\n",
    )

    result = blacken_docs.main((str(f),))

    assert result == 0
    assert not capsys.readouterr()[1]
    assert f.read_text() == ("```python\n" "f(1, 2, 3)\n" "```\n")


def test_integration_modifies(tmp_path, capsys):
    f = tmp_path / "f.md"
    f.write_text(
        "```python\n" "f(1,2,3)\n" "```\n",
    )

    result = blacken_docs.main((str(f),))

    assert result == 1
    out, _ = capsys.readouterr()
    assert out == f"{f}: Rewriting...\n"
    assert f.read_text() == ("```python\n" "f(1, 2, 3)\n" "```\n")


def test_integration_line_length(tmp_path):
    f = tmp_path / "f.md"
    f.write_text(
        "```python\n"
        "foo(very_very_very_very_very_very_very, long_long_long_long_long)\n"
        "```\n",
    )

    result = blacken_docs.main((str(f), "--line-length=80"))
    assert result == 0

    result2 = blacken_docs.main((str(f), "--line-length=50"))
    assert result2 == 1
    assert f.read_text() == (
        "```python\n"
        "foo(\n"
        "    very_very_very_very_very_very_very,\n"
        "    long_long_long_long_long,\n"
        ")\n"
        "```\n"
    )


def test_integration_preview(tmp_path):
    f = tmp_path / "f.md"
    f.write_text(
        dedent(
            """\
            ```python
            x = 'a' 'b'
            ```
            """
        )
    )

    result = blacken_docs.main((str(f), "--preview"))

    assert result == 1
    assert f.read_text() == dedent(
        """\
        ```python
        x = "ab"
        ```
        """
    )


def test_integration_py36(tmp_path):
    f = tmp_path / "f.md"
    f.write_text(
        "```python\n"
        "def very_very_long_function_name(\n"
        "    very_very_very_very_very_very,\n"
        "    very_very_very_very_very_very,\n"
        "    *long_long_long_long_long_long\n"
        "):\n"
        "    pass\n"
        "```\n",
    )

    result = blacken_docs.main((str(f),))
    assert result == 0

    result2 = blacken_docs.main((str(f), "--target-version=py36"))

    assert result2 == 1
    assert f.read_text() == (
        "```python\n"
        "def very_very_long_function_name(\n"
        "    very_very_very_very_very_very,\n"
        "    very_very_very_very_very_very,\n"
        "    *long_long_long_long_long_long,\n"
        "):\n"
        "    pass\n"
        "```\n"
    )


def test_integration_filename_last(tmp_path):
    f = tmp_path / "f.md"
    f.write_text(
        "```python\n"
        "def very_very_long_function_name(\n"
        "    very_very_very_very_very_very,\n"
        "    very_very_very_very_very_very,\n"
        "    *long_long_long_long_long_long\n"
        "):\n"
        "    pass\n"
        "```\n",
    )

    result = blacken_docs.main((str(f),))
    assert result == 0

    result2 = blacken_docs.main(("--target-version", "py36", str(f)))

    assert result2 == 1
    assert f.read_text() == (
        "```python\n"
        "def very_very_long_function_name(\n"
        "    very_very_very_very_very_very,\n"
        "    very_very_very_very_very_very,\n"
        "    *long_long_long_long_long_long,\n"
        "):\n"
        "    pass\n"
        "```\n"
    )


def test_integration_multiple_target_version(tmp_path):
    f = tmp_path / "f.md"
    f.write_text(
        "```python\n"
        "def very_very_long_function_name(\n"
        "    very_very_very_very_very_very,\n"
        "    very_very_very_very_very_very,\n"
        "    *long_long_long_long_long_long\n"
        "):\n"
        "    pass\n"
        "```\n",
    )

    result = blacken_docs.main((str(f),))
    assert result == 0

    result2 = blacken_docs.main(
        ("--target-version", "py35", "--target-version", "py36", str(f)),
    )
    assert result2 == 0


def test_integration_skip_string_normalization(tmp_path):
    f = tmp_path / "f.md"
    f.write_text(
        "```python\n" "f('hi')\n" "```\n",
    )

    result = blacken_docs.main((str(f), "--skip-string-normalization"))

    assert result == 0
    assert f.read_text() == ("```python\n" "f('hi')\n" "```\n")


def test_integration_syntax_error(tmp_path, capsys):
    f = tmp_path / "f.md"
    f.write_text(
        "```python\n" "f(\n" "```\n",
    )

    result = blacken_docs.main((str(f),))

    assert result == 2
    out, _ = capsys.readouterr()
    assert out.startswith(f"{f}:1: code block parse error")
    assert f.read_text() == ("```python\n" "f(\n" "```\n")


def test_integration_ignored_syntax_error(tmp_path, capsys):
    f = tmp_path / "f.md"
    f.write_text(
        "```python\n" "f( )\n" "```\n" "\n" "```python\n" "f(\n" "```\n",
    )

    result = blacken_docs.main((str(f), "--skip-errors"))

    assert result == 1
    out, _ = capsys.readouterr()
    assert f.read_text() == (
        "```python\n" "f()\n" "```\n" "\n" "```python\n" "f(\n" "```\n"
    )


def test_format_src_rst_jupyter_sphinx():
    before = (
        "hello\n" "\n" ".. jupyter-execute::\n" "\n" "    f(1,2,3)\n" "\n" "world\n"
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == (
        "hello\n" "\n" ".. jupyter-execute::\n" "\n" "    f(1, 2, 3)\n" "\n" "world\n"
    )


def test_format_src_rst_jupyter_sphinx_with_directive():
    before = (
        "hello\n"
        "\n"
        ".. jupyter-execute::\n"
        "    :hide-code:\n"
        "\n"
        "    f(1,2,3)\n"
        "\n"
        "world\n"
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == (
        "hello\n"
        "\n"
        ".. jupyter-execute::\n"
        "    :hide-code:\n"
        "\n"
        "    f(1, 2, 3)\n"
        "\n"
        "world\n"
    )


def test_works_on_python_docstrings():
    before = '''\
def f():
    """hello world

    .. code-block:: python

        f(1,2,3)

    ```python
    f(1,2,3)
    ```
    """
'''
    expected = '''\
def f():
    """hello world

    .. code-block:: python

        f(1, 2, 3)

    ```python
    f(1, 2, 3)
    ```
    """
'''
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == expected


def test_format_src_rst_pycon():
    before = (
        "hello\n"
        "\n"
        ".. code-block:: pycon\n"
        "\n"
        "    >>> f(1,2,3)\n"
        "    output\n"
        "\n"
        "world\n"
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == (
        "hello\n"
        "\n"
        ".. code-block:: pycon\n"
        "\n"
        "    >>> f(1, 2, 3)\n"
        "    output\n"
        "\n"
        "world\n"
    )


def test_format_src_rst_pycon_with_contiuation():
    before = (
        ".. code-block:: pycon\n"
        "\n"
        "    >>> d = {\n"
        '    ...   "a": 1,\n'
        '    ...   "b": 2,\n'
        '    ...   "c": 3,}\n'
        "\n"
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == (
        ".. code-block:: pycon\n"
        "\n"
        "    >>> d = {\n"
        '    ...     "a": 1,\n'
        '    ...     "b": 2,\n'
        '    ...     "c": 3,\n'
        "    ... }\n"
        "\n"
    )


def test_format_src_rst_pycon_adds_contiuation():
    before = ".. code-block:: pycon\n" "\n" '    >>> d = {"a": 1,"b": 2,"c": 3,}\n' "\n"
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == (
        ".. code-block:: pycon\n"
        "\n"
        "    >>> d = {\n"
        '    ...     "a": 1,\n'
        '    ...     "b": 2,\n'
        '    ...     "c": 3,\n'
        "    ... }\n"
        "\n"
    )


def test_format_src_rst_pycon_preserves_trailing_whitespace():
    before = (
        "hello\n"
        "\n"
        ".. code-block:: pycon\n"
        "\n"
        '    >>> d = {"a": 1, "b": 2, "c": 3}\n'
        "\n"
        "\n"
        "\n"
        "world\n"
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == before


def test_format_src_rst_pycon_indented():
    before = (
        ".. versionadded:: 3.1\n"
        "\n"
        "    hello\n"
        "\n"
        "    .. code-block:: pycon\n"
        "\n"
        "        >>> def hi():\n"
        "        ...     f(1,2,3)\n"
        "        ...\n"
        "\n"
        "    world\n"
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == (
        ".. versionadded:: 3.1\n"
        "\n"
        "    hello\n"
        "\n"
        "    .. code-block:: pycon\n"
        "\n"
        "        >>> def hi():\n"
        "        ...     f(1, 2, 3)\n"
        "        ...\n"
        "\n"
        "    world\n"
    )


def test_format_src_rst_pycon_code_block_is_final_line1():
    before = (
        ".. code-block:: pycon\n"
        "\n"
        "    >>> if True:\n"
        "    ...   pass\n"
        "    ...\n"
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == (
        ".. code-block:: pycon\n"
        "\n"
        "    >>> if True:\n"
        "    ...     pass\n"
        "    ...\n"
    )


def test_format_src_rst_pycon_code_block_is_final_line2():
    before = ".. code-block:: pycon\n" "\n" "    >>> if True:\n" "    ...   pass\n"
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == (
        ".. code-block:: pycon\n"
        "\n"
        "    >>> if True:\n"
        "    ...     pass\n"
        "    ...\n"
    )


def test_format_src_rst_pycon_nested_def1():
    before = (
        ".. code-block:: pycon\n"
        "\n"
        "    >>> if True:\n"
        "    ...     def f(): pass\n"
        "    ...\n"
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == (
        ".. code-block:: pycon\n"
        "\n"
        "    >>> if True:\n"
        "    ...     def f():\n"
        "    ...         pass\n"
        "    ...\n"
    )


def test_format_src_rst_pycon_nested_def2():
    before = (
        ".. code-block:: pycon\n"
        "\n"
        "    >>> if True:\n"
        "    ...     def f(): pass\n"
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == (
        ".. code-block:: pycon\n"
        "\n"
        "    >>> if True:\n"
        "    ...     def f():\n"
        "    ...         pass\n"
        "    ...\n"
    )


def test_format_src_rst_pycon_empty_line():
    before = (
        ".. code-block:: pycon\n"
        "\n"
        "    >>> l = [\n"
        "    ...\n"
        "    ...     1,\n"
        "    ... ]\n"
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == (
        ".. code-block:: pycon\n"
        "\n"
        "    >>> l = [\n"
        "    ...     1,\n"
        "    ... ]\n"
    )


def test_format_src_rst_pycon_preserves_output_indentation():
    before = (
        ".. code-block:: pycon\n"
        "\n"
        "    >>> 1 / 0\n"
        "    Traceback (most recent call last):\n"
        '      File "<stdin>", line 1, in <module>\n'
        "    ZeroDivisionError: division by zero\n"
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == before


def test_format_src_rst_pycon_elided_traceback():
    before = (
        ".. code-block:: pycon\n"
        "\n"
        "    >>> 1 / 0\n"
        "    Traceback (most recent call last):\n"
        "      ...\n"
        "    ZeroDivisionError: division by zero\n"
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == before


def test_format_src_rst_pycon_no_prompt():
    before = ".. code-block:: pycon\n" "\n" "    pass\n"
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == before


def test_format_src_rst_pycon_no_trailing_newline():
    before = ".. code-block:: pycon\n" "\n" "    >>> pass"
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == (".. code-block:: pycon\n" "\n" "    >>> pass\n")


def test_format_src_rst_pycon_comment_before_promopt():
    before = (
        ".. code-block:: pycon\n"
        "\n"
        "    # Comment about next line\n"
        "    >>> pass\n"
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == (
        ".. code-block:: pycon\n"
        "\n"
        "    # Comment about next line\n"
        "    >>> pass\n"
    )
