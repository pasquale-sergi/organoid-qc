# 🧬 OrganoidQC

**Image Quality Control system for organoid screening.** Automatically analyzes microscopy images and identifies those suitable for ML processing.

Built for biotech labs automating organoid workflows.

## Features

✨ **Image Analysis** - Focus (Laplacian), contrast, exposure detection + organoid diameter & circularity  
📊 **Batch Processing** - Upload with metadata (session, microscope, operator), real-time QC  
🎯 **ML Readiness** - Customizable thresholds, export CSV, auto-generate Python organization script  
🔧 **Equipment Monitoring** - Track microscope degradation via focus trend analysis per device

## Tech Stack

**Backend:** FastAPI, SQLAlchemy, OpenCV, SQLite  
**Frontend:** Vue 3, Vite, Axios  
**Testing:** pytest

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
2. Upload microscopy images with metadata (JPG, PNG, BMP, TIFF)
3. Adjust quality thresholds in real-time
4. Export ML-ready images as CSV or download Python organization script

## Key Features

- **Metadata Tracking** - Imaging session, microscope ID, operator for reproducibility
- **Equipment Health** - Detects microscope degradation via focus score trends
- **Batch Statistics** - Pass rate, average metrics, session-level breakdowns
- **Persistent State** - localStorage for experiment selection and metadata

## API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/upload/{exp_id}` | Upload & analyze images |
| GET | `/experiments/{id}/batch-report` | Batch statistics |
| GET | `/experiments/{id}/equipment-health` | Equipment degradation detection |
| GET | `/experiments/{id}/export-ml-ready` | Export ML-ready CSV |
| GET | `/experiments/{id}/generate-copy-script` | Generate Python organizer script |

## Quality Metrics

- **Focus Score** - Laplacian variance (higher = sharper image)
- **Contrast** - Pixel intensity standard deviation
- **Exposure** - Mean brightness (ideal: 50-200)
- **Circularity** - Organoid shape regularity (0-1)

## Testing

```bash
cd backend
.\venv\Scripts\python.exe -m pytest tests/test_image_processing.py -v
```

## Use Case

Accelerates organoid screening workflows by automating quality assessment, enabling equipment health monitoring, and ensuring reproducible batch processing—replacing manual microscopy inspection.

Inspired by biotech workflows with the [Orgadroid](https://www.visienco.ch/) system.

## License

MIT
