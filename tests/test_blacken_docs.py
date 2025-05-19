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


def test_format_src_markdown_python_after_newline():
    before = dedent(
        """\
        ```
        python --version
        echo "python"
        ```
        """
    )
    after, errors = blacken_docs.format_str(before, BLACK_MODE)
    assert errors == []
    assert after == before


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
    before = dedent(
        """\
        hello

        ```pycon

            >>> f(1,2,3)
            output
        ```
        world
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == dedent(
        """\
        hello

        ```pycon

        >>> f(1, 2, 3)
        output
        ```
        world
        """
    )


def test_format_src_markdown_pycon_after_newline():
    before = dedent(
        """\
        ```
        pycon is great
        >>> yes it is
        ```
        """
    )
    after, errors = blacken_docs.format_str(before, BLACK_MODE)
    assert errors == []
    assert after == before


def test_format_src_markdown_pycon_options():
    before = dedent(
        """\
        hello

        ```pycon title='Session 1'

            >>> f(1,2,3)
            output
        ```
        world
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == dedent(
        """\
        hello

        ```pycon title='Session 1'

        >>> f(1, 2, 3)
        output
        ```
        world
        """
    )


def test_format_src_markdown_pycon_twice():
    before = dedent(
        """\
        ```pycon
        >>> f(1,2,3)
        output
        ```
        example 2
        ```pycon
        >>> f(1,2,3)
        output
        ```
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == dedent(
        """\
        ```pycon
        >>> f(1, 2, 3)
        output
        ```
        example 2
        ```pycon
        >>> f(1, 2, 3)
        output
        ```
        """
    )


def test_format_src_markdown_comments_disable():
    before = dedent(
        """\
        <!-- blacken-docs:off -->
        ```python
        'single quotes rock'
        ```
        <!-- blacken-docs:on -->
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == before


def test_format_src_markdown_comments_disabled_enabled():
    before = dedent(
        """\
        <!-- blacken-docs:off -->
        ```python
        'single quotes rock'
        ```
        <!-- blacken-docs:on -->
        ```python
        'double quotes rock'
        ```
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == dedent(
        """\
        <!-- blacken-docs:off -->
        ```python
        'single quotes rock'
        ```
        <!-- blacken-docs:on -->
        ```python
        "double quotes rock"
        ```
        """
    )


def test_format_src_markdown_comments_before():
    before = dedent(
        """\
        <!-- blacken-docs:off -->
        <!-- blacken-docs:on -->
        ```python
        'double quotes rock'
        ```
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == dedent(
        """\
        <!-- blacken-docs:off -->
        <!-- blacken-docs:on -->
        ```python
        "double quotes rock"
        ```
        """
    )


def test_format_src_markdown_comments_after():
    before = dedent(
        """\
        ```python
        'double quotes rock'
        ```
        <!-- blacken-docs:off -->
        <!-- blacken-docs:on -->
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == dedent(
        """\
        ```python
        "double quotes rock"
        ```
        <!-- blacken-docs:off -->
        <!-- blacken-docs:on -->
        """
    )


def test_format_src_markdown_comments_only_on():
    # fmt: off
    before = dedent(
        """\
        <!-- blacken-docs:on -->
        ```python
        'double quotes rock'
        ```
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == dedent(
        """\
        <!-- blacken-docs:on -->
        ```python
        "double quotes rock"
        ```
        """
    )
    # fmt: on


def test_format_src_markdown_comments_only_off():
    # fmt: off
    before = dedent(
        """\
        <!-- blacken-docs:off -->
        ```python
        'single quotes rock'
        ```
        """
    )
    # fmt: on
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == before


def test_format_src_markdown_comments_multiple():
    before = dedent(
        """\
        <!-- blacken-docs:on -->
        <!-- blacken-docs:off -->
        <!-- blacken-docs:on -->
        <!-- blacken-docs:on -->
        <!-- blacken-docs:off -->
        <!-- blacken-docs:off -->
        ```python
        'single quotes rock'
        ```
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == before


def test_on_off_comments_in_code_blocks():
    before = dedent(
        """\
        ````md
        <!-- blacken-docs:off -->
        ```python
        f(1,2,3)
        ```
        <!-- blacken-docs:on -->
        ````
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == before


def test_format_src_markdown_comments_disable_pycon():
    before = dedent(
        """\
        <!-- blacken-docs:off -->
        ```pycon
        >>> 'single quotes rock'
        ```
        <!-- blacken-docs:on -->
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == before


def test_format_src_latex_minted():
    before = dedent(
        """\
        hello
        \\begin{minted}{python}
        f(1,2,3)
        \\end{minted}
        world!
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == dedent(
        """\
        hello
        \\begin{minted}{python}
        f(1, 2, 3)
        \\end{minted}
        world!
        """
    )


def test_format_src_latex_minted_opt():
    before = dedent(
        """\
        maths!
        \\begin{minted}[mathescape]{python}
        # Returns $\\sum_{i=1}^{n}i$
        def sum_from_one_to(n):
          r = range(1, n+1)
          return sum(r)
        \\end{minted}
        done
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == dedent(
        """\
        maths!
        \\begin{minted}[mathescape]{python}
        # Returns $\\sum_{i=1}^{n}i$
        def sum_from_one_to(n):
            r = range(1, n + 1)
            return sum(r)
        \\end{minted}
        done
        """
    )


def test_format_src_latex_minted_indented():
    # Personally I would have minted python code all flush left,
    # with only the Python code's own four space indentation:
    before = dedent(
        """\
        hello
          \\begin{minted}{python}
            if True:
              f(1,2,3)
          \\end{minted}
        world!
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == dedent(
        """\
        hello
          \\begin{minted}{python}
          if True:
              f(1, 2, 3)
          \\end{minted}
        world!
        """
    )


def test_format_src_latex_minted_pycon():
    before = dedent(
        """\
        Preceding text
        \\begin{minted}[gobble=2,showspaces]{pycon}
        >>> print( 'Hello World' )
        Hello World
        \\end{minted}
        Following text.
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == dedent(
        """\
        Preceding text
        \\begin{minted}[gobble=2,showspaces]{pycon}
        >>> print("Hello World")
        Hello World
        \\end{minted}
        Following text.
        """
    )


def test_format_src_latex_minted_pycon_indented():
    # Nicer style to put the \begin and \end on new lines,
    # but not actually required for the begin line
    before = dedent(
        """\
        Preceding text
          \\begin{minted}{pycon}
            >>> print( 'Hello World' )
            Hello World
          \\end{minted}
        Following text.
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == dedent(
        """\
        Preceding text
          \\begin{minted}{pycon}
          >>> print("Hello World")
          Hello World
          \\end{minted}
        Following text.
        """
    )


def test_format_src_latex_minted_comments_off():
    before = dedent(
        """\
        % blacken-docs:off
        \\begin{minted}{python}
        'single quotes rock'
        \\end{minted}
        % blacken-docs:on
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == before


def test_format_src_latex_minted_comments_off_pycon():
    before = dedent(
        """\
        % blacken-docs:off
        \\begin{minted}{pycon}
        >>> 'single quotes rock'
        \\end{minted}
        % blacken-docs:on
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == before


def test_format_src_pythontex():
    # fmt: off
    before = dedent(
        """\
        hello
        \\begin{pyblock}
        f(1,2,3)
        \\end{pyblock}
        world!
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == dedent(
        """\
        hello
        \\begin{pyblock}
        f(1, 2, 3)
        \\end{pyblock}
        world!
        """
    )
    # fmt: on


def test_format_src_pythontex_comments_off():
    before = dedent(
        """\
        % blacken-docs:off
        \\begin{pyblock}
        f(1,2,3)
        \\end{pyblock}
        % blacken-docs:on
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == before


def test_format_src_rst():
    before = dedent(
        """\
        hello

        .. code-block:: python

            f(1,2,3)

        world
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == dedent(
        """\
        hello

        .. code-block:: python

            f(1, 2, 3)

        world
        """
    )


def test_format_src_rst_empty():
    before = "some text\n\n.. code-block:: python\n\n\nsome other text\n"
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == before


def test_format_src_rst_literal_blocks():
    before = dedent(
        """\
        hello::

            f(1,2,3)

        world
        """
    )
    after, _ = blacken_docs.format_str(
        before,
        BLACK_MODE,
        rst_literal_blocks=True,
    )
    assert after == dedent(
        """\
        hello::

            f(1, 2, 3)

        world
        """
    )


def test_format_src_rst_literal_block_empty():
    before = dedent(
        """\
        hello::
        world
        """
    )
    after, _ = blacken_docs.format_str(
        before,
        BLACK_MODE,
        rst_literal_blocks=True,
    )
    assert after == before


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


def test_format_src_rst_literal_blocks_comments():
    before = dedent(
        """\
        .. blacken-docs:off
        Example::

            'single quotes rock'

        .. blacken-docs:on
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE, rst_literal_blocks=True)
    assert after == before


def test_format_src_rst_sphinx_doctest():
    before = dedent(
        """\
        .. testsetup:: group1

           import parrot
           mock = SomeMock( )

        .. testcleanup:: group1

           mock.stop( )

        .. doctest:: group1

           >>> parrot.voom( 3000 )
           This parrot wouldn't voom if you put 3000 volts through it!

        .. testcode::

           parrot.voom( 3000 )

        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == dedent(
        """\
        .. testsetup:: group1

           import parrot

           mock = SomeMock()

        .. testcleanup:: group1

           mock.stop()

        .. doctest:: group1

           >>> parrot.voom(3000)
           This parrot wouldn't voom if you put 3000 volts through it!

        .. testcode::

           parrot.voom(3000)

        """
    )


def test_format_src_rst_indented():
    before = dedent(
        """\
        .. versionadded:: 3.1

            hello

            .. code-block:: python

                def hi():
                    f(1,2,3)

            world
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == dedent(
        """\
        .. versionadded:: 3.1

            hello

            .. code-block:: python

                def hi():
                    f(1, 2, 3)

            world
        """
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
    before = dedent(
        """\
        .. code-block:: python
            :lineno-start: 10
            :emphasize-lines: 11

            def foo():
                bar(1,2,3)
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == dedent(
        """\
        .. code-block:: python
            :lineno-start: 10
            :emphasize-lines: 11

            def foo():
                bar(1, 2, 3)
        """
    )


def test_format_src_rst_python_inside_non_python_code_block():
    before = dedent(
        """\
        blacken-docs does changes like:

        .. code-block:: diff

             .. code-block:: python

            -    'Hello World'
            +    "Hello World"
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == before


def test_format_src_rst_python_comments():
    before = dedent(
        """\
        .. blacken-docs:off
        .. code-block:: python

            'single quotes rock'

        .. blacken-docs:on
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == before


def test_integration_ok(tmp_path, capsys):
    f = tmp_path / "f.md"
    f.write_text(
        "```python\nf(1, 2, 3)\n```\n",
    )

    result = blacken_docs.main((str(f),))

    assert result == 0
    assert not capsys.readouterr()[1]
    assert f.read_text() == ("```python\nf(1, 2, 3)\n```\n")


def test_integration_modifies(tmp_path, capsys):
    f = tmp_path / "f.md"
    f.write_text(
        "```python\nf(1,2,3)\n```\n",
    )

    result = blacken_docs.main((str(f),))

    assert result == 1
    out, _ = capsys.readouterr()
    assert out == f"{f}: Rewriting...\n"
    assert f.read_text() == ("```python\nf(1, 2, 3)\n```\n")


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


def test_integration_check(tmp_path):
    f = tmp_path / "f.md"
    text = dedent(
        """\
        ```python
        x = 'a' 'b'
        ```
        """
    )
    f.write_text(text)

    result = blacken_docs.main((str(f), "--check"))

    assert result == 1
    assert f.read_text() == text


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
        x = "a" "b"
        ```
        """
    )


def test_integration_pyi(tmp_path):
    f = tmp_path / "f.md"
    f.write_text(
        dedent(
            """\
            ```python
            class Foo: ...


            class Bar: ...
            ```
            """
        )
    )

    result = blacken_docs.main((str(f), "--pyi"))

    assert result == 1
    assert f.read_text() == dedent(
        """\
        ```python
        class Foo: ...
        class Bar: ...
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
        "```python\nf('hi')\n```\n",
    )

    result = blacken_docs.main((str(f), "--skip-string-normalization"))

    assert result == 0
    assert f.read_text() == ("```python\nf('hi')\n```\n")


def test_integration_syntax_error(tmp_path, capsys):
    f = tmp_path / "f.md"
    f.write_text(
        "```python\nf(\n```\n",
    )

    result = blacken_docs.main((str(f),))

    assert result == 2
    out, _ = capsys.readouterr()
    assert out.startswith(f"{f}:1: code block parse error")
    assert f.read_text() == ("```python\nf(\n```\n")


def test_integration_ignored_syntax_error(tmp_path, capsys):
    f = tmp_path / "f.md"
    f.write_text(
        "```python\nf( )\n```\n\n```python\nf(\n```\n",
    )

    result = blacken_docs.main((str(f), "--skip-errors"))

    assert result == 1
    out, _ = capsys.readouterr()
    assert f.read_text() == ("```python\nf()\n```\n\n```python\nf(\n```\n")


def test_format_src_rst_jupyter_sphinx():
    before = dedent(
        """\
        hello

        .. jupyter-execute::

            f(1,2,3)

        world
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == dedent(
        """\
        hello

        .. jupyter-execute::

            f(1, 2, 3)

        world
        """
    )


def test_format_src_rst_jupyter_sphinx_with_directive():
    before = dedent(
        """\
        hello

        .. jupyter-execute::
            :hide-code:

            f(1,2,3)

        world
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == dedent(
        """\
        hello

        .. jupyter-execute::
            :hide-code:

            f(1, 2, 3)

        world
        """
    )


def test_format_src_python_docstring_markdown():
    before = dedent(
        '''\
        def f():
            """
            hello world

            ```python
            f(1,2,3)
            ```
            """
            pass
        '''
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == dedent(
        '''\
        def f():
            """
            hello world

            ```python
            f(1, 2, 3)
            ```
            """
            pass
        '''
    )


def test_format_src_python_docstring_rst():
    before = dedent(
        '''\
        def f():
            """
            hello world

            .. code-block:: python

                f(1,2,3)
            """
            pass
        '''
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == dedent(
        '''\
        def f():
            """
            hello world

            .. code-block:: python

                f(1, 2, 3)
            """
            pass
        '''
    )


def test_format_src_rst_pycon():
    before = dedent(
        """\
        hello

        .. code-block:: pycon

            >>> f(1,2,3)
            output

        world
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == dedent(
        """\
        hello

        .. code-block:: pycon

            >>> f(1, 2, 3)
            output

        world
        """
    )


def test_format_src_rst_pycon_with_continuation():
    before = dedent(
        """\
        .. code-block:: pycon

            >>> d = {
            ...   "a": 1,
            ...   "b": 2,
            ...   "c": 3,}

        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == dedent(
        """\
        .. code-block:: pycon

            >>> d = {
            ...     "a": 1,
            ...     "b": 2,
            ...     "c": 3,
            ... }

        """
    )


def test_format_src_rst_pycon_adds_continuation():
    before = '.. code-block:: pycon\n\n    >>> d = {"a": 1,"b": 2,"c": 3,}\n\n'
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == dedent(
        """\
        .. code-block:: pycon

            >>> d = {
            ...     "a": 1,
            ...     "b": 2,
            ...     "c": 3,
            ... }

        """
    )


def test_format_src_rst_pycon_preserves_trailing_whitespace():
    before = dedent(
        """\
        hello

        .. code-block:: pycon

            >>> d = {"a": 1, "b": 2, "c": 3}



        world
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == before


def test_format_src_rst_pycon_indented():
    before = dedent(
        """\
        .. versionadded:: 3.1

            hello

            .. code-block:: pycon

                >>> def hi():
                ...     f(1,2,3)
                ...

            world
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == dedent(
        """\
        .. versionadded:: 3.1

            hello

            .. code-block:: pycon

                >>> def hi():
                ...     f(1, 2, 3)
                ...

            world
        """
    )


def test_format_src_rst_pycon_code_block_is_final_line1():
    before = dedent(
        """\
        .. code-block:: pycon

            >>> if True:
            ...   pass
            ...
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == dedent(
        """\
        .. code-block:: pycon

            >>> if True:
            ...     pass
            ...
        """
    )


def test_format_src_rst_pycon_code_block_is_final_line2():
    before = ".. code-block:: pycon\n\n    >>> if True:\n    ...   pass\n"
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == dedent(
        """\
        .. code-block:: pycon

            >>> if True:
            ...     pass
            ...
        """
    )


def test_format_src_rst_pycon_nested_def1():
    before = dedent(
        """\
        .. code-block:: pycon

            >>> if True:
            ...     def f(): pass
            ...
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == dedent(
        """\
        .. code-block:: pycon

            >>> if True:
            ...     def f():
            ...         pass
            ...
        """
    )


def test_format_src_rst_pycon_nested_def2():
    before = dedent(
        """\
        .. code-block:: pycon

            >>> if True:
            ...     def f(): pass
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == dedent(
        """\
        .. code-block:: pycon

            >>> if True:
            ...     def f():
            ...         pass
            ...
        """
    )


def test_format_src_rst_pycon_empty_line():
    before = dedent(
        """\
        .. code-block:: pycon

            >>> l = [
            ...
            ...     1,
            ... ]
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == dedent(
        """\
        .. code-block:: pycon

            >>> l = [
            ...     1,
            ... ]
        """
    )


def test_format_src_rst_pycon_preserves_output_indentation():
    before = dedent(
        """\
        .. code-block:: pycon

            >>> 1 / 0
            Traceback (most recent call last):
              File "<stdin>", line 1, in <module>
            ZeroDivisionError: division by zero
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == before


def test_format_src_rst_pycon_elided_traceback():
    before = dedent(
        """\
        .. code-block:: pycon

            >>> 1 / 0
            Traceback (most recent call last):
              ...
            ZeroDivisionError: division by zero
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == before


def test_format_src_rst_pycon_no_prompt():
    before = ".. code-block:: pycon\n\n    pass\n"
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == before


def test_format_src_rst_pycon_no_trailing_newline():
    before = ".. code-block:: pycon\n\n    >>> pass"
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == (".. code-block:: pycon\n\n    >>> pass\n")


def test_format_src_rst_pycon_comment_before_promopt():
    before = dedent(
        """\
        .. code-block:: pycon

            # Comment about next line
            >>> pass
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == dedent(
        """\
        .. code-block:: pycon

            # Comment about next line
            >>> pass
        """
    )


def test_format_src_rst_pycon_comments():
    before = dedent(
        """\
        .. blacken-docs:off
        .. code-block:: pycon

            >>> 'single quotes rock'

        .. blacken-docs:on
        """
    )
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == before


def test_format_src_rst_pycon_empty():
    before = "some text\n\n.. code-block:: pycon\n\n\nsome other text\n"
    after, _ = blacken_docs.format_str(before, BLACK_MODE)
    assert after == before
