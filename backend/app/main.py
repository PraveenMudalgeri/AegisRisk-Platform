from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import engine, Base
from .auth import routes as auth_routes
from .routes import assets, threats, controls, frameworks, risks, mappings

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AegisRisk GRC Platform",
    description="Backend API for AegisRisk GRC Platform",
    version="0.1.0",
    check_response=False
)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(assets.router, prefix="/api")
app.include_router(threats.router, prefix="/api")
app.include_router(controls.router, prefix="/api")
app.include_router(frameworks.router, prefix="/api")
app.include_router(risks.router, prefix="/api")
from .routes import reports
app.include_router(reports.router, prefix="/api")
app.include_router(mappings.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Welcome to AegisRisk GRC Platform API"}
