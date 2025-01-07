# main.py

import os

def run_people_counter():
    prototxt_path = "mobilenet_ssd/MobileNetSSD_deploy.prototxt"
    model_path = "mobilenet_ssd/MobileNetSSD_deploy.caffemodel"
    video_input_path = "videos/o.mp4"
    output_path = "output/output_01.avi"

    # Vérifier si les fichiers nécessaires existent
    if not os.path.exists(prototxt_path):
        print(f"[ERREUR] Fichier introuvable: {prototxt_path}")
        return

    if not os.path.exists(model_path):
        print(f"[ERREUR] Fichier introuvable: {model_path}")
        return

    if not os.path.exists(video_input_path):
        print(f"[ERREUR] Fichier introuvable: {video_input_path}")
        return

    # Exécution du script people_counter.py
    command = (
        f"python people_counter.py "
        f"--prototxt {prototxt_path} "
        f"--model {model_path} "
        f"--input {video_input_path} "
        f"--output {output_path}"
    )

    print("[INFO] Exécution du compteur de personnes...")
    os.system(command)
    print("[INFO] Traitement terminé.")

if __name__ == "__main__":
    run_people_counter()
