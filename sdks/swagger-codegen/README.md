# Swagger Codegen SDKs

This directory contains client SDKs generated using [Swagger Codegen v3](https://github.com/swagger-api/swagger-codegen).

**⚡ Quick Start**: For manual testing, check out [`api-client.http`](api-client.http) - a comprehensive HTTP client file with all endpoints ready to use in VS Code or IntelliJ!


## Generated SDKs

| Language | Directory | Build Tool | Status |
|----------|-----------|------------|--------|
| **TypeScript** | `typescript/` | npm | ✅ Generated |
| **Python** | `python/` | pip | ✅ Generated |
| **Swift** | `swift/` | CocoaPods | ✅ Generated |
| **HTTP Client** | `api-client.http` | VS Code/IntelliJ | ✅ Ready |


## Why Swagger Codegen?

While we also provide modern SDKs (using `@hey-api/openapi-ts`, `openapi-python-client`, etc.), Swagger Codegen offers:

- **Wide language support** (40+ languages)
- **Enterprise-ready** with mature, battle-tested code generation
- **Java ecosystem** support (Maven, Gradle, Android)
- **Customizable templates** for specific needs
- **Stable API** for CI/CD pipelines

## Prerequisites

**Docker** must be installed to run Swagger Codegen:
```bash
docker --version
```

If Docker is not installed: https://docs.docker.com/get-docker/

## Generation Commands

### TypeScript
```bash
docker run --rm -v ${PWD}:/local \
  swaggerapi/swagger-codegen-cli-v3 generate \
  -i /local/openapi.json \
  -l typescript-fetch \
  -o /local/sdks/swagger-codegen/typescript
```

### Python
```bash
docker run --rm -v ${PWD}:/local \
  swaggerapi/swagger-codegen-cli-v3 generate \
  -i /local/openapi.json \
  -l python \
  -o /local/sdks/swagger-codegen/python
```

### Swift
```bash
docker run --rm -v ${PWD}:/local \
  swaggerapi/swagger-codegen-cli-v3 generate \
  -i /local/openapi.json \
  -l swift5 \
  -o /local/sdks/swagger-codegen/swift
```

### Java
```bash
docker run --rm -v ${PWD}:/local \
  swaggerapi/swagger-codegen-cli-v3 generate \
  -i /local/openapi.json \
  -l java \
  -o /local/sdks/swagger-codegen/java
```

### Other Languages

List all available languages:
```bash
docker run --rm swaggerapi/swagger-codegen-cli-v3 langs
```

Available: `dart`, `aspnetcore`, `csharp`, `go`, `java`, `javascript`, `kotlin-client`, `kotlin-server`, `php`, `python-flask`, `r`, `ruby`, `scala`, `swift3`, `swift4`, `swift5`, `typescript-angular`, `typescript-axios`, `typescript-fetch`, and more!

Generate for any language:
```bash
docker run --rm -v ${PWD}:/local \
  swaggerapi/swagger-codegen-cli-v3 generate \
  -i /local/openapi.json \
  -l <LANGUAGE> \
  -o /local/sdks/swagger-codegen/<LANGUAGE>
```

## Usage Examples

### TypeScript

**Install:**
```bash
cd sdks/swagger-codegen/typescript
npm install
```

**Usage:**
```typescript
import { DefaultApi } from './api';

const api = new DefaultApi();

// Create a user
const user = await api.createUserUsersPost({
  userCreate: {
    email: "test@example.com",
    password: "SecurePass123!"
  }
});
```

### Python

**Install:**
```bash
cd sdks/swagger-codegen/python
pip install -e .
```

**Usage:**
```python
from swagger_client import ApiClient, Configuration
from swagger_client.api.default_api import DefaultApi
from swagger_client.models import UserCreate

# Configure API client
config = Configuration()
config.host = "http://localhost:8000"

api_client = ApiClient(configuration=config)
api = DefaultApi(api_client)

# Create a user
user_data = UserCreate(
    email="test@example.com",
    password="SecurePass123!"
)
user = api.create_user_users_post(user_create=user_data)
```

### Swift

**Install:**
```bash
cd sdks/swagger-codegen/swift
pod install
```

**Usage:**
```swift
import SwaggerClient

// Configure API
SwaggerClientAPI.basePath = "http://localhost:8000"

// Create a user
let userCreate = UserCreate(
    email: "test@example.com",
    password: "SecurePass123!"
)

DefaultAPI.createUserUsersPost(userCreate: userCreate) { response, error in
    if let user = response {
        print("Created user: \\(user)")
    }
}
```

### HTTP Client

The HTTP Client file (`api-client.http`) provides ready-to-use examples for all API endpoints.

**Tools Supported:**
- VS Code REST Client extension
- IntelliJ IDEA HTTP Client  
- JetBrains IDEs (PyCharm, WebStorm, GoLand, etc.)
- HTTPie / curl (copy-paste examples)

**Installation (VS Code):**
1. Install the [REST Client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client)
2. Open `sdks/swagger-codegen/api-client.http`
3. Click "Send Request" above any endpoint

**Installation (IntelliJ IDEA):**
1. Built-in support (no installation needed)
2. Open `sdks/swagger-codegen/api-client.http`
3. Click the ▶ icon next to any request

**Features:**
- ✅ All 10 API endpoints documented
- ✅ CRUD operations for Users and Blog Posts
- ✅ Complete workflow examples
- ✅ Error testing scenarios
- ✅ Pagination examples
- ✅ Bulk operation patterns
- ✅ Operation IDs matching generated SDKs

**Quick Example:**
```http
### Create a new user
POST http://localhost:8000/users/
Content-Type: application/json

{
  "email": "test@example.com",
  "password": "SecurePass123!",
  "first_name": "Test",
  "last_name": "User"
}

### List all users
GET http://localhost:8000/users/?skip=0&limit=10
```

**Using with curl:**
```bash
# Copy any request from api-client.http and convert to curl:
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"SecurePass123!"}'
```

**Using with HTTPie:**
```bash
# Install HTTPie
pip install httpie

# Make requests
http POST http://localhost:8000/users/ \
  email="test@example.com" \
  password="SecurePass123!"
```

**Variable Substitution:**
The HTTP file includes variables for easy customization:
- `{{baseUrl}}` - API base URL (default: `http://localhost:8000`)
- `{{contentType}}` - Content type (default: `application/json`)
- `{{userId}}` - User ID for operations
- `{{postId}}` - Post ID for operations
- `{{authorId}}` - Author ID for blog posts

**Advanced Usage:**
```http
# Define custom variables in VS Code settings.json
{
  "rest-client.environmentVariables": {
    "local": {
      "baseUrl": "http://localhost:8000"
    },
    "production": {
      "baseUrl": "https://api.example.com"
    }
  }
}
```

---

## Advanced Configuration

### Custom Package Names

**Python:**
```bash
docker run --rm -v ${PWD}:/local \
  swaggerapi/swagger-codegen-cli-v3 generate \
  -i /local/openapi.json \
  -l python \
  -o /local/sdks/swagger-codegen/python \
  --additional-properties=packageName=fastapi_client
```

**Java:**
```bash
docker run --rm -v ${PWD}:/local \
  swaggerapi/swagger-codegen-cli-v3 generate \
  -i /local/openapi.json \
  -l java \
  -o /local/sdks/swagger-codegen/java \
  --additional-properties=groupId=com.example,artifactId=fastapi-client,apiPackage=com.example.api
```

### Configuration Files

You can use config files for complex setups:

**swagger-config.json:**
```json
{
  "packageName": "fastapi_client",
  "packageVersion": "1.0.0",
  "projectName": "FastAPI Client"
}
```

Then generate:
```bash
docker run --rm -v ${PWD}:/local \
  swaggerapi/swagger-codegen-cli-v3 generate \
  -i /local/openapi.json \
  -l python \
  -o /local/sdks/swagger-codegen/python \
  -c /local/swagger-config.json
```

### Help and Options

**Get help for a specific generator:**
```bash
docker run --rm swaggerapi/swagger-codegen-cli-v3 config-help -l python
```

**See all options:**
```bash
docker run --rm swaggerapi/swagger-codegen-cli-v3 help generate
```

## Comparison: Swagger Codegen vs Modern Tools

| Feature | Swagger Codegen | Modern Tools |
|---------|-----------------|--------------|
| **Languages** | 40+ | Focused (3-5) |
| **Maturity** | Enterprise-ready | Modern, evolving |
| **Java Support** | Excellent | Limited |
| **Async/Await** | Limited | Native support |
| **Bundle Size** | Larger | Smaller, tree-shakeable |
| **Customization** | Template-based | Code-based |
| **Best For** | Enterprise, Java, Legacy | Modern web, async, TypeScript |

## When to Use Swagger Codegen

✅ **Use Swagger Codegen when:**
- You need Java, C#, or other enterprise languages
- Working with legacy systems
- Need OkHttp, Retrofit, or specific HTTP clients
- Require template customization
- Building Android apps

❌ **Use Modern Tools when:**
- Building modern web apps (TypeScript/Python)
- Need smaller bundle sizes
- Want native async/await support
- Prefer tree-shaking and ES modules
- Building iOS apps with Swift async/await

## Troubleshooting

### Docker Permission Denied (Linux)
```bash
sudo usermod -aG docker $USER
# Logout and login again
```

### Generation Fails
```bash
# Validate your OpenAPI schema first
curl http://localhost:8000/openapi.json | jq '.'

# Or use Swagger Editor
# https://editor.swagger.io/
```

### Missing Dependencies
```bash
# Each SDK has a README with installation instructions
cd sdks/swagger-codegen/<language>
cat README.md
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Generate SDKs

on:
  push:
    branches: [main]

jobs:
  generate-sdks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Start API server
        run: |
          cd backend
          pip install -r requirements.txt
          uvicorn main:app --host 0.0.0.0 --port 8000 &
          sleep 5
      
      - name: Export OpenAPI schema
        run: curl http://localhost:8000/openapi.json > openapi.json
      
      - name: Generate TypeScript SDK
        run: |
          docker run --rm -v ${PWD}:/local \
            swaggerapi/swagger-codegen-cli-v3 generate \
            -i /local/openapi.json \
            -l typescript-fetch \
            -o /local/sdks/swagger-codegen/typescript
      
      - name: Generate Python SDK
        run: |
          docker run --rm -v ${PWD}:/local \
            swaggerapi/swagger-codegen-cli-v3 generate \
            -i /local/openapi.json \
            -l python \
            -o /local/sdks/swagger-codegen/python
      
      - name: Commit SDKs
        run: |
          git config --global user.name "GitHub Actions"
          git config --global user.email "actions@github.com"
          git add sdks/
          git commit -m "Auto-generate SDKs" || echo "No changes"
          git push
```

## Resources

- **Swagger Codegen GitHub**: https://github.com/swagger-api/swagger-codegen
- **Documentation**: https://github.com/swagger-api/swagger-codegen/wiki
- **Docker Hub**: https://hub.docker.com/r/swaggerapi/swagger-codegen-cli-v3
- **OpenAPI Specification**: https://swagger.io/specification/

---

**Generated with**: Swagger Codegen CLI v3  
**Based on**: OpenAPI 3.1.0 Specification

*For modern SDK alternatives, see `../README.md`*
