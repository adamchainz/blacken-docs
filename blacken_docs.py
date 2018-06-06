import argparse
import contextlib
import re
import textwrap
from typing import Any
from typing import Generator
from typing import Match
from typing import Optional
from typing import Tuple

import black


MD_RE = re.compile(
    r'(?P<before>^(?P<indent> *)```python\n)'
    r'(?P<code>.*?)'
    r'(?P<after>^(?P=indent)```$)',
    re.DOTALL | re.MULTILINE,
)
RST_RE = re.compile(
    r'(?P<before>'
    r'^(?P<indent> *)\.\. (code-block|sourcecode):: python\n'
    r'((?P=indent) +:.*\n)*'
    r'\n*'
    r')'
    r'(?P<code>(^((?P=indent) +.*)?\n)+)',
    re.MULTILINE,
)
INDENT_RE = re.compile('^ +(?=[^ ])', re.MULTILINE)
TRAILING_NL_RE = re.compile(r'\n+\Z', re.MULTILINE)


class CodeBlockError(ValueError):
    pass


def format_str(src: str, **black_opts: Any) -> str:
    @contextlib.contextmanager
    def _reraise(match: Match[str]) -> Generator[None, None, None]:
        try:
            yield
        except Exception as e:
            raise CodeBlockError(match.start(), e)

    def _md_match(match: Match[str]) -> str:
        code = textwrap.dedent(match['code'])
        with _reraise(match):
            code = black.format_str(code, **black_opts)
        code = textwrap.indent(code, match['indent'])
        return f'{match["before"]}{code}{match["after"]}'

    def _rst_match(match: Match[str]) -> str:
        min_indent = min(INDENT_RE.findall(match['code']))
        trailing_ws_match = TRAILING_NL_RE.search(match['code'])
        assert trailing_ws_match
        trailing_ws = trailing_ws_match.group()
        code = textwrap.dedent(match['code'])
        with _reraise(match):
            code = black.format_str(code, **black_opts)
        code = textwrap.indent(code, min_indent)
        return f'{match["before"]}{code.rstrip()}{trailing_ws}'

    src = MD_RE.sub(_md_match, src)
    src = RST_RE.sub(_rst_match, src)
    return src


def format_file(filename: str, **black_opts: Any) -> int:
    with open(filename, encoding='UTF-8') as f:
        contents = f.read()
    try:
        new_contents = format_str(contents, **black_opts)
    except CodeBlockError as exc:
        offset, orig_exc = exc.args
        lineno = contents[:offset].count('\n') + 1
        print(f'{filename}:{lineno}: code block parse error {orig_exc}')
        return 1
    if contents != new_contents:
        print(f'{filename}: Rewriting...')
        with open(filename, 'w', encoding='UTF-8') as f:
            f.write(new_contents)
        return 1
    else:
        return 0


def main(argv: Optional[Tuple[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-l', '--line-length', type=int, default=black.DEFAULT_LINE_LENGTH,
    )
    parser.add_argument('--py36-plus', action='store_true')
    parser.add_argument(
        '-S', '--skip-string-normalization', action='store_true',
    )
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    black_opts = {
        'line_length': args.line_length,
        'mode': black.FileMode.AUTO_DETECT,
    }
    if args.py36_plus:
        black_opts['mode'] |= black.FileMode.PYTHON36
    if args.skip_string_normalization:
        black_opts['mode'] |= black.FileMode.NO_STRING_NORMALIZATION

    retv = 0
    for filename in args.filenames:
        retv |= format_file(filename, **black_opts)
    return retv


if __name__ == '__main__':
    exit(main())
