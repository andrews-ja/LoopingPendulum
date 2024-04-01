# Python modules
import os
import sys
import csv
from pathlib import Path


class PathClass:
    def __init__(self, SRC_DIR: Path) -> None:
        self.SRC_DIR = SRC_DIR
        self.CLASSES_DIR = SRC_DIR / "Classes"
        self.DATA_DIR = SRC_DIR / ".." / "data"
        self.MEDIA_DIR = SRC_DIR / ".." / "media"

        self.PLOTS_DIR = self.MEDIA_DIR / "plots"
        self.CLBR_DIR = self.MEDIA_DIR / "calibration"
        self.RECORDINGS_DIR = self.MEDIA_DIR / "recordings"

    def getPaths(
        self,
        *args: str,
    ) -> list[str]:
        return [getattr(self, arg).resolve() for arg in args]


def main() -> None:
    paths = PathClass(Path(__file__).parent)

    for path in paths.getPaths(paths.__dict__.keys()):
        if not os.path.exists(path):
            print(f"Error: Path does not exist: %s" % path)
            return

    # Constants
    COLOUR_RANGES = {
        ((0, 50, 50), (10, 255, 255)): "red",  # (0-10)
        ((170, 50, 50), (180, 255, 255)): "red",  # (170-180)
        ((36, 25, 25), (70, 255, 255)): "green",
    }
    (CLASSES_DIR, DATA_DIR, CLBR_DIR, RECORDINGS_DIR) = paths.getPaths
    ("CLASSES_DIR", "DATA_DIR", "CLBR_DIR", "RECORDINGS_DIR")

    sys.path += [str(CLASSES_DIR), str(DATA_DIR)]

    # Local modules
    from Tracker import MassTracker
    from Plotter import DataPlotter

    # Initializing objects
    tracker = MassTracker(COLOUR_RANGES, CLBR_DIR)
    plotter = DataPlotter()

    # Tracking
    ppm = tracker.calibrate("green", 0.27686)  # ppm = pixles per meter
    if ppm == -1:
        return

    for experimentFolder in next(os.walk(RECORDINGS_DIR)):
        runNum = 1

        for recFileName in next(os.walk(RECORDINGS_DIR / experimentFolder)):
            massCoords: tuple[list, list] = tracker.processRecordings(
                RECORDINGS_DIR / experimentFolder / recFileName, "red", "green"
            )  # ([(x, y), ...], [(x, y), ...])
            if not massCoords:
                return

            dispList = [[], []]
            n = 1

            # Replacing values in massCoords to metric distances between each x & y point for m1 and m2 respectively
            while n <= len(massCoords[0]):
                for i in massCoords:  # i corresponds to m1/m2
                    pixDiff = (
                        i[n][0] - i[-1][0],
                        i[n][1] - i[-1][1],
                    )  # (xDiff, yDif) where (0, 0) is the final pos of m1
                    distDiff = map(lambda x: x / ppm, pixDiff)  # (xDist, yDist)
                    dispList[i].append(distDiff)
                n += 1

        # Writing CSV data
        csvFilePath = f"{DATA_DIR}/{experimentFolder}/dispData/run{runNum}.csv"
        with open(csvFilePath, "w") as csvFile:
            print("Writing %s data to run%s.csv" % (experimentFolder, runNum))
            writer = csv.writer(csvFile)
            writer.writerow(("M1 Displacement", "M2 Displacement"))

            for rowNum in range(len(dispList[0])):
                writer.writerow((dispList[0][rowNum], dispList[1][rowNum]))

        # Plotting
        print("Plotting data from %s" % csvFilePath.split("/")[-1])
        plotter.plot(csvFilePath)


if __name__ == "__main__":
    main()

# TODO: add 'Edit CSV' to recommended extensions
