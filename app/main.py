from fastapi import FastAPI
from app.api.endpoints import router
from app.database.database import engine
from app.models.models import Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Prodigy Programs API",
    description="API for managing daily 5-minute program activities",
    version="1.0.0"
)

app.include_router(router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to Prodigy Programs API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)