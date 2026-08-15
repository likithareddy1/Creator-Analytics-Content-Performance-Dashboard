from fastapi import FastAPI

from app.routers import auth
from app.routers import content

from app.db.database import Base, engine
from app.models.content import Content


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Creator Analytics Content Performance Dashboard"
)


# Include Auth Router
app.include_router(auth.router)

# Include Content Analytics Router
app.include_router(content.router)


@app.get("/")
def root():
    return {"message": "API is running!"}