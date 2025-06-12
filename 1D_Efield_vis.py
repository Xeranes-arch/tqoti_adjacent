import numpy as np
import plotly.graph_objects as go

# --- Parameters ---
c = 1.0  # wave speed
x_min, x_max = 0, 4 * np.pi
num_x = 1000
x = np.linspace(x_min, x_max, num_x)

### CHANGE K VALUES AND THEIR POLARIZATIONS

k_values = [1]
polarizations = [(1.0, 0.0)]
phase_amps = [1]

###### PRESET LIST #################

# Uhhhh
# k_values = [1, -1, 10]
# polarizations = [(1.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
# phase_amps = [1, 1, np.exp(-1j * np.pi / 2)]

# Circular
# k_values = [1, 1]
# polarizations = [(1.0, 0.0), (0.0, 1.0)]
# phase_amps = [np.exp(-1j * np.pi / 2), 1]

# Standing wave
# k_values = [1, -1]
# polarizations = [(1.0, 0.0), (1.0, 0.0)]
# phase_amps = [1, 1]

###################################################

# Renormalize
norm = 0.618 * np.linalg.norm(phase_amps)
phase_amps = [i / norm for i in phase_amps]


# Phase Amplitudes
A_k = {(k, pol): amp for k, pol, amp in zip(k_values, polarizations, phase_amps)}

# Animation time settings
num_frames = 100
# Set duration to one whole cycle of the slowest beat (difference frequency)
try:

    if len(k_values) > 1:
        omegas = [c * abs(k) for k in k_values]

        # Search smallest difference
        maxm = 1000000
        min_pair = None

        # Check all pairs
        for a in omegas:
            if a < maxm:
                maxm = a
        print(maxm)

        beat_period = 2 * np.pi / maxm
        print(beat_period)
        t_vals = np.linspace(0, beat_period, num_frames)
    else:
        t_vals = np.linspace(0, 2 * np.pi, num_frames)
except:
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
    mode_lines = []
    for idx, (k, pol) in enumerate(zip(k_values, polarizations)):
        py, pz = pol
        omega = c * abs(k)
        alpha = A_k[(k, pol)] * np.exp(-1j * omega * t)
        E_mode = (
            alpha * np.exp(1j * k * x_plot) + np.conj(alpha * np.exp(1j * k * x_plot))
        ).real
        v += E_mode * py
        w += E_mode * pz

        # Draw the field component for this mode at all x (translucent)
        x_heads_mode = x0
        y_heads_mode = y0 + scale * E_mode * py
        z_heads_mode = z0 + scale * E_mode * pz

    x_heads = []
    y_heads = []
    z_heads = []
    line_segments = []
    line_segments.extend(mode_lines)
    for xi, yi, zi, vi, wi in zip(x0, y0, z0, v, w):
        x_head = xi
        y_head = yi + scale * vi
        z_head = zi + scale * wi
        x_heads.append(x_head)
        y_heads.append(y_head)
        z_heads.append(z_head)
        # line_segments.append(
        #     go.Scatter3d(
        #         x=[xi, x_head],
        #         y=[yi, y_head],
        #         z=[zi, z_head],
        #         mode="lines",
        #         line=dict(color="magenta", width=4),
        #         showlegend=False,
        #     )
        # )

    # Add a line connecting all the vector heads (total field)
    line_segments.append(
        go.Scatter3d(
            x=x_heads,
            y=y_heads,
            z=z_heads,
            mode="lines",
            line=dict(color="blue", width=3),
            name="Field tip trace",
            showlegend=False,
        )
    )

    # Add a line segment at x0[0] for each individual mode
    for idx, (k, pol) in enumerate(zip(k_values, polarizations)):
        py, pz = pol
        omega = c * abs(k)
        alpha = A_k[(k, pol)] * np.exp(-1j * omega * t)
        E_mode = (
            alpha * np.exp(1j * k * x0[0]) + np.conj(alpha * np.exp(1j * k * x0[0]))
        ).real
        vi_mode = E_mode * py
        wi_mode = E_mode * pz
        x_head = x0[0]
        y_head = y0[0] + scale * vi_mode
        z_head = z0[0] + scale * wi_mode
        line_segments.append(
            go.Scatter3d(
                x=[x0[0], x_head],
                y=[y0[0], y_head],
                z=[z0[0], z_head],
                mode="lines",
                line=dict(
                    color=["red", "green", "orange", "magenta", "cyan"][idx % 5],
                    width=4,
                ),
                showlegend=False,
            )
        )
    total_line_segments = []
    x_head = x0[0]
    y_head = y0[0] + scale * v[0]
    z_head = z0[0] + scale * w[0]
    total_line_segments.append(
        go.Scatter3d(
            x=[x0[0], x_head],
            y=[y0[0], y_head],
            z=[z0[0], z_head],
            mode="lines",
            line=dict(color="magenta", width=4),
            showlegend=False,
        )
    )
    line_segments.extend(total_line_segments)
    frames.append(go.Frame(data=line_segments, name=f"{t:.2f}"))

x_range = [0, 4 * np.pi]
y_range = [-4, 4]
z_range = [-4, 4]
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
        xaxis=dict(range=x_range, color="white", autorange=False),
        yaxis=dict(range=y_range, color="white", autorange=False),
        zaxis=dict(range=z_range, color="white", autorange=False),
        bgcolor="rgb(20,20,30)",
        aspectmode="cube",  # <-- Add this line to keep aspect ratio fixed
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
