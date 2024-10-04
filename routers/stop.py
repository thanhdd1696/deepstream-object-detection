import json
import time
import traceback

from fastapi import APIRouter, Depends, BackgroundTasks
from typing import Text
from configs.settings import settings
from deepstream.live import stop_pipeline

router = APIRouter()


@router.post("/stop")
async def start(
    background_task: BackgroundTasks = None,
):
    try:
        background_task.add_task(stop_pipeline)
        return {
            "status": "OK",
            "result": "processing"
        }
    except Exception as e:
        print(traceback.format_exc())
        return {
            "status": "failed",
            "result": ""
        }
