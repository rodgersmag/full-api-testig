import re
from datetime import UTC, datetime
from typing import Optional, List
from uuid import UUID, uuid4
from enum import Enum

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    SecretStr,
    field_validator,
)

class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"

# Password pattern - matches EXACTLY what we validate
# Uses ASCII-only character classes to avoid Unicode digit issues
PASSWORD_PATTERN = r'^[A-Za-z0-9@$!%*?&]{8,128}$'

def validate_password_complexity(v: Optional[SecretStr]) -> Optional[SecretStr]:
    """Shared password validation logic - matches schema exactly."""
    if v is None:
        return v
    
    value = v.get_secret_value()
    
    # Check length
    if len(value) < 8 or len(value) > 128:
        raise ValueError('Password must be between 8 and 128 characters')
    
    # Check allowed characters - ASCII only, no Unicode digits
    # This MUST match the JSON Schema pattern exactly
    if not re.match(r'^[A-Za-z0-9@$!%*?&]+$', value):
        raise ValueError('Password contains invalid characters. Only A-Z, a-z, 0-9, @$!%*?& are allowed')
    
    return v

class UserQueryParams(BaseModel):
    skip: int = Field(default=0, ge=0, description="Number of records to skip")
    limit: int = Field(default=100, ge=1, le=1000, description="Maximum records to return")
    
    model_config = {
        "json_schema_extra": {
            "examples": [{"skip": 0, "limit": 100}]
        }
    }

class UserBase(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    email: EmailStr
    # Include pattern in schema to guide test data generation
    # Note: StringConstraints doesn't work well with SecretStr in Pydantic v2
    # Use Field with json_schema_extra instead
    password: SecretStr = Field(
        ...,
        min_length=8,
        max_length=128,
        json_schema_extra={
            "pattern": PASSWORD_PATTERN,
            "format": None
        }
    )
    role: UserRole = Field(default=UserRole.USER)
    is_active: bool = Field(default=True)
    first_name: Optional[str] = Field(None, max_length=100, pattern=r'^[A-Za-z \'\-]+$')
    last_name: Optional[str] = Field(None, max_length=100, pattern=r'^[A-Za-z \'\-]+$')

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: SecretStr) -> SecretStr:
        return validate_password_complexity(v)

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
                "email": "email@example.com",
                "role": "USER",
                "is_active": True,
                "password": "SecurePassword123@!",
                "first_name": "John",
                "last_name": "Doe",
            }]
        }
    }

class UserCreate(BaseModel):
    email: EmailStr
    # Schema includes pattern for better test data generation
    # Note: StringConstraints doesn't work well with SecretStr in Pydantic v2
    password: SecretStr = Field(
        ...,
        min_length=8,
        max_length=128,
        json_schema_extra={
            "pattern": PASSWORD_PATTERN,
            "format": None  # Remove format:password to match our actual validation
        }
    )
    first_name: Optional[str] = Field(None, max_length=100, pattern=r'^[A-Za-z \'\-]+$')
    last_name: Optional[str] = Field(None, max_length=100, pattern=r'^[A-Za-z \'\-]+$')

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: SecretStr) -> SecretStr:
        return validate_password_complexity(v)

    model_config = ConfigDict(extra='forbid')  # Reject additional properties


class UserRead(BaseModel):
    """User model for API responses - excludes password field from serialization."""
    id: UUID
    email: EmailStr
    role: UserRole
    is_active: bool
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[SecretStr] = Field(
        None,
        min_length=8,
        max_length=128,
        json_schema_extra={
            "pattern": PASSWORD_PATTERN,
            "format": None
        }
    )
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    first_name: Optional[str] = Field(None, max_length=100, pattern=r'^[A-Za-z \'\-]+$')
    last_name: Optional[str] = Field(None, max_length=100, pattern=r'^[A-Za-z \'\-]+$')

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: Optional[SecretStr]) -> Optional[SecretStr]:
        return validate_password_complexity(v)

    model_config = ConfigDict(
        extra='forbid',  # Reject additional properties to avoid conflicts
        json_schema_extra={
            "examples": [{
                "email": "updated@example.com",
                "is_active": False,
            }]
        }
    )


class UserDelete(BaseModel):
    id: UUID