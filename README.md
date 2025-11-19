# FastAPI Testing Suite & SDK Generation

A comprehensive testing setup for FastAPI applications with schema-aligned validation, functional tests, load testing, and automated SDK generation.

## 🎯 Overview

This project demonstrates best practices for testing FastAPI APIs and generating client SDKs using:
- **Schemathesis** - Automated API schema-based testing
- **Pytest** - Unit and integration tests
- **Locust** - Load and performance testing
- **SDK Generation** - Multi-language client libraries

## ✅ Test Results

### Schemathesis Tests
```
✅ Examples:  1 passed
✅ Coverage:  10 passed
✅ Fuzzing:   10 passed
✅ Stateful:  245 passed

Test cases: 2270 generated, 2270 passed
Exit code: 0
```

### Pytest Tests
```
20 passed in 18.98s
```

### Load Tests (Locust)
```
376,415 total requests
~1,000 req/s throughput
1.37% failure rate
Response times: 200ms median, 9394ms max
99% of requests under 8700ms
```

## 📚 Documentation

- **[PYDANTIC_SCHEMA_VALIDATION_GUIDE.md](PYDANTIC_SCHEMA_VALIDATION_GUIDE.md)** - Complete guide for schema-validation alignment
- **[FASTAPI_ASSISTANT_PROMPT.md](FASTAPI_ASSISTANT_PROMPT.md)** - Reusable prompt for coding assistants
- **[LOAD_TESTING.md](LOAD_TESTING.md)** - Comprehensive Locust load testing guide
- **[FIXES_SUMMARY.md](FIXES_SUMMARY.md)** - Summary of fixes made to the API
- **[../sdks/README.md](../sdks/README.md)** - Client SDK documentation
- **[../sdks/SDK_GENERATION_SUMMARY.md](../sdks/SDK_GENERATION_SUMMARY.md)** - SDK generation details

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd backend
uv sync
```

### 2. Start the Server
```bash
uv run fastapi dev
```

Server runs on `http://localhost:8000`

### 3. Run Tests

#### Pytest (Unit/Integration Tests)
```bash
uv run pytest -v
```

Expected output:
```
================================= test session starts ==================================
platform darwin -- Python 3.13.0, pytest-8.4.2, pluggy-1.6.0
collected 20 items

backend/tests/test_blog_posts.py::test_blog_post_endpoints[POST /users/] PASSED [ 5%]
backend/tests/test_blog_posts.py::test_blog_post_endpoints[GET /users/] PASSED [10%]
...
backend/tests/test_users.py::test_users_endpoints[DELETE /posts/{post_id}] PASSED [100%]

====================================== 20 passed in 18.98s ==============================
```

#### Schemathesis (API Schema Tests)
```bash
st run http://localhost:8000/openapi.json
```

Expected output:
```
Schemathesis v4.4.4

 ✅ Loaded specification from http://localhost:8000/openapi.json
     Operations:       10 selected / 10 total

 ✅ Examples (in 0.15s)
     ✅  1 passed  ⏭   9 skipped

 ✅ Coverage (in 1.36s)
     ✅ 10 passed

 ✅ Fuzzing (in 9.18s)
     ✅ 10 passed

 ✅ Stateful (in 5.54s)
     Scenarios:    245
     ✅ 245 passed

Test cases: 2270 generated, 2270 passed
```

#### Locust (Load Tests)
```bash
# Web UI mode (recommended for exploration)
uv run locust

# Then open http://0.0.0.0:8089 in your browser
# Set: Number of users: 100, Spawn rate: 10, Host: http://localhost:8000

# Headless mode (for CI/CD)
uv run locust \
  --users 100 \
  --spawn-rate 10 \
  --run-time 1m \
  --headless \
  --html report.html
```

Expected metrics:
```
Type     Name                         # reqs      # fails |    Avg     Min     Max    Med
POST     /posts/ [Create]              13646    24(0.18%) |     69       0    1155     24
GET      /posts/ [Quick]              131573     0(0.00%) |   1009       0    9312    250
POST     /users/ [Create]              16237    27(0.17%) |     70       0    1195     25
GET      /users/ [Quick]              131043     0(0.00%) |   1003       0    9394    250
...
Aggregated                           376415  5157(1.37%) |    957       0    9394    200
```

## 📦 Client SDK Generation

This project supports generating client SDKs in **multiple languages** using different generators.

### Available SDKs

#### Modern SDKs (Recommended)
Generated with modern, maintained tools:

| Language | Generator | Location | Features |
|----------|-----------|----------|----------|
| **TypeScript** | `@hey-api/openapi-ts` | `../sdks/typescript/` | Fetch API, tree-shakeable |
| **Python** | `openapi-python-client` | `../sdks/python/` | httpx, Pydantic, async |
| **Swift** | `openapi-generator` | `../sdks/swift/` | async/await, SPM |
| **HTTP** | Manual | `../sdks/httpclient/` | REST Client examples |

#### Swagger Codegen SDKs
Generated with `swagger-codegen-cli-v3`:

| Language | Location | Build Tool |
|----------|----------|------------|
| **TypeScript** | `../sdks/swagger-codegen/typescript/` | npm |
| **Python** | `../sdks/swagger-codegen/python/` | pip |
| **Swift** | `../sdks/swagger-codegen/swift/` | CocoaPods |
| **Java** | `../sdks/swagger-codegen/java/` | Maven/Gradle |

### Generate All SDKs

#### 1. Export OpenAPI Schema
```bash
# From project root
curl http://localhost:8000/openapi.json > openapi.json
```

#### 2. Generate Modern SDKs

**TypeScript:**
```bash
npx -y @hey-api/openapi-ts \
  -i openapi.json \
  -o sdks/typescript \
  -c @hey-api/client-fetch
```

**Python:**
```bash
pip install openapi-python-client
openapi-python-client generate \
  --path openapi.json \
  --output-path sdks/python \
  --overwrite
```

**Swift:**
```bash
npx -y @openapitools/openapi-generator-cli generate \
  -i openapi.json \
  -g swift5 \
  -o sdks/swift \
  --additional-properties=responseAs=AsyncAwait,useSPMFileStructure=true
```

#### 3. Generate Swagger Codegen SDKs

**Prerequisites:** Docker must be installed

**TypeScript:**
```bash
docker run --rm -v ${PWD}:/local \
  swaggerapi/swagger-codegen-cli-v3 generate \
  -i /local/openapi.json \
  -l typescript-fetch \
  -o /local/sdks/swagger-codegen/typescript
```

**Python:**
```bash
docker run --rm -v ${PWD}:/local \
  swaggerapi/swagger-codegen-cli-v3 generate \
  -i /local/openapi.json \
  -l python \
  -o /local/sdks/swagger-codegen/python
```

**Swift:**
```bash
docker run --rm -v ${PWD}:/local \
  swaggerapi/swagger-codegen-cli-v3 generate \
  -i /local/openapi.json \
  -l swift5 \
  -o /local/sdks/swagger-codegen/swift
```

**Java:**
```bash
docker run --rm -v ${PWD}:/local \
  swaggerapi/swagger-codegen-cli-v3 generate \
  -i /local/openapi.json \
  -l java \
  -o /local/sdks/swagger-codegen/java
```

**List all available languages:**
```bash
docker run --rm swaggerapi/swagger-codegen-cli-v3 langs
```

### Using Generated SDKs

#### TypeScript (Modern)
```typescript
import { client } from './sdks/typescript';

client.setConfig({ baseUrl: 'http://localhost:8000' });

const user = await createUserUsersPost({
  body: {
    email: 'test@example.com',
    password: 'SecurePass123!',
  }
});
```

#### Python (Modern)
```python
from fast_api_client import Client
from fast_api_client.models import UserCreate
from fast_api_client.api.default import create_user_users_post

client = Client(base_url="http://localhost:8000")
user_data = UserCreate(email="test@example.com", password="SecurePass123!")
user = create_user_users_post.sync(client=client, body=user_data)
```

#### Swift (Modern)
```swift
import OpenAPIClient

OpenAPIClientAPI.basePath = "http://localhost:8000"

let user = try await DefaultAPI.createUserUsersPost(
    userCreate: UserCreate(
        email: "test@example.com",
        password: "SecurePass123!"
    )
)
```

#### HTTP Client
Open `sdks/httpclient/api.http` in VS Code with the REST Client extension.

**For detailed SDK usage, see:**
- `../sdks/README.md` - Overview and comparison
- `../sdks/typescript/QUICK_START.md` - TypeScript guide
- `../sdks/python/QUICK_START.md` - Python guide
- `../sdks/swift/QUICK_START.md` - Swift guide
- `../sdks/TESTING_GUIDE.md` - SDK testing examples

## 🏗️ Project Structure

```
fastapi-test/
├── backend/
│   ├── models/
│   │   ├── user.py              # User Pydantic models
│   │   └── blog_post.py         # BlogPost Pydantic models
│   ├── tests/
│   │   ├── test_users.py        # User endpoint tests
│   │   └── test_blog_posts.py   # BlogPost endpoint tests
│   ├── main.py                  # FastAPI application
│   ├── locustfile.py            # Locust load tests
│   ├── pyproject.toml           # Dependencies
│   └── README.md                # This file
├── sdks/                        # Generated client SDKs
│   ├── typescript/              # Modern TypeScript SDK
│   ├── python/                  # Modern Python SDK
│   ├── swift/                   # Modern Swift SDK
│   ├── httpclient/              # HTTP examples
│   ├── swagger-codegen/         # Swagger Codegen SDKs
│   │   ├── typescript/
│   │   ├── python/
│   │   ├── swift/
│   │   └── java/
│   ├── README.md
│   ├── SDK_GENERATION_SUMMARY.md
│   └── TESTING_GUIDE.md
├── openapi.json                 # Exported OpenAPI schema
├── PYDANTIC_SCHEMA_VALIDATION_GUIDE.md
├── FASTAPI_ASSISTANT_PROMPT.md
├── LOAD_TESTING.md
└── FIXES_SUMMARY.md
```

## 🔑 Key Principles

### 1. **Schema-Validation Alignment**
The OpenAPI schema and Pydantic validation must match **exactly**:
- ✅ ASCII-only regex patterns (`[0-9]` not `\d`)
- ✅ Remove `format:password` from SecretStr fields
- ✅ Strict boolean validation
- ✅ Timezone-aware datetime
- ✅ Forbid extra fields (`extra='forbid'`)
- ✅ Idempotent POST endpoints (no 409 conflicts)

### 2. **Comprehensive Testing**
- **Functional tests** with Schemathesis (2270 test cases)
- **Unit tests** with Pytest (20 tests)
- **Load tests** with Locust (realistic user simulation)

### 3. **Client SDK Generation**
- **Multiple languages** supported
- **Multiple generators** for flexibility
- **Type-safe** clients with full validation
- **Comprehensive documentation**

### 4. **Best Practices**
- Schema-first design
- Stateful testing for API lifecycles
- Performance benchmarking
- Continuous validation
- Multi-language SDK support

## 📊 API Endpoints

### Users API
- `GET /users/` - List users (pagination)
- `POST /users/` - Create user (idempotent)
- `GET /users/{user_id}` - Get user
- `PATCH /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user

### Blog Posts API
- `GET /posts/` - List posts (pagination)
- `POST /posts/` - Create post (idempotent)
- `GET /posts/{post_id}` - Get post
- `PATCH /posts/{post_id}` - Update post
- `DELETE /posts/{post_id}` - Delete post

## 🛠️ Development

### Adding New Endpoints

1. **Follow the template** in `FASTAPI_ASSISTANT_PROMPT.md`
2. **Define patterns first** (ASCII-only!)
3. **Create Pydantic models** with strict validation
4. **Make POST idempotent** (return existing resource)
5. **Add tests** (Pytest + Schemathesis)
6. **Run all tests** to verify
7. **Regenerate SDKs** if API changes

### Testing Checklist

- [ ] Schema patterns use ASCII ranges
- [ ] SecretStr fields have `format: None`
- [ ] Models have `extra='forbid'`
- [ ] Validators match schema exactly
- [ ] POST endpoints are idempotent
- [ ] All tests pass (Pytest + Schemathesis)
- [ ] Load tests show acceptable performance
- [ ] SDKs regenerated if API changed

## 📈 Performance Benchmarks

Our API achieves:
- **Response time**: 200ms median, 8700ms 99th percentile
- **Throughput**: ~1000 req/s (on localhost, development mode)
- **Reliability**: 98.6% success rate under heavy load (10,000 users)
- **Zero failures** in functional tests

*Note: Production performance will vary based on hardware, database, and network conditions.*

## 🔬 Advanced Testing

### Full Test Suite
Run all tests in sequence:

```bash
# 1. Unit/Integration tests
uv run pytest -v

# 2. Schema-based tests
st run http://localhost:8000/openapi.json

# 3. Load tests (1 minute, 100 users)
uv run locust --users 100 --spawn-rate 10 --run-time 1m --headless
```

### Distributed Load Testing
```bash
# Master
locust -f locustfile.py --master --expect-workers 4

# Workers (in separate terminals)
locust -f locustfile.py --worker --master-host=localhost
```

### Custom Test Scenarios
See `LOAD_TESTING.md` for:
- Baseline performance tests
- Stress testing
- Spike testing
- Endurance testing

## 🐛 Troubleshooting

### Schemathesis Warnings
See `LOAD_TESTING.md` section on "Schema validation mismatch" warnings. These are **expected** and **acceptable** when testing with random UUIDs.

### Load Test Failures
Check:
- Server is running (`http://localhost:8000`)
- No port conflicts
- Sufficient system resources
- Check Locust failure report for details

### Schema Validation Errors
Follow principles in `PYDANTIC_SCHEMA_VALIDATION_GUIDE.md`:
1. Tighten schema to match validation
2. Loosen validation to match schema
3. Never allow stricter validation than schema

### SDK Generation Issues

**Docker not found:**
```bash
# Install Docker Desktop or Docker Engine
# https://docs.docker.com/get-docker/
```

**Permission denied:**
```bash
# On Linux/macOS, add user to docker group
sudo usermod -aG docker $USER
# Then logout and login again
```

**OpenAPI schema issues:**
```bash
# Validate your schema
curl http://localhost:8000/openapi.json | jq '.'

# Or use online validator
# https://editor.swagger.io/
```

## � SDK Distribution

### Publishing SDKs

You can publish the generated SDKs to package registries:

**TypeScript (npm):**
```bash
cd sdks/typescript
npm publish
```

**Python (PyPI):**
```bash
cd sdks/python
python setup.py sdist bdist_wheel
twine upload dist/*
```

**Swift (Swift Package Registry):**
```bash
cd sdks/swift
# Tag and push to GitHub
git tag 1.0.0
git push origin 1.0.0
```

**Java (Maven Central):**
```bash
cd sdks/swagger-codegen/java
mvn deploy
```

## �📝 License

MIT

## 🤝 Contributing

1. Follow schema-validation alignment principles
2. Add tests for new features
3. Run full test suite before committing
4. Update documentation
5. Regenerate SDKs if API changes

## 🔗 Useful Links

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Schemathesis**: https://schemathesis.readthedocs.io/
- **Locust**: https://locust.io/
- **Swagger Codegen**: https://github.com/swagger-api/swagger-codegen
- **OpenAPI Generator**: https://openapi-generator.tech/
- **@hey-api/openapi-ts**: https://github.com/hey-api/openapi-ts

---

**Built with**: FastAPI, Pydantic, Schemathesis, Pytest, Locust, OpenAPI Codegen

**Testing**: ✅ Unit Tests | ✅ Schema Tests | ✅ Load Tests  
**SDKs**: 🟦 TypeScript | 🐍 Python | 🍎 Swift | ☕ Java

*Last Updated: 2025-11-19*
