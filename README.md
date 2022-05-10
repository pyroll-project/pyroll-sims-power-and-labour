# PyRoll Plugin

Template for PyRoll Plugin Repositories

- Rename the folder `pyroll_plugin` to the name of your plugin. Replace the dashes (`-`) in the name through
  underscores (`_`), since dashes are not valid in python identifiers. Place all your library code into this folder.

- Use [`pytest`](https://docs.pytest.org) for creating unit tests. Place all test files in the `tests` folder.

- Update the `pyproject.toml` with your metadata. It is recommended to use [`poetry`](https://python-poetry.org) to
  maintain dependencies, as is preconfigured.

- Place documentation in the `docs` folder:
    - it is recommended to provide a printable documentation based on the `docs.tex` template
    - include the result PDF in the commit and link it from `README.md` like [so](docs/docs.pdf)
    - include model and usage information in the documentation


