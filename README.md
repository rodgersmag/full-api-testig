# FastAPI Testing Suite

A comprehensive testing setup for FastAPI applications with schema-aligned validation, functional tests, and load testing.

## 🎯 Overview

This project demonstrates best practices for testing FastAPI APIs using:
- **Schemathesis** - Automated API schema-based testing
- **Pytest** - Unit and integration tests
- **Locust** - Load and performance testing

## ✅ Test Results

### Schemathesis Tests
```
✅ Examples:  1 passed
✅ Coverage:  10 passed
✅ Fuzzing:   10 passed
✅ Stateful:  210 passed

Test cases: 2255 generated, 2255 passed
Exit code: 0
```

### Pytest Tests
```
20 passed in 17.18s
```

### Load Tests (30s, 10 users)
```
501 total requests
~17 req/s throughput
1% failure rate
Response times: 3ms median, 33ms 99th percentile
```

## 📚 Documentation

- **[PYDANTIC_SCHEMA_VALIDATION_GUIDE.md](PYDANTIC_SCHEMA_VALIDATION_GUIDE.md)** - Complete guide for schema-validation alignment
- **[FASTAPI_ASSISTANT_PROMPT.md](FASTAPI_ASSISTANT_PROMPT.md)** - Reusable prompt for coding assistants
- **[LOAD_TESTING.md](LOAD_TESTING.md)** - Comprehensive Locust load testing guide
- **[FIXES_SUMMARY.md](FIXES_SUMMARY.md)** - Summary of fixes made to the API

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd backend
uv sync
```

### 2. Start the Server
```bash
uv run fastapi dev main.py
```

Server runs on `http://localhost:8000`

### 3. Run Tests

**Schemathesis (API Schema Tests):**
```bash
st run http://localhost:8000/openapi.json
```

**Pytest (Unit/Integration Tests):**
```bash
uv run pytest -v
```

**Locust (Load Tests):**
```bash
# Web UI mode
uv run locust -f locustfile.py --host=http://localhost:8000

# Headless mode
uv run locust -f locustfile.py \
  --host=http://localhost:8000 \
  --users 50 \
  --spawn-rate 5 \
  --run-time 1m \
  --headless \
  --html report.html
```

## 🏗️ Project Structure

```
fastapi-test/
├── backend/
│   ├── models/
│   │   ├── user.py           # User Pydantic models
│   │   └── blog_post.py      # BlogPost Pydantic models
│   ├── tests/
│   │   ├── test_users.py     # User endpoint tests
│   │   └── test_blog_posts.py # BlogPost endpoint tests
│   ├── main.py               # FastAPI application
│   ├── locustfile.py         # Locust load tests
│   └── pyproject.toml        # Dependencies
├── PYDANTIC_SCHEMA_VALIDATION_GUIDE.md
├── FASTAPI_ASSISTANT_PROMPT.md
├── LOAD_TESTING.md
├── FIXES_SUMMARY.md
└── README.md (this file)
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
- **Functional tests** with Schemathesis (2255 test cases)
- **Unit tests** with Pytest (20 tests)
- **Load tests** with Locust (realistic user simulation)

### 3. **Best Practices**
- Schema-first design
- Stateful testing for API lifecycles
- Performance benchmarking
- Continuous validation

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

### Testing Checklist

- [ ] Schema patterns use ASCII ranges
- [ ] SecretStr fields have `format: None`
- [ ] Models have `extra='forbid'`
- [ ] Validators match schema exactly
- [ ] POST endpoints are idempotent
- [ ] All tests pass (Pytest + Schemathesis)
- [ ] Load tests show acceptable performance

## 📈 Performance Benchmarks

Our API achieves:
- **Response time**: 3ms median, 33ms 99th percentile
- **Throughput**: ~17 req/s (on localhost, development mode)
- **Reliability**: 99% success rate under load
- **Zero failures** in functional tests

*Note: Production performance will vary based on hardware, database, and network conditions.*

## 🔬 Advanced Testing

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

## 📝 License

MIT

## 🤝 Contributing

1. Follow schema-validation alignment principles
2. Add tests for new features
3. Run full test suite before committing
4. Update documentation

---

**Built with**: FastAPI, Pydantic, Schemathesis, Pytest, Locust

*Last Updated: 2025-11-18*
