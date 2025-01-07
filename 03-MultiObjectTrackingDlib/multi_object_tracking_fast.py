from utils import FPS
import numpy as np
import dlib
import cv2
import imutils


def start_tracker(box, label, rgb, inputQueue, outputQueue):
    tracker = dlib.correlation_tracker()
    rect = dlib.rectangle(*box)
    tracker.start_track(rgb, rect)

    while True:
        rgb = inputQueue.get()
        if rgb is None:
            break

        tracker.update(rgb)
        pos = tracker.get_position()
        startX = int(pos.left())
        startY = int(pos.top())
        endX = int(pos.right())
        endY = int(pos.bottom())

        outputQueue.put((label, (startX, startY, endX, endY)))


if __name__ == '__main__':
    print("[INFO] Starting video stream...")

    vs = cv2.VideoCapture('race.mp4')
    if not vs.isOpened():
        print("[ERROR] Unable to open video file 'race.mp4'.")
        exit(1)

    writer = None
    fps = FPS().start()

    while True:
        (grabbed, frame) = vs.read()

        if frame is None:
            print("[ERROR] No frame captured. Ending video stream.")
            break

        frame = imutils.resize(frame, width=600)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == 27:
            break

        fps.update()

    fps.stop()
    print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    if writer is not None:
        writer.release()

    cv2.destroyAllWindows()
    vs.release()
