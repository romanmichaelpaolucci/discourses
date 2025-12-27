"""
Discourses - Official Python SDK

Institutional-grade financial sentiment analysis with era-calibrated lexicons.

Basic Usage:
    >>> from discourses import Discourses
    >>> 
    >>> client = Discourses(api_key="your-api-key")
    >>> 
    >>> # Analyze single text
    >>> result = client.analyze("Strong growth with excellent outlook")
    >>> print(f"Label: {result.label}, Outlook: {result.outlook:.2f}")
    >>> 
    >>> # Compare across eras
    >>> comparison = client.compare_eras("Diamond hands!", eras=["primitive", "meme"])
    >>> for era, data in comparison.results.items():
    ...     print(f"{era}: {data['classification']['label']}")
    >>> 
    >>> # Batch analysis
    >>> texts = [{"id": "1", "text": "Bullish!"}, {"id": "2", "text": "Bearish..."}]
    >>> batch = client.batch(texts, era="meme")

For more information, visit https://discourses.io/documentation
"""

__version__ = "1.1.4"
__author__ = "discourses.io"
__email__ = "support@discourses.io"

# Main client
from discourses.client import Discourses

# Constants and enums
from discourses.constants import Era, BASE_URL

# Exception classes
from discourses.exceptions import (
    DiscoursesError,
    APIError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    ResourceNotFoundError,
)

# Response models
from discourses.models import (
    AnalysisResult,
    CompareResult,
    BatchResult,
)

# Public API
__all__ = [
    # Version info
    "__version__",
    "__author__",
    "__email__",
    # Main client
    "Discourses",
    # Enums
    "Era",
    # Constants
    "BASE_URL",
    # Exceptions
    "DiscoursesError",
    "APIError",
    "AuthenticationError",
    "RateLimitError",
    "ValidationError",
    "ResourceNotFoundError",
    # Models
    "AnalysisResult",
    "CompareResult",
    "BatchResult",
]
