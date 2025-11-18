"""
Shared pytest configuration and fixtures for Schemathesis tests.

This conftest.py provides:
- Schema fixture for loading the OpenAPI schema from Docker containers
- Authentication setup using custom auth class
- Database connection for testing against containerized PostgreSQL
"""
import os
import pytest
import schemathesis
import requests
import time



@pytest.fixture(scope="session")
def schema():
    """
    Load the OpenAPI schema from the Docker container.
    This fixture is session-scoped, so the schema is loaded once per test session.
    """
    return schemathesis.openapi.from_url("http://localhost:8000/openapi.json")