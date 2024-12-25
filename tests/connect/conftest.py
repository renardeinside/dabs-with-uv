from pathlib import Path
import pytest
from dabs_with_uv.logger import logger
from dotenv import load_dotenv
from databricks.connect import DatabricksSession


@pytest.fixture(scope="session", autouse=True)
def session() -> None:
    dotenv_file = (
        Path(__file__).parent.parent.parent / ".env"
    )  # tests/connect/conftest.py -> ../../.env (project root)
    if dotenv_file:
        logger.info(f"Loading environment variables from {dotenv_file}")
        load_dotenv(dotenv_file)
    else:
        logger.warning("No .env file found. Environment variables will not be loaded.")

    logger.info("Creating Databricks session")
    _ = (
        DatabricksSession.builder.serverless()
        .getOrCreate()
    )
    logger.info("Databricks session created")
