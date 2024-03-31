# Python Modules
import os
import sys
from pathlib import Path

class PathClass:
    def __init__(self, SRC_DIR: Path):
        self.SRC_DIR = SRC_DIR

        self.CLASSES_DIR = SRC_DIR/"Classes"
        self.DATA_DIR = SRC_DIR/".."/"data"
        self.MEDIA_DIR = SRC_DIR/'..'/"media"

        self.PLOTS_DIR = self.MEDIA_DIR/"plots"
        self.CLBR_DIR = self.MEDIA_DIR/"calibration"
        self.RECORDINGS_DIR = self.MEDIA_DIR/"experimentRecordings"

        self.ANGLES_DIR = self.RECORDINGS_DIR/"angleRecordings"
        self.LENGTHS_DIR = self.RECORDINGS_DIR/"lengthRecordings"
        self.WEIGHTS_DIR = self.RECORDINGS_DIR/"weightsRecordings"

    def getStrPaths(self, *args: str) -> list[str]:
        return [str(getattr(self, arg).resolve()) for arg in args]

def main() -> None:
    paths = PathClass(Path(__file__).parent)

    for path in paths.getStrPaths(paths.__dict__.keys()):
        if not os.path.exists(path):
            print(f"Error: Path does not exist: %s" % path)
            return

    sys.path += paths.getStrPaths("CLASSES_DIR")

    #Local Modules
    from Tracker import MassTracker
    from Plotter import DataPlotter

    # Constants
    COLOUR_RANGES = {
        ((0,50,50), (10,255,255)): "red", # (0-10)
        ((170,50,50), (180,255,255)): "red", # (170-180)
        ((36, 25, 25), (70, 255,255)): "green"
    }
    FPS = 60

    # Initializing Objects
    tracker = MassTracker(COLOUR_RANGES, paths.CLBR_DIR, paths.RECORDINGS_DIR)
    plotter = DataPlotter()

    # Tracking
    ppm = tracker.calibrate("green", 0.27686) # ppm = pixles per meter
    if ppm == -1: return

    for folder in next(os.walk(paths.getStrPaths("RECORDINGS_DIR"))):
        massCoords = tracker.processRecordings(folder, 'red', 'green')
        if massCoords == -1: return

        distDiffs = ([(0, 0)], [(0, 0)])
        n = 1

        # Replacing values in massCoords to metric distances between each x & y point for m1 and m2 respectively
        for i in massCoords: # i corresponds to m1/m2
            pixDiff = (i[n][0] - i[n-1][0], i[n][1] - i[n-1][1]) # (xDiff, yDif)
            distDiff = map(lambda x: x/ppm, pixDiff) # (xDist, yDist)
            distDiffs[i].append(distDiff)
            n += 1

        #TODO: add data from each recording to appropriate csv file

    # Plotting
    #TODO: Create relevant plots for each csv file and populate 'plots' folder

if __name__ == '__main__':
    main()

#TODO: add 'Edit CSV' to recommended extensions