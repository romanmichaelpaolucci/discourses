"""
Data models for the Discourses SDK.

This module defines dataclasses for API request and response objects,
providing type-safe access to analysis results.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class AnalysisResult:
    """
    Result from single text sentiment analysis.
    
    Contains the sentiment classification, confidence, and detailed scores
    from analyzing text with an era-specific lexicon.
    
    Attributes:
        label: Sentiment classification (very_bullish, bullish, neutral, bearish, very_bearish)
        confidence: Model confidence in the classification (0.0 to 1.0)
        outlook: Overall sentiment score (0.0 to 1.0, higher = more bullish)
        scores: Detailed sentiment breakdown (bullish, bearish, neutral, confusion)
        word_count: Number of words in the text
        matched_count: Number of sentiment words matched
        negation_count: Number of negation words detected
        raw: Raw API response for advanced usage
    
    Example:
        >>> result = client.analyze("Strong growth with excellent outlook")
        >>> print(f"Label: {result.label}")  # Label: very_bullish
        >>> print(f"Outlook: {result.outlook:.2f}")  # Outlook: 0.93
    """
    
    label: str
    confidence: float
    outlook: float
    scores: Dict[str, float]
    word_count: int = 0
    matched_count: int = 0
    negation_count: int = 0
    raw: Dict[str, Any] = field(default_factory=dict, repr=False)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AnalysisResult":
        """Create AnalysisResult from API response dictionary."""
        classification = data.get("classification", {})
        scores = data.get("scores", {})
        analysis = data.get("analysis", {})
        
        return cls(
            label=classification.get("label", "neutral"),
            confidence=float(classification.get("confidence", 0)),
            outlook=float(scores.get("outlook", 0)),
            scores={
                "bullish": float(scores.get("bullish", 0)),
                "bearish": float(scores.get("bearish", 0)),
                "neutral": float(scores.get("neutral", 0)),
                "confusion": float(scores.get("confusion", 0)),
            },
            word_count=int(analysis.get("word_count", 0)),
            matched_count=int(analysis.get("matched_count", 0)),
            negation_count=int(analysis.get("negation_count", 0)),
            raw=data,
        )
    
    @property
    def is_bullish(self) -> bool:
        """True if sentiment is bullish or very_bullish."""
        return "bullish" in self.label
    
    @property
    def is_bearish(self) -> bool:
        """True if sentiment is bearish or very_bearish."""
        return "bearish" in self.label
    
    @property
    def is_neutral(self) -> bool:
        """True if sentiment is neutral."""
        return self.label == "neutral"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "label": self.label,
            "confidence": self.confidence,
            "outlook": self.outlook,
            "scores": self.scores,
            "word_count": self.word_count,
            "matched_count": self.matched_count,
        }


@dataclass
class CompareResult:
    """
    Result from comparing text across multiple eras.
    
    Provides per-era sentiment analysis and drift metrics to understand
    how the same text would be interpreted in different time periods.
    
    Attributes:
        results: Dictionary of per-era analysis results
        drift: Semantic drift metrics (direction, magnitude, min_era, peak_era)
        meta: Processing metadata (eras_compared, model, processing_time_ms)
        raw: Raw API response for advanced usage
    
    Example:
        >>> comparison = client.compare_eras("Diamond hands!", eras=["primitive", "meme"])
        >>> 
        >>> for era, data in comparison.results.items():
        ...     print(f"{era}: {data['classification']['label']}")
        >>> 
        >>> print(f"Drift: {comparison.drift['magnitude']:.2f}")
    """
    
    results: Dict[str, Dict[str, Any]]
    drift: Dict[str, Any]
    meta: Dict[str, Any]
    raw: Dict[str, Any] = field(default_factory=dict, repr=False)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CompareResult":
        """Create CompareResult from API response dictionary."""
        return cls(
            results=data.get("results", {}),
            drift=data.get("drift", {}),
            meta=data.get("meta", {}),
            raw=data,
        )
    
    def get_era(self, era: str) -> Optional[Dict[str, Any]]:
        """Get result for a specific era."""
        return self.results.get(era)
    
    @property
    def drift_direction(self) -> str:
        """Direction of semantic drift."""
        return self.drift.get("direction", "stable")
    
    @property
    def drift_magnitude(self) -> float:
        """Magnitude of semantic drift."""
        return float(self.drift.get("magnitude", 0))
    
    @property
    def peak_era(self) -> str:
        """Era with highest sentiment."""
        return self.drift.get("peak_era", "")
    
    @property
    def min_era(self) -> str:
        """Era with lowest sentiment."""
        return self.drift.get("min_era", "")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "results": self.results,
            "drift": self.drift,
            "meta": self.meta,
        }


@dataclass
class BatchResult:
    """
    Result from batch text analysis.
    
    Contains results for each text in the batch, keyed by your custom IDs.
    
    Attributes:
        results: Dictionary of results keyed by text ID
        meta: Processing metadata (era, texts_processed, texts_failed, processing_time_ms)
        raw: Raw API response for advanced usage
    
    Example:
        >>> texts = [{"id": "post_1", "text": "Bullish!"}]
        >>> batch = client.batch(texts, era="meme")
        >>> 
        >>> for post_id, data in batch.results.items():
        ...     print(f"{post_id}: {data['classification']['label']}")
        >>> 
        >>> print(f"Processed: {batch.texts_processed}")
    """
    
    results: Dict[str, Dict[str, Any]]
    meta: Dict[str, Any]
    raw: Dict[str, Any] = field(default_factory=dict, repr=False)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BatchResult":
        """Create BatchResult from API response dictionary."""
        return cls(
            results=data.get("results", {}),
            meta=data.get("meta", {}),
            raw=data,
        )
    
    def __iter__(self):
        """Iterate over results as (id, data) tuples."""
        return iter(self.results.items())
    
    def __len__(self) -> int:
        """Return number of results."""
        return len(self.results)
    
    def __getitem__(self, key: str) -> Dict[str, Any]:
        """Get result by ID."""
        return self.results[key]
    
    @property
    def texts_processed(self) -> int:
        """Number of texts successfully processed."""
        return self.meta.get("texts_processed", len(self.results))
    
    @property
    def texts_failed(self) -> int:
        """Number of texts that failed processing."""
        return self.meta.get("texts_failed", 0)
    
    @property
    def era(self) -> str:
        """Era used for analysis."""
        return self.meta.get("era", "")
    
    @property
    def processing_time_ms(self) -> int:
        """Total processing time in milliseconds."""
        return self.meta.get("processing_time_ms", 0)
    
    def get_successful(self) -> Dict[str, Dict[str, Any]]:
        """Get only successfully processed results."""
        return {k: v for k, v in self.results.items() if "error" not in v}
    
    def get_failed(self) -> Dict[str, Dict[str, Any]]:
        """Get only failed results."""
        return {k: v for k, v in self.results.items() if "error" in v}
