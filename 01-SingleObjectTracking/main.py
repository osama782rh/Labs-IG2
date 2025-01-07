import os
import subprocess

VIDEOS = [
    "american_pharoah.mp4",
    "dashcam_boston.mp4",
    "drone.mp4",
    "highway.mp4",
    "nascar_01.mp4",
    "nascar_02.mp4",
    "race.mp4"
]


def display_menu():
    print("\n=== Menu de Test des Vidéos ===")
    for i, video in enumerate(VIDEOS):
        print(f"{i + 1}. {video}")
    print("0. Quitter")


def run_tracker(video_name):
    script_path = os.path.join(os.path.dirname(__file__), 'test_all_videos_trackers.py')
    video_path = os.path.abspath(os.path.join(os.path.dirname(__file__), video_name))

    if not os.path.exists(script_path):
        print(f"Erreur : le fichier {script_path} n'existe pas.")
        return

    if not os.path.exists(video_path):
        print(f"Erreur : la vidéo {video_path} n'existe pas.")
        return

    print(f"\nLancement du suivi pour {video_name}...\n")
    subprocess.run(["python", script_path, video_path], check=True)


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
