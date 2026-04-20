from fastapi import FastAPI
from app.database import engine, Base
from app.routers import pc, session, auth

from app.models.pc import PCStation
from app.models.session import UsageSession
from app.models.user import User

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CyberCore iCafe Management API")

app.include_router(auth.router)
app.include_router(pc.router)
app.include_router(session.router)

@app.get("/")
def root():
    return {"message": "Welcome to CyberCore iCafe API"}