---

## 🔁 ROUND 2 (added 2026-10-18)

New lists with **zero overlap** with the round-1 lists, covering **more licenses** (zlib, CC0-1.0, CC-BY-4.0, BSD-2-Clause added) and a **3D / powerful-games focus** (topics: 3d-game, fps, voxel, godot, racing-game, open-world, webgl-game) plus deeper star ranges (10–40★, 5–25★ etc.):

| File | Games | Highlights |
|---|---|---|
| `data/native_games_round2.csv` | **1638** | 3D-heavy: 407 GDScript (Godot), 306 C++, 283 C#, 232 Java, 178 Rust, 164 C, 40 Kotlin |
| `data/web_games_round2.csv` | **757** | incl. WebGL 3D games; 569 JavaScript, 187 TypeScript |

Round-2 license coverage: MIT (894 native / 431 web), GPL-3.0 (529/162), Apache-2.0 (100/89), GPL-2.0 (33/10), zlib (26/1), BSD-2-Clause (16/4), CC0-1.0 (15/15), Unlicense (9/9), AGPL-3.0 (7/15), MPL-2.0 (6/9), CC-BY-4.0 (2/3), BSD-3-Clause (1/9).

**Grand total across both rounds: 3995 unique games** (1600 in round 1 + 2395 in round 2).

> Note: round-2 queries (topic:godot, topic:fps, topic:voxel, etc.) can also surface game **engines/tools** (e.g. godot, recastnavigation). Filter with the `description`/`topics` columns if you only want playable games — or keep the engines, they are exactly what you need to build powerful 3D games.

---

## 🔍 ROUND 3 — Duplicate Verification (added 2026-10-19)

All **3995 games** were cross-checked for duplicates (same game cloned & re-released under a different repo):

| Check | Result |
|---|---|
| Exact repo-URL duplicates | **0** |
| Normalized URL duplicates (case / `.git` / trailing slash) | **0** |
| Same normalized game-name clusters | **79 clusters / 205 games** |
| → of which fork-suspects (identical repo name, different owner) | **56 clusters / 146 games** |
| Clone families (same concept, independent implementations) | **39 families / 750 entries** |

New files:

| File | Rows | Content |
|---|---|---|
| `data/duplicates_same_name.csv` | 205 | Entries sharing an identical normalized game name — the real duplicate candidates |
| `data/clone_families.csv` | 750 | Classic-game families (snake 94, minecraft 70, chess 57, tetris 50, tictactoe 48, osu 33, flappy 32, pong 30 …) |
| `data/verification_summary.json` | – | Machine-readable stats, method & notable findings |

**Decision columns (already computed for you):**
- `recommended = BEST` → highest-starred member of the cluster/family (pick this one)
- `is_latest = yes` → most recently updated member
- `dup_repo_name = yes` → another entry in the same cluster has the identical repo name (fork / re-release suspect — the strongest same-game signal)

**Notable confirmed duplicates / forks:**
- `space-wizards/space-station-14` vs `space-syndicate/space-station-14` (fork build) → keep the first
- `code-yeongyu/wobble-rush-3d` vs `aayushman-singh/wobble-rush-3d` (identical repo name) → keep the first
- `KranX/Vangers` (original, 739★) vs `kvark/vange-rs` (Rust re-implementation of the same game)
- 3 repos all named `PlantsVsZombies` → keep `limuy2022/PlantsVsZombies`

> Bottom line: no repo enters the lists twice at URL level. The 146 fork-suspect games are flagged in `data/duplicates_same_name.csv` — for each cluster just use the row with `recommended=BEST` (or `is_latest=yes` for the newest version).

## 📄 Full Word Report

Download the complete research report — **all 3,995 games** with links, licenses, languages, stars, descriptions, duplicate-verification results, license cheat-sheet and APK guide — as a single Word document:

[**Open-Source-Games-Report.doc**](Open-Source-Games-Report.doc) (right-click → Save link as… / Download button)
