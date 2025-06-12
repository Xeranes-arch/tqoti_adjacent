import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

# 2D electric field with four orientations.
# I don't know either if it makes any sense. It's AI slop.


# Grid setup
L = 10
N = 50
x = np.linspace(-L, L, N)
y = np.linspace(-L, L, N)
X, Y = np.meshgrid(x, y)

# Define wavevectors and polarizations for basis modes
k_vals = [
    (1, 0),
    (0, 1),
    (1, 1),
    (-1, 1),
    (2, 0),
]
polarizations = [
    np.array([0, 1]),
    np.array([1, 0]),
    np.array([1, -1]),
    np.array([1, 1]),
]
polarizations = [p / np.linalg.norm(p) for p in polarizations]


def compute_basis(kx, ky, pol):
    kdotr = kx * X + ky * Y
    phase = np.exp(1j * kdotr)
    Ex = pol[0] * phase
    Ey = pol[1] * phase
    return Ex, Ey


E_modes = [compute_basis(kx, ky, pol) for (kx, ky), pol in zip(k_vals, polarizations)]


def plot_field(j_coeffs):
    Ex_total = np.zeros_like(X, dtype=np.complex128)
    Ey_total = np.zeros_like(Y, dtype=np.complex128)
    for jn, (Ex, Ey) in zip(j_coeffs, E_modes):
        Ex_total += jn * Ex
        Ey_total += jn * Ey
    ax.clear()
    ax.quiver(X, Y, Ex_total.real, Ey_total.real, scale=50, color="red")
    ax.set_title("Electric Field $\\mathbf{E}(\\mathbf{r}, t)$")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.axis("equal")
    ax.grid(True)
    canvas.draw()


def update_plot(*args):
    j_coeffs = [
        complex(j1r.get(), j1i.get()),
        complex(j2r.get(), j2i.get()),
        complex(j3r.get(), j3i.get()),
        complex(j4r.get(), j4i.get()),
    ]
    plot_field(j_coeffs)


root = tk.Tk()
root.title("2D Electric Field Interactive")

# Sliders for real and imaginary parts
j1r = tk.DoubleVar(value=1)
j1i = tk.DoubleVar(value=0)
j2r = tk.DoubleVar(value=0)
j2i = tk.DoubleVar(value=0)
j3r = tk.DoubleVar(value=0)
j3i = tk.DoubleVar(value=0)
j4r = tk.DoubleVar(value=0)
j4i = tk.DoubleVar(value=0)

slider_defs = [
    ("j1 real", j1r),
    ("j1 imag", j1i),
    ("j2 real", j2r),
    ("j2 imag", j2i),
    ("j3 real", j3r),
    ("j3 imag", j3i),
    ("j4 real", j4r),
    ("j4 imag", j4i),
]

slider_frame = tk.Frame(root)
slider_frame.pack(side=tk.LEFT, fill=tk.Y)
for i, (label, var) in enumerate(slider_defs):
    tk.Label(slider_frame, text=label).grid(row=i, column=0)
    scale = tk.Scale(
        slider_frame,
        variable=var,
        from_=-2,
        to=2,
        resolution=0.1,
        orient=tk.HORIZONTAL,
        length=120,
        command=lambda x: update_plot(),
    )
    scale.grid(row=i, column=1)

fig, ax = plt.subplots(figsize=(6, 6))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

update_plot()  # Initial plot

root.mainloop()
