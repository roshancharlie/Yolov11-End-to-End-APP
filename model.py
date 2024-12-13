from ultralytics import YOLO

model = YOLO()
class_map = model.names


def detect(image, inference_id):
    results = model.predict(source=image, save=True, show=False, save_crop=True, project="yolo-11", name=inference_id)
    detection_results = []
    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()
        confidences = result.boxes.conf.cpu().numpy()
        classes = result.boxes.cls.cpu().numpy()

        for box, conf, cls in zip(boxes, confidences, classes):
            detection_results.append({
                "class_name": class_map[int(cls)],
                "confidence": float(conf),
                "bounding_box": {
                    "x_min": float(box[0]),
                    "y_min": float(box[1]),
                    "x_max": float(box[2]),
                    "y_max": float(box[3]),
                }
            })
        return detection_results
