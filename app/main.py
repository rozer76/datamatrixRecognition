import base64

import cv2
import numpy as np
import uvicorn
import zxingcpp
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(title="DataMatrix Recognition API")


class RecognizeRequest(BaseModel):
    file_data: str
    operation_uuid: str


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/recognize")
async def recognize(request: RecognizeRequest):
    try:
        image_bytes = base64.b64decode(request.file_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)

        if image is None:
            raise ValueError("Не удалось декодировать изображение из base64")

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        results = zxingcpp.read_barcodes(thresh)

        if results:
            decoded_text = results[0].text
            return JSONResponse(
                status_code=200,
                content={
                    "operation_uuid": request.operation_uuid,
                    "status": "success",
                    "data": decoded_text,
                },
            )
        else:
            raise ValueError("DataMatrix код не найден на изображении")

    except ValueError as ex:
        err_template = "ШТРИХКОД НЕ РАСПОЗНАН. Ошибка типа {0}"
        err_message = err_template.format(type(ex).__name__)
        return JSONResponse(
            status_code=400,
            content={
                "operation_uuid": request.operation_uuid,
                "status": "error",
                "message": err_message,
            },
        )

    except Exception as ex:
        err_template = "ШТРИХКОД НЕ РАСПОЗНАН. Ошибка типа {0}"
        err_message = err_template.format(type(ex).__name__)
        return JSONResponse(
            status_code=500,
            content={
                "operation_uuid": request.operation_uuid,
                "status": "error",
                "message": err_message,
            },
        )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    err_template = "ШТРИХКОД НЕ РАСПОЗНАН. Ошибка типа {0}"
    err_message = err_template.format(type(exc).__name__)
    return JSONResponse(
        status_code=500,
        content={
            "operation_uuid": "",
            "status": "error",
            "message": err_message,
        },
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
