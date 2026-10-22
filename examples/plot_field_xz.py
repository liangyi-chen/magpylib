"""
Plot the magnetic field in the XZ plane.

Data file columns: x, y, z, Bx, By, Bz   (units: m, T)

The data in this file lies on a single y = const plane (an XZ slice), on a
regular 41 x 31 grid (x: -1.0 to 1.0 m, z: 0.0 to 1.5 m).

Produces:
  - A filled color map of |B| = sqrt(Bx^2 + By^2 + Bz^2)
  - Field-line direction shown as arrows (quiver) using the in-plane
    components (Bx, Bz), colored/scaled to show direction of the field
    lines in the XZ plane.

Usage:
    python plot_field_xz.py <datafile> [output.png]
"""

import sys
import numpy as np
import matplotlib.pyplot as plt


def load_data(path):
    data = np.loadtxt(path)
    x, y, z, bx, by, bz = data.T
    return x, y, z, bx, by, bz


def main():
    infile = sys.argv[1] if len(sys.argv) > 1 else \
        "Source_magnet_downstream_field_for_turbo_36cmheight.dat"
    outfile = sys.argv[2] if len(sys.argv) > 2 else "field_xz_plot.png"

    x, y, z, bx, by, bz = load_data(infile)

    y_val = np.unique(y)
    if y_val.size != 1:
        print(f"Warning: data spans {y_val.size} distinct y values "
              f"({y_val.min()}..{y_val.max()}); using all points as an "
              f"unstructured XZ slice.")
    else:
        print(f"Data is a single XZ plane at y = {y_val[0]} m")

    # Unique, sorted axis values -> regular grid
    xu = np.unique(x)
    zu = np.unique(z)
    nx, nz = xu.size, zu.size

    # Map each point to grid indices (robust to any row ordering)
    xi = np.searchsorted(xu, x)
    zi = np.searchsorted(zu, z)

    BX = np.full((nz, nx), np.nan)
    BZ = np.full((nz, nx), np.nan)
    BMAG = np.full((nz, nx), np.nan)

    b_total = np.sqrt(bx**2 + by**2 + bz**2)

    BX[zi, xi] = bx
    BZ[zi, xi] = bz
    BMAG[zi, xi] = b_total

    X, Z = np.meshgrid(xu, zu)

    fig, ax = plt.subplots(figsize=(9, 7))

    # --- Color map of |B| ---
    pcm = ax.pcolormesh(X, Z, BMAG*10000, shading="auto", cmap="plasma")
    cbar = fig.colorbar(pcm, ax=ax, pad=0.02)
    cbar.set_label("|B| (G)")

    # --- Field line direction arrows (quiver), subsampled for clarity ---
    skip = 4  # plot every 2nd grid point in each direction
    Xs = X[::skip, ::skip]
    Zs = Z[::skip, ::skip]
    BXs = BX[::skip, ::skip]
    BZs = BZ[::skip, ::skip]
    '''
    # Normalize arrow direction (so arrow length shows direction only,
    # not magnitude, which is already shown by the color map)
    mag_inplane = np.sqrt(BXs**2 + BZs**2)
    mag_inplane[mag_inplane == 0] = np.nan
    U = BXs / mag_inplane
    V = BZs / mag_inplane
    '''
    #No normalizaion
    U = BXs
    V = BZs
    ax.quiver(Xs, Zs, U, V, color="white", 
              scale=20, 
              width=0.003,
              pivot="mid", alpha=0.9)

    ax.set_xlabel("x (m)")
    ax.set_ylabel("z (m)")
    y0 = y_val[0] if y_val.size == 1 else np.mean(y)
    ax.set_title(f"Magnetic field magnitude and direction in XZ plane\n"
                 f"(y = {y0:.3f} m)")
    ax.set_aspect("equal")

    fig.tight_layout()
    fig.savefig(outfile, dpi=200)
    print(f"Saved plot to {outfile}")


if __name__ == "__main__":
    main()
