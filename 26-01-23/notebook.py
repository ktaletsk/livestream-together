import marimo

__generated_with = "0.19.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import pandas as pd
    return (pd,)


@app.cell
def _():
    import anywidget
    import traitlets
    return anywidget, traitlets


@app.cell
def _(pd):
    from pathlib import Path
    df = pd.read_csv(
        Path.home() / 'git' / 'tidytuesday' / 'data' / '2025' / '2025-04-01' / 'pokemon_df.csv'
    )
    df
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Looking at the metadata, we have the following columns for our data

    |variable        |class     |description                           |
    |:---------------|:---------|:-------------------------------------|
    |id              |integer   |The unique ID of each Pokemon.|
    |pokemon         |character |The name of each pokemon.|
    |species_id      |integer   |The species ID of each Pokemon.|
    |height          |double    |The height of each pokemon.|
    |weight          |double    |The weight of each pokemon. |
    |base_experience |integer   |The base experience of each Pokemon. |
    |type_1          |character |The primary type. |
    |type_2          |character |The secondary type. |
    |hp              |integer   |The HP (hit points). |
    |attack          |integer   |The attack points. |
    |defense         |integer   |The defense points. |
    |special_attack  |integer   |The special attack points. |
    |special_defense |integer   |The special defense points. |
    |speed           |integer   |The speed. |
    |color_1         |character |The primary color of each pokemon. |
    |color_2         |character |The secondary color of each pokemon. |
    |color_f         |character |The final color of each pokemon. |
    |egg_group_1     |character |The primary egg group. |
    |egg_group_2     |character |The secondary egg group. |
    |url_icon        |character |The URL for the icon of each Pokemon (if available). Note that these are missing the starting "https:". |
    |generation_id   |integer   |The generation ID of each Pokemon. |
    |url_image       |character |The URL for the image of each Pokemon. |
    """)
    return


@app.cell
def _(df):
    df.columns.to_list()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    What actually matters for Pokemon battles? If I had to guess, "height", "weight", "base_experience", "hp", "attack", "defense", "special_attack", "special_defense", "speed"
    """)
    return


@app.cell
def _(anywidget, data, mo, traitlets):
    class CompareWidget(anywidget.AnyWidget):
        _esm = """
        function render({ model, el }) {
          const root = document.createElement("div");
          root.className = "compare-root";

          function optionsHtml(options, selected) {
            return options
              .map(
                (opt) =>
                  `<option value="${opt}" ${
                    opt === selected ? "selected" : ""
                  }>${opt}</option>`
              )
              .join("");
          }

          function card(side, name, data, options) {
            const stats = (data && data.stats) || {};
            const rows = Object.entries(stats)
              .map(([k, v]) => `<tr><td>${k}</td><td>${v}</td></tr>`)
              .join("");
            const image =
              data && typeof data.image === "string" && data.image.length > 0
                ? data.image
                : null;
            const label = name || "Select a Pokemon";
            const imageHtml = image
              ? `<img src="${image}" alt="${label}" />`
              : `<div class="no-image">No image</div>`;
            return `
              <div class="poke-card">
                <select class="poke-select" data-side="${side}">
                  ${optionsHtml(options, name)}
                </select>
                ${imageHtml}
                <div class="poke-name">${label}</div>
                <table class="poke-stats">${rows}</table>
              </div>
            `;
          }

          function renderCards() {
            const options = model.get("options") || [];
            const data = model.get("data") || {};
            const leftName =
              model.get("left_name") || options[0] || "";
            const rightName =
              model.get("right_name") || options[1] || leftName || "";
            root.innerHTML = `
              <div class="compare">
                ${card("left", leftName, data[leftName], options)}
                ${card("right", rightName, data[rightName], options)}
              </div>
            `;
            root.querySelectorAll(".poke-select").forEach((select) => {
              select.addEventListener("change", (event) => {
                const side = event.target.dataset.side;
                const value = event.target.value;
                if (side === "left") {
                  model.set("left_name", value);
                } else {
                  model.set("right_name", value);
                }
                model.save_changes();
              });
            });
          }

          renderCards();
          model.on("change:options", renderCards);
          model.on("change:data", renderCards);
          model.on("change:left_name", renderCards);
          model.on("change:right_name", renderCards);
          el.appendChild(root);
        }
        export default { render };
        """
        _css = """
        .compare-root { pointer-events: auto; }
        .compare { display: flex; gap: 24px; align-items: flex-start; flex-wrap: wrap; }
        .poke-card {
          width: 220px;
          border: 1px solid #e5e7eb;
          border-radius: 12px;
          padding: 12px;
          background: #ffffff;
          color: #111827;
          box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        }
        .poke-select {
          width: 100%;
          margin-bottom: 8px;
          padding: 6px;
          border-radius: 8px;
          border: 1px solid #e5e7eb;
          background: #ffffff;
          color: #111827;
          pointer-events: auto;
          position: relative;
          z-index: 2;
        }
        .poke-card img {
          width: 180px;
          height: 180px;
          object-fit: contain;
          display: block;
          margin: 0 auto 6px auto;
        }
        .no-image {
          width: 180px;
          height: 180px;
          margin: 0 auto 6px auto;
          display: flex;
          align-items: center;
          justify-content: center;
          border: 1px dashed #d1d5db;
          color: #6b7280;
          font-size: 12px;
          background: #f9fafb;
        }
        .poke-name { font-weight: 600; margin: 6px 0 8px 0; text-align: center; }
        .poke-stats { width: 100%; border-collapse: collapse; font-size: 12px; }
        .poke-stats td { padding: 2px 0; }
        .poke-card.empty { color: #6b7280; text-align: center; }
        @media (prefers-color-scheme: dark) {
          .poke-card { background: #111827; color: #f9fafb; border-color: #374151; }
          .poke-select { background: #111827; color: #f9fafb; border-color: #374151; }
          .no-image { border-color: #4b5563; color: #9ca3af; background: #0f172a; }
          .poke-card.empty { color: #9ca3af; }
        }
        """
        options = traitlets.List([]).tag(sync=True)
        left_name = traitlets.Unicode("").tag(sync=True)
        right_name = traitlets.Unicode("").tag(sync=True)
        data = traitlets.Dict({}).tag(sync=True)

    options = sorted(data.keys())
    left_name = options[0] if options else ""
    right_name = options[1] if len(options) > 1 else left_name
    compare = mo.ui.anywidget(
        CompareWidget(
            options=options,
            left_name=left_name,
            right_name=right_name,
            data=data,
        )
    )
    compare
    return


@app.cell
def _(df):
    def fix_url(url):
        if isinstance(url, str) and url.startswith("//"):
            return "https:" + url
        return url

    data = {}
    rows = df.dropna(subset=["pokemon"]).drop_duplicates("pokemon")
    for _, row in rows.iterrows():
        image = fix_url(row["url_image"])
        if not isinstance(image, str) or not image:
            image = None
        data[row["pokemon"]] = {
            "image": image,
            "stats": {
                "hp": int(row["hp"]),
                "attack": int(row["attack"]),
                "defense": int(row["defense"]),
                "speed": int(row["speed"]),
            },
        }
    return (data,)


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
