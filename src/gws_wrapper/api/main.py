from fastapi import FastAPI
from loguru import logger

app = FastAPI(title="gws-wrap API")

@app.get("/")
async def root():
    return {"message": "Google Workspace CLI Wrapper API"}

def run():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
