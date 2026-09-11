import magpylib as magpy
import pyvista as pv
import numpy as np
import time

def solenoid_polyline_vertices(r, L, N, P, right_handed=True):   
    # r: radius, L: length, N: num of turns, P: points per turn
    total_points = int(N * P)
    theta = np.linspace(0, 2 * np.pi * N, total_points)
    
    x = r * np.cos(theta)
    
    # Flip the sign of Y depending on the desired chirality
    if right_handed:
        y = r * np.sin(theta)
    else:
        y = -r * np.sin(theta)
        
    # Centered on z=0 plane
    z = np.linspace(-L / 2, L / 2, total_points)
    
    vertices = list(zip(x, y, z))
    return vertices

start_time = time.perf_counter()

#Creat coil vertices from function
coil1_vertices = solenoid_polyline_vertices(0.01, 0.01, 30, 10, True)
coil2_vertices = solenoid_polyline_vertices(0.01, 0.01, 30, 10, False)

coil1 = magpy.current.Polyline(
    vertices = coil1_vertices,
    position = (0, 0, 0.1),
    current = 10,
    )
    
coil2 = magpy.current.Polyline(
    vertices = coil2_vertices,
    position = (0, 0, -0.05),
    current = 10,
    )

print(f"Magnets created. Took: {time.perf_counter() - start_time:.4f} seconds")

start_time = time.perf_counter()
# Create a 3D grid with Pyvista
grid = pv.ImageData(
    dimensions=(41, 41, 41),
    spacing=(0.001, 0.001, 0.001),
    origin=(-0.02, -0.02, -0.02),
)
print(f"Grid created. Took: {time.perf_counter() - start_time:.4f} seconds")

start_time = time.perf_counter()
# Compute B-field and add as data to grid
grid["B"] = (coil1.getB(grid.points)+coil2.getB(grid.points)) * 1000  # T -> mT
print(f"B field computed. Took: {time.perf_counter() - start_time:.4f} seconds")

start_time = time.perf_counter()
# Compute the field lines
seed = pv.Disc(inner=0.001, outer=0.003, r_res=1, c_res=9)
strl = grid.streamlines_from_source(
    seed,
    vectors="B",
    max_step_length=2,
    max_length=.02,
    integration_direction="both",
)
print(f"Field lines computed. Took: {time.perf_counter() - start_time:.4f} seconds")

start_time = time.perf_counter()
# Create a Pyvista plotting scene
pl = pv.Plotter()

# Add magnet to scene - streamlines units in (m)
magpy.show(coil1, coil2, canvas=pl, units_length="m", backend="pyvista")

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
