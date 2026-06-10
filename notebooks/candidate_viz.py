import marimo

__generated_with = "0.23.2"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import pandas as pd
    import random
    from pathlib import Path
    from wigglystuff import ThreeWidget
    import colorsys
    import hashlib

    def get_color(s):
        h_bytes = hashlib.md5(s.encode("utf-8")).digest()
        h_int = int.from_bytes(h_bytes[:8], "big")

        h = (h_int % 360) / 360.0  # clean mapping to [0,1)

        r, g, b = colorsys.hsv_to_rgb(h, 0.65, 0.85)

        return "#{:02x}{:02x}{:02x}".format(
            int(r * 255), int(g * 255), int(b * 255)
        )



    return ThreeWidget, get_color, mo, pd


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Distribution of Candidates
    """)
    return


@app.cell
def _(pd):
    cand_path = '/Volumes/travelpassport/tables/candidates_ThreeWidget.csv'

    cand = pd.read_csv(cand_path)
    return (cand,)


@app.cell
def _(cand):
    cand
    return


@app.cell
def _(cand, get_color):
    points = []

    for i, (x, y, z, sphere_name) in cand[['X', 'Y', 'Z', 'sphere_name']].iterrows():

        points.append(
            {
                "x":x,
                "y":y,
                "z":z,
                "color":get_color(sphere_name),
                "size": .5
            }
        )
    return (points,)


@app.cell
def _(ThreeWidget, mo, points):
    three = ThreeWidget(
        data=points,
        width=800,
        height=600,
        show_grid=True,
        show_axes=True,
        axis_labels=["X (pc)", "Y (pc)", "Z (pc)"],
        dark_mode=False
      )
    widget = mo.ui.anywidget(three)
    return (widget,)


@app.cell
def _(mo, widget):
    mo.hstack([widget], justify='center')
    return


@app.cell
def _(widget):
    widget.start_rotate(speed=3)
    return


if __name__ == "__main__":
    app.run()
