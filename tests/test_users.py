"""
Schemathesis tests for User endpoints.

This module tests all user-related endpoints:
- GET /users - List users with pagination
- GET /users/{user_id} - Get specific user
- POST /users - Create new user
- PUT /users/{user_id} - Update user
- DELETE /users/{user_id} - Delete user

Schemathesis automatically generates test cases based on the OpenAPI schema
and validates responses against the schema. This tests the robustness of the API by:
- Testing valid inputs
- Testing invalid inputs (edge cases, type mismatches, etc.)
- Validating responses match the schema
- Ensuring proper error handling
"""
import schemathesis
import os


# Load the OpenAPI schema from the Docker container
# This will test against the containerized API instead of running locally
schema = schemathesis.openapi.from_url("http://localhost:8000/openapi.json")


@schema.parametrize()
def test_users_endpoints(case):
    """
    Test all /users endpoints.
    
    This single test function will be parametrized by Schemathesis to test:
    - GET /users - List users with pagination
    - GET /users/{user_id} - Get specific user
    - POST /users - Create new user
    - PUT /users/{user_id} - Update user
    - DELETE /users/{user_id} - Delete user
    
    Schemathesis will generate multiple test cases for each endpoint,
    testing various input combinations, edge cases, and error conditions.
    """
    # Only test users endpoints
    if not case.operation.path.startswith("/users"):
        return
    # Call the containerized API with authentication
    case.call_and_validate()
