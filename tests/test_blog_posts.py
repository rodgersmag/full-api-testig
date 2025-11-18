"""
Schemathesis tests for Blog Post endpoints.

This module tests all blog post-related endpoints:
- GET /posts/ - List posts with pagination and filtering
- GET /posts/{post_id} - Get specific post
- POST /posts/ - Create new post
- PATCH /posts/{post_id} - Update post
- DELETE /posts/{post_id} - Delete post

Follows FASTAPI_ASSISTANT_PROMPT.md principles:
- Schema and validation are perfectly aligned
- No 409 conflicts (idempotent POST)
- ASCII-only patterns
- No business logic validation beyond schema
"""
import schemathesis


# Load the OpenAPI schema from the running local server
schema = schemathesis.openapi.from_url("http://localhost:8000/openapi.json")


@schema.parametrize()
def test_blog_post_endpoints(case):
    """
    Test all /posts endpoints.
    
    This single test function will be parametrized by Schemathesis to test:
    - GET /posts/ - List posts with pagination
    - GET /posts/{post_id} - Get specific post
    - POST /posts/ - Create new post
    - PATCH /posts/{post_id} - Update post
    - DELETE /posts/{post_id} - Delete post
    
    Schemathesis will generate multiple test cases for each endpoint,
    testing various input combinations, edge cases, and error conditions.
    """
    # Only test blog post endpoints
    if not case.operation.path.startswith("/posts"):
        return
    
    # Call the API and validate
    # No special handling needed - schema and validation are aligned!
    case.call_and_validate()
