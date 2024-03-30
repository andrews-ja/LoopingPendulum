# Python Modules
import sys
from pathlib import Path

class PathClass:
    def __init__(self, SRC_DIR: Path):
        self.SRC_DIR = SRC_DIR
        self.CLASSES_DIR = SRC_DIR/"Classes"

        self.DATA_DIR = SRC_DIR/".."/"data"

        self.MEDIA_DIR = SRC_DIR/'..'/"media"
        self.RECORDINGS_DIR = self.MEDIA_DIR/"recordings"

    def getStrPaths(self, *args: str) -> list[str]:
        return [str(getattr(self, arg).resolve()) for arg in args]

def main()->None:
    paths = PathClass(Path(__file__).parent)
    sys.path += paths.getStrPaths("CLASSES_DIR")

    #Local Modules
    from Tracker import MassTracker
    from Plotter import DataPlotter

    #tracker = MassTracker()
    #plotter = DataPlotter()

    #tracker.calibrate()

if __name__ == '__main__':
    main()