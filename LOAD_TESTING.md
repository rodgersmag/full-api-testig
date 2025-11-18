# Load Testing with Locust

This guide explains how to perform load testing on the FastAPI application using Locust.

## Table of Contents
1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Load Test Scenarios](#load-test-scenarios)
4. [Running Tests](#running-tests)
5. [Interpreting Results](#interpreting-results)
6. [Best Practices](#best-practices)

---

## Installation

Locust is already installed if you've set up the project dependencies:

```bash
uv add locust
```

Or with pip:
```bash
pip install locust
```

---

## Quick Start

### 1. Start the FastAPI Server
```bash
uv run fastapi dev main.py
```

The server will run on `http://localhost:8000`

### 2. Run Locust with Web UI
```bash
cd backend
locust -f locustfile.py --host=http://localhost:8000
```

### 3. Open Locust Web Interface
Navigate to `http://localhost:8089` in your browser.

### 4. Configure and Start Test
- **Number of users**: Total users to simulate (e.g., 100)
- **Spawn rate**: Users to add per second (e.g., 10)
- Click **Start Swarming**

---

## Load Test Scenarios

Our `locustfile.py` includes two user types:

### 1. `APIUser` - Realistic User Simulation

Simulates realistic API usage patterns with the following tasks:

#### User Endpoints (Weight)
- `list_users` (2x) - GET /users/
- `create_user` (3x) - POST /users/
- `get_user` (2x) - GET /users/{user_id}
- `update_user` (1x) - PATCH /users/{user_id}
- `delete_user` (1x) - DELETE /users/{user_id}

#### Blog Post Endpoints (Weight)
- `list_posts` (2x) - GET /posts/
- `create_post` (3x) - POST /posts/
- `get_post` (2x) - GET /posts/{post_id}
- `update_post` (1x) - PATCH /posts/{post_id}
- `delete_post` (1x) - DELETE /posts/{post_id}

**Wait Time**: 1-5 seconds between tasks (realistic user behavior)

### 2. `QuickTest` - Stress Test

Rapidly hits endpoints to test high request rates:
- **Very short wait times** (0.1-0.5 seconds)
- **Focus on read operations** (lists)
- **Minimal creates**

Use this to test maximum throughput.

---

## Running Tests

### Interactive Mode (Web UI)

**Basic test:**
```bash
locust -f locustfile.py --host=http://localhost:8000
```

**With specific user class:**
```bash
# Test only realistic users
locust -f locustfile.py --host=http://localhost:8000 --class-picker

# Or specify directly
locust -f locustfile.py --host=http://localhost:8000 --users 100 --spawn-rate 10
```

### Headless Mode (CI/CD)

**Quick test (1 minute, 50 users):**
```bash
locust -f locustfile.py \
  --host=http://localhost:8000 \
  --users 50 \
  --spawn-rate 5 \
  --run-time 1m \
  --headless \
  --html report.html
```

**Stress test (5 minutes, 200 users):**
```bash
locust -f locustfile.py \
  --host=http://localhost:8000 \
  --users 200 \
  --spawn-rate 20 \
  --run-time 5m \
  --headless \
  --html stress-test-report.html \
  --csv stress-test
```

**Specific user class:**
```bash
# Test only QuickTest users
locust -f locustfile.py \
  --host=http://localhost:8000 \
  --users 100 \
  --spawn-rate 50 \
  --run-time 2m \
  --headless \
  --user-class QuickTest \
  --html quick-test-report.html
```

### Advanced Options

**Custom spawn pattern:**
```bash
locust -f locustfile.py \
  --host=http://localhost:8000 \
  --users 100 \
  --spawn-rate 10 \
  --run-time 10m \
  --headless \
  --step-load \
  --step-users 10 \
  --step-time 1m
```

**Distributed load testing (multiple workers):**
```bash
# Master
locust -f locustfile.py --master --expect-workers 4

# Workers (run in separate terminals)
locust -f locustfile.py --worker --master-host=localhost
locust -f locustfile.py --worker --master-host=localhost
locust -f locustfile.py --worker --master-host=localhost
locust -f locustfile.py --worker --master-host=localhost
```

---

## Interpreting Results

### Web UI Metrics

When viewing `http://localhost:8089`, you'll see:

#### Statistics Tab
- **Requests/s**: Current request rate
- **Failures/s**: Current failure rate
- **Response Time (ms)**: Median, 95th percentile, 99th percentile
- **Request Count**: Total requests made
- **Failure %**: Percentage of failed requests

#### Charts Tab
- **Total Requests per Second**: Graph of request throughput
- **Response Times**: Percentile distribution over time
- **Number of Users**: User count over time

#### Failures Tab
- Lists all failed requests with error messages
- Grouped by endpoint and error type

### Key Metrics to Watch

#### 1. **Response Time**
- **Good**: < 100ms (median), < 500ms (95th percentile)
- **Acceptable**: < 500ms (median), < 2000ms (95th percentile)
- **Poor**: > 1000ms (median)

#### 2. **Throughput**
- Monitor **Requests/s** to see max capacity
- Look for plateau - indicates bottleneck

#### 3. **Failure Rate**
- **Target**: < 1% failures
- **Investigation needed**: > 5% failures
- **System overload**: > 10% failures

#### 4. **Error Types**
- **404**: Expected for deleted resources
- **422**: Validation errors (should be low)
- **500**: Server errors (investigate immediately)
- **Connection errors**: Server crashed or overloaded

### HTML Reports

After headless run, open `report.html`:

```bash
open report.html  # macOS
xdg-open report.html  # Linux
start report.html  # Windows
```

Contains:
- Full statistics table
- Response time graphs
- Failure summary
- Test configuration details

### CSV Reports

Generated with `--csv` flag:
- `{name}_stats.csv` - Request statistics
- `{name}_stats_history.csv` - Time series data
- `{name}_failures.csv` - Failure details

Use for:
- Long-term trend analysis
- Comparing test runs
- Creating custom visualizations

---

## Best Practices

### 1. **Start Small**
```bash
# Start with low load
locust -f locustfile.py --host=http://localhost:8000 --users 10 --spawn-rate 2
```

### 2. **Gradually Increase Load**
```bash
# Incrementally increase users
--users 10 → --users 50 → --users 100 → --users 200
```

### 3. **Monitor System Resources**
```bash
# In another terminal, monitor:
top  # CPU and memory
htop  # Better visualization
# Or use Activity Monitor (macOS) / Task Manager (Windows)
```

### 4. **Test Realistic Scenarios**
- Use `APIUser` for normal load simulation
- Use `QuickTest` for stress testing
- Mix both for comprehensive testing

### 5. **Run Tests Multiple Times**
```bash
# Run 3 times and average results
for i in {1..3}; do
  locust -f locustfile.py --host=http://localhost:8000 \
    --users 100 --spawn-rate 10 --run-time 2m \
    --headless --html report-$i.html
  sleep 30  # Cool down between runs
done
```

### 6. **Clean Database Between Tests**
Our in-memory database persists during tests. For consistent results:
- Restart FastAPI server between major test runs
- Or implement a cleanup endpoint

### 7. **Test Different Endpoints Separately**

**Users only:**
```python
# Modify locustfile.py to comment out post tasks
```

**Posts only:**
```python
# Modify locustfile.py to comment out user tasks
```

### 8. **Use Distributed Mode for High Load**
For testing > 1000 users, use distributed mode:
```bash
# Run multiple workers as shown in Advanced Options
```

---

## Troubleshooting

### Issue: Connection Refused
**Cause**: FastAPI server not running
**Solution**: 
```bash
uv run fastapi dev main.py
```

### Issue: High Failure Rate
**Cause**: Server overloaded or validation errors
**Solution**:
- Check Failures tab in Locust UI
- Reduce user count
- Check FastAPI logs

### Issue: Slow Response Times
**Cause**: CPU/memory bottleneck, inefficient code
**Solution**:
- Monitor system resources
- Profile code with `py-spy` or `cProfile`
- Optimize database queries (when using real DB)

### Issue: Locust Process Crashes
**Cause**: Too many users on single Locust instance
**Solution**:
- Use distributed mode
- Reduce user count
- Increase system resources

---

## Example Test Scenarios

### Scenario 1: Baseline Performance Test
```bash
# Measure normal operating capacity
locust -f locustfile.py \
  --host=http://localhost:8000 \
  --users 50 \
  --spawn-rate 5 \
  --run-time 5m \
  --headless \
  --html baseline-report.html
```

**Expected Results:**
- Response times: < 100ms median
- Throughput: > 100 req/s
- Failure rate: < 1%

### Scenario 2: Stress Test
```bash
# Find breaking point
locust -f locustfile.py \
  --host=http://localhost:8000 \
  --users 500 \
  --spawn-rate 50 \
  --run-time 3m \
  --headless \
  --html stress-report.html
```

**Watch for:**
- When response times start degrading
- Maximum sustainable throughput
- Failure rate threshold

### Scenario 3: Spike Test
```bash
# Sudden traffic increase
locust -f locustfile.py \
  --host=http://localhost:8000 \
  --users 200 \
  --spawn-rate 100 \
  --run-time 2m \
  --headless
```

**Tests:**
- How API handles sudden load
- Recovery time
- Error handling

### Scenario 4: Endurance Test
```bash
# Long-running test for memory leaks
locust -f locustfile.py \
  --host=http://localhost:8000 \
  --users 30 \
  --spawn-rate 3 \
  --run-time 30m \
  --headless \
  --html endurance-report.html
```

**Monitor:**
- Memory usage over time
- Response time degradation
- Any resource leaks

---

## Next Steps

1. **Run baseline test** to establish normal performance
2. **Identify bottlenecks** using profiling tools
3. **Optimize code** based on results
4. **Add real database** and test performance
5. **Implement caching** for frequently accessed data
6. **Add rate limiting** to protect against abuse
7. **Test in production-like environment** (not localhost)

---

*Last Updated: 2025-11-18*
