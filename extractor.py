import requests
import os
import cv2
from datetime import datetime, time
from retinaface import RetinaFace
from requests.auth import HTTPDigestAuth

HIKVISION_HOST = "${CAMERA_HOST}"
USERNAME = "${USERNAME}"
PASSWORD = "${PASSWORD}"
STREAM_URL = f"{HIKVISION_HOST}/ISAPI/Event/notification/alertStream"
SAVE_DIR = "${DIRECTORY}"
os.makedirs(SAVE_DIR, exist_ok=True)

JPEG_START = b'\xff\xd8'
JPEG_END = b'\xff\xd9'

TARGET_SIZE = (112, 112)

def is_within_working_hours():
    now = datetime.now().time()
    return time(9, 0) <= now <= time(18, 0)

print("[INFO] Connecting к alertStream...")
response = requests.get(STREAM_URL, auth=HTTPDigestAuth(USERNAME, PASSWORD), stream=True)

buffer = b""
image_count = 0
face_crop_count = 0

print("[INFO] Stremaing...")

for chunk in response.iter_content(chunk_size=1024):
    if not chunk or not is_within_working_hours():
        continue

    buffer += chunk

    while True:
        start = buffer.find(JPEG_START)
        end = buffer.find(JPEG_END, start)

        if start != -1 and end != -1:
            jpeg_data = buffer[start:end + 2]
            buffer = buffer[end + 2:]
            image_count += 1

            img_path = os.path.join(SAVE_DIR, f"frame_{image_count:04d}.jpg")
            with open(img_path, "wb") as f:
                f.write(jpeg_data)
            print(f"Saved image: {img_path}")

            if image_count % 2 == 1:
                try:
                    faces = RetinaFace.extract_faces(img_path=img_path, align=True)
                    for face in faces:
                        face_resized = cv2.resize(face, TARGET_SIZE)
                        face_path = os.path.join(SAVE_DIR, f"face_{face_crop_count:04d}.jpg")
                        cv2.imwrite(face_path, cv2.cvtColor(face_resized, cv2.COLOR_RGB2BGR))
                        print(f"Saved face crop: {face_path}")
                        face_crop_count += 1
                except Exception as e:
                    print(f"[!] Error during {img_path}: {e}")

        else:
            break
