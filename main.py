from fastapi import FastAPI
import uvicorn
from src.api.routes import router
from src.api.auth_routes import router as auth_router
from src.config import config

app = FastAPI(title="Podcast Platform API", version="1.0.0")

app.include_router(auth_router)
app.include_router(router)

@app.get("/")
def root():
    return {
        "name": "Podcast Platform API",
        "version": "1.0.0",
        "docs": "/docs",
        "auth": "/auth/login"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=config.API_PORT)