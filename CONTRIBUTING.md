Install project automation tool [`nox`](https://nox.thea.codes/en/stable/):

```shell
python -m pip install --user nox
```

### Unit Tests

```shell
nox -s tests
```

### Lint

```shell
nox -s lint
```

### Publish to PyPI

```shell
nox -s publish
```

### Running all checks at one

Before publishing, run all checks at once

```shell
nox
```
