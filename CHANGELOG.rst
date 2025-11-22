Changelog
=========


v0.5.3 (2025-11-22)
-------------------

Changes
~~~~~~~
- Cleanup type annotations on overridden class method. [Stephen L
  Arnold]
- Cleanup typo in readme file. [Stephen L Arnold]
- Cleanup some doc strings and update changelog. [Stephen L Arnold]

Fixes
~~~~~
- Replace self.log with logging.debug statements. [Stephen L Arnold]

  * print output is not so compatible with console consumers, eg, picotui
  * this preserves the original output and makes it adjustable with a
    quiet default
  * update consumer test with caplog fixture


v0.5.2 (2025-11-09)
-------------------

Changes
~~~~~~~
- Adjust build dep min versions for el9 build env. [Stephen L Arnold]

  * set version_scheme for setuptools_scm to "no-guess-dev"


v0.5.1 (2025-11-09)
-------------------

Changes
~~~~~~~
- Backport pkg metadata for el9 and add gitchangelog cfg, update readme.
  [Stephen L Arnold]

  * create changelog file for next release
- Remove docs build from release workflow until we have docs. [Stephen L
  Arnold]
- Add empty __init__.py to package dir, update tests and authors.
  [Stephen L Arnold]
- Add reuse status badge, display version in tox dev env. [Stephen L
  Arnold]
- Cleanup pre-commit hooks, apply format fixes, update readme. [Stephen
  L Arnold]
- Cleanup REUSE config and symlink license, update docstring. [Stephen L
  Arnold]

  * add simple consumer test, use pytest fixtures

Fixes
~~~~~
- Restore expected behavior of download-artifact action. [Stephen L
  Arnold]
- Add type annotations and py.typed marker. [Stephen L Arnold]

  * quotes around type hints using '|' are apparently required on less than
    python 3.10
- Allow windows line-endings in test assert, cleanup tox cmds. [Stephen
  L Arnold]


v0.5.0 (2025-06-03)
-------------------

Fixes
~~~~~
- Cleanup some lint, adjust some configs. [Stephen L Arnold]

Other
~~~~~
- Initial project commit with tox and GH workflows. [Stephen L Arnold]
- Initial commit. [Steve Arnold]
