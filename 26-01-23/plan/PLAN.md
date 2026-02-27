# Pokemon Battle Feature - Implementation Plan

## Goal
Transform the Pokemon comparison widget into an interactive battle simulator
using the TidyTuesday Pokemon dataset.

## Dataset
- Source: TidyTuesday 2025-04-01 Pokemon dataset
- Key stats used: hp, attack, defense, special_attack, special_defense, speed
- Type information: type_1, type_2 (for type effectiveness)

## Architecture

### 1. Data Preparation (`data` cell)
- Load Pokemon CSV from TidyTuesday GitHub raw URL
- Build a dictionary keyed by pokemon name with:
  - Image URL (fixed with `https:` prefix)
  - Type info (type_1, type_2)
  - Battle stats (hp, attack, defense, special_attack, special_defense, speed)

### 2. Type Effectiveness Chart (`type_chart` cell)
- Full Gen-I-style type chart with ~90 matchup entries
- Covers all 18 types (normal, fire, water, electric, grass, ice, fighting,
  poison, ground, flying, psychic, bug, rock, ghost, dragon, dark, steel, fairy)
- Multipliers: 2.0 (super effective), 0.5 (not very effective), 0.0 (immune)
- Dual-type defenders get multiplied factors

### 3. Battle Simulator (`simulate_battle` function)
- Turn-based battle using simplified Pokemon damage formula
- Speed determines turn order (random on tie)
- Each turn: both Pokemon attack (faster goes first)
- Damage = floor(((22 * power * A / D) / 50 + 2) * type_mult * rand)
  - Move power fixed at 80
  - A/D = best of physical (attack/defense) or special (sp_atk/sp_def)
  - Random factor: 0.85-1.0
- Battle log records every hit with attacker, defender, damage, effectiveness,
  and remaining HP for both sides

### 4. BattleWidget (anywidget)
- **Layout**: Two Pokemon cards with a "Fight!" button in between
- **Pokemon cards**: dropdown selector, sprite image, name, HP bar, stat table
- **HP bars**: color-coded (green > 50%, yellow > 20%, red <= 20%)
  with smooth CSS transitions
- **Fight button**: triggers animated battle replay
- **Battle log**: scrollable panel showing each attack with damage and
  effectiveness messages ("super effective!", "not very effective...", "no effect!")
- **Winner banner**: animated gold banner announcing the winner
- **Dark mode**: full CSS support via `prefers-color-scheme`

### 5. Reactive Wiring (marimo cells)
- Selecting a Pokemon in either dropdown triggers `model.save_changes()`
- A reactive cell watches `compare.left_name` / `compare.right_name`
- On change, runs `simulate_battle()` and sets `compare.widget.battle_log`
- The widget auto-replays the battle animation on each new log

## Tech Stack
- **marimo** - reactive notebook framework
- **anywidget** - custom Jupyter-compatible widgets with ESM + CSS
- **pandas** - data loading and manipulation
- **traitlets** - widget state synchronization

## Files Changed
- `26-01-23/notebook.py` - main notebook with all battle logic and widget
