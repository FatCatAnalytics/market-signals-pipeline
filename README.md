# Market Signals Pipeline

Automated corporate change signal detection for a list of companies.

## What it does
1. Reads a CSV of company names (`company_list_sample.csv`)
2. Fetches recent news via **Tavily** (free tier: 1,000 searches/month)
3. Classifies 7 signal types using your **local llama-server** (Qwen3.6-35B or any GGUF)
4. Writes a pixel-perfect **Excel report** matching the reference format

## Setup

```bash
pip install -r requirements.txt
```

### Start llama-server (Windows)
```
llama-server.exe ^
  -m C:\models\Qwen3.6-35B-A3B-UD-Q4_K_XL.gguf ^
  --threads 14 -c 8192 ^
  --spec-type draft-mtp --spec-draft-n-max 2 ^
  --host 127.0.0.1 --port 8080
```

### Configure
Edit `config.py`:
- Set `TAVILY_API_KEY` (or use `set TAVILY_API_KEY=tvly-xxx`)
- Set `LLAMA_SERVER_URL` if not using default `http://127.0.0.1:8080`
- Adjust `MIN_CONFIDENCE` (2 = more signals, 4 = fewer/higher quality)

## Run

```bash
# Default: reads company_list_sample.csv → writes market_signals_report.xlsx
python pipeline.py

# Custom paths
python pipeline.py --input my_companies.csv --output results.xlsx

# Pass Tavily key inline
python pipeline.py --tavily-key tvly-XXXX

# Force fresh start (ignore checkpoint)
python pipeline.py --no-resume
```

## CSV format
| Column | Required | Notes |
|--------|----------|-------|
| `company` (or `company_name`, `name`, `entity`) | Yes | Company name |
| `sector` (or `industry`) | No | Improves search relevance |

## Output sheets
| Sheet | Contents |
|-------|----------|
| Signal Summary Dashboard | All companies, tick/dash grid, totals, summaries |
| Sector Changes | Companies with sector change detail |
| HQ Changes | HQ moves + USA region classification |
| M&A & Spinoffs | Merger/acquisition/divestiture detail |
| Renaming Rebranding | Name change detail |
| Operational Changes | Restructuring, shutdowns, significant cuts |
| Bankruptcy | Filing type and date |
| Pipeline Stats | Run metadata, signal counts, runtime |

## Signal types detected
- **Sector/Subsector Change** — company moved to a different industry
- **HQ/Domicile Change** — HQ relocation or legal redomicile
- **M&A / Spinoffs** — mergers, acquisitions, takeovers, spinoffs
- **Renaming/Rebranding** — legal or brand name change
- **Operational Change/Shutdown** — major restructuring or full wind-down
- **Bankruptcy/Liquidation** — insolvency or administration filing

## Files
| File | Purpose |
|------|---------|
| `config.py` | All constants — edit before running |
| `search.py` | Tavily search module |
| `classifier.py` | llama-server 3-pass classifier |
| `excel_writer.py` | openpyxl Excel writer |
| `pipeline.py` | Main orchestrator + CLI |
| `requirements.txt` | pip dependencies |
