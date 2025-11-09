Python Log Watcher
==================

**Watch files for changes**.

Real-time log file watcher supporting log rotation.
Works with Python >= 3.2, on both POSIX and Windows.


|ci| |wheels| |bandit| |release|

|pre| |cov| |pylint|

|tag| |license| |reuse| |python|

A python class that "watches" a directory and calls a callback(filename, lines)
function every time one of the watched files gets written to, in real time.

.. note:: The "initial coommit" in the changelog file was cleaned up and
          packaged from `this ActiveState recipe`_.


.. _this ActiveState recipe: https://code.activestate.com/recipes/577968-log-watcher-tail-f-log/

Practically speaking, this can be compared to ``tail -F *.log`` UNIX
command, but instead of having lines printed to stdout a python
function gets called.

Similar to tail, it takes care of "watching" new files which are
created after initialization and "unwatching" those which are removed
in the meantime. This means you'll be able to "follow" and support also
rotating log files.

Example::

  >>> def callback(filename, lines):
  ...     print(filename, lines)
  ...
  >>> lw = LogWatcher("/var/log/", callback)
  >>> lw.loop()


Dev tools
=========

Local tool dependencies to aid in development; install them for
maximum enjoyment.

Tox
---

As long as you have git and at least Python 3.8, then you can install
and use tox_.  After cloning the repository, you can run the repo
checks with the ``tox`` command.  It will build a virtual python
environment for each installed version of python with all the python
dependencies and run the specified commands, eg:

::

  $ git clone https://github.com/sarnold/pylogtailer
  $ cd pylogtailer/
  $ tox -e py

The above will run the default test command using the (local) default
Python version.  To specify the Python version and host OS type, run
something like::

  $ tox -e py313-linux

To build and check the Python package, run::

  $ tox -e build,check

Full list of additional ``tox`` commands:

* ``tox -e dev`` build a python venv and install in editable mode
* ``tox -e build`` build the python packages and run package checks
* ``tox -e check`` install the wheel package from above
* ``tox -e lint`` run ``pylint`` (somewhat less permissive than PEP8/flake8 checks)
* ``tox -e mypy`` run mypy import and type checking
* ``tox -e style`` run flake8 style checks
* ``tox -e reuse`` run the ``reuse lint`` command and install sbom4python
* ``tox -e changes`` generate a new changelog file

To build/lint the api docs, use the following tox commands:

* ``tox -e docs`` build the documentation using sphinx and the api-doc plugin
* ``tox -e ldocs`` run the Sphinx doc-link checking
* ``tox -e cdocs`` run ``make clean`` in the docs build


We use gitchangelog_  to generate a changelog and/or release notes, as
well as the gitchangelog message format to help it categorize/filter
commits for tidier output.  Please use the appropriate ACTION modifiers
for important changes in Pull Requests.

Pre-commit
----------

This repo is also pre-commit_ enabled for various linting and format
checks.  The checks run automatically on commit and will fail the
commit (if not clean) with some checks performing simple file corrections.

If other checks fail on commit, the failure display should explain the error
types and line numbers. Note you must fix any fatal errors for the
commit to succeed; some errors should be fixed automatically (use
``git status`` and ``git diff`` to review any changes).

See the following sections for more information on gitchangelog and pre-commit.

You will need to install pre-commit before contributing any changes;
installing it using your system's package manager is recommended,
otherwise install with pip into your usual virtual environment using
something like::

  $ sudo emerge pre-commit  --or--
  $ pip install pre-commit

then install it into the repo you just cloned::

  $ git clone https://github.com/sarnold/pylogtailer.git
  $ cd pylogtailer/
  $ pre-commit install

It's usually a good idea to update the hooks to the latest version::

    pre-commit autoupdate


SBOM and license info
=====================

This project is now compliant with the REUSE Specification Version 3.3, so the
corresponding license information for all files can be found in the ``REUSE.toml``
configuration file with license text(s) in the ``LICENSES/`` folder.

Related metadata can be (re)generated with the following tools and command
examples.

* reuse-tool_ - REUSE_ compliance linting and sdist (source files) SBOM generation
* sbom4python_ - generate SBOM with full dependency chain

Commands
--------

Use tox to create the environment and run the lint command::

  $ tox -e reuse                      # --or--
  $ tox -e reuse -- spdx > sbom.txt   # generate sdist files sbom

Note you can pass any of the other reuse commands after the ``--`` above.

Use the above environment to generate the full SBOM in text format::

  $ source .tox/reuse/bin/activate
  $ sbom4python --system --use-pip -o <file_name>.txt

Be patient; the last command above may take several minutes. See the
doc links above for more detailed information on the tools and
specifications.

.. _Tox: https://github.com/tox-dev/tox
.. _reuse-tool: https://github.com/fsfe/reuse-tool
.. _REUSE: https://reuse.software/spec-3.3/
.. _sbom4python: https://github.com/anthonyharrison/sbom4python
.. _gitchangelog: https://github.com/sarnold/gitchangelog
.. _pre-commit: http://pre-commit.com/


.. |ci| image:: https://github.com/sarnold/pylogtailer/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/sarnold/pylogtailer/actions/workflows/ci.yml
    :alt: CI Status

.. |wheels| image:: https://github.com/sarnold/pylogtailer/actions/workflows/wheels.yml/badge.svg
    :target: https://github.com/sarnold/pylogtailer/actions/workflows/wheels.yml
    :alt: Wheel Status

.. |badge| image:: https://github.com/sarnold/pylogtailer/actions/workflows/pylint.yml/badge.svg
    :target: https://github.com/sarnold/pylogtailer/actions/workflows/pylint.yml
    :alt: Pylint Status

.. |release| image:: https://github.com/sarnold/pylogtailer/actions/workflows/release.yml/badge.svg
    :target: https://github.com/sarnold/pylogtailer/actions/workflows/release.yml
    :alt: Release Status

.. |bandit| image:: https://github.com/sarnold/pylogtailer/actions/workflows/bandit.yml/badge.svg
    :target: https://github.com/sarnold/pylogtailer/actions/workflows/bandit.yml
    :alt: Security check - Bandit

.. |cov| image:: https://raw.githubusercontent.com/sarnold/pylogtailer/badges/main/test-coverage.svg
    :target: https://github.com/sarnold/pylogtailer/actions/workflows/coverage.yml
    :alt: Test coverage

.. |pylint| image:: https://raw.githubusercontent.com/sarnold/pylogtailer/badges/main/pylint-score.svg
    :target: https://github.com/sarnold/pylogtailer/actions/workflows/pylint.yml
    :alt: Pylint Score

.. |license| image:: https://img.shields.io/badge/license-MIT-blue
    :target: https://github.com/sarnold/pylogtailer/blob/main/LICENSE
    :alt: License

.. |tag| image:: https://img.shields.io/github/v/tag/sarnold/pylogtailer?color=green&include_prereleases&label=latest%20release
    :target: https://github.com/sarnold/pylogtailer/releases
    :alt: GitHub tag

.. |python| image:: https://img.shields.io/badge/python-3.9+-blue.svg
    :target: https://www.python.org/downloads/
    :alt: Python

.. |reuse| image:: https://img.shields.io/badge/REUSE-compliant-blue.svg
    :target: https://reuse.software/spec-3.3/
    :alt: REUSE

.. |pre| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
