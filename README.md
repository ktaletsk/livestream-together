# DataHeads — df.head(3)

![DataHeads Episode 1](assets/episode_one_thumbnail.png)

A friendly, cross-ecosystem podcast where three hosts analyze the same dataset
for ~1 hour using their own tools — then compare approaches and results.
Each episode follows a TidyTuesday dataset.

## Hosts

- **Konstantin Taletskiy** ([@ktaletsk](https://github.com/ktaletsk)) — Jupyter OSS developer at Anaconda and founder of orbrx
- **Rodrigo Silva Ferreira** ([@rodrigosf672](https://github.com/rodrigosf672)) — QA engineer at Posit PBC, focused on quality and usability of open-source R and Python tooling
- **Yann Debray** ([@yanndebray](https://github.com/yanndebray)) — MATLAB Online product manager at MathWorks and author of "MATLAB with Python"

## Episodes

### Ep 1 — Pokemon

https://github.com/user-attachments/assets/3732e8c5-59e5-40e7-a4f8-1db2d586ae53

**Dataset:** [TidyTuesday 2025-04-01 Pokemon](https://github.com/rfordatascience/tidytuesday) — 949 rows, 22 columns (stats, types, size, image URLs).

**What each host built:**
- **Konstantin** — Marimo notebook; discovered that Marimo's dataframe viewer renders Pokemon sprites inline from URLs. Built an AnyWidget comparison card widget to view stats side-by-side; battle mode is a work-in-progress.
- **Rodrigo** — PyScript app pulling sprites and stats live from the PokeAPI (no local image hosting). Supports type/legendary filters and runs animated turn-based battles with sound. ([app](https://pokemon-simulator-pyscript.netlify.app/) · [repo](https://github.com/rodrigosf672/pyscript-pokemon-app))
- **Yann** — MATLAB running inside a GitHub Codespace dev container, served as a full browser-based IDE. Showed the MATLAB VS Code extension working inside Positron and discussed JupyterHub integration for enterprise deployments.

**Topics discussed:**
- Notebook ecosystem: Jupyter (700+ extensions), Marimo reactivity, Positron's new notebook editor (Feb 2026)
- Docker and dev containers: reproducible experiments, JupyterHub at scale, Ollama + Open UI setups, remote SSH from Positron into AWS
- [JupyterLab extension marketplace](https://labextensions.dev) Codespaces launcher: 900 auto-generated branches, one per extension
- Package management: UV vs Conda; praise for Marimo's inline package install UX
- Claude Code used live to sketch a battle mechanic — left as a cliffhanger

**Next episode:** finish the battle widgets, compare all three implementations, and dig into data questions (does height drive speed? does weight drive strength?).
