# Testing
This project uses `pytest` and `pytest-asyncio` for testing, along with `unittest` for unit testing (particularly for mocking and patching).

# Run tests

Tests can be run using the test script:

```bash
./scripts/test.sh
```

The script runs pytest with the following features:
- Code coverage reporting (minimum 80% coverage required)
- Coverage reports in terminal, HTML, and XML formats
- Verbose output

You can pass additional pytest arguments to the script:

```bash
./scripts/test.sh -s
```
