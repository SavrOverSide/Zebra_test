from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
import cv2, glob, os

model = YOLO("yolov8s_vietnamese_dishes.pt")
os.makedirs("vis2", exist_ok=True)

for path in glob.glob("dataset/images/filtered/*.jpg"):
    img = cv2.imread(path)
    res = model(img, conf=0.25)[0]

    anno = Annotator(img)
    for b in res.boxes:
        cls = int(b.cls)
        anno.box_label(b.xyxy[0], model.names[cls], color=(0,255,0))

    cv2.imwrite(f"vis/{os.path.basename(path)}", img)
print("готово → vis/")
