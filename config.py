"""
config.py — central configuration for market_signals_pipeline
=============================================================
Edit this file before your first run. Everything else reads from here.
"""

import os

# ─────────────────────────────────────────────────────────────────────────────
# SEC EDGAR  (free, no key — just needs a real email in User-Agent)
# ─────────────────────────────────────────────────────────────────────────────
# Replace with your real email — SEC blocks generic User-Agent strings
EDGAR_USER_AGENT_EMAIL: str = os.environ.get("EDGAR_EMAIL", "aetingu@gmail.com")

# ─────────────────────────────────────────────────────────────────────────────
# TAVILY SEARCH
# ─────────────────────────────────────────────────────────────────────────────
# Get a free API key at https://tavily.com  (1,000 searches/month free)
# Set here OR export as environment variable:  set TAVILY_API_KEY=tvly-xxx
TAVILY_API_KEY: str = os.environ.get("TAVILY_API_KEY", "tvly-YOUR_KEY_HERE")

# Searches per company (5 targeted queries × up to 5 results each)
TAVILY_MAX_RESULTS: int = 5       # results per query
TAVILY_SEARCH_DEPTH: str = "advanced"   # "basic" (faster) or "advanced" (better)

# ─────────────────────────────────────────────────────────────────────────────
# MODEL BACKEND SELECTOR
# ─────────────────────────────────────────────────────────────────────────────
# True  = use Databricks Foundation Model APIs (recommended for Databricks runs)
# False = use local llama-server (for running on your Windows workstation)
USE_DATABRICKS_MODEL: bool = bool(os.environ.get("USE_DATABRICKS_MODEL", "False").strip() in ("1","True","true"))

# ─────────────────────────────────────────────────────────────────────────────
# DATABRICKS FOUNDATION MODEL API / MODEL SERVING
# ─────────────────────────────────────────────────────────────────────────────
# Workspace URL — e.g. https://adb-1234567890123456.7.azuredatabricks.net
DATABRICKS_HOST:  str = os.environ.get("DATABRICKS_HOST",  "https://YOUR_WORKSPACE.azuredatabricks.net")

# Personal Access Token — generate in Databricks → Settings → Developer → Access Tokens
# Inside a Databricks notebook/job this is injected automatically by the runner.
DATABRICKS_TOKEN: str = os.environ.get("DATABRICKS_TOKEN", "")

# Endpoint for Stage 2 classifier (high-quality, larger model).
# Override from a Databricks Job parameter by setting DATABRICKS_CLASSIFIER_ENDPOINT.
# Examples:
#   databricks-qwen3-next-80b-a3b-instruct
#   qwen3-6-corporate-classifier
#   your-own-model-serving-endpoint-name
DATABRICKS_CLASSIFIER_ENDPOINT: str = os.environ.get(
    "DATABRICKS_CLASSIFIER_ENDPOINT",
    "databricks-qwen3-next-80b-a3b-instruct",
)

# Endpoint for Stage 1C prescreener (fast, cheap — fires for every company).
# Override from a Databricks Job parameter by setting DATABRICKS_PRESCREENER_ENDPOINT.
DATABRICKS_PRESCREENER_ENDPOINT: str = os.environ.get(
    "DATABRICKS_PRESCREENER_ENDPOINT",
    "databricks-meta-llama-3-1-8b-instruct",
)

# ─────────────────────────────────────────────────────────────────────────────
# LOCAL LLAMA-SERVER  (for Qwen3.6-35B-A3B-MTP or any GGUF model)
# ─────────────────────────────────────────────────────────────────────────────
# Start the server before running the pipeline:
#
#   llama-server.exe \
#     -m C:/models/Qwen3.6-35B-A3B-UD-Q4_K_XL.gguf \
#     --threads 14 -c 8192 \
#     --spec-type draft-mtp --spec-draft-n-max 2 \
#     --host 127.0.0.1 --port 8080
#
LLAMA_SERVER_URL: str = os.environ.get("LLAMA_SERVER_URL", "http://127.0.0.1:8080")
LLAMA_SERVER_TIMEOUT: int = 180    # seconds — increase for large models / slow CPU

# ─────────────────────────────────────────────────────────────────────────────
# INPUT / OUTPUT
# ─────────────────────────────────────────────────────────────────────────────
DEFAULT_INPUT_CSV:  str = "company_list_sample.csv"
DEFAULT_OUTPUT_XLS: str = "market_signals_report.xlsx"

# ─────────────────────────────────────────────────────────────────────────────
# PIPELINE BEHAVIOUR
# ─────────────────────────────────────────────────────────────────────────────
# Date window shown in column headers and summaries
DATE_RANGE: str = "Nov 2024 – Jun 2026"

# Minimum LLM confidence (1–5) to accept a signal.
# Raise to 3–4 for higher precision. Lower to 1 for maximum recall.
MIN_CONFIDENCE: int = 2

# Three-pass classifier (higher quality, ~3× slower).
# Set False to use single-pass (faster, ~70% quality).
USE_IMPROVED_CLASSIFIER: bool = True

# Characters of fetched content sent to the LLM per chunk
# With 6 sources now feeding context, increase the window to fit more content.
# 5 chunks × 3,000 = 15,000 chars — well within Qwen3.6's 8K token context
# (15,000 chars ≈ 3,750 tokens at ~4 chars/token).
CONTEXT_CHUNK_SIZE: int = 3_000
MAX_CONTEXT_CHUNKS: int = 5       # = 15,000 total chars (was 3 → 9,000)

# Seconds to wait between companies (avoids Tavily rate limits)
INTER_COMPANY_DELAY: float = 1.0

# ─────────────────────────────────────────────────────────────────────────────
# BRAVE SEARCH API  (optional — $5 monthly credit ~1,000 queries)
# Get key at: https://api-dashboard.search.brave.com
# Leave as-is if you don’t have a Brave key — pipeline works without it.
# ─────────────────────────────────────────────────────────────────────────────
BRAVE_API_KEY: str = os.environ.get("BRAVE_API_KEY", "BSA-YOUR_KEY_HERE")

# ─────────────────────────────────────────────────────────────────────────────
# CACHE
# ─────────────────────────────────────────────────────────────────────────────
# Search results are cached to avoid redundant API calls within a batch.
# Cache lives alongside the output file. Each company is keyed by name + week
# number so cache auto-expires after 7 days.
CACHE_DIR:       str = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".search_cache")
CACHE_TTL_HOURS: int = 168   # 7 days

# ─────────────────────────────────────────────────────────────────────────────
# TWO-STAGE PRESCREENER
# ─────────────────────────────────────────────────────────────────────────────
# Minimum LLM score (1–5) to trigger Stage 2 Tavily deep fetch.
# 3 = plausible signal (recommended — balances recall vs Tavily usage)
# 4 = strong signal only (saves more Tavily credits, slightly lower recall)
PRESCREEN_MIN_SCORE: int = 3

# Set True to log prescreener decisions to a CSV alongside the output XLSX.
# Useful for tuning PRESCREEN_MIN_SCORE on your company list.
PRESCREEN_LOG: bool = True

# ─────────────────────────────────────────────────────────────────────────────
# EXCEL STYLE CONSTANTS  (exact values from reference file)
# ─────────────────────────────────────────────────────────────────────────────
# Dashboard column widths  [A, B, C, D, E, F, G, H, I, J, K]
DASH_COL_WIDTHS = [38, 11, 11, 10, 12, 14, 13, 9, 70, 13, 11]

# Detail sheet column widths  [Company, Detail, Sources]
DETAIL_COL_WIDTHS_DEFAULT = [34, 82, 52]
DETAIL_COL_WIDTHS_HQ      = [34, 14, 52, 52]  # extra USA Region col

HEADER_ROW_HEIGHT:   float = 36.0
DATA_ROW_HEIGHT:     float = 55.0   # default; auto-expand for long content

# Hex colours
COLOR_HEADER_FILL   = "1F4E79"   # dark navy
COLOR_ALT_ROW       = "EAF1FB"   # light blue
COLOR_WHITE_ROW     = "FFFFFF"
COLOR_TICK          = "1F7A1F"   # dark green
COLOR_DASH          = "9E9E9E"   # mid grey
COLOR_COMPANY_TEXT  = "1F4E79"   # navy bold
COLOR_BODY_TEXT     = "1A1A1A"   # near-black
COLOR_SOURCES_TEXT  = "505D6B"   # steel grey
COLOR_REGION_TEXT   = "1F4E79"   # navy bold (region labels)
COLOR_TOTAL_TEXT    = "1F4E79"   # navy bold (signal count)
COLOR_BORDER        = "C9D6E8"   # light blue-grey border

# USA region groups
USA_REGIONS = {
    "USA West", "USA New York", "USA Midwest",
    "USA South", "USA Boston",  "USA Northeast",
}
