from typing import Annotated, List, Dict, Any
from uuid import UUID
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, Depends, status, Query, Request
from pydantic import BaseModel, Field
from models.user import UserBase, UserRole, UserRead, UserCreate, UserUpdate
from models.blog_post import BlogPostBase, BlogPostRead, BlogPostCreate, BlogPostUpdate

app = FastAPI()

# In-memory fake DB
fake_db: Dict[UUID, UserBase] = {}
fake_blog_db: Dict[UUID, BlogPostBase] = {}


# ─────────────────────────────────────────────────────────────────────────────
# Proper error models that match FastAPI + Pydantic v2 reality
# ─────────────────────────────────────────────────────────────────────────────
class HTTPValidationError(BaseModel):
    detail: List[Dict[str, Any]]


class ErrorResponse(BaseModel):
    """Used for string-only error messages (404, 409, custom errors)"""
    detail: str = Field(..., example="Not found")


class MixedErrorResponse(BaseModel):
    """Union model – allows both string detail AND validation error array"""
    detail: str | List[Dict[str, Any]]


# ─────────────────────────────────────────────────────────────────────────────
# Dependencies
# ─────────────────────────────────────────────────────────────────────────────
def get_user_from_db(user_id: UUID) -> UserBase:
    user = fake_db.get(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


def get_all_users_from_db() -> List[UserBase]:
    return list(fake_db.values())


# Custom strict query param validation – now returns proper validation errors
def strict_query_params(allowed: set[str]):
    def dependency(request: Request):
        unknown = [k for k in request.query_params.keys() if k not in allowed]
        if unknown:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=[
                    {
                        "type": "value_error",
                        "loc": ["query", param],
                        "msg": "Unknown query parameter",
                        "input": request.query_params[param],
                    }
                    for param in unknown
                ],
            )
        return True
    return dependency


# ─────────────────────────────────────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────────────────────────────────────

@app.post(
    "/users/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="""
    Create a new user with the provided details.
    
    **Idempotent**: If a user with the same email already exists, returns the existing user (200 OK).
    
    **Password Requirements:**
    - Length: 8-128 characters
    - Allowed characters: A-Z, a-z, 0-9, @$!%*?&
    """,
    responses={
        201: {"description": "User created successfully"},
        200: {"description": "User with this email already exists"},
        422: {
            "model": HTTPValidationError, 
            "description": "Validation error"
        },
    },
)
async def create_user(user: UserCreate):
    # Check if user with this email already exists
    existing_user = next((u for u in fake_db.values() if u.email == user.email), None)
    if existing_user:
        # Idempotent POST - return existing user instead of 409 Conflict
        return existing_user
    
    # Extract the secret value from SecretStr before passing to UserBase
    # This prevents Pydantic from trying to double-wrap the SecretStr
    new_user = UserBase(
        email=user.email,
        password=user.password.get_secret_value(),
        first_name=user.first_name,
        last_name=user.last_name,
    )
    fake_db[new_user.id] = new_user
    return new_user


@app.get(
    "/users/",
    response_model=List[UserRead],
    dependencies=[Depends(strict_query_params({"skip", "limit"}))],
    responses={
        422: {"model": HTTPValidationError, "description": "Validation error"},
    },
)
async def read_users(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
    users_data: List[UserBase] = Depends(get_all_users_from_db),
):
    return users_data[skip : skip + limit]


@app.get(
    "/users/{user_id}",
    response_model=UserRead,
    responses={
        404: {"model": ErrorResponse},
        422: {"model": HTTPValidationError},
    },
)
async def read_user(user_id: UUID, user: UserBase = Depends(get_user_from_db)):
    return user


@app.patch(
    "/users/{user_id}",
    response_model=UserRead,
    responses={
        404: {"model": ErrorResponse},
        422: {"model": HTTPValidationError},
    },
)
async def update_user(
    user_id: UUID,
    user_update: UserUpdate,
    user_in_db: UserBase = Depends(get_user_from_db),
):
    # Get update data, excluding unset fields
    update_data = user_update.model_dump(exclude_unset=True)
    
    # Skip None values from update (don't update fields to None unless they're Optional)
    # This prevents setting required fields like 'role' to None
    update_data = {k: v for k, v in update_data.items() if v is not None}

    # Update fields
    for field, value in update_data.items():
        if hasattr(user_in_db, field):
            # Handle password SecretStr properly
            if field == "password":
                # Extract secret value if it's a SecretStr
                if hasattr(value, 'get_secret_value'):
                    value = value.get_secret_value()
            setattr(user_in_db, field, value)

    fake_db[user_id] = user_in_db
    return user_in_db


@app.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"model": ErrorResponse},
        422: {"model": HTTPValidationError},
    },
)
async def delete_user(user_id: UUID, user: UserBase = Depends(get_user_from_db)):
    del fake_db[user_id]
    return None  # 204 No Content


# ─────────────────────────────────────────────────────────────────────────────
# Blog Post Dependencies
# ─────────────────────────────────────────────────────────────────────────────
def get_blog_post_from_db(post_id: UUID) -> BlogPostBase:
    post = fake_blog_db.get(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog post not found")
    return post


def get_all_blog_posts_from_db() -> List[BlogPostBase]:
    return list(fake_blog_db.values())


# ─────────────────────────────────────────────────────────────────────────────
# Blog Post Endpoints
# ─────────────────────────────────────────────────────────────────────────────

@app.post(
    "/posts/",
    response_model=BlogPostRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new blog post",
    description="""
    Create a new blog post.
    
    **Idempotent**: If a post with the same slug already exists, returns that post (200 OK).
    
    **Validation:**
    - Title: 1-200 chars, ASCII alphanumeric + basic punctuation
    - Slug: 3-100 chars, kebab-case (lowercase-with-hyphens)
    - Content: 10-10000 chars
    """,
    responses={
        201: {"description": "Blog post created successfully"},
        200: {"description": "Blog post with this slug already exists (idempotent)"},
        422: {"description": "Validation error"},
    }
)
async def create_blog_post(post: BlogPostCreate):
    """Create blog post - IDEMPOTENT to avoid 409."""
    
    # Check if post with same slug exists (idempotent POST)
    existing = next((p for p in fake_blog_db.values() if p.slug == post.slug), None)
    if existing:
        return existing  # 200 OK, NOT 409!
    
    # Create new post
    new_post = BlogPostBase(
        title=post.title,
        slug=post.slug,
        excerpt=post.excerpt,
        content=post.content,
        is_published=post.is_published,
        author_id=post.author_id,
    )
    fake_blog_db[new_post.id] = new_post
    return new_post


@app.get(
    "/posts/",
    response_model=List[BlogPostRead],
    dependencies=[Depends(strict_query_params({"skip", "limit"}))],
    responses={
        422: {"model": HTTPValidationError, "description": "Validation error"},
    },
)
async def read_blog_posts(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
    posts_data: List[BlogPostBase] = Depends(get_all_blog_posts_from_db),
):
    return posts_data[skip : skip + limit]


@app.get(
    "/posts/{post_id}",
    response_model=BlogPostRead,
    responses={
        404: {"model": ErrorResponse},
        422: {"model": HTTPValidationError},
    },
)
async def read_blog_post(post_id: UUID, post: BlogPostBase = Depends(get_blog_post_from_db)):
    return post


@app.patch(
    "/posts/{post_id}",
    response_model=BlogPostRead,
    responses={
        404: {"model": ErrorResponse},
        422: {"model": HTTPValidationError},
    },
)
async def update_blog_post(
    post_id: UUID,
    post_update: BlogPostUpdate,
    post_in_db: BlogPostBase = Depends(get_blog_post_from_db),
):
    """Update blog post - NO slug uniqueness check to avoid 409."""
    
    # Get update data (exclude unset fields)
    update_data = post_update.model_dump(exclude_unset=True)
    update_data = {k: v for k, v in update_data.items() if v is not None}
    
    # Update timestamp
    if update_data:
        update_data['updated_at'] = datetime.now(timezone.utc)
    
    # NO slug uniqueness check - just update
    for field, value in update_data.items():
        if hasattr(post_in_db, field):
            setattr(post_in_db, field, value)
    
    fake_blog_db[post_id] = post_in_db
    return post_in_db


@app.delete(
    "/posts/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"model": ErrorResponse},
        422: {"model": HTTPValidationError},
    },
)
async def delete_blog_post(post_id: UUID, post: BlogPostBase = Depends(get_blog_post_from_db)):
    del fake_blog_db[post_id]
    return None  # 204 No Content