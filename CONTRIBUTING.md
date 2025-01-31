[Poetry]: https://python-poetry.org/
[Pylint]: https://www.pylint.org/
[isort]: https://pycqa.github.io/isort/
[mypy]: http://mypy-lang.org/
[django-pytest]: https://pytest-django.readthedocs.io/en/latest/
[pytest]: https://docs.pytest.org/en/stable/
[Sphinx]: https://www.sphinx-doc.org/en/master/
[readthedocs]: https://readthedocs.org/
[me]: https://github.com/bckohan
[black]: https://black.readthedocs.io/en/stable/
[pyright]: https://github.com/microsoft/pyright

# Contributing

Contributions are encouraged! Please use the issue page to submit feature
requests or bug reports. Issues with attached PRs will be given priority and
have a much higher likelihood of acceptance. Please also open an issue and
associate it with any submitted PRs. That said, the aim is to keep this library
as lightweight as possible. Only features with broad-based use cases will be
considered.

We are actively seeking additional maintainers. If you're interested, please
[contact me](https://github.com/bckohan).

## Installation

`django-typer` uses [Poetry](https://python-poetry.org/) for environment, package, and dependency
management:

```shell
poetry install
```

## Documentation

`django-typer` documentation is generated using [Sphinx](https://www.sphinx-doc.org/en/master/) with the
[readthedocs](https://readthedocs.org/) theme. Any new feature PRs must provide updated documentation for
the features added. To build the docs run doc8 to check for formatting issues
then run Sphinx:

```bash
cd ./doc
poetry run doc8 --ignore-path build --max-line-length 100
poetry run make html
```

## Static Analysis

`django-typer` uses [Pylint](https://www.pylint.org/) for Python linting and [mypy](http://mypy-lang.org/) and [pyright](https://github.com/microsoft/pyright) for static type
checking. Header imports are also standardized using [isort](https://pycqa.github.io/isort/) and formatting is
done with [black](https://black.readthedocs.io/en/stable/). Before any PR is accepted the following must be run, and
static analysis tools should not produce any errors or warnings. Disabling
certain errors or warnings where justified is acceptable:

```bash
poetry run isort django_typer
poetry run black django_typer
poetry run pylint django_typer
poetry run mypy django_typer
pyright
poetry check
poetry run pip check
poetry run python -m readme_renderer ./README.md
```

## Running Tests

`django-typer` is set up to use [pytest](https://docs.pytest.org/en/stable/) to run unit tests. All the tests are
housed in `django_typer/tests/tests.py`. Before a PR is accepted, all tests
must be passing and the code coverage must be at 100%. A small number of
exempted error handling branches are acceptable.

To run the full suite:

```shell
poetry run pytest
```

To run a single test, or group of tests in a class:

```shell
poetry run pytest <path_to_tests_file>::ClassName::FunctionName
```

For instance, to run all tests in BasicTests, and then just the
test_call_command test you would do:

```shell
poetry run pytest django_typer/tests/tests.py::BasicTests
poetry run pytest django_typer/tests/tests.py::BasicTests::test_call_command
```
