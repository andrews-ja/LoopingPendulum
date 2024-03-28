import cv2 as cv
from pathlib import Path

class Tracker:
    def __innit__(
            self,
            cap_path: Path
    ) -> None:
        self.cap = cv.VideoCapture(cap_path)
        assert self.cap.isOpened(), f"incorrect path: {cap_path}"

    def getFrame(self, cap: cv.VideoCapture):
        success, frame = self.cap.read()
        return frame if success else "Could not read frame"

    def closeCap(self) -> int:
        try:
            self.cap.release(); return 1
        except Exception as e:
            print(f"Capture did not close: {e}"); return 0
