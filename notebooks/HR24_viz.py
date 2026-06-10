import marimo

__generated_with = "0.23.2"
app = marimo.App(width="medium")


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
    import astropy.units as u
    from astropy.coordinates import SkyCoord, Galactic
    import matplotlib.pyplot as plt

    def get_color(s):
        h_bytes = hashlib.md5(s.encode("utf-8")).digest()
        h_int = int.from_bytes(h_bytes[:8], "big")

        h = (h_int % 360) / 360.0  # clean mapping to [0,1)

        r, g, b = colorsys.hsv_to_rgb(h, 0.65, 0.85)

        return "#{:02x}{:02x}{:02x}".format(
            int(r * 255), int(g * 255), int(b * 255)
        )

    def xyz(ra, dec, parallax):
        """
            Converts ICRS ra (deg), dec (deg), parallax (mas) to heliocentric
            Cartesian XYZ (pc)

        Returns:
            numpy.ndarray : (n x 3) XYZ array
        """
        coords = SkyCoord(
            ra=ra * u.deg,
            dec=dec * u.deg,
            distance=1000 / parallax * u.pc,
            frame="icrs",
        ).transform_to(Galactic())

        return coords.cartesian.xyz.to(u.pc).value.T



    return ThreeWidget, get_color, mo, pd, xyz


@app.cell
def _():
    hclu_path = '/Volumes/travelpassport/litclusterdatabases/HR24/HR24_clusters.csv'
    clu_param_path = '/Users/sharifi/Documents/prospectus_demos/data/clu_params.csv'
    hmem_path = '/Volumes/travelpassport/litclusterdatabases/HR24/HR24_members.h5'
    return clu_param_path, hclu_path, hmem_path


@app.cell
def _(clu_param_path, hclu_path, hmem_path, pd):
    hclu = pd.read_csv(hclu_path)
    clu_param = pd.read_csv(clu_param_path)
    hmem = pd.read_hdf(hmem_path)
    hclu = hclu.loc[hclu.dist50 < 500]
    hmem = hmem.loc[hmem.Name.isin(hclu.Name)]
    hmem = hmem.loc[hmem.Plx > 0]

    # hmem = hmem.loc[hmem.Name.isin(clu_param.name)]
    return (hmem,)


@app.cell
def _(hmem, xyz):
    hmem[['x', 'y', 'z']] = xyz(hmem.RA_ICRS.values, hmem.DE_ICRS.values, hmem.Plx.values)
    return


@app.cell
def _(get_color, hmem):
    points = []

    for i, (x, y, z, name) in hmem[['x', 'y', 'z', 'Name']].iterrows():

        points.append(
            {
                "x":x,
                "y":y,
                "z":z,
                "color":get_color(name),
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


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
