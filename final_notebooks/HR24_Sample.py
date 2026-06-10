import marimo

__generated_with = "0.23.8"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return


@app.cell
def _():
    import pandas as pd

    return (pd,)


@app.cell
def _(pd):
    df = pd.read_csv("https://astro.gsu.edu/~sharifi/prospectus/data/hunt_sample.csv")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
