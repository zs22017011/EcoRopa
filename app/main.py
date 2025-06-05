from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import Base, engine
from app.routers import auth, users, items, geolocation, credits, messages

Base.metadata.create_all(bind=engine)

app = FastAPI(title="EcoRopa API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(items.router, prefix="/items", tags=["Items"])
app.include_router(geolocation.router, prefix="/recycle-points", tags=["Recycle Points"])
app.include_router(credits.router, prefix="/credits", tags=["Credits"])
app.include_router(messages.router, prefix="/messages", tags=["Messages"])
