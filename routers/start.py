import json
import time
import traceback

from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi import File, UploadFile
from typing import Text

from configs.settings import settings
from services.rabbitmq import publisher
from deepstream.live import start_pipeline

router = APIRouter()


def init_external_services(shipment_id):
    # publisher.startup(shipment_id)
    pass

@router.post("/start")
async def start(
    shipment_id: int = 1,
    background_task: BackgroundTasks = None,
):
    try:
        init_external_services(shipment_id)
        background_task.add_task(start_pipeline)
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
