import magpylib as magpy
import numpy as np

magnet = magpy.magnet.Cylinder(
    polarization=(0, 0, 1),
    dimension=(1, 1),
)
current = magpy.current.Circle(
    position = [(0, 0, z) for z in (-5, 0, 5)],
    current=1,
    diameter=3,
)
dipole = magpy.misc.Dipole(
    moment=(0, 0, 1),
    position=np.linspace((2, 0, -2), (2, 0, 2), 20),
)
sensor = magpy.Sensor(
    pixel=[(0, 0, z) for z in (-0.5, 0, 0.5)],
    position=(-2, 0, 0),
)
magpy.show(magnet, current, dipole, sensor)