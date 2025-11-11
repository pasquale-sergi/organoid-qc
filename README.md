# 🧬 OrganoidQC

**Image Quality Control system for organoid screening.** Automatically analyzes microscopy images and identifies those suitable for ML processing.

## Features

✨ **Image Analysis** - Focus, contrast, exposure detection + organoid metrics  
📊 **Batch Processing** - Upload with metadata, real-time QC, equipment monitoring  
🎯 **ML Readiness** - Customizable thresholds, export CSV, auto-generate Python script

## Tech Stack

**Backend:** FastAPI, SQLAlchemy, OpenCV, SQLite  
**Frontend:** Vue 3, Vite, Axios

## Quick Start

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Backend: `http://localhost:8000` | Frontend: `http://localhost:5173`

## Usage

1. Create experiment
2. Upload microscopy images (JPG, PNG, BMP, TIFF)
3. Adjust quality thresholds (focus, contrast, exposure)
4. Export ML-ready images or download Python organization script

## API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/upload/{exp_id}` | Upload & analyze images |
| GET | `/experiments/{id}/batch-report` | Batch statistics |
| GET | `/experiments/{id}/export-ml-ready` | Export CSV |
| GET | `/experiments/{id}/generate-copy-script` | Python organizer |

## Quality Metrics

- **Focus Score** - Laplacian variance (higher = sharper)
- **Contrast** - Pixel intensity std dev
- **Exposure** - Mean brightness (ideal: 50-200)
- **Circularity** - Shape regularity (0-1)

## Configuration

Edit `backend/config.py`:
```python
DEFAULT_FOCUS_THRESHOLD = 150
DEFAULT_CONTRAST_THRESHOLD = 20
DEFAULT_EXPOSURE_MIN = 30
DEFAULT_EXPOSURE_MAX = 225
```

## Use Case

Accelerates organoid screening by automating quality assessment, ensuring consistency, and enabling scalable batch processing—replacing tedious manual microscopy inspection.

## License

MIT
