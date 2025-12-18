"""
Exceptions for the Discourses SDK.

This module defines custom exception classes for handling various
API error conditions in a type-safe manner.
"""

from typing import Any, Dict, Optional


class DiscoursesError(Exception):
    """
    Base exception for all Discourses SDK errors.
    
    All custom exceptions inherit from this class, allowing you to catch
    all SDK-related errors with a single except clause.
    
    Attributes:
        message: Human-readable error description
        status_code: HTTP status code (if applicable)
        response: Raw API response data (if available)
    
    Example:
        >>> try:
        ...     result = client.analyze("text")
        ... except DiscoursesError as e:
        ...     print(f"Error: {e.message}")
    """
    
    def __init__(
        self,
        message: str = "An error occurred",
        status_code: Optional[int] = None,
        response: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.response = response or {}
        super().__init__(message)
    
    def __str__(self) -> str:
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(message='{self.message}', status_code={self.status_code})"


class APIError(DiscoursesError):
    """
    General API error for unexpected responses.
    
    Raised when the API returns an error that doesn't fit into
    more specific exception categories (500 errors, network issues, etc.)
    
    Example:
        >>> try:
        ...     result = client.analyze("text")
        ... except APIError as e:
        ...     print(f"API Error: {e}")
        ...     # Implement retry logic
    """
    pass


class AuthenticationError(DiscoursesError):
    """
    Raised when API authentication fails.
    
    This typically indicates an invalid, expired, or missing API key.
    Check your API key at https://discourses.io/dashboard
    
    Common causes:
        - Invalid API key
        - Expired API key
        - API key not provided
        - Account suspended
    
    Example:
        >>> try:
        ...     client = Discourses(api_key="invalid")
        ...     result = client.analyze("text")
        ... except AuthenticationError as e:
        ...     print("Check your API key at https://discourses.io/dashboard")
    """
    
    def __init__(
        self,
        message: str = "Authentication failed",
        status_code: int = 401,
        response: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, status_code, response)


class RateLimitError(DiscoursesError):
    """
    Raised when API rate limits are exceeded.
    
    Includes information about when you can retry the request.
    Consider upgrading your plan for higher rate limits.
    
    Attributes:
        retry_after: Seconds until rate limit resets (if provided)
    
    Example:
        >>> try:
        ...     result = client.analyze("text")
        ... except RateLimitError as e:
        ...     if e.retry_after:
        ...         time.sleep(e.retry_after)
        ...     # Retry the request
    """
    
    def __init__(
        self,
        message: str = "Rate limit exceeded",
        status_code: int = 429,
        response: Optional[Dict[str, Any]] = None,
        retry_after: Optional[int] = None,
    ) -> None:
        super().__init__(message, status_code, response)
        self.retry_after = retry_after
    
    def __str__(self) -> str:
        base = super().__str__()
        if self.retry_after:
            return f"{base} (retry after {self.retry_after}s)"
        return base


class ValidationError(DiscoursesError):
    """
    Raised when request validation fails.
    
    This indicates an issue with the data sent to the API,
    such as empty text, invalid era, or malformed request.
    
    Common causes:
        - Empty or whitespace-only text
        - Text exceeding length limits
        - Invalid era specification
        - Missing required fields
    
    Example:
        >>> try:
        ...     result = client.analyze("")  # Empty text
        ... except ValidationError as e:
        ...     print(f"Invalid input: {e.message}")
    """
    
    def __init__(
        self,
        message: str = "Validation failed",
        status_code: Optional[int] = 400,
        response: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, status_code, response)


class ResourceNotFoundError(DiscoursesError):
    """
    Raised when a requested resource is not found.
    
    Example:
        >>> try:
        ...     result = client.get_analysis("nonexistent-id")
        ... except ResourceNotFoundError as e:
        ...     print("Analysis not found")
    """
    
    def __init__(
        self,
        message: str = "Resource not found",
        status_code: int = 404,
        response: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, status_code, response)
