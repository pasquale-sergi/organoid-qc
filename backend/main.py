from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import init_db
from routes import experiments, images, batch, exports, debug

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    init_db()
    yield

app = FastAPI(
    title="OrganoidQC API",
    description="Image Quality Control for Organoid Screening",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include routers
app.include_router(experiments.router)
app.include_router(images.router)
app.include_router(batch.router)
app.include_router(exports.router)
app.include_router(debug.router)

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "OrganoidQC API"}