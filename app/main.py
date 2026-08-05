from fastapi import FastAPI
<<<<<<< HEAD
from app.db.database import engine, Base
from app.models.user import User
from app.routers.users import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CreatorIQ API")

app.include_router(user_router)

@app.get("/")
def home():
    return {
        "message": "CreatorIQ API is running"
    }
=======
from app.routers import auth

app = FastAPI(title="Creator Analytics Content Performance Dashboard")

# Include Auth Router
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "API is running!"}
>>>>>>> 567a2ff61666ec1d3b961045a6a013fac9a11976
