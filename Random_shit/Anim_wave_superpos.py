import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

### This is not how moving left works...
# Makes an animation for two waves overlapping with imaginary part.

# 1D grid setup
L = 10
N = 200
x = np.linspace(-L, L, N)

# Two basic modes: right-moving and left-moving
k_vals = [1, -1]


def compute_basis(k, x0=0):
    return np.exp(1j * k * (x - x0))


# E_modes and j_coeffs can be changed freely, the rest adapts automatically
E_modes = [
    compute_basis(k_vals[0]),  # right-moving, centered
    compute_basis(k_vals[1]),  # left-moving, centered
    # compute_basis(k_vals[0], x0=5),  # right-moving, offset to the right (x0=5)
]

# Only set coefficients for the independent modes (e.g., right-moving)
j1 = 2 + 1j
# j3 = 1 + 0j

# Apply reality constraint: for each +k mode, set the -k mode coefficient as its conjugate
j2 = np.conj(j1)
j_coeffs = [j1, j2]  # If you add more pairs, follow this pattern

# Animation parameters
t_min, t_max = 0, 10
frames = 100
t_vals = np.linspace(t_min, t_max, frames)
# Automatically determine omega for each mode
omega_vals = []
for mode, j in zip(E_modes, j_coeffs):
    # Try to infer k from the mode by comparing to exp(ikx) at x=0 and x=1
    # This works for modes of the form exp(i*k*(x-x0))
    phase0 = np.angle(mode[0])
    phase1 = np.angle(mode[1])
    dk = x[1] - x[0]
    k_est = (phase1 - phase0) / dk
    omega_vals.append(abs(k_est))

fig, axs = plt.subplots(3, 1, figsize=(8, 8), sharex=True)


def compute_E_parts(t):
    E_parts = []
    for jn, En, omega in zip(j_coeffs, E_modes, omega_vals):
        E_parts.append(jn * np.exp(-1j * omega * t) * En)
    return E_parts


def animate(i):
    t = t_vals[i]
    for ax in axs:
        ax.clear()
    E_parts = compute_E_parts(t)
    # Plot all right-moving modes (assume all with k>0 or as desired)
    axs[0].set_ylabel("Right-moving")
    axs[1].set_ylabel("Left-moving")
    axs[2].set_ylabel("Total")
    axs[2].set_xlabel("x")
    axs[0].set_xlim(-L, L)
    axs[1].set_xlim(-L, L)
    axs[2].set_xlim(-L, L)
    axs[0].set_ylim(-3, 3)
    axs[1].set_ylim(-3, 3)
    axs[2].set_ylim(-3, 3)
    axs[0].grid(True)
    axs[1].grid(True)
    axs[2].grid(True)
    # Assign modes to subplots based on index (customize as needed)
    if len(E_parts) == 2:
        # Two modes: right and left
        axs[0].plot(
            x, E_parts[0].real, ":", color="tab:blue", label="Re[mode 1]", alpha=0.7
        )
        axs[0].plot(
            x, E_parts[0].imag, "--", color="tab:red", label="Im[mode 1]", alpha=0.7
        )
        axs[1].plot(
            x, E_parts[1].real, ":", color="tab:blue", label="Re[mode 2]", alpha=0.7
        )
        axs[1].plot(
            x, E_parts[1].imag, "--", color="tab:red", label="Im[mode 2]", alpha=0.7
        )
    elif len(E_parts) == 3:
        # First and third are right-moving, second is left-moving
        axs[0].plot(
            x, E_parts[0].real, ":", color="tab:blue", label="Re[mode 1]", alpha=0.7
        )
        axs[0].plot(
            x, E_parts[0].imag, "--", color="tab:red", label="Im[mode 1]", alpha=0.7
        )
        axs[0].plot(
            x,
            E_parts[2].real,
            ":",
            color="tab:green",
            label="Re[mode 3] (offset)",
            alpha=0.7,
        )
        axs[0].plot(
            x,
            E_parts[2].imag,
            "--",
            color="tab:orange",
            label="Im[mode 3] (offset)",
            alpha=0.7,
        )
        axs[1].plot(
            x, E_parts[1].real, ":", color="tab:blue", label="Re[mode 2]", alpha=0.7
        )
        axs[1].plot(
            x, E_parts[1].imag, "--", color="tab:red", label="Im[mode 2]", alpha=0.7
        )
    else:
        # Generic: plot all modes in axs[0], leave axs[1] empty
        for idx, E_part in enumerate(E_parts):
            axs[0].plot(x, E_part.real, ":", label=f"Re[mode {idx+1}]", alpha=0.7)
            axs[0].plot(x, E_part.imag, "--", label=f"Im[mode {idx+1}]", alpha=0.7)
    # Total
    E_total = np.sum(E_parts, axis=0)
    axs[2].plot(x, E_total.real, color="blue", linewidth=2, label="Re[E(x)] (total)")
    axs[2].plot(
        x,
        E_total.imag,
        color="red",
        linestyle="--",
        linewidth=2,
        label="Im[E(x)] (total)",
    )
    fig.suptitle(f"1D Electric Field $E(x, t)$: Modes and Total, t={t:.2f}")
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    return axs


ani = FuncAnimation(fig, animate, frames=frames, blit=False, interval=30)

writer = FFMpegWriter(fps=30, bitrate=1800)
ani.save("1Dwaves_animation.mp4", writer=writer)
