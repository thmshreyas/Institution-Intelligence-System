<<<<<<< HEAD
# Institution Intelligence Platform

Discover, verify, and analyze higher education institutions using AISHE data, web crawling, and AI-generated intelligence reports.

## Features

- **Discovery** — AISHE university source
- **Verification** — Age, Engineering, MBA, PhD checks
- **Data collection** — Leadership and address extraction
- **Scoring** — Confidence scoring and eligibility
- **Reports** — Markdown reports per qualified institution
- **API** — FastAPI backend with institution endpoints
- **UI** — React dashboard with college list and detail reports
- **AI** — Gemini-powered report refinement (with local fallback)

## Project Structure

```
institution-intelligence-platform/
├── backend/              # FastAPI app
├── frontend/             # React + Vite + Tailwind UI
├── src/
│   ├── discovery/        # AISHE discovery
│   ├── website/          # Website resolver (Serper)
│   ├── web/              # Website crawler
│   ├── verification/     # Age, engineering, MBA, PhD
│   ├── collectors/       # Leadership, address
│   ├── scoring/          # Confidence scorer
│   ├── pipeline/         # Batch pipeline runner
│   └── llm/              # Gemini + local report parser
├── data/                 # AISHE Excel (not in repo — add locally)
├── output/               # Generated CSVs and reports
├── run_batch1.py         # CLI pipeline runner
└── requirements.txt
```

## Setup

### 1. Clone and configure

```powershell
git clone <your-repo-url>
cd institution-intelligence-platform
copy .env.example .env
```

Edit `.env` with your API keys:

```env
SERPER_API_KEY=your_serper_api_key
GEMINI_API_KEY=your_gemini_api_key
TARGET_QUALIFIED=2
AISHE_DATA_PATH=data/AISHE.xlsx
USE_GEMINI=true
```

### 2. Add AISHE data

Copy your `AISHE.xlsx` file into the `data/` folder. See `data/README.md`.

### 3. Backend

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Frontend

```powershell
cd frontend
npm install
cd ..
```

## Running

### Run pipeline (CLI — recommended)

Processes universities until `TARGET_QUALIFIED` colleges are found:

```powershell
.\venv\Scripts\python run_batch1.py
```

Outputs:
- `output/qualified_colleges.csv`
- `output/all_results.csv`
- `output/reports/*.md`

### Run API server

```powershell
.\venv\Scripts\uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000
```

### Run frontend

```powershell
cd frontend
npm run dev
```

Open http://localhost:5173

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/institutions` | List colleges from reports |
| GET | `/institutions/{name}` | Full profile + AI report |
| POST | `/run-pipeline` | Run pipeline (long-running) |
| GET | `/reports/{name}` | Raw markdown report |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `SERPER_API_KEY` | Serper API for website search and age lookup |
| `GEMINI_API_KEY` | Google Gemini for AI report summaries |
| `USE_GEMINI` | `true`/`false` — enable or disable Gemini |
| `GEMINI_MODEL` | Gemini model name (default: `gemini-2.0-flash`) |
| `TARGET_QUALIFIED` | Number of qualified colleges to collect |
| `AISHE_DATA_PATH` | Path to AISHE Excel file |
| `VITE_API_BASE_URL` | Frontend API URL (dev: `http://127.0.0.1:8000`) |

## Notes

- Run the pipeline via CLI (`run_batch1.py`) rather than the API during development — the API blocks until the pipeline finishes.
- If Gemini quota is exceeded, the app falls back to a local report parser automatically.
- Never commit `.env` or API keys. Use `.env.example` as a template.

## License

Private — all rights reserved.
=======
# Institution-Intelligence-System
>>>>>>> 83051e22aefc273902f1b82473418c918c425f18
