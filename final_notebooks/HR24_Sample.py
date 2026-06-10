import marimo

__generated_with = "0.23.8"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import pandas as pd
    import colorsys
    import numpy as np
    from wigglystuff import ThreeWidget


    def id_to_colors(ids):
        """
        Map IDs to visually distinct hex colors using:
          - golden-ratio spaced hues
          - alternating saturation/value levels

        Parameters
        ----------
        ids : array-like
            Unique identifiers (ints, strings, etc.)

        Returns
        -------
        dict
            ID -> hex color
        """
        ids = np.asarray(ids)
        n = len(ids)

        # Golden ratio conjugate for good hue spacing
        phi = (np.sqrt(5) - 1) / 2
        hues = (np.arange(n) * phi) % 1

        # Alternate perceptual levels
        saturations = [0.60, 0.75]
        values = [0.80, 0.95]

        colors = {}

        for i, (ID, h) in enumerate(zip(ids, hues)):
            s = saturations[(i // 2) % len(saturations)]
            v = values[i % len(values)]

            r, g, b = colorsys.hsv_to_rgb(h, s, v)

            colors[ID] = "#{:02x}{:02x}{:02x}".format(
                int(r * 255),
                int(g * 255),
                int(b * 255)
            )

        return colors

    return ThreeWidget, id_to_colors, np, pd


@app.cell
def _(pd):
    hmem = pd.read_csv("https://astro.gsu.edu/~sharifi/prospectus/data/hunt_sample.csv")
    return (hmem,)


@app.cell
def _(hmem, id_to_colors, np):
    unique_ids = np.sort(hmem["ID"].unique())
    color_map = id_to_colors(unique_ids)
    return (color_map,)


@app.cell
def _(color_map, hmem):
    points = []

    for _, row in hmem[['x', 'y', 'z', 'ID']].iterrows():
        points.append({
            "x": row["x"],
            "y": row["y"],
            "z": row["z"],
            "color": color_map[row["ID"]],
            "size": 0.5
        })
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
        dark_mode=True
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


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
