import base64
import json
import os

from dotenv import load_dotenv


load_dotenv()
TAG_JSON_PATH = os.getenv("TAG_JSON_PATH")


def encode_tag_data(data: str) -> str:
    return base64.b64encode(data.encode("utf-8")).decode("utf-8")


file_in = open(TAG_JSON_PATH, "r", encoding="utf-8")

tag_json = json.loads(file_in.read())
file_in.close()
for k, v in tag_json.items():
    data = v["data"]
    tag_json[k]["data"] = encode_tag_data(data)

file_out = open(TAG_JSON_PATH, "w", encoding="utf-8")
file_out.write(json.dumps(tag_json, sort_keys=True))
file_out.close()
