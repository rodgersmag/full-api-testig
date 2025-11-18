import re
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator, ConfigDict

# ASCII-only patterns (following FASTAPI_ASSISTANT_PROMPT.md rules)
TITLE_PATTERN = r'^[A-Za-z0-9 \'\"\-\!\?\.\,\:\;]+$'  # Explicit ASCII chars
SLUG_PATTERN = r'^[a-z0-9]+(?:-[a-z0-9]+)*$'  # kebab-case, ASCII only
EXCERPT_PATTERN = r'^[A-Za-z0-9 \'\"\-\!\?\.\,\:\;\n]+$'  # Text with newlines
CONTENT_PATTERN = r'^[\w\W]+$'  # Any content (we'll rely on length validation)


def utc_now() -> datetime:
    """Get current UTC time with timezone info."""
    return datetime.now(timezone.utc)


class BlogPostBase(BaseModel):
    """Base model with common fields."""
    id: UUID = Field(default_factory=uuid4)
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Post title"
    )
    slug: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="URL-friendly slug (kebab-case)",
        pattern=SLUG_PATTERN
    )
    excerpt: Optional[str] = Field(
        None,
        max_length=500,
        description="Optional short excerpt/teaser"
    )
    content: str = Field(
        ...,
        min_length=10,
        max_length=10000,
        description="Full markdown/HTML content"
    )
    is_published: bool = Field(False, description="Published status", strict=True)
    author_id: UUID = Field(..., description="Author UUID")
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class BlogPostCreate(BaseModel):
    """Request body for creating a new blog post."""
    
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Post title",
        pattern=TITLE_PATTERN
    )
    
    slug: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="URL-friendly slug (kebab-case)",
        pattern=SLUG_PATTERN
    )
    
    excerpt: Optional[str] = Field(
        None,
        max_length=500,
        description="Optional short excerpt/teaser",
        pattern=EXCERPT_PATTERN
    )
    
    content: str = Field(
        ...,
        min_length=10,
        max_length=10000,
        description="Full markdown/HTML content"
    )
    
    is_published: bool = Field(False, description="Publish immediately?", strict=True)
    author_id: UUID = Field(..., description="Author UUID")

    # Validators MUST match schema exactly (not stricter!)
    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v: str) -> str:
        if not re.match(SLUG_PATTERN, v):
            raise ValueError("Slug must be kebab-case with ASCII letters, numbers, and hyphens only")
        return v

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        if not re.match(TITLE_PATTERN, v):
            raise ValueError("Title contains forbidden characters")
        return v

    @field_validator("excerpt")
    @classmethod
    def validate_excerpt(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not re.match(EXCERPT_PATTERN, v):
            raise ValueError("Excerpt contains forbidden characters")
        return v

    # Forbid unknown fields (Schemathesis will send random extras!)
    model_config = ConfigDict(extra="forbid")


class BlogPostUpdate(BaseModel):
    """Partial update for blog posts (all fields optional)."""
    
    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=200,
        pattern=TITLE_PATTERN
    )
    slug: Optional[str] = Field(
        None,
        min_length=3,
        max_length=100,
        pattern=SLUG_PATTERN
    )
    excerpt: Optional[str] = Field(
        None,
        max_length=500,
        pattern=EXCERPT_PATTERN
    )
    content: Optional[str] = Field(
        None,
        min_length=10,
        max_length=10000
    )
    is_published: Optional[bool] = Field(None, strict=True)
    author_id: Optional[UUID] = None

    # Same validators as create (only run when value is provided)
    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not re.match(SLUG_PATTERN, v):
            raise ValueError("Slug must be kebab-case with ASCII letters, numbers, and hyphens only")
        return v

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not re.match(TITLE_PATTERN, v):
            raise ValueError("Title contains forbidden characters")
        return v

    @field_validator("excerpt")
    @classmethod
    def validate_excerpt(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not re.match(EXCERPT_PATTERN, v):
            raise ValueError("Excerpt contains forbidden characters")
        return v

    model_config = ConfigDict(extra="forbid")


class BlogPostRead(BaseModel):
    """Response model - no sensitive data."""
    id: UUID
    title: str
    slug: str
    excerpt: Optional[str] = None
    content: str
    is_published: bool
    author_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
