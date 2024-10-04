
from pathlib import Path
from typing import Union

from dotenv import load_dotenv
dotenv_path = Path('secrets/local.env')
load_dotenv(dotenv_path=dotenv_path)
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from configs.settings import settings
from routers.start import router as start_router
from routers.stop import router as stop_router


app = FastAPI()
app.include_router(start_router)
app.include_router(stop_router)


@app.get("/")
def health_check():
    return JSONResponse({
        "status": "OK"
    })





