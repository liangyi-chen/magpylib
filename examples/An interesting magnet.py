import magpylib as magpy
import pyvista as pv
import numpy as np
import matplotlib.pyplot as plt
import time
import csv

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

def solenoid_with_simplified_winding(r_in, r_out, L, N, center, current):  #Use the solenoid() function, but reduce number of windings while keep the amp turns to keep field the same
    winding_binning = 4 #bin every 4 turns into one turn
    N = N/winding_binning
    current *= winding_binning
    return solenoid(r_in, r_out, L, N, center, current)

#Center of the magnet in the global coordinate z axis, nominal is -296.1321503e-3 m
mag_center_coordinate = 0

I_M = 21.0 #Main coil current, nominal = 21.0 A
coilM1 = solenoid_with_simplified_winding(0.1397, 0.1431, 0.42, 7559, 0+mag_center_coordinate, I_M)
coilM2 = solenoid_with_simplified_winding(0.1431, 0.1465, 0.0656, 1180.7, 0.1772+mag_center_coordinate, I_M)
coilM3 = solenoid_with_simplified_winding(0.1431, 0.1465, 0.0656, 1180.7, -0.1772+mag_center_coordinate, I_M)

Main = magpy.Collection(coilM1, coilM2, coilM3)
print("Main generated.")

I_A = 0 #Mirror A current, nominal = 38.6 A
coilA1 = solenoid_with_simplified_winding(0.1397, 0.15756, 0.127, 12000, -0.3+mag_center_coordinate, I_A)
coilA2 = solenoid_with_simplified_winding(0.15756, 0.163275, 0.127, 7031.3, -0.3+mag_center_coordinate, I_A)
coilA3 = solenoid_with_simplified_winding(0.1465, 0.15755, 0.0656, 3837.1, -0.1772+mag_center_coordinate, -I_A)
coilA4 = solenoid_with_simplified_winding(0.15755, 0.161043, 0.0656, 2219.5, -0.1772+mag_center_coordinate, -I_A)
coilA5 = solenoid_with_simplified_winding(0.1431, 0.143525, 0.078, 175.5, 0.08+mag_center_coordinate, -I_A)
coilA6 = solenoid_with_simplified_winding(0.1431, 0.143525, 0.006, 13.5, 0.2+mag_center_coordinate, -I_A)
coilA7 = solenoid_with_simplified_winding(0.1633, 0.163725, 0.038, 85.5, 0.3+mag_center_coordinate, -I_A)

MirrorA = magpy.Collection(coilA1, coilA2, coilA3, coilA4, coilA5, coilA6, coilA7)
print("Mirror A generated.")

I_B = 0 #Mirror A current, nominal = 30.6 A
coilB1 = solenoid_with_simplified_winding(0.1397, 0.15756, 0.127, 12000, 0.3+mag_center_coordinate, I_B)
coilB2 = solenoid_with_simplified_winding(0.15756, 0.163275, 0.127, 7031.3, 0.3+mag_center_coordinate, I_B)
coilB3 = solenoid_with_simplified_winding(0.1465, 0.15755, 0.0656, 3837.1, 0.1772+mag_center_coordinate, -I_B)
coilB4 = solenoid_with_simplified_winding(0.15755, 0.161043, 0.0656, 2219.5, 0.1772+mag_center_coordinate, -I_B)
coilB5 = solenoid_with_simplified_winding(0.1431, 0.143525, 0.078, 175.5, -0.08+mag_center_coordinate, -I_B)
coilB6 = solenoid_with_simplified_winding(0.1431, 0.143525, 0.006, 13.5, -0.2+mag_center_coordinate, -I_B)
coilB7 = solenoid_with_simplified_winding(0.1633, 0.163725, 0.038, 85.5, -0.3+mag_center_coordinate, -I_B)

MirrorB = magpy.Collection(coilB1, coilB2, coilB3, coilB4, coilB5, coilB6, coilB7)
print("Mirror B generated.")

magnet = magpy.Collection(Main, MirrorA, MirrorB)

print(f"Magnets created. Took: {time.perf_counter() - start_time:.4f} seconds")

'''
#Quick plot check for Bz field
observers = np.linspace((0, 0, -0.9), (0, 0, 0.3), 121)
B = magpy.getB(magnet, observers)
#print(B)

Bz_with_z = np.column_stack((observers[:,2], B[:,2]))
#print(Bz_with_z)

#plot Bz against z
plt.plot(Bz_with_z[:,0], Bz_with_z[:,1]*10000)
plt.xlabel("z (m)")
plt.ylabel(r"$B_z$ (G)")
plt.show()
'''
'''
#Quick plot of 2D field map in a XY plane
x = np.linspace(-100e-3, 100e-3, 21)
y = np.linspace(-100e-3, 100e-3, 21)
z = np.linspace(10e-3, 10e-3, 1)

# all grid points as an (N, 3) array
X, Y, Z = np.meshgrid(x, y, z, indexing="ij")
observers = np.stack((X.ravel(), Y.ravel(), Z.ravel()), axis=1)

B = magpy.getB(magnet, observers)
plt.quiver(X, Y, B[:,0], B[:,1], color='g')
plt.grid()
plt.show()
'''
'''
#Quick plot of 3D field map
x = np.linspace(-100e-3, 100e-3, 11)
y = np.linspace(-100e-3, 100e-3, 11)
z = np.linspace(-10e-3, 500e-3, 5)

# all grid points as an (N, 3) array
X, Y, Z = np.meshgrid(x, y, z, indexing="ij")
observers = np.stack((X.ravel(), Y.ravel(), Z.ravel()), axis=1)

B = magpy.getB(magnet, observers)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.quiver(X.ravel(), Y.ravel(), Z.ravel(), B[:,0], B[:,1], B[:,2], color=['blue', 'red'], arrow_length_ratio=0.1)
# Set grid limits
ax.set_xlim([-3, 5])
ax.set_ylim([-3, 5])
ax.set_zlim([-3, 5])

# Add labels
ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')
ax.set_zlabel('Z Axis')

plt.show()
'''

#Field data output
'''Saved for full profile
x = np.linspace(-0.1, 0.1, 201)
y = np.linspace(-0.1, 0.1, 201)
z = np.linspace(-0.01, 0.5, 511)
'''
x = np.linspace(0, 1, 201)
y = np.linspace(0, 0, 1)
z = np.linspace(0, 0, 1)

# all grid points as an (N, 3) array
X, Y, Z = np.meshgrid(x, y, z, indexing="ij")
observers = np.stack((X.ravel(), Y.ravel(), Z.ravel()), axis=1)

BLOCK = 1000
fmt = ["%.3f"] * 3 + ["%.8e"] * 3

with open("data.dat", "w", encoding="utf-8") as file:
    for i in range(0, len(observers), BLOCK):
        obs = observers[i:i+BLOCK]
        B = magpy.getB(magnet, obs)
        np.savetxt(file, np.hstack((obs, B)), delimiter="\t", fmt=fmt)

