# Python modules
import os
import math
from pathlib import Path

# Pip libraries
import cv2 as cv
import numpy as np
from PIL import Image

indent = "    "


class MassTracker:
    def __innit__(
        self,
        colourRanges: dict,
        clbrPath: str,
    ) -> None:
        self.colourRanges = colourRanges
        self.clbrPath = clbrPath

    def _findColour(
        self, frame: np.ndarray, colour: str
    ) -> tuple[int, int, int, int] | None:

        frameHSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        for range in self.colourRanges:
            if range == colour:
                mask += cv.inRange(frameHSV, range[0], range[1])

        # (x1, y1, x2, y2)
        BBox = Image.fromarray(mask).getbbox()

        return BBox

    def calbirate(self, clbrColour: str, clbrSize: int) -> float:
        ppmList: list[float] = []

        print("Looking for images in: '%s'..." % self.clbrPath)
        for _, _, file in next(os.walk(self.clbrPath)):
            print(indent + "File found: '%s'" % file)

            fileType = file.split(".")[-1]

            if fileType in ["jpeg", "jpg", "png"]:
                img = cv.imread(self.clbrPath, cv.IMREAD_COLOR)
                clbrBBox = self._findColour(img, clbrColour)  # (x1, y1, x2, y2)

                if clbrBBox:
                    ppm = (
                        math.hypot(clbrBBox[0] + clbrBBox[2], clbrBBox[1] + clbrBBox[3])
                        / clbrSize
                    )
                    ppmList.append(ppm)
                    print(indent * 2 + "Value added: %s" % ppm)
                else:
                    print(indent * 2 + "Error: Calibration box not found")
                    return -1
            else:
                print(indent + "Error: Invalid fileType: %s" % fileType)
                return -1

        avgPpm = sum(ppmList) / len(ppmList)

        if avgPpm > 0:
            print("Tracker calibrated ==> pixles * meter^-1 = %s\n" % avgPpm)
            return avgPpm

        print("Error: No files found")
        return -1

    def processRecording(
        self,
        filePath: str,
        m1Colour: str,
        m2Colour: str,
    ) -> tuple[list, list] | None:
        m1Pos, m2Pos = [], []

        fileName = filePath.split("/")[-1]
        experimentPath = filePath.removesuffix(fileName)

        print("Searching for recordings in: '%s'..." % experimentPath)
        print(indent + "Analysing recording: '%s'..." % fileName)

        fileType = fileName.split(".")[-1]

        if fileType in ["mp4", "avi"]:
            cap = cv.VideoCapture(filePath)
            assert cap.isOpened(), indent + "Error: Cannot open recording %s" % fileName

            ret, frame = cap.read()
            assert ret, indent * 2 + "Error: Could not read frame"

            m1BBox = self._findColour(frame, m1Colour)
            m2BBox = self._findColour(frame, m2Colour)

            getCoords = lambda BBox: (
                (BBox[0] + BBox[2]) / 2,
                (BBox[1] + BBox[3]) / 2,
            )  # (x, y)

            m1Pos.append(getCoords(m1BBox))
            m2Pos.append(getCoords(m2BBox))

            print(indent * 2 + "Data added")

            try:
                cap.release()
                return (m1Pos, m2Pos)
            except Exception as e:
                print(
                    indent * 2 + "Error: Capture '%s' did not close: %s" % fileName, e
                )
                return
        print("Invalid file type %s" % fileType)
