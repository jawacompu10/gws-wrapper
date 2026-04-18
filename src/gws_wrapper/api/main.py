from fastapi import FastAPI
from loguru import logger
from gws_wrapper.api.routes import mail, calendar

app = FastAPI(title="gws-wrap API")

app.include_router(mail.router)
app.include_router(calendar.router)

@app.get("/")
async def root():
    return {"message": "Google Workspace CLI Wrapper API"}

def run():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
