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

I_M = 18.557 #Main coil current
coilM1 = solenoid(0.1397, 0.1431, 0.42, 7559, 0, I_M)
coilM2 = solenoid(0.1431, 0.1465, 0.0656, 1180.7, 0.1772, I_M)
coilM3 = solenoid(0.1431, 0.1465, 0.0656, 1180.7, -0.1772, I_M)

Main = magpy.Collection(coilM1, coilM2, coilM3)
print("Main generated.")

I_A = 32.010 #Mirror A current
coilA1 = solenoid(0.1397, 0.15756, 0.127, 12000, 0.3, I_A)
coilA2 = solenoid(0.15756, 0.163275, 0.127, 7031.3, 0.3, I_A)
coilA3 = solenoid(0.1465, 0.15755, 0.0656, 3837.1, 0.1772, -I_A)
coilA4 = solenoid(0.15755, 0.161043, 0.0656, 2219.5, 0.1772, -I_A)
coilA5 = solenoid(0.1431, 0.143525, 0.078, 175.5, -0.08, -I_A)
coilA6 = solenoid(0.1431, 0.143525, 0.006, 13.5, -0.2, -I_A)
coilA7 = solenoid(0.1633, 0.163725, 0.038, 85.5, -0.3, -I_A)

MirrorA = magpy.Collection(coilA1, coilA2, coilA3, coilA4, coilA5, coilA6, coilA7)
print("Mirror A generated.")

I_B = 27.210 #Mirror A current
coilB1 = solenoid(0.1397, 0.15756, 0.127, 12000, -0.3, I_B)
coilB2 = solenoid(0.15756, 0.163275, 0.127, 7031.3, -0.3, I_B)
coilB3 = solenoid(0.1465, 0.15755, 0.0656, 3837.1, -0.1772, -I_B)
coilB4 = solenoid(0.15755, 0.161043, 0.0656, 2219.5, -0.1772, -I_B)
coilB5 = solenoid(0.1431, 0.143525, 0.078, 175.5, 0.08, -I_B)
coilB6 = solenoid(0.1431, 0.143525, 0.006, 13.5, 0.2, -I_B)
coilB7 = solenoid(0.1633, 0.163725, 0.038, 85.5, 0.3, -I_B)

MirrorB = magpy.Collection(coilB1, coilB2, coilB3, coilB4, coilB5, coilB6, coilB7)
print("Mirror B generated.")

magnet = magpy.Collection(Main, MirrorA, MirrorB)

print(f"Magnets created. Took: {time.perf_counter() - start_time:.4f} seconds")

sensor_position = np.linspace((0, 0, -0.4), (0, 0, 0.4), 81)
sens = magpy.Sensor(position = sensor_position)
B = magpy.getB(magnet, sens)
#print(B)

Bz_with_z = np.column_stack((sensor_position[:,2], B[:,2]))
#print(Bz_with_z)

#plot Bz against z
plt.plot(Bz_with_z[:,0], Bz_with_z[:,1]*10000)
plt.xlabel("z (m)")
plt.ylabel(r"$B_z$ (G)")
plt.show()