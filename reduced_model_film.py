########################################################################################
# UWS / Film Reduced Model (Tabulated Framework)
#
# Title: Tabulated Reduced-Order Model for UWS Film Decomposition in SCR-Relevant Flows
#
# Manuscript status: Submitted (Chemical Engineering Journal)
#
# Author: Shlomo Hareli
# Karlsruhe Institute of Technology (KIT)
########################################################################################

import numpy as np
import matplotlib.pyplot as plt
import pickle

import all_process_phi as ap  # required dependency (progress-variable utilities)


########################################################################################
# Load precomputed table
########################################################################################
with open("uws_film_table.pkl", "rb") as f:
    TL = pickle.load(f)


########################################################################################
# Parameter grids (fixed model definition)
########################################################################################
Tf_grid = np.array([400.0, 450.0, 500.0, 550.0, 600.0, 650.0])
Tg_grid = np.array([450.0, 500.0, 550.0, 600.0, 650.0, 700.0])
r_grid  = np.array([5.00E-05, 1.00E-04])


########################################################################################
# Trilinear interpolation (DO NOT MODIFY — core model)
########################################################################################
def Trilinear_interpolation(table, Tf_grid, Tg_grid, r_grid, Tf0, Tg0, r0):
    """
    Trilinear interpolation in (Tf, Tg, r) parameter space.

    Returns:
        ndarray: interpolated trajectory [n_state, 24]
    """

    # ---------------- index search ----------------
    iTf1 = np.searchsorted(Tf_grid, Tf0)
    iTf0 = max(iTf1 - 1, 0)
    iTf1 = min(iTf1, len(Tf_grid) - 1)

    iTg1 = np.searchsorted(Tg_grid, Tg0)
    iTg0 = max(iTg1 - 1, 0)
    iTg1 = min(iTg1, len(Tg_grid) - 1)

    iR1 = np.searchsorted(r_grid, r0)
    iR0 = max(iR1 - 1, 0)
    iR1 = min(iR1, len(r_grid) - 1)

    # ---------------- grid values ----------------
    Tf0v, Tf1v = Tf_grid[iTf0], Tf_grid[iTf1]
    Tg0v, Tg1v = Tg_grid[iTg0], Tg_grid[iTg1]
    R0v,  R1v  = r_grid[iR0], r_grid[iR1]

    # ---------------- interpolation weights ----------------
    a = 0.0 if Tf1v == Tf0v else (Tf0 - Tf0v) / (Tf1v - Tf0v)
    b = 0.0 if Tg1v == Tg0v else (Tg0 - Tg0v) / (Tg1v - Tg0v)
    c = 0.0 if R1v  == R0v  else (r0  - R0v)  / (R1v  - R0v)

    # ---------------- corner states ----------------
    Q000 = table[:, :, iTf0, iTg0, iR0]
    Q001 = table[:, :, iTf0, iTg0, iR1]
    Q010 = table[:, :, iTf0, iTg1, iR0]
    Q011 = table[:, :, iTf0, iTg1, iR1]

    Q100 = table[:, :, iTf1, iTg0, iR0]
    Q101 = table[:, :, iTf1, iTg0, iR1]
    Q110 = table[:, :, iTf1, iTg1, iR0]
    Q111 = table[:, :, iTf1, iTg1, iR1]

    # ---------------- trilinear interpolation ----------------
    return (
        (1-a)*(1-b)*(1-c)*Q000 +
        (1-a)*(1-b)*c*Q001 +
        (1-a)*b*(1-c)*Q010 +
        (1-a)*b*c*Q011 +
        a*(1-b)*(1-c)*Q100 +
        a*(1-b)*c*Q101 +
        a*b*(1-c)*Q110 +
        a*b*c*Q111
    )


########################################################################################
# Reduced model solver
########################################################################################
def RED(Tf0, Tg0, r0, nup=10000):
    """
    Solve reduced-order film model.

    Returns:
        red : ndarray shape (nup+1, 24)
    """

    I = Trilinear_interpolation(TL, Tf_grid, Tg_grid, r_grid, Tf0, Tg0, r0)

    red = np.zeros((nup + 1, 24))

    phi = I[-1, 0]
    dt = 300.0 / nup

    for i in range(nup + 1):

        dphi_dt = np.interp(phi, I[:, 0], I[:, 1])

        red[i, 0] = phi
        red[i, -1] = dphi_dt

        # reconstruct all state variables from phi
        for j in range(21):
            red[i, j + 2] = np.interp(phi, I[:, 0], I[:, j + 2])

        phi += dt * dphi_dt

    return red


########################################################################################
# Visualization
########################################################################################
def plot_property(red, p=12):
    """
    Plot selected property vs time.
    """
    plt.figure()
    plt.plot(red[:, 22], red[:, p])
    plt.xlabel("Time [s]")
    plt.ylabel(f"State variable index {p}")
    plt.tight_layout()
    plt.show()


########################################################################################
# Example execution
########################################################################################
if __name__ == "__main__":

    Tf0 = 475
    Tg0 = 675
    r0  = 7.50E-05

    red = RED(Tf0, Tg0, r0, nup=10000)
    plot_property(red, p=12)
