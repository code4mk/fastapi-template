# Linting and formatting

## with script

```bash
uv sync --extra dev
./scripts/lint.sh
./scripts/format.sh
```


## with pre-commit

```bash
uv sync --extra dev
pre-commit install
```

> [!NOTE]  
> pre-commit will run automatically when you commit your changes.