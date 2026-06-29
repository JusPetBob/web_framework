import sys
from typing import Literal

from PyQt6.QtWidgets import QApplication
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np


class Display:
    def __init__(self, x, y, z):
        self.x = 0
        self.y = 0
        self.z = 0

        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication(sys.argv)

        self.view = gl.GLViewWidget()
        self.view.setWindowTitle("3D Display")
        self.view.resize(900, 700)
        
        self.view.addItem(gl.GLTextItem(pos=(x, 0, 0), text="X"))
        self.view.addItem(gl.GLTextItem(pos=(0, y, 0), text="Y"))
        self.view.addItem(gl.GLTextItem(pos=(0, 0, z), text="Z"))
        
        self.view.show()

        # Camera
        self.view.setCameraPosition(distance=max(x, y, z) * 1.5)

        # Axis
        axis = gl.GLAxisItem()
        axis.setSize(x, y, z)
        self.view.addItem(axis)

        # Single point
        self.point = gl.GLScatterPlotItem(
            pos=np.array([[0.0, 0.0, 0.0]]),
            color=(1, 0, 0, 1),
            size=15,
            pxMode=True,
        )
        self.view.addItem(self.point)

        self.app.processEvents()

    def set_pos(self, x, y, z):
        self.x, self.y, self.z = x, y, z

        self.point.setData(
            pos=np.array([[x, y, z]], dtype=float)
        )

        # Update window
        self.app.processEvents()

    def step_x(self, dir: Literal[-1, 0, 1]):
        self.set_pos(self.x + dir, self.y, self.z)

    def step_y(self, dir: Literal[-1, 0, 1]):
        self.set_pos(self.x, self.y + dir, self.z)

    def step_z(self, dir: Literal[-1, 0, 1]):
        self.set_pos(self.x, self.y, self.z + dir)
    
    def step_all(self, xdir: Literal[-1, 0, 1], ydir: Literal[-1, 0, 1], zdir: Literal[-1, 0, 1]):
        self.set_pos(self.x+xdir, self.y+ydir, self.z+zdir)


if __name__ == "__main__":
    d = Display(2000, 2000, 1000)

    for i in range(1000):
        d.step_all(1,1,1)

    input()