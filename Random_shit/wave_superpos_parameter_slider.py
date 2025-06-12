import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

# This doesn't enforce E field to be real.
# It's just a visualization tool from the perspective of tqoqi
# And then only roughly


# 1D grid setup
L = 10
N = 200
x = np.linspace(-L, L, N)

# Two basic modes: right-moving and left-moving
k_vals = [1, -1]


def compute_basis(k):
    return np.exp(1j * k * x)


E_modes = [compute_basis(k) for k in k_vals]


def plot_field(j_coeffs):
    # Get current time from slider
    t = t_var.get()
    # Angular frequencies (omega = |k|)
    omega_vals = [abs(k) for k in k_vals]
    fig.clf()
    axs = fig.subplots(3, 1, sharex=True)
    E_parts = []
    for idx, (jn, En, k, omega) in enumerate(
        zip(j_coeffs, E_modes, k_vals, omega_vals)
    ):
        # Add time dependence: exp(-i omega t)
        E_part = jn * np.exp(-1j * omega * t) * En
        E_parts.append(E_part)
        axs[idx].plot(
            x, E_part.real, linestyle=":", color="tab:blue", label=f"Re[mode {idx+1}]"
        )
        axs[idx].plot(
            x, E_part.imag, linestyle="--", color="tab:red", label=f"Im[mode {idx+1}]"
        )
        axs[idx].set_ylabel(f"Mode {idx+1}")
        axs[idx].grid(True)
        axs[idx].set_xlim(-L, L)
        axs[idx].set_ylim(-3, 3)
    E_total = sum(E_parts)
    axs[2].plot(x, E_total.real, color="blue", linewidth=2, label="Re[E(x)] (total)")
    axs[2].plot(
        x,
        E_total.imag,
        color="red",
        linestyle="--",
        linewidth=2,
        label="Im[E(x)] (total)",
    )
    axs[2].set_ylabel("Total")
    axs[2].set_xlabel("x")
    axs[2].grid(True)
    axs[2].set_xlim(-L, L)
    axs[2].set_ylim(-3, 3)
    fig.suptitle(f"1D Electric Field $E(x, t)$: Modes and Total, t={t:.2f}")
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    canvas.draw()


def update_plot(*args):
    j_coeffs = [
        complex(j1r.get(), j1i.get()),
        complex(j2r.get(), j2i.get()),
    ]
    plot_field(j_coeffs)


def plot_bases():
    """Visualize the real and imaginary parts of the basis functions."""
    fig, ax = plt.subplots(figsize=(7, 4))
    for k, En in zip(k_vals, E_modes):
        ax.plot(x, En.real, label=f"Re[exp({k}ix)]", linestyle="-")
        ax.plot(x, En.imag, label=f"Im[exp({k}ix)]", linestyle="--")
    ax.set_title("Basis Functions: Real and Imaginary Parts")
    ax.set_xlabel("x")
    ax.set_ylabel("Amplitude")
    ax.grid(True)
    ax.set_xlim(-L, L)
    plt.show()


# plot_bases()
# exit()

root = tk.Tk()
root.title("1D Electric Field Interactive")

# Sliders for real and imaginary parts
j1r = tk.DoubleVar(value=2)
j1i = tk.DoubleVar(value=0)
j2r = tk.DoubleVar(value=1)
j2i = tk.DoubleVar(value=0)
t_var = tk.DoubleVar(value=0)  # Time variable

slider_defs = [
    ("j1 real (k=1)", j1r),
    ("j1 imag (k=1)", j1i),
    ("j2 real (k=-1)", j2r),
    ("j2 imag (k=-1)", j2i),
    ("time t", t_var),
]

slider_frame = tk.Frame(root)
slider_frame.pack(side=tk.LEFT, fill=tk.Y)
for i, (label, var) in enumerate(slider_defs):
    tk.Label(slider_frame, text=label).grid(row=i, column=0)
    scale = tk.Scale(
        slider_frame,
        variable=var,
        from_=-10,
        to=10,
        resolution=0.05 if label == "time t" else 0.1,
        orient=tk.HORIZONTAL,
        length=120,
        command=lambda x: update_plot(),
    )
    scale.grid(row=i, column=1)

fig, ax = plt.subplots(figsize=(7, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

update_plot()  # Initial plot

# Explanation:
# The imaginary part Im[E(x)] is affected by the imaginary parts of j1 and j2,
# but only if the basis functions themselves have a nonzero imaginary part at x.
# For exp(ikx), Im[exp(ikx)] = sin(kx).
# If you set j1i or j2i nonzero, you will see Im[E(x)] change.
# However, if both j1i and j2i are zero, Im[E(x)] will be zero.
# Try moving the sliders for "j1 imag (k=1)" or "j2 imag (k=-1)" to see the effect.

# If you set, for example:
#   j1r = 0, j1i = 1, j2r = 0, j2i = 0
# then E(x) = 1j * exp(1j * x) = exp(1j * (x + pi/2)), so Im[E(x)] = cos(x)
# Similarly, other combinations will give different Im[E(x)] profiles.

root.mainloop()
