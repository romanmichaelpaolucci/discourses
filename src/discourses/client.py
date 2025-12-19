"""
Main client for the Discourses API.

This module provides the Discourses class, which is the primary interface
for interacting with the Discourses sentiment analysis API.
"""

from typing import List, Optional, Union, Dict, Any

import requests

from discourses.constants import BASE_URL, DEFAULT_TIMEOUT, ENDPOINTS, Era
from discourses.exceptions import (
    AuthenticationError,
    RateLimitError,
    ValidationError,
    APIError,
)
from discourses.models import AnalysisResult, CompareResult, BatchResult


class Discourses:
    """
    Client for the Discourses financial sentiment analysis API.
    
    The Discourses API provides institutional-grade sentiment analysis using
    era-calibrated lexicons, powered by academic methodology.
    
    Args:
        api_key: Your Discourses API key. Get one at https://discourses.io/dashboard
        base_url: API base URL (default: https://discourses.io/api/v1)
        timeout: Request timeout in seconds (default: 30)
    
    Example:
        >>> from discourses import Discourses
        >>> client = Discourses(api_key="your-api-key")
        >>> 
        >>> # Single text analysis
        >>> result = client.analyze("Strong growth ahead")
        >>> print(f"Label: {result.label}, Outlook: {result.outlook:.2f}")
        >>>
        >>> # Compare across eras
        >>> comparison = client.compare_eras("Diamond hands!", eras=["primitive", "meme"])
        >>> for era, data in comparison.results.items():
        ...     print(f"{era}: {data['classification']['label']}")
        >>>
        >>> # Batch analysis
        >>> texts = [{"id": "1", "text": "Bullish!"}, {"id": "2", "text": "Bearish..."}]
        >>> batch = client.batch(texts, era="present")
    
    Attributes:
        api_key: The API key used for authentication.
        base_url: The base URL for API requests.
        timeout: Request timeout in seconds.
    """
    
    def __init__(
        self,
        api_key: str,
        base_url: str = BASE_URL,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> None:
        if not api_key:
            raise ValueError("api_key is required")
        
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "discourses-python/1.0.0",
        })
    
    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make an API request.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            data: Request body data
            
        Returns:
            Parsed JSON response
            
        Raises:
            AuthenticationError: If API key is invalid
            RateLimitError: If rate limit exceeded
            ValidationError: If request validation fails
            APIError: For other API errors
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self._session.request(
                method=method,
                url=url,
                json=data,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            raise APIError(f"Request timed out after {self.timeout}s")
        except requests.exceptions.ConnectionError:
            raise APIError("Failed to connect to API")
        except requests.exceptions.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")
        
        return self._handle_response(response)
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Handle API response and raise appropriate exceptions.
        
        Args:
            response: requests Response object
            
        Returns:
            Parsed JSON response
            
        Raises:
            AuthenticationError: For 401 responses
            RateLimitError: For 429 responses
            ValidationError: For 400/422 responses
            APIError: For other error responses
        """
        try:
            data = response.json()
        except ValueError:
            data = {"message": response.text or "Unknown error"}
        
        if response.status_code == 200:
            return data
        
        message = data.get("message", data.get("error", "Unknown error"))
        
        if response.status_code == 401:
            raise AuthenticationError(
                message=message,
                status_code=response.status_code,
                response=data,
            )
        
        if response.status_code == 429:
            retry_after_header = response.headers.get("X-RateLimit-Reset")
            retry_after = None
            if retry_after_header:
                try:
                    retry_after = int(retry_after_header)
                except (ValueError, TypeError):
                    pass
            raise RateLimitError(
                message=message,
                status_code=response.status_code,
                response=data,
                retry_after=retry_after,
            )
        
        if response.status_code in (400, 422):
            raise ValidationError(
                message=message,
                status_code=response.status_code,
                response=data,
            )
        
        raise APIError(
            message=message,
            status_code=response.status_code,
            response=data,
        )
    
    def analyze(
        self,
        text: str,
        era: Optional[Union[str, Era]] = None,
    ) -> AnalysisResult:
        """
        Analyze sentiment of text.
        
        Analyzes financial text and returns sentiment classification,
        confidence, and detailed sentiment scores.
        
        Args:
            text: The text to analyze (news, social media, research, etc.)
            era: Era to use for analysis (primitive, meme, present).
                 If not specified, uses the API default.
        
        Returns:
            AnalysisResult with label, confidence, outlook, and scores.
        
        Raises:
            ValidationError: If text is empty or too long
            AuthenticationError: If API key is invalid
            RateLimitError: If rate limit exceeded
        
        Example:
            >>> result = client.analyze("Strong growth with excellent outlook")
            >>> print(f"Label: {result.label}")  # very_bullish
            >>> print(f"Outlook: {result.outlook:.2f}")  # 0.93
            >>> print(f"Bullish: {result.is_bullish}")  # True
        """
        if not text or not text.strip():
            raise ValidationError("text cannot be empty")
        
        request_data: Dict[str, Any] = {"text": text}
        
        if era:
            era_value = str(era) if isinstance(era, Era) else era
            request_data["era"] = era_value
        
        data = self._request(
            method="POST",
            endpoint=ENDPOINTS["analyze"],
            data=request_data,
        )
        
        return AnalysisResult.from_dict(data)
    
    def compare_eras(
        self,
        text: str,
        eras: Optional[List[Union[str, Era]]] = None,
    ) -> CompareResult:
        """
        Analyze text across multiple eras to understand semantic drift.
        
        Compare how the same text would be interpreted in different time
        periods, perfect for backtesting, historical analysis, and
        understanding how financial language evolves.
        
        Args:
            text: The text to analyze across eras.
            eras: List of eras to compare (primitive, meme, present).
                  Defaults to all eras if not specified.
        
        Returns:
            CompareResult with results per era and drift analysis.
        
        Raises:
            ValidationError: If text is empty or eras list is invalid
            AuthenticationError: If API key is invalid
            RateLimitError: If rate limit exceeded
        
        Example:
            >>> result = client.compare_eras(
            ...     "Diamond hands! To the moon!",
            ...     eras=["primitive", "meme", "present"]
            ... )
            >>> 
            >>> for era, data in result.results.items():
            ...     label = data['classification']['label']
            ...     outlook = data['scores']['outlook']
            ...     print(f"{era}: {label} ({outlook:.2f})")
            >>>
            >>> print(f"Drift: {result.drift_magnitude:.2f}")
        """
        if not text or not text.strip():
            raise ValidationError("text cannot be empty")
        
        request_data: Dict[str, Any] = {"text": text}
        
        if eras:
            request_data["eras"] = [str(e) if isinstance(e, Era) else e for e in eras]
        
        data = self._request(
            method="POST",
            endpoint=ENDPOINTS["compare_eras"],
            data=request_data,
        )
        
        return CompareResult.from_dict(data)
    
    def batch(
        self,
        texts: List[Dict[str, str]],
        era: Union[str, Era] = Era.PRESENT,
    ) -> BatchResult:
        """
        Analyze multiple texts in a single request.
        
        Efficient batch processing for analyzing large volumes of text.
        Each text should have an 'id' and 'text' field.
        
        Args:
            texts: List of dicts with 'id' and 'text' keys.
            era: Era to use for analysis (primitive, meme, present).
        
        Returns:
            BatchResult with results keyed by your custom IDs.
        
        Raises:
            ValidationError: If texts list is empty or malformed
            AuthenticationError: If API key is invalid
            RateLimitError: If rate limit exceeded
        
        Example:
            >>> texts = [
            ...     {"id": "post_1", "text": "Bullish on this!"},
            ...     {"id": "post_2", "text": "Bearish sentiment here"},
            ... ]
            >>> result = client.batch(texts, era="meme")
            >>> 
            >>> for post_id, data in result.results.items():
            ...     label = data['classification']['label']
            ...     print(f"{post_id}: {label}")
        """
        if not texts:
            raise ValidationError("texts list cannot be empty")
        
        # Validate each text has id and text
        for i, item in enumerate(texts):
            if not isinstance(item, dict):
                raise ValidationError(f"Item {i} must be a dict with 'id' and 'text' keys")
            if "id" not in item or "text" not in item:
                raise ValidationError(f"Item {i} must have 'id' and 'text' keys")
        
        era_value = str(era) if isinstance(era, Era) else era
        
        request_data: Dict[str, Any] = {
            "texts": texts,
            "era": era_value,
        }
        
        data = self._request(
            method="POST",
            endpoint=ENDPOINTS["batch"],
            data=request_data,
        )
        
        return BatchResult.from_dict(data)
    
    def __repr__(self) -> str:
        return f"Discourses(base_url='{self.base_url}')"
