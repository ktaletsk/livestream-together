import marimo

__generated_with = "0.20.2"
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
    df = pd.read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/refs/heads/main/data/2025/2025-04-01/pokemon_df.csv")
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


@app.cell(hide_code=True)
def _(anywidget, data, mo, traitlets):
    class BattleWidget(anywidget.AnyWidget):
        _esm = """
        function render({ model, el }) {
          const root = document.createElement("div");
          root.className = "compare-root";
          let animInterval = null;

          function optionsHtml(options, selected) {
            return options
              .map(
                (opt) =>
                  `<option value="${opt}" ${opt === selected ? "selected" : ""}>${opt}</option>`
              )
              .join("");
          }

          function hpColor(pct) {
            if (pct > 50) return "#22c55e";
            if (pct > 20) return "#eab308";
            return "#ef4444";
          }

          function card(side, name, pData, options, hpPct) {
            const stats = (pData && pData.stats) || {};
            const displayStats = ["hp","attack","defense","special_attack","special_defense","speed"];
            const rows = displayStats
              .filter((k) => stats[k] !== undefined)
              .map((k) => {
                const label = k.replace(/_/g, " ");
                return `<tr><td>${label}</td><td>${stats[k]}</td></tr>`;
              })
              .join("");
            const image =
              pData && typeof pData.image === "string" && pData.image.length > 0
                ? pData.image
                : null;
            const label = name || "Select a Pokemon";
            const imageHtml = image
              ? `<img src="${image}" alt="${label}" />`
              : `<div class="no-image">No image</div>`;
            const hp = stats.hp || 0;
            const hpVal = Math.round(hp * hpPct / 100);
            return `
              <div class="poke-card">
                <select class="poke-select" data-side="${side}">
                  ${optionsHtml(options, name)}
                </select>
                ${imageHtml}
                <div class="poke-name">${label}</div>
                <div class="hp-bar-container">
                  <div class="hp-bar" data-side="${side}" style="width:${hpPct}%;background:${hpColor(hpPct)}"></div>
                </div>
                <div class="hp-text" data-side="${side}">HP: ${hpVal} / ${hp}</div>
                <table class="poke-stats">${rows}</table>
              </div>
            `;
          }

          function renderCards() {
            if (animInterval) { clearInterval(animInterval); animInterval = null; }
            const options = model.get("options") || [];
            const data = model.get("data") || {};
            const leftName = model.get("left_name") || options[0] || "";
            const rightName = model.get("right_name") || options[1] || leftName || "";
            root.innerHTML = `
              <div class="compare">
                ${card("left", leftName, data[leftName], options, 100)}
                <div class="battle-center">
                  <button class="fight-btn">Fight!</button>
                </div>
                ${card("right", rightName, data[rightName], options, 100)}
              </div>
              <div class="battle-log" id="battle-log"></div>
              <div class="winner-banner" id="winner-banner" style="display:none"></div>
            `;

            root.querySelectorAll(".poke-select").forEach((select) => {
              select.addEventListener("change", (event) => {
                const side = event.target.dataset.side;
                const value = event.target.value;
                if (side === "left") { model.set("left_name", value); }
                else { model.set("right_name", value); }
                model.save_changes();
              });
            });

            const fightBtn = root.querySelector(".fight-btn");
            if (fightBtn) {
              fightBtn.addEventListener("click", () => startBattle());
            }
          }

          function startBattle() {
            const log = model.get("battle_log") || [];
            if (!log.length) return;
            const data = model.get("data") || {};
            const leftName = model.get("left_name");
            const rightName = model.get("right_name");
            const leftData = data[leftName] || {};
            const rightData = data[rightName] || {};
            const maxHpA = (leftData.stats || {}).hp || 1;
            const maxHpB = (rightData.stats || {}).hp || 1;

            const fightBtn = root.querySelector(".fight-btn");
            if (fightBtn) { fightBtn.disabled = true; fightBtn.textContent = "Fighting..."; }
            const logEl = root.querySelector("#battle-log");
            const bannerEl = root.querySelector("#winner-banner");
            if (logEl) logEl.innerHTML = "";
            if (bannerEl) { bannerEl.style.display = "none"; bannerEl.textContent = ""; }

            let idx = 0;
            animInterval = setInterval(() => {
              if (idx >= log.length) {
                clearInterval(animInterval);
                animInterval = null;
                if (fightBtn) { fightBtn.disabled = false; fightBtn.textContent = "Fight!"; }
                return;
              }
              const evt = log[idx];
              idx++;

              if (evt.winner) {
                if (bannerEl) {
                  bannerEl.textContent = evt.winner + " wins!";
                  bannerEl.style.display = "block";
                }
                if (fightBtn) { fightBtn.disabled = false; fightBtn.textContent = "Fight!"; }
                clearInterval(animInterval);
                animInterval = null;
                return;
              }

              const hpPctA = Math.max(0, (evt.hp_a / evt.max_hp_a) * 100);
              const hpPctB = Math.max(0, (evt.hp_b / evt.max_hp_b) * 100);

              const leftBar = root.querySelector('.hp-bar[data-side="left"]');
              const rightBar = root.querySelector('.hp-bar[data-side="right"]');
              const leftText = root.querySelector('.hp-text[data-side="left"]');
              const rightText = root.querySelector('.hp-text[data-side="right"]');

              if (leftBar) {
                leftBar.style.width = hpPctA + "%";
                leftBar.style.background = hpColor(hpPctA);
              }
              if (rightBar) {
                rightBar.style.width = hpPctB + "%";
                rightBar.style.background = hpColor(hpPctB);
              }
              if (leftText) leftText.textContent = "HP: " + Math.max(0, evt.hp_a) + " / " + evt.max_hp_a;
              if (rightText) rightText.textContent = "HP: " + Math.max(0, evt.hp_b) + " / " + evt.max_hp_b;

              let effText = "";
              if (evt.effective === "super") effText = " It's super effective!";
              else if (evt.effective === "not_very") effText = " It's not very effective...";
              else if (evt.effective === "immune") effText = " It had no effect!";

              const msg = document.createElement("div");
              msg.className = "log-entry";
              msg.innerHTML = `<strong>${evt.attacker}</strong> deals <strong>${evt.damage}</strong> damage to <strong>${evt.defender}</strong>.${effText} (HP: ${evt.hp_left})`;
              if (logEl) {
                logEl.appendChild(msg);
                logEl.scrollTop = logEl.scrollHeight;
              }
            }, 800);
          }

          renderCards();
          model.on("change:options", renderCards);
          model.on("change:data", renderCards);
          model.on("change:left_name", renderCards);
          model.on("change:right_name", renderCards);
          model.on("change:battle_log", renderCards);
          el.appendChild(root);
        }
        export default { render };
        """
        _css = """
        .compare-root { pointer-events: auto; }
        .compare { display: flex; gap: 24px; align-items: flex-start; flex-wrap: wrap; justify-content: center; }
        .poke-card {
          width: 240px;
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
        .hp-bar-container {
          width: 100%;
          height: 14px;
          background: #e5e7eb;
          border-radius: 7px;
          overflow: hidden;
          margin-bottom: 4px;
        }
        .hp-bar {
          height: 100%;
          border-radius: 7px;
          transition: width 0.4s ease, background 0.4s ease;
        }
        .hp-text {
          font-size: 11px;
          text-align: center;
          margin-bottom: 8px;
          color: #6b7280;
        }
        .poke-stats { width: 100%; border-collapse: collapse; font-size: 12px; }
        .poke-stats td { padding: 2px 0; }
        .poke-stats td:first-child { text-transform: capitalize; }
        .battle-center {
          display: flex;
          align-items: center;
          justify-content: center;
          padding-top: 120px;
        }
        .fight-btn {
          padding: 12px 32px;
          font-size: 18px;
          font-weight: 700;
          border: none;
          border-radius: 12px;
          background: linear-gradient(135deg, #ef4444, #f97316);
          color: #fff;
          cursor: pointer;
          box-shadow: 0 4px 14px rgba(239,68,68,0.4);
          transition: transform 0.15s ease, box-shadow 0.15s ease;
          pointer-events: auto;
        }
        .fight-btn:hover:not(:disabled) {
          transform: scale(1.05);
          box-shadow: 0 6px 20px rgba(239,68,68,0.5);
        }
        .fight-btn:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }
        .battle-log {
          max-height: 220px;
          overflow-y: auto;
          margin-top: 16px;
          padding: 10px 14px;
          border: 1px solid #e5e7eb;
          border-radius: 10px;
          background: #f9fafb;
          font-size: 13px;
          line-height: 1.6;
        }
        .log-entry { padding: 2px 0; }
        .winner-banner {
          margin-top: 12px;
          padding: 16px;
          text-align: center;
          font-size: 24px;
          font-weight: 800;
          border-radius: 12px;
          background: linear-gradient(135deg, #fbbf24, #f59e0b);
          color: #111827;
          animation: pop 0.4s ease;
        }
        @keyframes pop {
          0% { transform: scale(0.8); opacity: 0; }
          100% { transform: scale(1); opacity: 1; }
        }
        @media (prefers-color-scheme: dark) {
          .poke-card { background: #111827; color: #f9fafb; border-color: #374151; }
          .poke-select { background: #111827; color: #f9fafb; border-color: #374151; }
          .no-image { border-color: #4b5563; color: #9ca3af; background: #0f172a; }
          .hp-bar-container { background: #374151; }
          .hp-text { color: #9ca3af; }
          .battle-log { background: #1f2937; border-color: #374151; color: #f9fafb; }
          .winner-banner { color: #111827; }
        }
        """
        options = traitlets.List([]).tag(sync=True)
        left_name = traitlets.Unicode("").tag(sync=True)
        right_name = traitlets.Unicode("").tag(sync=True)
        data = traitlets.Dict({}).tag(sync=True)
        battle_log = traitlets.List([]).tag(sync=True)

    options = sorted(data.keys())
    left_name = options[0] if options else ""
    right_name = options[1] if len(options) > 1 else left_name
    compare = mo.ui.anywidget(
        BattleWidget(
            options=options,
            left_name=left_name,
            right_name=right_name,
            data=data,
            battle_log=[],
        )
    )
    compare
    return (compare,)


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
        t2 = row.get("type_2", None)
        if not isinstance(t2, str) or not t2 or t2 == "nan":
            t2 = None
        data[row["pokemon"]] = {
            "image": image,
            "type_1": str(row["type_1"]).lower() if isinstance(row["type_1"], str) else "normal",
            "type_2": t2.lower() if t2 else None,
            "stats": {
                "hp": int(row["hp"]),
                "attack": int(row["attack"]),
                "defense": int(row["defense"]),
                "special_attack": int(row["special_attack"]),
                "special_defense": int(row["special_defense"]),
                "speed": int(row["speed"]),
            },
        }
    return (data,)


@app.cell
def _():
    type_chart = {
        ("normal", "rock"): 0.5, ("normal", "ghost"): 0.0, ("normal", "steel"): 0.5,
        ("fire", "fire"): 0.5, ("fire", "water"): 0.5, ("fire", "grass"): 2.0,
        ("fire", "ice"): 2.0, ("fire", "bug"): 2.0, ("fire", "rock"): 0.5,
        ("fire", "dragon"): 0.5, ("fire", "steel"): 2.0,
        ("water", "fire"): 2.0, ("water", "water"): 0.5, ("water", "grass"): 0.5,
        ("water", "ground"): 2.0, ("water", "rock"): 2.0, ("water", "dragon"): 0.5,
        ("electric", "water"): 2.0, ("electric", "electric"): 0.5, ("electric", "grass"): 0.5,
        ("electric", "ground"): 0.0, ("electric", "flying"): 2.0, ("electric", "dragon"): 0.5,
        ("grass", "fire"): 0.5, ("grass", "water"): 2.0, ("grass", "grass"): 0.5,
        ("grass", "poison"): 0.5, ("grass", "ground"): 2.0, ("grass", "flying"): 0.5,
        ("grass", "bug"): 0.5, ("grass", "rock"): 2.0, ("grass", "dragon"): 0.5,
        ("grass", "steel"): 0.5,
        ("ice", "fire"): 0.5, ("ice", "water"): 0.5, ("ice", "grass"): 2.0,
        ("ice", "ice"): 0.5, ("ice", "ground"): 2.0, ("ice", "flying"): 2.0,
        ("ice", "dragon"): 2.0, ("ice", "steel"): 0.5,
        ("fighting", "normal"): 2.0, ("fighting", "ice"): 2.0, ("fighting", "poison"): 0.5,
        ("fighting", "flying"): 0.5, ("fighting", "psychic"): 0.5, ("fighting", "bug"): 0.5,
        ("fighting", "rock"): 2.0, ("fighting", "ghost"): 0.0, ("fighting", "dark"): 2.0,
        ("fighting", "steel"): 2.0, ("fighting", "fairy"): 0.5,
        ("poison", "grass"): 2.0, ("poison", "poison"): 0.5, ("poison", "ground"): 0.5,
        ("poison", "rock"): 0.5, ("poison", "ghost"): 0.5, ("poison", "steel"): 0.0,
        ("poison", "fairy"): 2.0,
        ("ground", "fire"): 2.0, ("ground", "electric"): 2.0, ("ground", "grass"): 0.5,
        ("ground", "poison"): 2.0, ("ground", "flying"): 0.0, ("ground", "bug"): 0.5,
        ("ground", "rock"): 2.0, ("ground", "steel"): 2.0,
        ("flying", "electric"): 0.5, ("flying", "grass"): 2.0, ("flying", "fighting"): 2.0,
        ("flying", "bug"): 2.0, ("flying", "rock"): 0.5, ("flying", "steel"): 0.5,
        ("psychic", "fighting"): 2.0, ("psychic", "poison"): 2.0, ("psychic", "psychic"): 0.5,
        ("psychic", "dark"): 0.0, ("psychic", "steel"): 0.5,
        ("bug", "fire"): 0.5, ("bug", "grass"): 2.0, ("bug", "fighting"): 0.5,
        ("bug", "poison"): 0.5, ("bug", "flying"): 0.5, ("bug", "psychic"): 2.0,
        ("bug", "ghost"): 0.5, ("bug", "dark"): 2.0, ("bug", "steel"): 0.5,
        ("bug", "fairy"): 0.5,
        ("rock", "fire"): 2.0, ("rock", "ice"): 2.0, ("rock", "fighting"): 0.5,
        ("rock", "ground"): 0.5, ("rock", "flying"): 2.0, ("rock", "bug"): 2.0,
        ("rock", "steel"): 0.5,
        ("ghost", "normal"): 0.0, ("ghost", "psychic"): 2.0, ("ghost", "ghost"): 2.0,
        ("ghost", "dark"): 0.5,
        ("dragon", "dragon"): 2.0, ("dragon", "steel"): 0.5, ("dragon", "fairy"): 0.0,
        ("dark", "fighting"): 0.5, ("dark", "psychic"): 2.0, ("dark", "ghost"): 2.0,
        ("dark", "dark"): 0.5, ("dark", "fairy"): 0.5,
        ("steel", "fire"): 0.5, ("steel", "water"): 0.5, ("steel", "electric"): 0.5,
        ("steel", "ice"): 2.0, ("steel", "rock"): 2.0, ("steel", "steel"): 0.5,
        ("steel", "fairy"): 2.0,
        ("fairy", "fire"): 0.5, ("fairy", "fighting"): 2.0, ("fairy", "poison"): 0.5,
        ("fairy", "dragon"): 2.0, ("fairy", "dark"): 2.0, ("fairy", "steel"): 0.5,
    }

    def get_type_multiplier(atk_type, def_types):
        mult = 1.0
        for dt in def_types:
            if dt:
                mult *= type_chart.get((atk_type, dt), 1.0)
        return mult

    return get_type_multiplier, type_chart


@app.cell
def _():
    import math
    import random

    def simulate_battle(name_a, name_b, data, get_type_mult):
        a = data[name_a]
        b = data[name_b]
        hp_a = a["stats"]["hp"]
        hp_b = b["stats"]["hp"]
        max_hp_a = hp_a
        max_hp_b = hp_b
        move_power = 80
        log = []
        turn = 0

        speed_a = a["stats"]["speed"]
        speed_b = b["stats"]["speed"]

        while hp_a > 0 and hp_b > 0:
            turn += 1
            if speed_a > speed_b:
                order = [(name_a, a, name_b), (name_b, b, name_a)]
            elif speed_b > speed_a:
                order = [(name_b, b, name_a), (name_a, a, name_b)]
            else:
                if random.random() < 0.5:
                    order = [(name_a, a, name_b), (name_b, b, name_a)]
                else:
                    order = [(name_b, b, name_a), (name_a, a, name_b)]

            for atk_name, atk, def_name in order:
                defender = a if def_name == name_a else b
                def_types = [defender.get("type_1"), defender.get("type_2")]
                atk_type = atk.get("type_1", "normal")

                phys = atk["stats"]["attack"] / defender["stats"]["defense"]
                spec = atk["stats"]["special_attack"] / defender["stats"]["special_defense"]
                if phys >= spec:
                    A = atk["stats"]["attack"]
                    D = defender["stats"]["defense"]
                else:
                    A = atk["stats"]["special_attack"]
                    D = defender["stats"]["special_defense"]

                type_mult = get_type_mult(atk_type, def_types)
                rand_factor = random.uniform(0.85, 1.0)
                damage = math.floor(((22 * move_power * A / D) / 50 + 2) * type_mult * rand_factor)
                damage = max(1, damage)

                if def_name == name_a:
                    hp_a = max(0, hp_a - damage)
                    hp_left = hp_a
                else:
                    hp_b = max(0, hp_b - damage)
                    hp_left = hp_b

                if type_mult > 1.0:
                    effective = "super"
                elif type_mult < 1.0 and type_mult > 0:
                    effective = "not_very"
                elif type_mult == 0:
                    effective = "immune"
                else:
                    effective = "normal"

                log.append({
                    "turn": turn,
                    "attacker": atk_name,
                    "defender": def_name,
                    "damage": damage,
                    "effective": effective,
                    "hp_left": hp_left,
                    "hp_a": hp_a,
                    "hp_b": hp_b,
                    "max_hp_a": max_hp_a,
                    "max_hp_b": max_hp_b,
                })

                if hp_a <= 0 or hp_b <= 0:
                    break

        winner = name_a if hp_a > 0 else name_b
        log.append({"winner": winner})
        return log

    return (simulate_battle,)


@app.cell
def _(compare, data, get_type_multiplier, simulate_battle):
    _left = compare.left_name
    _right = compare.right_name
    if _left and _right and _left in data and _right in data:
        _log = simulate_battle(_left, _right, data, get_type_multiplier)
        compare.widget.battle_log = _log
    return


if __name__ == "__main__":
    app.run()
