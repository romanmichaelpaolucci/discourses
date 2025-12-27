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
    "analyze": "/analyze/era",
    "compare_eras": "/analyze/compare-eras",
    "batch": "/analyze/batch",
}


class Era(str, Enum):
    """
    Financial language eras for sentiment analysis.
    
    Each era captures distinct vocabulary and sentiment patterns
    characteristic of that time period in financial markets.
    
    Attributes:
        PRIMITIVE: < 2016 - Historical filings, early Twitter, pre-social sentiment
                   - 5,557 tokens
                   - Traditional financial vocabulary
                   - Formal market language
        
        RAMP: 2016-2019 - Fintech emergence, crypto adoption, algorithmic trading era
              - 7,751 tokens
              - Rise of fintech terminology
              - Early crypto vocabulary
        
        MEME: 2019-2023 - WSB, Reddit, meme stocks, retail revolution vernacular
              - 9,822 tokens
              - WSB culture and terminology
              - Crypto/DeFi vocabulary
              - Emoji-based sentiment (🚀, 💎, 🙌)
              - "Diamond hands", "to the moon", "HODL"
        
        PRESENT: > 2023 - Current analysis with aggregate of all eras
                 - 11,195 tokens
                 - Most comprehensive lexicon
                 - Hybrid vocabulary
    
    Example:
        >>> from discourses import Era
        >>> client.analyze("Diamond hands!", era=Era.MEME)
    """
    
    PRIMITIVE = "primitive"
    RAMP = "ramp"
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
            value: Era string (e.g., 'primitive', 'ramp', 'meme', 'present')
        
        Returns:
            Matching Era enum
        
        Raises:
            ValueError: If no matching era found
        """
        value = value.lower().strip()
        
        if value == "primitive":
            return cls.PRIMITIVE
        if value == "ramp":
            return cls.RAMP
        if value == "meme":
            return cls.MEME
        if value == "present":
            return cls.PRESENT
        
        raise ValueError(f"Unknown era: {value}. Valid eras: primitive, ramp, meme, present")


# Rate Limiting
RATE_LIMIT_REQUESTS = 100  # requests per minute (varies by plan)
