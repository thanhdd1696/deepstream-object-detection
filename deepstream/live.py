from uuid import uuid4
from argparse import ArgumentParser

from deepstream.app.pipeline import pipeline


def start_pipeline():
    inference_id = str(uuid4())
    pipeline.start(inference_id)


def stop_pipeline():
    pipeline.stop()


if __name__ == "__main__":
    start_pipeline()
    stop_pipeline()
