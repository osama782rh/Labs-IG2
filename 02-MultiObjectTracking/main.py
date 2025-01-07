import os
import subprocess

VIDEOS = [
    "los_angeles.mp4",
    "nascar.mp4",
    "soccer_01.mp4",
    "soccer_02.mp4"
]

def display_menu():
    print("\n=== Menu de Test des Vidéos (Multi-Object Tracking) ===")
    for i, video in enumerate(VIDEOS):
        print(f"{i + 1}. {video}")
    print("0. Quitter")


def run_tracker(video_name):
    script_path = os.path.join(os.path.dirname(__file__), 'test_videos_trackers_multiobject.py')
    video_path = os.path.abspath(os.path.join(os.path.dirname(__file__), video_name))

    if not os.path.exists(script_path):
        print(f"Erreur : le fichier {script_path} n'existe pas.")
        return

    if not os.path.exists(video_path):
        print(f"Erreur : la vidéo {video_path} n'existe pas.")
        return

    print(f"\nLancement du suivi multi-objets pour {video_name}...")
    print(f"[DEBUG] Script Path: {script_path}")
    print(f"[DEBUG] Video Path: {video_path}")

    try:
        subprocess.run(["python", script_path, "-v", video_path, "--mode", "multi"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERREUR] Échec de l'exécution : {e}")


if __name__ == "__main__":
    while True:
        display_menu()
        choice = input("Choisissez une vidéo à tester (0 pour quitter) : ")

        if choice == "0":
            print("Sortie du programme.")
            break

        if choice.isdigit() and 1 <= int(choice) <= len(VIDEOS):
            selected_video = VIDEOS[int(choice) - 1]
            run_tracker(selected_video)
        else:
            print("Choix invalide, veuillez réessayer.")
