import base64
from unittest.mock import patch, MagicMock

import numpy as np
import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

TEST_UUID = "550e8400-e29b-41d4-a716-446655440000"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_recognize_success():
    fake_result = MagicMock()
    fake_result.text = "0104607024328011210000012345\x1d911234"
    with patch("main.zxingcpp.read_barcodes", return_value=[fake_result]):
        dummy_image = np.zeros((100, 100, 3), dtype=np.uint8)
        import cv2

        _, encoded = cv2.imencode(".png", dummy_image)
        b64_data = base64.b64encode(encoded.tobytes()).decode("utf-8")

        response = client.post(
            "/recognize",
            json={"file_data": b64_data, "operation_uuid": TEST_UUID},
        )

    assert response.status_code == 200
    body = response.json()
    assert body["operation_uuid"] == TEST_UUID
    assert body["status"] == "success"
    assert body["data"] == "0104607024328011210000012345\x1d911234"


def test_recognize_barcode_not_found():
    with patch("main.zxingcpp.read_barcodes", return_value=[]):
        dummy_image = np.zeros((100, 100, 3), dtype=np.uint8)
        import cv2

        _, encoded = cv2.imencode(".png", dummy_image)
        b64_data = base64.b64encode(encoded.tobytes()).decode("utf-8")

        response = client.post(
            "/recognize",
            json={"file_data": b64_data, "operation_uuid": TEST_UUID},
        )

    assert response.status_code == 400
    body = response.json()
    assert body["operation_uuid"] == TEST_UUID
    assert body["status"] == "error"
    assert "ШТРИХКОД НЕ РАСПОЗНАН" in body["message"]
    assert "ValueError" in body["message"]


def test_recognize_invalid_base64():
    response = client.post(
        "/recognize",
        json={"file_data": "not_valid_base64!!!", "operation_uuid": TEST_UUID},
    )

    assert response.status_code == 400
    body = response.json()
    assert body["operation_uuid"] == TEST_UUID
    assert body["status"] == "error"
    assert "ШТРИХКОД НЕ РАСПОЗНАН" in body["message"]


def test_recognize_non_image_base64():
    b64_data = base64.b64encode(b"this is not an image").decode("utf-8")
    response = client.post(
        "/recognize",
        json={"file_data": b64_data, "operation_uuid": TEST_UUID},
    )

    assert response.status_code == 400
    body = response.json()
    assert body["operation_uuid"] == TEST_UUID
    assert body["status"] == "error"
    assert "ШТРИХКОД НЕ РАСПОЗНАН" in body["message"]


def test_recognize_missing_fields():
    response = client.post("/recognize", json={"file_data": "abc"})
    assert response.status_code == 422

    response = client.post("/recognize", json={"operation_uuid": TEST_UUID})
    assert response.status_code == 422

    response = client.post("/recognize", json={})
    assert response.status_code == 422


def test_recognize_general_exception():
    with patch("main.zxingcpp.read_barcodes", side_effect=RuntimeError("test error")):
        dummy_image = np.zeros((100, 100, 3), dtype=np.uint8)
        import cv2

        _, encoded = cv2.imencode(".png", dummy_image)
        b64_data = base64.b64encode(encoded.tobytes()).decode("utf-8")

        response = client.post(
            "/recognize",
            json={"file_data": b64_data, "operation_uuid": TEST_UUID},
        )

    assert response.status_code == 500
    body = response.json()
    assert body["operation_uuid"] == TEST_UUID
    assert body["status"] == "error"
    assert "ШТРИХКОД НЕ РАСПОЗНАН" in body["message"]
    assert "RuntimeError" in body["message"]