# History Predictor

A small web app that asks **"what if?"** about major historical events and generates
a plausible alternate timeline with social, economic, and political consequences.

The backend is FastAPI. The frontend is plain HTML, CSS, and JavaScript served by the
same app. Generation uses Groq's `openai/gpt-oss-120b` model with structured JSON output.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
# Put your Groq API key in .env
uvicorn app.main:app --reload
```

Open <http://localhost:8000> for the website, or
<http://localhost:8000/docs> for the API docs.

## How It Works

1. You pick a predefined event or enter your own.
2. The app retrieves a few relevant paragraphs from a small in-memory historical corpus.
3. Groq generates a structured alternate timeline.
4. The timeline is validated and rendered year by year.

No vector database, Redis, Celery, or database is required. The cache is in memory and
the corpus is a plain Python list, which keeps the demo easy to run and understand.

## Project Layout

```text
app/
  main.py                 FastAPI app + static website
  api/routes.py           /api/v1 endpoints
  api/schemas.py          request/response models
  core/config.py          environment settings
  core/llm_client.py      Groq client with structured output
  data/corpus.py          small historical corpus
  data/events.py          predefined events
  models/timeline.py      Pydantic timeline models
  services/prompt_builder.py
  services/rag_pipeline.py
  services/timeline_generator.py
  services/validation.py
  services/cache.py
  static/                 HTML, CSS, JavaScript
tests/                    pytest suite
```

## API

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/v1/health` | Health check |
| `GET` | `/api/v1/events` | List predefined events |
| `POST` | `/api/v1/generate` | Generate an alternate timeline |
| `GET` | `/api/v1/corpus/search?query=...` | Search the historical corpus |
| `POST` | `/api/v1/corpus/reset` | Reload the corpus |

Example request:

```bash
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "event": {
      "name": "Cuban Missile Crisis",
      "start_date": "1962-10-16",
      "end_date": "1962-10-28",
      "description": "A confrontation over Soviet missiles in Cuba.",
      "key_figures": ["John F. Kennedy", "Nikita Khrushchev"],
      "geographic_scope": "Caribbean / Global",
      "event_type": "political_crisis"
    },
    "num_years": 6
  }'
```

## Notes

- Generations are capped at 6 years because Groq's free tier has tight output-token
  limits. Each request produces a complete, validated JSON timeline.
- The API key stays on the server. The browser only talks to this app.
- Counterfactual scenarios are AI-generated speculation, not historical fact.

## Tests

```bash
pip install -e ".[dev]"
pytest
```
