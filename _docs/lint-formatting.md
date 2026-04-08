# Linting and formatting

## with script

```bash
uv sync --extra dev
./scripts/lint.sh
./scripts/format.sh
```


## with pre-commit

### install pre-commit
```bash
uv sync --extra dev
uv run pre-commit-install
```

### uninstall pre-commit
if you want to uninstall pre-commit, you can run the following command:

```bash
uv run pre-commit uninstall
```

> [!NOTE]  
> pre-commit will run automatically when you commit your changes.