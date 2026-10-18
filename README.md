# 🎮 Open-Source Games Research — Native (APK-ready) + Web (HTML5)

**Research date:** 2026-10-18 · **Method:** GitHub Search API (250+ license-specific queries) · **Curated by:** Vibe agent for agentpocket0-gif

## 📌 हिंदी सारांश (TL;DR)

| File | कितने Games | क्या है |
|---|---|---|
| `data/native_games.csv` | **600 games** | Native गेम्स (C++/Java/C#/Kotlin/GDScript/Rust) — APK में convert करने लायक, हर गेम का license दिया है |
| `data/web_games.csv` | **1000 games** | HTML5/JS वेब गेम्स — WebView/Capacitor से APK बनाई जा सकती हैं |
| `scripts/collect_games.py` | — | Scraper script — fresh list generate करता है |
| `.github/workflows/refresh-games.yml` | — | GitHub Actions — हर सप्ताह list auto-refresh करता है |

**लाइसेंस जानकारी:** MIT, Apache-2.0, BSD, Unlicense = permissive (modify + launch कर सकते हो, बस credit दो)। GPL/AGPL/LGPL = copyleft (तुम्हारा modified code भी open करना होगा)। GPL वाले games Play Store पर launch तो हो सकते हैं, पर अपना source code publish करना पड़ेगा। बिना license वाले repos इस list में डाले ही नहीं गए।

⚠️ **Launch से पहले हर repo का LICENSE खुद verify करें** — code और assets (art/music) के licenses अलग-अलग हो सकते हैं।

## 📂 Files in this repo

| Path | Description |
|---|---|
| `data/native_games.csv` | 600 native open-source games, sorted by stars (quality proxy) |
| `data/web_games.csv` | 1000 open-source HTML5/JS/TS browser games, sorted by stars |
| `data/native_games_stats.json` | License + language breakdown of the native list |
| `data/web_games_stats.json` | License + language breakdown of the web list |
| `scripts/collect_games.py` | Re-runs the whole research (GitHub Search API) and regenerates the CSVs |
| `.github/workflows/refresh-games.yml` | Weekly auto-refresh via GitHub Actions (also manual trigger) |

### CSV columns

`name, repo_url, description, language, stars, license, topics, last_updated, source_query, archived`

## 📜 License cheat-sheet

| License family | Can modify? | Must release your source? | Commercial use | Notes |
|---|---|---|---|---|
| MIT | ✅ | ❌ | ✅ | Easiest — keep the copyright notice |
| Apache-2.0 | ✅ | ❌ | ✅ | Adds patent protection |
| BSD (2/3-clause) | ✅ | ❌ | ✅ | Similar to MIT |
| Unlicense / CC0 | ✅ | ❌ | ✅ | Public domain |
| LGPL-2.1/3.0 | ✅ (link, don't rewrite) | Only for the library part | ✅ | Good for engine-based games |
| MPL-2.0 | ✅ | Only modified files | ✅ | File-level copyleft |
| GPL-2.0/3.0 | ✅ | ✅ **Yes** | ✅ | Your modified game's source must be published |
| AGPL-3.0 | ✅ | ✅ **Yes** (even for online play) | ✅ | Strictest copyleft — avoid if you want closed modifications |

> All 1600 entries in this repo carry one of these licenses as detected by GitHub's API. "Custom/Other" licenses were excluded from auto-collection except where verified.

## 📱 Native games → APK (conversion paths)

| Game language | How to build an APK |
|---|---|
| Java / Kotlin | Android Studio directly (many are already Android projects) |
| C / C++ | Android Studio + NDK/CMake; SDL-based games have ready Android ports |
| C# | Unity (if Unity project) or Godot (C# support) export |
| GDScript | Godot Editor → Export → Android (one-click APK) |
| Rust | cargo-ndk / target android |
| libGDX (Java) | Gradle: `./gradlew android:assembleRelease` |
| Lua (LÖVE) | love-android packaging |

Top native examples in the list: **Mindustry** (GPL-3.0), **OpenRA** (GPL-3.0), **OpenRCT2** (GPL-3.0), **Unciv** (MPL-2.0), **Luanti/Minetest** (LGPL-2.1), **Shattered Pixel Dungeon** (GPL-3.0), **SuperTuxKart** (GPL-3.0), **OpenTTD** (GPL-2.0), **Endless Sky** (GPL-3.0), **Warzone 2100** (GPL-2.0).

## 🌐 Web games → APK

1. **WebView wrapper** — simplest; host the game and load it (or bundle files in `assets/`)
2. **Capacitor / Cordova** — proper Android project wrapper for HTML5 games
3. **PWA + Trusted Web Activity (TWA)** — publish the site as a PWA, wrap with Bubblewrap

Top web examples: **2048** (MIT), **shapez.io** (GPL-3.0), **sandspiel** (MIT), **flexboxfroggy** (MIT), **isocity** (MIT), **AncientBeast** (AGPL-3.0).

## 🔄 Auto-refresh (GitHub Actions)

The workflow `.github/workflows/refresh-games.yml`:

- Runs **every Monday** on schedule, or **manually** (Actions tab → "Refresh open-source games research" → Run workflow)
- Re-runs `scripts/collect_games.py` (uses the built-in `GITHUB_TOKEN`, no setup needed)
- Commits updated CSVs automatically if anything changed

Run locally:

```bash
pip install -r scripts/requirements.txt  # (none needed — stdlib only)
GH_TOKEN=github_pat_xxx python scripts/collect_games.py
```

## ⚠️ Caveats

- License data comes from GitHub's license detection — always open the repo's LICENSE file before shipping.
- A few entries may be game **engines/tools** rather than playable games (filter with the `description`/`topics` columns).
- Game **assets** (sprites, music) can carry different licenses than code (e.g., CC-BY-SA). Check before commercial use.
- Star counts reflect research date (2026-10-18); use them as a quality/popularity proxy.
