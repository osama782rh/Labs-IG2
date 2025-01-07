import os
import subprocess
from pathlib import Path


def list_labs(base_path):
    labs = []
    for folder in os.listdir(base_path):
        lab_path = os.path.join(base_path, folder)
        if os.path.isdir(lab_path):
            # Recherche récursive pour trouver main.py dans chaque dossier
            for root, dirs, files in os.walk(lab_path):
                if 'main.py' in files:
                    labs.append(folder)
                    break  # Passe au dossier suivant après avoir ajouté ce lab
    return sorted(set(labs))  # Utilisation de set pour éviter les doublons


def display_menu(labs):
    print("\n[INFO] Sélectionnez un laboratoire à exécuter :")
    for i, lab in enumerate(labs):
        print(f"{i + 1}. {lab}")
    print("0. Quitter")


def run_lab(lab_name, base_path):
    lab_directory = os.path.join(base_path, lab_name)
    lab_path = os.path.join(lab_directory, 'main.py')

    if os.path.exists(lab_path):
        print(f"[INFO] Lancement de {lab_name}...")
        try:
            os.chdir(lab_directory)
            subprocess.run(['python', 'main.py'], check=True)
            os.chdir(base_path)
        except subprocess.CalledProcessError as e:
            print(f"[ERREUR] Échec de l'exécution de {lab_name}/main.py : {e}")
        except Exception as e:
            print(f"[ERREUR] Une erreur s'est produite : {e}")
            os.chdir(base_path)
    else:
        print(f"[ERREUR] Le fichier main.py est introuvable dans {lab_name}")


def main():
    base_path = Path(__file__).parent
    labs = list_labs(base_path)

    while True:
        display_menu(labs)
        choix = input("Votre choix : ")

        if choix == '0':
            print("[INFO] Fin du programme.")
            break

        try:
            choix = int(choix)
            if 1 <= choix <= len(labs):
                selected_lab = labs[choix - 1]
                run_lab(selected_lab, base_path)
            else:
                print("[ERREUR] Choix invalide. Veuillez entrer un nombre valide.")
        except ValueError:
            print("[ERREUR] Entrée non valide. Veuillez entrer un nombre.")


if __name__ == "__main__":
    main()