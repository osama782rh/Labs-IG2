import cv2
import torch
from ultralytics import YOLO
from pathlib import Path


def load_yolov8_model():
    # Charger le modèle YOLOv8 pré-entrainé
    model_path = "yolov8n.pt"
    model = YOLO(model_path)
    return model


def detect_pedestrians(frame, model):
    # Utilisation du modèle pour détecter les objets dans la frame
    results = model(frame)

    # Dessiner les boîtes autour des détections
    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            confidence = box.conf[0]
            cls = int(box.cls[0])

            # Si la classe est "person" (classe 0 dans COCO)
            if cls == 0:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f'Person {confidence:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                            (0, 255, 0), 2)
    return frame


def process_video(video_path, model):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("[ERREUR] Impossible d'ouvrir la vidéo.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Détection de piétons
        frame = detect_pedestrians(frame, model)

        cv2.imshow("Pedestrian Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def capture_from_webcam(model):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("[ERREUR] Impossible d'ouvrir la webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = detect_pedestrians(frame, model)
        cv2.imshow("Webcam Pedestrian Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    model = load_yolov8_model()

    print("[INFO] Options disponibles :")
    print("1. Détection de piétons à partir d'une vidéo")
    print("2. Détection de piétons depuis la webcam")

    choice = input("Choisissez une option (1 ou 2) : ")

    if choice == '1':
        video_folder = "data"
        videos = list(Path(video_folder).glob("*.webm"))

        if not videos:
            print("[ERREUR] Aucune vidéo trouvée.")
        else:
            print("[INFO] Vidéos disponibles :")
            for i, video in enumerate(videos):
                print(f"{i + 1}. {video.name}")

            video_choice = int(input("Choisissez une vidéo à traiter : ")) - 1

            if 0 <= video_choice < len(videos):
                selected_video = str(videos[video_choice])
                print(f"[INFO] Traitement de la vidéo : {selected_video}")
                process_video(selected_video, model)
            else:
                print("[ERREUR] Choix invalide.")
    elif choice == '2':
        print("[INFO] Capture depuis la webcam...")
        capture_from_webcam(model)
    else:
        print("[ERREUR] Option invalide.")
