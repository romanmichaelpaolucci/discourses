<p align="center">
  <a href="https://discourses.io" target="_blank">
    <img src="https://raw.githubusercontent.com/romanmichaelpaolucci/discourses/main/assets/discourses.png" alt="discourses.io" width="140" />
  </a>
</p>

<h1 align="center" style="margin-top: 0;">discourses.io Python SDK</h1>

<p align="center">
  <strong>Official Python SDK for discourses.io — the financial social media platform and financial language processing API</strong>
</p>

<p align="center">
  <a href="https://badge.fury.io/py/discourses"><img src="https://badge.fury.io/py/discourses.svg" alt="PyPI version"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python 3.8+"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
</p>

<p align="center">
  <a href="https://discourses.io/research"><strong>📄 Read the Whitepaper</strong></a>
  &nbsp;&nbsp;·&nbsp;&nbsp;
  <a href="https://discourses.io/documentation/methodology"><strong>🔬 Methodology</strong></a>
  &nbsp;&nbsp;·&nbsp;&nbsp;
  <a href="https://discourses.io/documentation"><strong>📖 Documentation</strong></a>
  &nbsp;&nbsp;·&nbsp;&nbsp;
  <a href="https://discourses.io/dashboard"><strong>🔑 Get API Key</strong></a>
</p>

---

## Why discourses.io?

[discourses.io](https://discourses.io) is a **financial social media platform** and **financial language processing API** built for the modern market.

Traditional sentiment analysis treats language as static. But financial language evolves—"diamond hands" meant nothing in 2008, but signals strong conviction today. **discourses.io** solves this with **era-calibrated lexicons** built on academic and industrial quantitative research.

| Era | Period | Lexicon | Use Case |
|:---:|:------:|:-------:|:---------|
| **Primitive** | < 2016 | 5,557 tokens | Historical filings, early Twitter, pre-social sentiment |
| **Ramp** | 2016 — 2019 | 7,751 tokens | Fintech emergence, crypto adoption, algorithmic trading era |
| **Meme** | 2019 — 2023 | 9,822 tokens | WSB, Reddit, meme stocks, retail revolution vernacular |
| **Present** | > 2023 | 11,195 tokens | Current analysis with aggregate of all eras |

---

## Installation

```bash
pip install discourses
```

---

## Quick Start

```python
from discourses import Discourses

client = Discourses(api_key="your-api-key")
result = client.analyze("Strong growth with excellent outlook ahead")

print(result.label)      # "very_bullish"
print(result.outlook)    # 0.99
```

---

## API Reference

### 🔑 Initialize the Client

Every request requires authentication with your API key. Get yours at [discourses.io/dashboard](https://discourses.io/dashboard).

```python
from discourses import Discourses

client = Discourses(api_key="your-api-key")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | `str` | *required* | Your discourses.io API key |
| `base_url` | `str` | `https://discourses.io/api/v1` | API base URL |
| `timeout` | `int` | `30` | Request timeout in seconds |

---

## Endpoints

<br>

### 📊 Analyze — Single Text Sentiment

> **`POST /analyze`** — [Documentation](https://discourses.io/documentation#analyze)

Analyze sentiment of any financial text. Returns classification, confidence, and detailed sentiment scores.

```python
from discourses import Discourses

# Initialize client
client = Discourses(api_key="your-api-key")

# Analyze text
result = client.analyze("Strong growth with excellent outlook ahead")

# Access the results
print(f"Label:      {result.label}")
print(f"Confidence: {result.confidence:.2%}")
print(f"Outlook:    {result.outlook:.4f}")
print(f"Bullish:    {result.scores['bullish']:.4f}")
print(f"Bearish:    {result.scores['bearish']:.4f}")
print(f"Words:      {result.word_count}")
```

**Expected Output:**

```
Label:      very_bullish
Confidence: 80.05%
Outlook:    0.9257
Bullish:    0.4917
Bearish:    0.2981
Words:      6
```

<details>
<summary><strong>Response Object: <code>AnalysisResult</code></strong></summary>

| Field | Type | Description |
|-------|------|-------------|
| `label` | `str` | `"very_bullish"`, `"bullish"`, `"neutral"`, `"bearish"`, `"very_bearish"` |
| `confidence` | `float` | Model confidence (0.0 to 1.0) |
| `outlook` | `float` | Overall sentiment score (0.0 to 1.0) |
| `scores` | `dict` | Detailed scores: `bullish`, `bearish`, `neutral`, `confusion` |
| `word_count` | `int` | Number of words analyzed |
| `matched_count` | `int` | Sentiment words matched |

**Helper Properties:**
- `result.is_bullish` → `True` if label contains "bullish"
- `result.is_bearish` → `True` if label contains "bearish"
- `result.is_neutral` → `True` if label is "neutral"

</details>

---

<br>

### 🔄 Compare Eras — Cross-Era Analysis

> **`POST /analyze/compare-eras`** — [Documentation](https://discourses.io/documentation#compare-eras)

Analyze how the same text is interpreted across different market eras. Essential for understanding semantic drift and backtesting strategies.

```python
from discourses import Discourses

# Initialize client
client = Discourses(api_key="your-api-key")

# Compare sentiment across eras
result = client.compare_eras(
    text="This stock is going to the moon! Diamond hands!",
    eras=["primitive", "ramp", "meme", "present"]
)

# View per-era results
print("Era-by-Era Sentiment:")
print("-" * 50)
for era, data in result.results.items():
    label = data['classification']['label']
    outlook = data['scores']['outlook']
    print(f"  {era:12} {label:14} (outlook: {outlook:.4f})")

# Check semantic drift
print()
print(f"Drift Direction: {result.drift['direction']}")
print(f"Drift Magnitude: {result.drift['magnitude']:.4f}")
print(f"Peak Era:        {result.drift['peak_era']}")
```

**Expected Output:**

```
Era-by-Era Sentiment:
--------------------------------------------------
  primitive    bullish        (outlook: 0.6912)
  ramp         bullish        (outlook: 0.7845)
  meme         very_bullish   (outlook: 0.9933)
  present      very_bullish   (outlook: 0.9977)

Drift Direction: positive_shift
Drift Magnitude: 0.3065
Peak Era:        present
```

> 💡 **Notice how "diamond hands" and "to the moon" have much stronger bullish signals in the meme and present eras compared to primitive!**

<details>
<summary><strong>Response Object: <code>CompareResult</code></strong></summary>

| Field | Type | Description |
|-------|------|-------------|
| `results` | `dict` | Per-era analysis results |
| `drift` | `dict` | Semantic drift metrics |
| `meta` | `dict` | Processing metadata |

**Drift Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `direction` | `str` | `"positive_shift"`, `"negative_shift"`, or `"stable"` |
| `magnitude` | `float` | Size of the drift (0.0 to 1.0) |
| `min_era` | `str` | Era with lowest sentiment |
| `peak_era` | `str` | Era with highest sentiment |

</details>

---

<br>

### ⚡ Batch — High-Volume Processing

> **`POST /analyze/batch`** — [Documentation](https://discourses.io/documentation#batch)

Efficiently analyze multiple texts in a single request. Perfect for processing feeds, historical data, or real-time streams.

```python
from discourses import Discourses

# Initialize client
client = Discourses(api_key="your-api-key")

# Texts to analyze (with custom IDs)
texts = [
    {"id": "post_1", "text": "Diamond hands! This is going to the moon"},
    {"id": "post_2", "text": "Bearish on this one, expecting a pullback"},
    {"id": "post_3", "text": "Strong growth with excellent outlook ahead"},
]

# Batch analyze with specific era
result = client.batch(texts=texts, era="meme")

# Process results
print("Batch Sentiment Analysis")
print("=" * 55)
for post_id, data in result.results.items():
    label = data['classification']['label']
    outlook = data['scores']['outlook']
    emoji = "🟢" if "bullish" in label else "🔴" if "bearish" in label else "⚪"
    print(f"{emoji} {post_id}: {label:14} (outlook: {outlook:.4f})")

print()
print(f"Processed: {result.meta['texts_processed']}")
print(f"Failed:    {result.meta['texts_failed']}")
```

**Expected Output:**

```
Batch Sentiment Analysis
=======================================================
🟢 post_1: bullish        (outlook: 0.6735)
🟢 post_2: very_bullish   (outlook: 0.9353)
🟢 post_3: very_bullish   (outlook: 0.9257)

Processed: 3
Failed:    0
```

<details>
<summary><strong>Response Object: <code>BatchResult</code></strong></summary>

| Field | Type | Description |
|-------|------|-------------|
| `results` | `dict` | Results keyed by your custom IDs |
| `meta` | `dict` | Processing metadata |

**Meta Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `era` | `str` | Era used for analysis |
| `texts_processed` | `int` | Successfully processed count |
| `texts_failed` | `int` | Failed count |
| `processing_time_ms` | `int` | Total processing time |

</details>

---

## Era Selection Guide

| Use Case | Recommended Era |
|----------|-----------------|
| Modern social media sentiment | `present` |
| Meme stock / crypto analysis | `meme` |
| Fintech / crypto adoption era | `ramp` |
| Traditional financial news | `primitive` |
| Understanding semantic drift | `compare_eras()` |

```python
# Modern analysis (> 2023)
client.analyze(text, era="present")

# Meme-era analysis (2019-2023, WSB, crypto culture)
client.analyze(text, era="meme")

# Ramp era (2016-2019, fintech emergence)
client.analyze(text, era="ramp")

# Traditional financial language (< 2016)
client.analyze(text, era="primitive")

# Compare across all eras
client.compare_eras(text, eras=["primitive", "ramp", "meme", "present"])
```

---

## Error Handling

The SDK provides typed exceptions for robust error handling:

```python
from discourses import (
    Discourses,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    DiscoursesError,
)

client = Discourses(api_key="your-api-key")

try:
    result = client.analyze("Market analysis text")
    
except AuthenticationError:
    # Invalid or expired API key
    print("Check your API key at https://discourses.io/dashboard")
    
except RateLimitError as e:
    # Too many requests
    print(f"Rate limited. Retry after {e.retry_after} seconds")
    
except ValidationError as e:
    # Invalid input (empty text, too long, etc.)
    print(f"Invalid input: {e.message}")
    
except DiscoursesError as e:
    # Catch-all for other API errors
    print(f"API error: {e}")
```

---

## Links

<table>
  <tr>
    <td align="center">📄</td>
    <td><a href="https://discourses.io/research"><strong>Whitepaper</strong></a><br>Academic research & methodology</td>
    <td align="center">📖</td>
    <td><a href="https://discourses.io/documentation"><strong>Documentation</strong></a><br>Full API reference</td>
  </tr>
  <tr>
    <td align="center">🔬</td>
    <td><a href="https://discourses.io/documentation/methodology"><strong>Methodology</strong></a><br>How era-calibration works</td>
    <td align="center">🔑</td>
    <td><a href="https://discourses.io/dashboard"><strong>Dashboard</strong></a><br>Get your API key</td>
  </tr>
  <tr>
    <td align="center">💬</td>
    <td><a href="https://github.com/romanmichaelpaolucci/discourses/issues"><strong>Issues</strong></a><br>Report bugs & requests</td>
    <td align="center">📦</td>
    <td><a href="https://pypi.org/project/discourses/"><strong>PyPI</strong></a><br>Package & versions</td>
  </tr>
</table>

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

<p align="center">
  <sub>Built with ❤️ by <a href="https://discourses.io">discourses.io</a></sub>
</p>
