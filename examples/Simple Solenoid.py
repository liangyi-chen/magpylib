import magpylib as magpy
import pyvista as pv
import numpy as np
import matplotlib.pyplot as plt
import time

start_time = time.perf_counter()

def solenoid(r_in, r_out, L, N, center, current):   #Function to generate a solenoid coil with provided parameters
    d = (L*(r_out-r_in)/N)**0.5
    N_L = int(np.round(L/d))
    N_r = int(np.round((r_out-r_in)/d))
    solenoid_coil = magpy.Collection()
    for z in np.linspace(center-L/2, center+L/2, N_L):
        for r in np.linspace(r_in, r_out, N_r):
            winding = magpy.current.Circle(
                current = current*N/(N_L*N_r),  #scale the current by the error introduced by using integer N_L and N_r
                diameter = 2*r,
                position = (0, 0, z),
                )
        solenoid_coil.add(winding)
    return solenoid_coil

coil1 = solenoid(0.1397, 0.1431, 0.42, 7559, 0, 1)
coil2 = solenoid(0.1431, 0.1465, 0.0656, 1180.7, 0.1772, 1)
coil3 = solenoid(0.1431, 0.1465, 0.0656, 1180.7, -0.1772, 1)

magnet = magpy.Collection(coil1, coil2, coil3)

print(f"Magnets created. Took: {time.perf_counter() - start_time:.4f} seconds")

sensor_position = np.linspace((0, 0, -0.4), (0, 0, 0.4), 81)
sens = magpy.Sensor(position = sensor_position)
B = magpy.getB(magnet, sens)
print(B)

Bz_with_z = np.column_stack((sensor_position[:,2], B[:,2]))
print(Bz_with_z)

#plot Bz against z
plt.plot(Bz_with_z[:,0], Bz_with_z[:,1])
plt.xlabel("z (m)")
plt.ylabel(r"$B_z$ (T)")
plt.show()
'''
start_time = time.perf_counter()
# Create a 3D grid with Pyvista
grid = pv.ImageData(
    dimensions=(41, 41, 41),
    spacing=(0.001, 0.001, 0.1),
    origin=(-0.02, -0.02, -0.02),
)
print(f"Grid created. Took: {time.perf_counter() - start_time:.4f} seconds")

start_time = time.perf_counter()
# Compute B-field and add as data to grid
grid["B"] = magnet.getB(grid.points) * 1000  # T -> mT
print(f"B field computed. Took: {time.perf_counter() - start_time:.4f} seconds")

start_time = time.perf_counter()
# Compute the field lines
seed = pv.Disc(inner=0.001, outer=0.003, r_res=1, c_res=9)
strl = grid.streamlines_from_source(
    seed,
    vectors="B",
    max_step_length=2,
    max_length=.1,
    integration_direction="both",
)
print(f"Field lines computed. Took: {time.perf_counter() - start_time:.4f} seconds")

start_time = time.perf_counter()
# Create a Pyvista plotting scene
pl = pv.Plotter()

# Add magnet to scene - streamlines units in (m)
magpy.show(magnet, canvas=pl, units_length="m", backend="pyvista")

# Prepare legend parameters
legend_args = {
    "title": "B (mT)",
    "title_font_size": 20,
    "color": "black",
    "position_y": 0.25,
    "vertical": True,
}

# Add streamlines and legend to scene
pl.add_mesh(
    strl.tube(radius=0.0001),
    cmap="bwr",
    scalar_bar_args=legend_args,
)
print(f"Plot generated. Took: {time.perf_counter() - start_time:.4f} seconds")

# Prepare and show scene
pl.camera.position = (0.03, 0.03, 0.03)
pl.show()
'''