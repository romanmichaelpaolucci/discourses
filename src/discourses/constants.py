"""
Constants for the Discourses SDK.

This module defines API configuration values, endpoints, and enumerations
used throughout the SDK.
"""

from enum import Enum


# API Configuration
BASE_URL = "https://discourses.io/api/v1"
DEFAULT_TIMEOUT = 30  # seconds


# API Endpoints
ENDPOINTS = {
    "analyze": "/analyze",
    "compare_eras": "/analyze/compare-eras",
    "batch": "/analyze/batch",
}


class Era(str, Enum):
    """
    Financial language eras for sentiment analysis.
    
    Each era captures distinct vocabulary and sentiment patterns
    characteristic of that time period in financial markets.
    
    Attributes:
        PRIMITIVE: Pre-2015 traditional financial vocabulary
                   - Formal market language
                   - Institutional terminology
                   - Pre-social media patterns
        
        MEME: 2015-2021 retail trading revolution
              - WSB culture and terminology
              - Crypto/DeFi vocabulary
              - Emoji-based sentiment (🚀, 💎, 🙌)
              - "Diamond hands", "to the moon", "HODL"
        
        PRESENT: 2021-present modern market discourse
                 - Post-meme institutionalization
                 - Hybrid vocabulary
                 - Most comprehensive lexicon
    
    Example:
        >>> from discourses import Era
        >>> client.analyze("Diamond hands!", era=Era.MEME)
    """
    
    PRIMITIVE = "primitive"
    MEME = "meme"
    PRESENT = "present"
    
    def __str__(self) -> str:
        return self.value
    
    @classmethod
    def all(cls) -> list:
        """Return list of all eras."""
        return [era for era in cls]
    
    @classmethod
    def from_string(cls, value: str) -> "Era":
        """
        Create Era from string value.
        
        Args:
            value: Era string (e.g., 'primitive', 'meme', 'present')
        
        Returns:
            Matching Era enum
        
        Raises:
            ValueError: If no matching era found
        """
        value = value.lower().strip()
        
        if value == "primitive":
            return cls.PRIMITIVE
        if value == "meme":
            return cls.MEME
        if value == "present":
            return cls.PRESENT
        
        raise ValueError(f"Unknown era: {value}. Valid eras: primitive, meme, present")


# Rate Limiting
RATE_LIMIT_REQUESTS = 100  # requests per minute (varies by plan)
