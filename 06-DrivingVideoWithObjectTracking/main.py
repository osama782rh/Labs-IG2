import os
import cv2
from pathlib import Path
import numpy as np


def load_yolo_model():
    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    return net, output_layers


def detect_objects(frame, net, output_layers):
    height, width = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    detections = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []

    for output in detections:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5:  # Seulement les détections fiables
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    return boxes, confidences, class_ids


def draw_labels(frame, boxes, confidences, class_ids, classes):
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    font = cv2.FONT_HERSHEY_SIMPLEX

    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = confidences[i]
            color = (0, 255, 0)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, f"{label} {round(confidence, 2)}", (x, y - 5), font, 0.6, color, 2)


def object_tracking(video_path, net, output_layers, classes):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("[ERREUR] Impossible d'ouvrir la vidéo.")
        return

    print(f"[INFO] Lecture de la vidéo : {video_path}")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        boxes, confidences, class_ids = detect_objects(frame, net, output_layers)
        draw_labels(frame, boxes, confidences, class_ids, classes)

        cv2.imshow("Video", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def list_videos():
    video_folder = "."
    files = list(Path(video_folder).glob("*.mov")) + list(Path(video_folder).glob("*.mp4"))
    return files


if __name__ == "__main__":
    videos = list_videos()

    if not videos:
        print("[ERREUR] Aucune vidéo trouvée dans le dossier.")
    else:
        print("[INFO] Vidéos disponibles :")
        for i, video in enumerate(videos):
            print(f"{i + 1}. {video.name}")

        choice = int(input("Choisissez une vidéo à lancer (entrez le numéro) : ")) - 1

        if 0 <= choice < len(videos):
            selected_video = str(videos[choice])
            print(f"[INFO] Vidéo sélectionnée : {selected_video}")

            # Charger le modèle YOLO
            net, output_layers = load_yolo_model()

            # Classes pour YOLO (COCO dataset)
            classes = open("coco.names").read().strip().split("\n")

            # Lancer la détection et le suivi
            object_tracking(selected_video, net, output_layers, classes)
        else:
            print("[ERREUR] Choix invalide.")
