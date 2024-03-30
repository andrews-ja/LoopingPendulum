# Python Modules
import os
import sys
import numpy as np
from pathlib import Path

# Pip Libraries
import cv2 as cv

# Paths
from main import PathClass

sys.path.append(str(Path(__file__).parent.parent.resolve()))
sys.path += PathClass(Path(__file__).parent.parent).getStrPaths("CLASSES_DIR")

class MassTracker:
    def __innit__(
            self,
            clbrImgPath: Path,
            capPath: Path
    ) -> None:
        self.clbrImg = cv.imread(clbrImgPath, cv.IMREAD_COLOR)
        assert self.clbrImg.size() > 0, f"img not found at path: {clbrImgPath}"

        self.cap = cv.VideoCapture(capPath)
        assert self.cap.isOpened(), f"video not found at path: {capPath}"

    def calbirate(self):
        pass
    
    def _processFrame(self, cap: cv.VideoCapture):
        ret, frame = cap.read()
        assert ret, "Could not read frame"

        frameHSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        redMask0 = cv.inRange(frameHSV, np.array([0,50,50]), np.array([10,255,255]))
        redMask1 = cv.inRange(frameHSV, np.array([170,50,50]), np.array([180,255,255]))
        greenMask = cv.inRange(frameHSV, (36, 25, 25), (70, 255,255))

        fullMask = redMask0 + redMask1 + greenMask

        filteredFrame = cv.bitwise_and(frameHSV, frameHSV, mask=fullMask)

    def closeCap(self) -> int:
        try:
            self.cap.release(); return 1
        except Exception as e:
            print(f"Capture did not close: {e}"); return 0