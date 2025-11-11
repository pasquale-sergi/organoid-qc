from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./organoid_qc.db"

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)


def init_db():
    """Initialize database schema"""
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS experiments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                experiment_id INTEGER NOT NULL,
                filename TEXT NOT NULL,
                
                -- Image quality metrics
                focus_score REAL,
                contrast_level REAL,
                exposure_level REAL,
                is_ml_ready BOOLEAN DEFAULT 0,
                quality_reason TEXT,
                
                -- Organoid context
                organoid_diameter REAL,
                organoid_shape_regularity REAL,
                
                -- Batch tracking
                imaging_session_id TEXT,
                microscope_id TEXT,
                operator_id TEXT,
                acquisition_time TIMESTAMP,
                
                -- Downstream integration
                orgadroid_classification TEXT,
                orgadroid_confidence REAL,
                target_well_id TEXT,
                
                -- Metadata
                width INTEGER,
                height INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (experiment_id) REFERENCES experiments(id)
            )
        """))

        try:
            conn.execute(text("ALTER TABLE images ADD COLUMN file_path TEXT"))
        except:
            pass

        try:
            conn.execute(text("ALTER TABLE images ADD COLUMN thumbnail_path TEXT"))
        except:
            pass
        
def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()