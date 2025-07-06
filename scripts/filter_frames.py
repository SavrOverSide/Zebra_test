import cv2, os, glob, shutil
from ultralytics import YOLO
from tqdm import tqdm

IMG_DIR   = "dataset/images/raw"
OUT_DIR   = "dataset/images/filtered"
STRIDE_N  = 2           # берём каждый 3-й кадр
DIFF_THR  = 8         # средняя разница (0-255)
FOOD_PROXY = {
    'bowl','cup','bottle','wine glass','fork',
    'knife','spoon','pizza','cake','sandwich',
    'plate', 'dining table', 'knife', 'fork', 'spoon'
}

model = YOLO("yolov8n.pt")      # скачает COCO-веса автоматически
os.makedirs(OUT_DIR, exist_ok=True)

prev_gray = None
kept = 0
for idx, path in enumerate(tqdm(sorted(glob.glob(f"{IMG_DIR}/*.jpg")))):
    if idx % STRIDE_N:                      # ──► 1. Stride
        continue

    img  = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if prev_gray is not None:               # ──► 2. Pixel diff
        if cv2.absdiff(gray, prev_gray).mean() < DIFF_THR:
            continue
    prev_gray = gray

    # ──► 3. Proxy-food detector
    res = model(img, verbose=False)[0]
    if not any(model.names[int(b.cls)] in FOOD_PROXY and b.conf > .25
               for b in res.boxes):
        continue

    shutil.copy2(path, f"{OUT_DIR}/frame_{kept:05d}.jpg")
    kept += 1

print(f"✓  Отобрано {kept} кадров.")
