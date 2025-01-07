import os
import cv2
import imutils
from imutils.video import FPS
import sys
import subprocess

if len(sys.argv) < 3:
    print("Usage : python test_videos_trackers_multiobject.py <video_path> <mode>")
    sys.exit(1)

video_path = sys.argv[1]
mode = sys.argv[2]
converted_path = os.path.abspath(video_path)

# Conversion de la video si necessaire
def convert_video(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Erreur : Le fichier source {input_path} est introuvable.")
        sys.exit(1)

    if not os.path.exists(output_path):
        print(f"Conversion de {input_path} en {output_path}...")
        conversion_command = [
            'ffmpeg', '-i', input_path, '-qscale:v', '2', output_path
        ]
        result = subprocess.run(conversion_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0:
            print(f"Erreur lors de la conversion : {result.stderr.decode(errors='replace')}")
            sys.exit(1)

convert_video(video_path, converted_path)

if not os.path.exists(converted_path):
    print("Erreur : conversion échouée.")
    sys.exit(1)

trackers = ["csrt", "kcf"]

try:
    cv2.legacy.TrackerMOSSE_create()
    trackers.append("mosse")
except AttributeError:
    print("Tracker MOSSE non disponible. Il sera ignoré.")

try:
    cv2.legacy.TrackerMIL_create()
    trackers.append("mil")
except AttributeError:
    print("Tracker MIL non disponible. Il sera ignoré.")

# Tester le suivi d'objet avec selection automatique
def test_tracker(video_path, tracker_name):
    OPENCV_OBJECT_TRACKERS = {
        "csrt": cv2.legacy.TrackerCSRT_create,
        "kcf": cv2.legacy.TrackerKCF_create,
    }

    if "mosse" in trackers:
        OPENCV_OBJECT_TRACKERS["mosse"] = cv2.legacy.TrackerMOSSE_create

    if "mil" in trackers:
        OPENCV_OBJECT_TRACKERS["mil"] = cv2.legacy.TrackerMIL_create

    tracker = OPENCV_OBJECT_TRACKERS[tracker_name]()
    vs = cv2.VideoCapture(video_path, cv2.CAP_FFMPEG)

    if not vs.isOpened():
        print(f"Erreur : impossible d'ouvrir la vidéo {video_path}")
        return

    initBB = None
    fps = None

    ret, frame = vs.read()
    if not ret:
        print("Erreur lors de la lecture initiale de la vidéo.")
        return

    frame = imutils.resize(frame, width=600)
    initBB = cv2.selectROI("Frame", frame, fromCenter=False, showCrosshair=True)

    if initBB and all(initBB):
        tracker.init(frame, initBB)
        fps = FPS().start()
    else:
        print("Aucune selection detectee. Sortie du suivi.")
        vs.release()
        cv2.destroyAllWindows()
        return

    while True:
        ret, frame = vs.read()
        if not ret:
            print("Fin de la vidéo.")
            break

        frame = imutils.resize(frame, width=600)
        (H, W) = frame.shape[:2]

        success, box = tracker.update(frame)
        if success:
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        fps.update()
        fps.stop()

        info = [
            ("Tracker", tracker_name),
            ("Success", "Yes" if success else "No"),
            ("FPS", "{:.2f}".format(fps.fps())),
        ]

        for (i, (k, v)) in enumerate(info):
            text = "{}: {}".format(k, v)
            cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        try:
            if key == ord("q") or cv2.getWindowProperty("Frame", cv2.WND_PROP_AUTOSIZE) < 1:
                break
        except cv2.error:
            break

    vs.release()
    cv2.destroyAllWindows()

print(f"Testing video {os.path.basename(converted_path)} with trackers: {trackers}")
for tracker_name in trackers:
    test_tracker(converted_path, tracker_name)