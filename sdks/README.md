# Client SDKs

This directory contains auto-generated client SDKs for the FastAPI application.

## 📦 Available SDKs

All SDKs are generated using **Swagger Codegen v3** and are located in the `swagger-codegen/` directory.

| Language | Location | Build Tool | Status |
|----------|----------|------------|--------|
| **TypeScript** | `swagger-codegen/typescript/` | npm | ✅ |
| **Python** | `swagger-codegen/python/` | pip | ✅ |
| **Swift** | `swagger-codegen/swift/` | CocoaPods | ✅ |
| **HTTP Client** | `swagger-codegen/api-client.http` | VS Code/IntelliJ | ✅ |

## 🚀 Quick Start

### HTTP Client (Easiest)

**For manual testing and exploration:**

1. Open `swagger-codegen/api-client.http` in VS Code or IntelliJ
2. Install REST Client extension (VS Code) or use built-in HTTP client (IntelliJ)
3. Click "Send Request" above any endpoint
4. All 10 endpoints documented with examples!

### TypeScript

```bash
cd swagger-codegen/typescript
npm install
```

```typescript
import { DefaultApi } from './api';

const api = new DefaultApi();
const user = await api.createUserUsersPost({
  userCreate: {
    email: "test@example.com",
    password: "SecurePass123!"
  }
});
```

### Python

```bash
cd swagger-codegen/python
pip install -e .
```

```python
from swagger_client.api.default_api import DefaultApi
from swagger_client.models import UserCreate

api = DefaultApi()
user = api.create_user_users_post(
    user_create=UserCreate(
        email="test@example.com",
        password="SecurePass123!"
    )
)
```

### Swift

```bash
cd swagger-codegen/swift
pod install
```

```swift
import SwaggerClient

SwaggerClientAPI.basePath = "http://localhost:8000"

let userCreate = UserCreate(
    email: "test@example.com",
    password: "SecurePass123!"
)

DefaultAPI.createUserUsersPost(userCreate: userCreate) { response, error in
    if let user = response {
        print("Created user: \(user)")
    }
}
```

## 📖 Documentation

For detailed documentation, usage examples, and advanced configuration:

**👉 See [`swagger-codegen/README.md`](swagger-codegen/README.md)**

This includes:
- Installation instructions for all SDKs
- Complete usage examples
- HTTP Client guide
- SDK generation commands
- Customization options
- Troubleshooting
- CI/CD integration

## 🔄 Regenerating SDKs

If the API changes, regenerate SDKs using Docker:

```bash
# Export OpenAPI schema
curl http://localhost:8000/openapi.json > openapi.json

# TypeScript
docker run --rm -v ${PWD}:/local \
  swaggerapi/swagger-codegen-cli-v3 generate \
  -i /local/openapi.json \
  -l typescript-fetch \
  -o /local/sdks/swagger-codegen/typescript

# Python
docker run --rm -v ${PWD}:/local \
  swaggerapi/swagger-codegen-cli-v3 generate \
  -i /local/openapi.json \
  -l python \
  -o /local/sdks/swagger-codegen/python

# Swift
docker run --rm -v ${PWD}:/local \
  swaggerapi/swagger-codegen-cli-v3 generate \
  -i /local/openapi.json \
  -l swift5 \
  -o /local/sdks/swagger-codegen/swift
```

**📋 List all 40+ available languages:**
```bash
docker run --rm swaggerapi/swagger-codegen-cli-v3 langs
```

## 🎯 API Endpoints

All SDKs cover these 10 endpoints:

**Users:**
- `POST /users/` - Create user
- `GET /users/` - List users
- `GET /users/{user_id}` - Get user
- `PATCH /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user

**Blog Posts:**
- `POST /posts/` - Create post
- `GET /posts/` - List posts
- `GET /posts/{post_id}` - Get post
- `PATCH /posts/{post_id}` - Update post
- `DELETE /posts/{post_id}` - Delete post

## ✨ Features

All SDKs include:

- ✅ **Type Safety** - Full type definitions for all models
- ✅ **Validation** - Request/response validation
- ✅ **Error Handling** - Typed error responses
- ✅ **Documentation** - Inline docs from OpenAPI spec
- ✅ **Enterprise Ready** - Battle-tested code generation

## 📦 Why Swagger Codegen?

- **40+ languages** supported
- **Enterprise-ready** and battle-tested
- **Stable CI/CD** integration
- **Template customization** for specific needs
- **Wide adoption** in industry

## 🔗 Resources

- **Main Documentation**: `swagger-codegen/README.md`
- **API Docs**: `http://localhost:8000/docs` (when server is running)
- **OpenAPI Spec**: `http://localhost:8000/openapi.json`
- **Swagger Codegen**: https://github.com/swagger-api/swagger-codegen

---

**Generated with**: Swagger Codegen CLI v3  
**OpenAPI Version**: 3.1.0

*Last Updated: 2025-11-19*
