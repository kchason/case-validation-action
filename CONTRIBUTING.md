# Contribution Guide

Contributions in the form of issues and pull requests are welcome. Please read the following guidelines before contributing.

## Pre-commit Hooks

This project uses [pre-commit](https://pre-commit.com/) to run a series of checks before committing code. To install the pre-commit hooks, run the following command:

```bash
pre-commit install
```

Run the following command to run the pre-commit hooks on all files:

```bash
pre-commit run --all-files
```

## Security Testing

This project uses [KICS](https://docs.kics.io/latest/getting-started/) to scan for security issues in the infrastructure such as the `Dockerfile`. To run the scan, run the following command:

```bash
docker run -t -v $(pwd):/path checkmarx/kics:latest scan -p /path -o "/path/"
```

This will generate a `results.json` file as well as print the contents to the console. Any findings above a `low` severity should be addressed before committing code as they will fail the CI pipeline.
