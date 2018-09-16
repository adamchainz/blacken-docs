import black

import blacken_docs


OPTS = {
    'line_length': black.DEFAULT_LINE_LENGTH,
    'mode': black.FileMode.AUTO_DETECT,
}


def test_format_src_trivial():
    assert blacken_docs.format_str('', **OPTS)[0] == ''


def test_format_src_markdown_simple():
    before = (
        '```python\n'
        'f(1,2,3)\n'
        '```\n'
    )
    after = blacken_docs.format_str(before, **OPTS)[0]
    assert after == (
        '```python\n'
        'f(1, 2, 3)\n'
        '```\n'
    )


def test_format_src_indented_markdown():
    before = (
        '- do this pls:\n'
        '  ```python\n'
        '  f(1,2,3)\n'
        '  ```\n'
        '- also this\n'
    )
    after = blacken_docs.format_str(before, **OPTS)[0]
    assert after == (
        '- do this pls:\n'
        '  ```python\n'
        '  f(1, 2, 3)\n'
        '  ```\n'
        '- also this\n'
    )


def test_format_src_rst():
    before = (
        'hello\n'
        '\n'
        '.. code-block:: python\n'
        '\n'
        '    f(1,2,3)\n'
        '\n'
        'world\n'
    )
    after = blacken_docs.format_str(before, **OPTS)[0]
    assert after == (
        'hello\n'
        '\n'
        '.. code-block:: python\n'
        '\n'
        '    f(1, 2, 3)\n'
        '\n'
        'world\n'
    )


def test_format_src_rst_indented():
    before = (
        '.. versionadded:: 3.1\n'
        '\n'
        '    hello\n'
        '\n'
        '    .. code-block:: python\n'
        '\n'
        '        def hi():\n'
        '            f(1,2,3)\n'
        '\n'
        '    world\n'
    )
    after = blacken_docs.format_str(before, **OPTS)[0]
    assert after == (
        '.. versionadded:: 3.1\n'
        '\n'
        '    hello\n'
        '\n'
        '    .. code-block:: python\n'
        '\n'
        '        def hi():\n'
        '            f(1, 2, 3)\n'
        '\n'
        '    world\n'
    )


def test_format_src_rst_with_highlight_directives():
    before = (
        '.. code-block:: python\n'
        '    :lineno-start: 10\n'
        '    :emphasize-lines: 11\n'
        '\n'
        '    def foo():\n'
        '        bar(1,2,3)\n'
    )
    after = blacken_docs.format_str(before, **OPTS)[0]
    assert after == (
        '.. code-block:: python\n'
        '    :lineno-start: 10\n'
        '    :emphasize-lines: 11\n'
        '\n'
        '    def foo():\n'
        '        bar(1, 2, 3)\n'
    )


def test_integration_ok(tmpdir, capsys):
    f = tmpdir.join('f.md')
    f.write(
        '```python\n'
        'f(1, 2, 3)\n'
        '```\n',
    )
    assert not blacken_docs.main((str(f),))
    assert not capsys.readouterr()[1]
    assert f.read() == (
        '```python\n'
        'f(1, 2, 3)\n'
        '```\n'
    )


def test_integration_modifies(tmpdir, capsys):
    f = tmpdir.join('f.md')
    f.write(
        '```python\n'
        'f(1,2,3)\n'
        '```\n',
    )
    assert blacken_docs.main((str(f),))
    out, _ = capsys.readouterr()
    assert out == f'{f}: Rewriting...\n'
    assert f.read() == (
        '```python\n'
        'f(1, 2, 3)\n'
        '```\n'
    )


def test_integration_line_length(tmpdir):
    f = tmpdir.join('f.md')
    f.write(
        '```python\n'
        'foo(very_very_very_very_very_very_very, long_long_long_long_long)\n'
        '```\n',
    )
    assert not blacken_docs.main((str(f), '--line-length=80'))
    assert blacken_docs.main((str(f), '--line-length=50'))
    assert f.read() == (
        '```python\n'
        'foo(\n'
        '    very_very_very_very_very_very_very,\n'
        '    long_long_long_long_long,\n'
        ')\n'
        '```\n'
    )


def test_integration_py36(tmpdir):
    f = tmpdir.join('f.md')
    f.write(
        '```python\n'
        'def very_very_long_function_name(\n'
        '    very_very_very_very_very_very,\n'
        '    very_very_very_very_very_very,\n'
        '    *long_long_long_long_long_long\n'
        '):\n'
        '    pass\n'
        '```\n',
    )
    assert not blacken_docs.main((str(f),))
    assert blacken_docs.main((str(f), '--py36'))
    assert f.read() == (
        '```python\n'
        'def very_very_long_function_name(\n'
        '    very_very_very_very_very_very,\n'
        '    very_very_very_very_very_very,\n'
        '    *long_long_long_long_long_long,\n'
        '):\n'
        '    pass\n'
        '```\n'
    )


def test_integration_skip_string_normalization(tmpdir):
    f = tmpdir.join('f.md')
    f.write(
        '```python\n'
        "f('hi')\n"
        '```\n',
    )
    assert not blacken_docs.main((str(f), '--skip-string-normalization'))
    assert f.read() == (
        '```python\n'
        "f('hi')\n"
        '```\n'
    )


def test_integration_syntax_error(tmpdir, capsys):
    f = tmpdir.join('f.md')
    f.write(
        '```python\n'
        'f(\n'
        '```\n',
    )
    assert blacken_docs.main((str(f),))
    out, _ = capsys.readouterr()
    assert out.startswith(f'{f}:1: code block parse error')
    assert f.read() == (
        '```python\n'
        'f(\n'
        '```\n'
    )


def test_integration_ignored_syntax_error(tmpdir, capsys):
    f = tmpdir.join('f.md')
    f.write(
        '```python\n'
        'f( )\n'
        '```\n'
        '\n'
        '```python\n'
        'f(\n'
        '```\n',
    )
    assert blacken_docs.main((str(f), '--skip-errors'))
    out, _ = capsys.readouterr()
    assert f.read() == (
        '```python\n'
        'f()\n'
        '```\n'
        '\n'
        '```python\n'
        'f(\n'
        '```\n'
    )
