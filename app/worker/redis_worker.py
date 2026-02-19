import json
import time

import redis

from app.converters import csv_to_excel, img_to_jpg, pdf_to_docs

redis_client = redis.Redis(host="localhost", port=6379, db=0)


def process_job(job_data):
    ext = job_data["to_ext"]
    path = job_data["input_path"]

    if ext == "jpg":
        return img_to_jpg(path)

    elif ext == "xlsx":
        return csv_to_excel(path)

    elif ext == "docx":
        return pdf_to_docs(path)

    else:
        raise ValueError("Unsupported conversion")


def start_worker():
    print("Redis worker started...")

    while True:
        job = redis_client.blpop("file_conversion_queue", timeout=5)

        if job:
            job_bytes = job
            job_data = json.loads(job_bytes)
            process_job(job_data)
            print("Processing:", job_data)
            output = process_job(job_data)
            print("Done:", output)

        time.sleep(1)
