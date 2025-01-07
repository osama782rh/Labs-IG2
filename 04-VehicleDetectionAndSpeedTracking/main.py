import cv2
import dlib
import time
import threading
import math
from speed_check import trackMultipleObjects


def main():
    print("[INFO] Starting Vehicle Detection and Speed Tracking...")
    try:
        trackMultipleObjects()
        print("[INFO] Process Completed Successfully.")
    except Exception as e:
        print(f"[ERROR] An error occurred: {str(e)}")


if __name__ == '__main__':
    main()
