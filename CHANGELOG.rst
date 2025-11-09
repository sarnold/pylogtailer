Changelog
=========


v0.5.1 (2025-11-08)
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
