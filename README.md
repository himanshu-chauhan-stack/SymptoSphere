# SymptoSphere

SymptoSphere is an AI-powered disease prediction web app built with Flask, custom frontend UI, SQLite, and a multi-model ML pipeline.

## Highlights

- Flask backend with Jinja2 templates
- Modern responsive UI (no Bootstrap)
- Symptom-based prediction with top 3 diseases and confidence bars
- Multi-model comparison table with best-model selection reason
- Treatment panel: overview, medicines, home remedies, precautions, urgency level
- AI doctor recommendation cards with fictional doctor personas
- Multilingual interface (English + Hindi) with no page reload
- SQLite-backed disease and doctor mapping data

## Tech Stack

- Backend: Flask, Python
- ML: scikit-learn, joblib
- Database: SQLite
- Frontend: HTML, CSS, JavaScript
- Deployment Target: Vercel

## Local Run

1. Install runtime dependencies:

```bash
pip install -r requirements.txt
```

2. Start the app:

```bash
python app.py
```

3. Open:

```text
http://127.0.0.1:5000
```

## Optional Model Retraining

If you want to retrain with all optional ML trainers locally:

```bash
pip install -r requirements-train.txt
python train.py
```

## Deploy on Vercel

This repository is already prepared for Vercel with:

- `api/index.py` (serverless WSGI entrypoint)
- `vercel.json` (routing config)
- `.vercelignore` (excludes training-only files)

### Option A: Vercel Dashboard (Recommended)

1. Push this repo to GitHub.
2. Open Vercel and click `Add New Project`.
3. Import `himanshu-chauhan-stack/SymptoSphere`.
4. Keep default build settings.
5. Deploy.

### Option B: Vercel CLI

```bash
npm i -g vercel
vercel login
vercel --prod
```

### Notes for Vercel Runtime

- SQLite runs from writable `/tmp` automatically in serverless mode.
- Inference uses the bundled lightweight model artifact in `ml/models/model_bundle.joblib`.
- You can optionally set `SECRET_KEY` in Vercel project environment variables.

## Team / Creator

- Himanshu Chauhan
- Avishhoray Raj
- Nihal Kumar

## Disclaimer

SymptoSphere is an educational AI tool. It does not replace professional medical advice.
