import argparse
import contextlib
import re
import textwrap
from typing import Generator
from typing import List
from typing import Match
from typing import NamedTuple
from typing import Optional
from typing import Sequence
from typing import Tuple

import black


MD_RE = re.compile(
    r'(?P<before>^(?P<indent> *)```python\n)'
    r'(?P<code>.*?)'
    r'(?P<after>^(?P=indent)```\s*$)',
    re.DOTALL | re.MULTILINE,
)
RST_RE = re.compile(
    r'(?P<before>'
    r'^(?P<indent> *)\.\. (code|code-block|sourcecode|ipython):: python\n'
    r'((?P=indent) +:.*\n)*'
    r'\n*'
    r')'
    r'(?P<code>(^((?P=indent) +.*)?\n)+)',
    re.MULTILINE,
)
INDENT_RE = re.compile('^ +(?=[^ ])', re.MULTILINE)
TRAILING_NL_RE = re.compile(r'\n+\Z', re.MULTILINE)


class CodeBlockError(NamedTuple):
    offset: int
    exc: Exception


def format_str(
        src: str, black_mode: black.FileMode,
) -> Tuple[str, Sequence[CodeBlockError]]:
    errors: List[CodeBlockError] = []

    @contextlib.contextmanager
    def _collect_error(match: Match[str]) -> Generator[None, None, None]:
        try:
            yield
        except Exception as e:
            errors.append(CodeBlockError(match.start(), e))

    def _md_match(match: Match[str]) -> str:
        code = textwrap.dedent(match['code'])
        with _collect_error(match):
            code = black.format_str(code, mode=black_mode)
        code = textwrap.indent(code, match['indent'])
        return f'{match["before"]}{code}{match["after"]}'

    def _rst_match(match: Match[str]) -> str:
        min_indent = min(INDENT_RE.findall(match['code']))
        trailing_ws_match = TRAILING_NL_RE.search(match['code'])
        assert trailing_ws_match
        trailing_ws = trailing_ws_match.group()
        code = textwrap.dedent(match['code'])
        with _collect_error(match):
            code = black.format_str(code, mode=black_mode)
        code = textwrap.indent(code, min_indent)
        return f'{match["before"]}{code.rstrip()}{trailing_ws}'

    src = MD_RE.sub(_md_match, src)
    src = RST_RE.sub(_rst_match, src)
    return src, errors


def format_file(
        filename: str, black_mode: black.FileMode, skip_errors: bool,
) -> int:
    with open(filename, encoding='UTF-8') as f:
        contents = f.read()
    new_contents, errors = format_str(contents, black_mode)
    for error in errors:
        lineno = contents[:error.offset].count('\n') + 1
        print(f'{filename}:{lineno}: code block parse error {error.exc}')
    if errors and not skip_errors:
        return 1
    if contents != new_contents:
        print(f'{filename}: Rewriting...')
        with open(filename, 'w', encoding='UTF-8') as f:
            f.write(new_contents)
        return 1
    else:
        return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-l', '--line-length', type=int, default=black.DEFAULT_LINE_LENGTH,
    )
    parser.add_argument(
        '-t',
        '--target-version',
        action='append',
        type=lambda v: black.TargetVersion[v.upper()],
        default=[],
        help=f'choices: {[v.name.lower() for v in black.TargetVersion]}',
        dest='target_versions',
    )
    parser.add_argument(
        '-S', '--skip-string-normalization', action='store_true',
    )
    parser.add_argument('-E', '--skip-errors', action='store_true')
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    black_mode = black.FileMode(
        target_versions=args.target_versions,
        line_length=args.line_length,
        string_normalization=not args.skip_string_normalization,
    )

    retv = 0
    for filename in args.filenames:
        retv |= format_file(filename, black_mode, skip_errors=args.skip_errors)
    return retv


if __name__ == '__main__':
    exit(main())
