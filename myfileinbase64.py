import base64
import json
import sys


def file_to_base64_json(input_path, output_path):
    with open(input_path, "rb") as f:
        file_bytes = f.read()

    b64_str = base64.b64encode(file_bytes).decode("utf-8")

    payload = {
        "file_data": b64_str,
        "operation_uuid": "550e8400-e29b-41d4-a716-446655440000",
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Использование: python myfileinbase64.py <входной_файл> <выходной_json>")
        sys.exit(1)

    file_to_base64_json(sys.argv[1], sys.argv[2])
