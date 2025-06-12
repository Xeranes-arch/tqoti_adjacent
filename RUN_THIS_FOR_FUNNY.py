import numpy as np
import plotly.graph_objects as go

# --- Parameters ---
c = 1.0  # wave speed
x_min, x_max = -10, 10
num_x = 200
x = np.linspace(x_min, x_max, num_x)

### CHANGE K VALUES AND THEIR POLARIZATIONS
k_values = [1, 1.3]
A_k = {k: 1.0 for k in k_values}
polarizations = [
    (1.0, 0.0),
    (0.0, 1.0),
]

# Animation time settings
num_frames = 100
# Set duration to one whole cycle of the slowest beat (difference frequency)
if len(k_values) > 1:
    omega1 = c * abs(k_values[0])
    omega2 = c * abs(k_values[1])
    beat_period = 2 * np.pi / abs(omega1 - omega2)
    t_vals = np.linspace(0, beat_period, num_frames)
else:
    t_vals = np.linspace(0, 2 * np.pi, num_frames)

step = 1
x_plot = x[::step]
x0 = x_plot
y0 = np.zeros_like(x0)
z0 = np.zeros_like(x0)
scale = 1.0

# Precompute all frames
frames = []
for t in t_vals:
    # Compute vector components with polarization
    v = np.zeros_like(x_plot)
    w = np.zeros_like(x_plot)
    mode_heads = []
    mode_lines = []
    for idx, k in enumerate(k_values):
        py, pz = polarizations[idx]
        omega = c * abs(k)
        alpha = A_k[k] * np.exp(-1j * omega * t)
        E_mode = (
            alpha * np.exp(1j * k * x_plot) + np.conj(alpha * np.exp(1j * k * x_plot))
        ).real
        v += E_mode * py
        w += E_mode * pz

        # Individual mode contribution at x0[0]
        vi_mode = E_mode[0] * py
        wi_mode = E_mode[0] * pz
        x_head_mode = x0[0]
        y_head_mode = y0[0] + scale * vi_mode
        z_head_mode = z0[0] + scale * wi_mode
        mode_heads.append((x_head_mode, y_head_mode, z_head_mode))
        # Add line for this mode
        mode_lines.append(
            go.Scatter3d(
                x=[x0[0], x_head_mode],
                y=[y0[0], y_head_mode],
                z=[z0[0], z_head_mode],
                mode="lines",
                line=dict(
                    color=["red", "green", "orange", "magenta", "cyan"][idx % 5],
                    width=3,
                ),
                name=f"Mode {idx+1}",
                showlegend=False,
            )
        )

    # Total field at x0[0]
    x_head = x0[0]
    y_head = y0[0] + scale * v[0]
    z_head = z0[0] + scale * w[0]
    # Only show the total field at x0[0]
    line_segments = []
    line_segments.extend(mode_lines)
    line_segments.append(
        go.Scatter3d(
            x=[x0[0], x_head],
            y=[y0[0], y_head],
            z=[z0[0], z_head],
            mode="lines",
            line=dict(color="blue", width=5),
            name="Total field",
            showlegend=False,
        )
    )
    frames.append(go.Frame(data=line_segments, name=f"{t:.2f}"))

# Compute axis ranges to fit all frames
all_y = []
all_z = []
for frame in frames:
    for trace in frame.data:
        if isinstance(trace, go.Scatter3d):
            all_y.extend(trace.y)
            all_z.extend(trace.z)
y_range = [np.min([np.min(y0), np.min(all_y)]), np.max([np.max(y0), np.max(all_y)])]
z_range = [np.min([np.min(z0), np.min(all_z)]), np.max([np.max(z0), np.max(all_z)])]
x_range = [np.min(x0), np.max(x0)]

# Initial frame
init_data = frames[0].data

fig = go.Figure(
    data=init_data,
    frames=frames,
)

fig.update_layout(
    scene=dict(
        xaxis_title="x",
        yaxis_title="Re[E(x,t)]",
        zaxis_title="Field vector",
        xaxis=dict(range=x_range, color="white"),
        yaxis=dict(range=y_range, color="white"),
        zaxis=dict(range=z_range, color="white"),
        bgcolor="rgb(20,20,30)",
    ),
    title="1D Electric Field Vectors (Plotly, lines/arrows, animated)",
    margin=dict(l=0, r=0, b=0, t=40),
    showlegend=False,
    paper_bgcolor="rgb(10,10,15)",
    font=dict(color="white"),
    updatemenus=[
        {
            "type": "buttons",
            "buttons": [
                {
                    "label": "Play",
                    "method": "animate",
                    "args": [
                        None,
                        {
                            "frame": {"duration": 60, "redraw": True},
                            "fromcurrent": True,
                        },
                    ],
                },
                {
                    "label": "Pause",
                    "method": "animate",
                    "args": [
                        [None],
                        {
                            "frame": {"duration": 0, "redraw": False},
                            "mode": "immediate",
                        },
                    ],
                },
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top",
        }
    ],
    sliders=[
        {
            "steps": [
                {
                    "args": [
                        [f"{t:.2f}"],
                        {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"},
                    ],
                    "label": f"{i}",
                    "method": "animate",
                }
                for i, t in enumerate(t_vals)
            ],
            "transition": {"duration": 0},
            "x": 0.1,
            "len": 0.9,
            "currentvalue": {"prefix": "Frame: "},
            "pad": {"b": 10, "t": 60},
        }
    ],
)

fig.show()
fig.write_html("Efield_plot_animated.html")
print(
    "Plot saved as Efield_plot_animated.html. Open this file in your browser to view the animation."
)
