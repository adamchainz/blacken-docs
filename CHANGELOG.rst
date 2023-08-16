=========
Changelog
=========

1.16.0 (2023-08-16)
-------------------

* Allow Markdown fence options.

  Thanks to initial work from Matthew Anderson in `PR #246 <https://github.com/adamchainz/blacken-docs/pull/246>`__.

* Expand Markdown detection to all Python language names from Pygments: ``py``, ``sage``, ``python3``, ``py3``, and ``numpy``.

* Preserve leading whitespace lines in reStructuredText code blocks.

  Thanks to Julianus Pfeuffer for the report in `Issue #217 <https://github.com/adamchainz/blacken-docs/issues/217>`__.

* Use exit code 2 to indicate errors from Black, whilst exit code 1 remains for “files have been formatted”.

  Thanks to Julianus Pfeuffer for the report in `Issue #218 <https://github.com/adamchainz/blacken-docs/issues/218>`__.

* Support passing the ``--preview`` option through to Black, to select the future style.

* Remove ``language_version`` from ``.pre-commit-hooks.yaml``.
  This change allows ``default_language_version`` in ``.pre-commit-config.yaml` to take precedence.

  Thanks to Aneesh Agrawal in `PR #258 <https://github.com/adamchainz/blacken-docs/pull/258>`__.

1.15.0 (2023-07-09)
-------------------

* Drop Python 3.7 support.

1.14.0 (2023-06-13)
-------------------

* Support Python 3.12.

1.13.0 (2023-01-16)
-------------------

* Note Adam Johnson is new maintainer.

* Require Black 22.1.0+.

* Add ``--rst-literal-blocks`` option, to also format text in reStructuredText literal blocks, starting with ``::``.
  Sphinx highlights these with the project’s default language, which defaults to Python.

1.12.1 (2022-01-30)
-------------------

* Fix compatibility with Black 22.1.0.

  Thanks to Jelle Zijlstra for the fix in `PR #142 <https://github.com/adamchainz/blacken-docs/pull/142>`__.

* Drop Python 3.6 support.

  Thanks to Anthony Sottile in `PR #140 <https://github.com/adamchainz/blacken-docs/pull/140>`__.

1.12.0 (2021-11-19)
-------------------

* Fix nested reStructuredText code blocks.

No changelog kept for earlier versions.
See `log on GitHub <https://github.com/adamchainz/blacken-docs/commits/main>`__ for details.
