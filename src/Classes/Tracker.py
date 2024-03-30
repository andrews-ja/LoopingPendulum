# Python Modules
import os
import math
from pathlib import Path

# Pip Libraries
import cv2 as cv
import numpy as np
from PIL import Image

global indent
indent = '    '

class MassTracker:
    def __innit__(
            self,
            colourRanges: dict,
            clbrPath: str,
            recordingPath: str
    ) -> None:
        self.colourRanges = colourRanges
        self.clbrPath = clbrPath
        self.recordingPath = recordingPath
    
    def _findColour(
        self,
        frame: np.ndarray,
        colour: str
    ) -> tuple[int, int, int, int] | None:

        frameHSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        for range in self.colourRanges:
            if range == colour:
                mask += cv.inRange(frameHSV, range[0], range[1])

        # (x1, y1, x2, y2)
        BBox = Image.fromarray(mask).getbbox()

        return BBox
        
    def calbirate(
        self,
        clbrColour: str,
        clbrSize: int
    ) -> int:
        ppmList: list[float] = []

        print("Looking for images in: '%s'..." % self.clbrPath)
        for file in next(os.walk(self.clbrPath)):
            print(indent + "File found: '%s'" % file)

            filetype = file.split('.')[-1]

            if filetype in ['jpeg', 'jpg', 'png']:   
                img = cv.imread(self.clbrPath, cv.IMREAD_COLOR)
                clbrBBox = self._findColour(img, clbrColour) # (x1, y1, x2, y2)

                if clbrBBox:
                    ppm = math.hypot(clbrBBox[0] + clbrBBox[2], clbrBBox[1] + clbrBBox[3]) / clbrSize
                    ppmList.append(ppm)
                    print(indent*2 + "Value added: %s" % ppm)
                else:
                    print(indent*2 + "Error: Calibration box not found"); return -1

            else:
                print(indent + "Error: Invalid filetype: %s" % filetype); return -1

        avgPpm = sum(ppmList)/len(ppmList)

        if avgPpm > 0:
            print("Tracker calibrated ==> pixles * meter^-1 = %s\n" %avgPpm)
            return avgPpm
        
        print("Error: No files found"); return -1

    def processRecordings(
        self,
        m1Colour: str,
        m2Colour: str,
    ) -> tuple[
        list[tuple[int, int]],
        list[tuple[int, int]]
        ]:
        m1Pos, m2Pos = [], []

        print("Searching for recordings in: '%s'..." % self.recordingPath)
        for file in next(os.walk(self.recordingPath)):
            print(indent + "Analysing recording: '%s'..." % file)

            filetype = file.split('.')[-1]

            if filetype in ['mp4', 'avi']:
                cap = cv.VideoCapture(file)
                assert self.cap.isOpened(), indent + "Error: Cannot open recording %s" % file

                ret, frame = cap.read()
                assert ret, indent*2 + "Error: Could not read frame"

                m1BBox = self._findColour(frame, m1Colour)
                m2BBox = self._findColour(frame, m2Colour)

                getCoords: tuple[int, int] = lambda BBox: ((BBox[0] + BBox[2])/2 , (BBox[1] + BBox[3])/2) # (x, y)

                m1Pos.append(getCoords(m1BBox))
                m2Pos.append(getCoords(m2BBox))

                print(indent*2 + "Data added")

                try:
                    self.cap.release()
                    return (m1Pos, m2Pos)
                except Exception as e:
                    print(indent*2 + "Error: Capture %s did not close: %s" % file, e); return -1

        print(indent + "Experiment analysed: %s\n" % self.recordingPath)
    print("Media processed ==> Data saved")
