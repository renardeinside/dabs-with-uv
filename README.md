# Databricks Asset Bundles Example with uv

This project shows an example of a Python project that uses uv for dependency management and Databricks Asset Bundles for deployment.

## Local development

Prerequisites:
- Python 3.9+
- `uv`
- Databricks CLI
- Databricks workspace

Steps:
1. Clone the repository
2. Setup the uv env:
```
uv sync
```

## Running tests from local machine

Add the `DATABRICKS_CONFIG_PROFILE` environment variable to your `.env` file:
```bash
DATABRICKS_CONFIG_PROFILE=<your-profile-name>
```

Then, run the tests via pytest:
```bash
pytest
```

## Deployment 

To deploy the app, login to your Databricks workspace from Databricks CLI:
```bash
databricks auth login 
```

Deploy the workflow:
```bash
databricks bundle deploy --var="catalog=your_catalog" --var="schema=default" -t dev
```

## Tech used


- [Databricks Asset Bundles](https://docs.databricks.com/en/dev-tools/bundles/index.html) - The tool to create, manage, and deploy Databricks Workflows
- [uv](https://docs.astral.sh/uv/) - An extremely fast Python package and project manager, written in Rust
- [hatch-vcs](https://github.com/ofek/hatch-vcs) - Plugin that uses your preferred version control system (like Git) to determine project versions
- [pydantic](https://docs.pydantic.dev/latest/) - data validation library for Python