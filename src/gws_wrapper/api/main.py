from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from loguru import logger
from gws_wrapper.api.routes import mail, calendar, drive

app = FastAPI(title="gws-wrap API")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error", "detail": str(exc)},
    )

app.include_router(mail.router)
app.include_router(calendar.router)
app.include_router(drive.router)

@app.get("/")
async def root():
    return {"message": "Google Workspace CLI Wrapper API"}

def run():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
