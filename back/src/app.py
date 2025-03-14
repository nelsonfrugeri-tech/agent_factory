import uvicorn
from fastapi import FastAPI
from src.router.router import main_router

def api():
    fast_api = FastAPI(title="modelhub-api", description="ModelHub API")
    fast_api.include_router(main_router)
    return fast_api

if __name__ == "__main__":
    uvicorn.run(
        api(), 
        host="0.0.0.0", 
        port=8080,
    )