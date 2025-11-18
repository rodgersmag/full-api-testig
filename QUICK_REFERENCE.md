# Quick Reference - Testing Commands

## Start Server
```bash
cd backend
uv run fastapi dev main.py
```

## Run Tests

### Schemathesis (Schema-Based API Tests)
```bash
cd backend
st run http://localhost:8000/openapi.json
```

### Pytest (Unit/Integration Tests)
```bash
cd backend
uv run pytest -v
```

### Locust (Load Tests)

**Interactive Web UI:**
```bash
cd backend
uv run locust -f locustfile.py --host=http://localhost:8000
# Open http://localhost:8089
```

**Headless Quick Test:**
```bash
cd backend
uv run locust -f locustfile.py \
  --host=http://localhost:8000 \
  --users 50 \
  --spawn-rate 5 \
  --run-time 1m \
  --headless \
  --html load-test-report.html
```

## Full Test Suite
```bash
# Terminal 1: Start server
cd backend && uv run fastapi dev main.py

# Terminal 2: Run all tests
cd backend
uv run pytest -v && \
st run http://localhost:8000/openapi.json && \
uv run locust -f locustfile.py --host=http://localhost:8000 \
  --users 30 --spawn-rate 3 --run-time 30s --headless
```

## Common Scenarios

### Test New Endpoint
```bash
# 1. Run pytest
uv run pytest -v tests/test_users.py

# 2. Run schemathesis
st run http://localhost:8000/openapi.json

# 3. Verify no failures
```

### Performance Check
```bash
# Quick load test (10 users, 30 seconds)
uv run locust -f locustfile.py --host=http://localhost:8000 \
  --users 10 --spawn-rate 2 --run-time 30s --headless
```

### Debug Failed Test
```bash
# Run with verbose output
uv run pytest -vv tests/test_users.py::test_users_endpoints

# Check server logs in FastAPI terminal
```

## Useful Flags

### Pytest
- `-v` - Verbose output
- `-vv` - Extra verbose
- `-k pattern` - Run tests matching pattern
- `-x` - Stop on first failure
- `--pdb` - Drop into debugger on failure

### Schemathesis
- `--checks all` - Run all checks
- `--max-examples 100` - Generate more test cases
- `--seed 12345` - Reproducible tests

### Locust
- `--users N` - Number of simulated users
- `--spawn-rate N` - Users to add per second
- `--run-time Nm` - Run for N minutes
- `--headless` - No web UI
- `--html report.html` - Generate HTML report
- `--csv results` - Generate CSV report
