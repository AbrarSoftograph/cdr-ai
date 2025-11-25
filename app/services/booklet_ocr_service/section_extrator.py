from ultralytics import YOLO
from PIL import Image
from typing import List, Dict, Any


def extract_objects_from_images(images: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """
    Extract objects from a list of images using YOLO object detection and return structured data based on image type.

    Args:
        images: List of dictionaries, each with a key ('outlet_copy' or 'partner_copy') and value (image file path)

    Returns:
        List of dictionaries containing structured data based on image type
    """
    # Load YOLO model (auto-downloads yolov8n.pt if not present)
    model = YOLO("app\\ml_models\\cdr_book_v2_100_multiple_class.pt")

    results = []
    for img_dict in images:
        # Assume each dict has only one key-value pair
        key, img_path = list(img_dict.items())[0]

        # Open image
        img = Image.open(img_path)

        # Run prediction
        res = model(img, conf=0.5, iou=0.45)

        detections = {}
        for r in res:
            boxes = r.boxes
            if boxes:
                class_ids = boxes.cls
                xyxy = boxes.xyxy
                for i in range(len(class_ids)):
                    cls = int(class_ids[i])
                    name = model.names[cls]
                    x1, y1, x2, y2 = map(int, xyxy[i].tolist())
                    # Crop the detected object
                    cropped = img.crop((x1, y1, x2, y2))
                    # If multiple detections of same class, keep the last one
                    detections[name] = cropped

        # Structure the result based on key
        if key == "outlet_copy":
            result = {"type": "outlet_copy", "data": {"outlet_id": detections.get("outlet_id")}}
        elif key == "partner_copy":
            partner_1_data = {
                "name_1": detections.get("name_1"),
                "partner_code_1": detections.get("partner_code_1"),
                "age_1": detections.get("age_1"),
                "date_1": detections.get("date_1"),
                "sign_1": detections.get("sign_1"),
                "cheek_mark_1": detections.get("cheek_mark_1"),
                "phn_number_1": detections.get("phn_number_1"),
            }
            partner_2_data = {
                "name": detections.get("name"),
                "partner_code": detections.get("partner_code"),
                "age": detections.get("age"),
                "date": detections.get("date"),
                "sign": detections.get("sign"),
                "cheek_mark": detections.get("cheek_mark"),
                "phn_number": detections.get("phn_number"),
            }
            result = {
                "type": "partner_copy",
                "data": {"partner_1": partner_1_data, "partner_2": partner_2_data},
            }
        else:
            # If key is neither, perhaps raise error or skip
            raise ValueError(f"Unknown image type: {key}")

        results.append(result)
    return results


if __name__ == "__main__":
    # Example usage with new format
    # Assuming we have images in timages, assign types for demonstration
    images = [
        # {"outlet_copy" : "app/test_images/IMG20251111132440.jpg"},
        {"partner_copy": "app/test_images/1000084045.jpg"},
        # {"outlet_copy" : "app/test_images/IMG20251111132509_jpg.rf.b74cbaa9d3b7828f3167e14762d723af.jpg"},# noqa: E501
        # {"partner_copy" : "app/test_images/IMG20251111132016_jpg.rf.9fa3ce5211919c581b8b1fa5790efa34.jpg"}, # noqa: E501
    ]
    result = extract_objects_from_images(images=images)
    print((result))

    # Save cropped images to app/test_images/crops
    # crops_folder = 'app/test_images/crops'
    # os.makedirs(crops_folder, exist_ok=True)

    # saved_count = 0
    # for img_path, detections in result.items():
    #     img_basename = os.path.basename(img_path).split('.')[0]
    #     for obj_name, cropped in detections.items():
    #         save_path = os.path.join(crops_folder, f'{img_basename}_{obj_name}.png')
    #         cropped.save(save_path)
    #         print(f"Saved {save_path}")
    #         saved_count += 1

    # print(f"Total cropped images saved: {saved_count}")
