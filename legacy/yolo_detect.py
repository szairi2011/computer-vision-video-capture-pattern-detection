import cv2
from ultralytics import YOLO

class YOLODetector:
    def __init__(self, model_name='yolov8n.pt', classes=None, conf=0.3):
        """
        model_name: YOLOv8 model file (e.g., 'yolov8n.pt')
        classes: list of class names to detect (None = all)
        conf: confidence threshold
        """
        self.model = YOLO(model_name)
        self.classes = classes
        self.conf = conf

    def detect(self, frame):
        results = self.model(frame, conf=self.conf)
        boxes = []
        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                label = self.model.names[cls_id]
                if self.classes is None or label in self.classes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    boxes.append({
                        'box': (x1, y1, x2, y2),
                        'label': label,
                        'conf': conf
                    })
        return boxes

    @staticmethod
    def draw_boxes(frame, boxes):
        for b in boxes:
            x1, y1, x2, y2 = b['box']
            label = f"{b['label']} {b['conf']:.2f}"
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.putText(frame, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
        return frame
