import marimo

__generated_with = "0.23.2"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import pandas as pd
    import random
    from pathlib import Path
    from wigglystuff import ThreeWidget
    import colorsys

    def distinct_color(i):
        # golden ratio conjugate ensures good spacing
        phi = 0.618033988749895

        h = (i * phi) % 1.0   # evenly spread hue
        s = 0.65              # fixed saturation
        v = 0.85              # fixed brightness

        r, g, b = colorsys.hsv_to_rgb(h, s, v)

        # convert [0,1] → [0,255]
        r = int(r * 255)
        g = int(g * 255)
        b = int(b * 255)

        return f"#{r:02x}{g:02x}{b:02x}"


    BASE_DIR = Path(__file__).resolve().parent

    DATA_PATH = BASE_DIR.parent / "data"
    return DATA_PATH, ThreeWidget, distinct_color, mo, np, pd, random


@app.cell
def _(mo):
    mo.md(r"""
    ## Distribution of Spheres
    This shows the spherical volumes of radius 180 pc around each of the 288 open clusters and moving groups in the Solar Neighborhood we are surveying for spatially extended populations of escaping low-mass stars.
    """)
    return


@app.cell
def _(np):
    def points_on_sphere(N, r=1.0, center=(0, 0, 0)):
        """
        Generate N points uniformly distributed on the surface of a sphere.
        """
        cx, cy, cz = center

        # Draw random 3D vectors from a normal distribution
        vec = np.random.normal(size=(N, 3))

        # Normalize each vector to lie on the unit sphere
        vec /= np.linalg.norm(vec, axis=1)[:, None]

        # Scale by radius and shift to center
        vec = r * vec + np.array([cx, cy, cz])

        return vec

    return (points_on_sphere,)


@app.cell
def _(DATA_PATH, pd):
    hclu = pd.read_csv(DATA_PATH / "clu_params.csv")
    return (hclu,)


@app.cell
def _(distinct_color, hclu, points_on_sphere, random):
    random.seed(42)
    points = []

    for i, (x_clu, y_clu, z_clu) in hclu[['x', 'y', 'z']].iterrows():

        xyz = points_on_sphere(5000, r=180, center=(x_clu, y_clu, z_clu))
        color_val = distinct_color(i)

        for point in xyz:

            points.append(
                {
                    "x":point[0],
                    "y":point[1],
                    "z":point[2],
                    "color":color_val,
                    "size": 10
                }
            )
    return (points,)


@app.cell
def _(ThreeWidget, mo, points):
    three = ThreeWidget(
        data=points,
        width=1000,
        height=600,
        show_grid=True,
        show_axes=True,
        axis_labels=["X (pc)", "Y (pc)", "Z (pc)"]
      )
    widget = mo.ui.anywidget(three)
    return (widget,)


@app.cell
def _(mo, widget):
    mo.hstack([widget], justify='center')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Tip 💡: You can rotate and zoom in on the figure
    """)
    return


@app.cell
def _(widget):
    widget.start_rotate(speed=5)
    return


if __name__ == "__main__":
    app.run()
