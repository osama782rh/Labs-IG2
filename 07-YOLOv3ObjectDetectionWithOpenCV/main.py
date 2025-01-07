import cv2
import numpy as np
import os
from pathlib import Path


# Chargement du modèle YOLO
def load_yolo_model():
    weights_path = "yolov3-coco/yolov3.weights"
    cfg_path = "yolov3-coco/yolov3.cfg"
    labels_path = "yolov3-coco/coco-labels"

    # Charger les classes COCO
    classes = open(labels_path).read().strip().split("\n")

    # Charger YOLO
    net = cv2.dnn.readNet(weights_path, cfg_path)
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

    return net, output_layers, classes


# Détection des objets dans une frame
def detect_objects(frame, net, output_layers):
    height, width = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    outputs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []

    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5:  # Seulement les détections avec forte confiance
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


# Dessiner les boîtes autour des objets détectés
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


# Suivi de la vidéo avec détection en temps réel
def process_video(video_path, net, output_layers, classes):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("[ERREUR] Impossible d'ouvrir la vidéo.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Détecter et dessiner les objets
        boxes, confidences, class_ids = detect_objects(frame, net, output_layers)
        draw_labels(frame, boxes, confidences, class_ids, classes)

        cv2.imshow("YOLO Object Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# Liste des vidéos disponibles dans le dossier
def list_videos():
    video_folder = "."
    files = list(Path(video_folder).glob("*.mov")) + list(Path(video_folder).glob("*.mp4"))
    return files


if __name__ == "__main__":
    videos = list_videos()

    if not videos:
        print("[ERREUR] Aucune vidéo trouvée.")
    else:
        print("[INFO] Vidéos disponibles :")
        for i, video in enumerate(videos):
            print(f"{i + 1}. {video.name}")

        choice = int(input("Choisissez une vidéo à traiter (entrez le numéro) : ")) - 1

        if 0 <= choice < len(videos):
            selected_video = str(videos[choice])
            print(f"[INFO] Vidéo sélectionnée : {selected_video}")

            # Charger le modèle YOLO
            net, output_layers, classes = load_yolo_model()

            # Lancer le traitement de la vidéo
            process_video(selected_video, net, output_layers, classes)
        else:
            print("[ERREUR] Choix invalide.")
