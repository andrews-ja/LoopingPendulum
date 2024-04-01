# Python modules
import os
from pathlib import Path

# Pip libraries
import numpy as np
import pandas as pd
import plotly.express as px


class DataPlotter:
    def __innit__(self, FPS=60) -> None:
        self.FPS = FPS

    def plot(self, csvPath: str):
        pass
