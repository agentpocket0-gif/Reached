#!/usr/bin/env python3
"""
Collect open-source games research from the GitHub Search API.

Regenerates:
  data/native_games.csv   (up to 600 native games, APK-ready technologies)
  data/web_games.csv      (up to 1000 HTML5/JS browser games)
  data/*_stats.json       (license + language breakdowns)

Usage:
  GH_TOKEN=<token> python scripts/collect_games.py
(Uses stdlib only. Token optional but recommended: higher rate limits.)
"""

import csv
import json
import os
import re
import time
import urllib.parse
import urllib.request

TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
API = "https://api.github.com/search/repositories"

NATIVE_BASES = [
    "topic:game language:C++ stars:>40",
    "topic:game language:C# stars:>40",
    "topic:game language:C stars:>25",
    "topic:game language:Java stars:>20",
    "topic:game language:Kotlin stars:>15",
    "topic:game language:Rust stars:>25",
    "topic:game language:GDScript stars:>10",
    "topic:android-game stars:>15",
    "topic:godot-game stars:>10",
    "topic:roguelike stars:>25",
    "topic:open-source-game stars:>8",
    "topic:libgdx game stars:>10",
]

WEB_BASES = [
    "topic:javascript-game stars:>8",
    "topic:browser-game stars:>8",
    "topic:html5-game stars:>8",
    "topic:web-game stars:>8",
    "topic:canvas-game stars:>8",
    "topic:js13kgames stars:>3",
    "topic:phaser-game stars:>5",
    "topic:game language:JavaScript stars:>15",
    "topic:game language:TypeScript stars:>15",
]

WEB_VOLUME_BASES = [
    "topic:javascript-game stars:<9",
    "topic:browser-game stars:<9",
    "topic:html5-game stars:<9",
    "topic:web-game stars:<9",
    "topic:canvas-game stars:<9",
    "topic:js13kgames stars:<4",
]

LICENSES = [
    "mit", "gpl-3.0", "gpl-2.0", "lgpl-2.1", "lgpl-3.0",
    "agpl-3.0", "apache-2.0", "bsd-3-clause", "bsd-2-clause",
    "mpl-2.0", "unlicense",
]

NATIVE_LANGS = {"C", "C++", "C#", "Java", "Kotlin", "GDScript", "Rust",
                "Lua", "Zig", "Go", "Haxe", "Pascal", "Objective-C", "D", "Vala"}
WEB_LANGS = {"JavaScript", "TypeScript", "CoffeeScript"}

BAD_DESC = re.compile(
    r"(awesome[- ]list|awesome games|awesome open|boilerplate|cheat ?sheet|"
    r"curated list|list of (open[- ]source|free|best)|tutorial|for beginners|"
    r"learning (to|how) (code|program)|interview (questions|prep)|\bapi\b|"
    r"emulator|\bsdk\b|\bengine\b|\bframework\b|game server|dedicated server)", re.I)

SEEDS = [
    ("SuperTuxKart", "SuperTuxKart/stk-code", "https://github.com/SuperTuxKart/stk-code",
     "3D open-source arcade kart racer (Tux mascot), has Android port", "C++", 4300, "gpl-3.0"),
    ("Luanti (Minetest)", "luanti-org/luanti", "https://github.com/luanti-org/luanti",
     "Open-source voxel sandbox game engine + game, Android port available", "C++", 11000, "lgpl-2.1"),
    ("OpenTTD", "OpenTTD/OpenTTD", "https://github.com/OpenTTD/OpenTTD",
     "Transport strategy simulation game based on Transport Tycoon Deluxe", "C++", 6500, "gpl-2.0"),
    ("Battle for Wesnoth", "wesnoth/wesnoth", "https://github.com/wesnoth/wesnoth",
     "Turn-based tactical strategy game with fantasy theme, has Android port", "C++", 5300, "gpl-2.0"),
    ("Warzone 2100", "Warzone2100/warzone2100", "https://github.com/Warzone2100/warzone2100",
     "Post-apocalyptic real-time strategy game, has Android port", "C++", 3300, "gpl-2.0"),
    ("OpenRA", "OpenRA/OpenRA", "https://github.com/OpenRA/OpenRA",
     "Open-source real-time strategy engine for Red Alert/Command & Conquer", "C#", 14300, "gpl-3.0"),
    ("Freeciv", "freeciv/freeciv", "https://github.com/freeciv/freeciv",
     "Civilization-style empire-building strategy game", "C", 1400, "gpl-2.0"),
    ("Xonotic", "xonotic/xonotic", "https://github.com/xonotic/xonotic",
     "Fast-paced arena first-person shooter (assets CC-BY-SA)", "C", 1500, "gpl-2.0"),
    ("Hedgewars", "hedgewars/hedgewars", "https://github.com/hedgewars/hedgewars",
     "Turn-based artillery game (Worms-like), official Android port exists", "Pascal", 700, "gpl-2.0"),
    ("Endless Sky", "endless-sky/endless-sky", "https://github.com/endless-sky/endless-sky",
     "Space trading and combat game (Escape Velocity-like)", "C++", 5000, "gpl-3.0"),
    ("Shattered Pixel Dungeon", "00-Evan/shattered-pixel-dungeon",
     "https://github.com/00-Evan/shattered-pixel-dungeon",
     "Roguelike dungeon crawler, NATIVE Android game (APK-ready)", "Java", 4900, "gpl-3.0"),
    ("Mindustry", "Anuken/Mindustry", "https://github.com/Anuken/Mindustry",
     "Tower-defense factory-building RTS, native Android/iOS ports", "Java", 26000, "gpl-3.0"),
]

HEADER = ["name", "repo_url", "description", "language", "stars",
          "license", "topics", "last_updated", "source_query", "archived"]


def search(query, retries=5):
    url = API + "?q=" + urllib.parse.quote(query) + "&sort=stars&order=desc&per_page=100"
    for attempt in range(retries):
        try:
            headers = {"Accept": "application/vnd.github+json",
                       "User-Agent": "open-source-games-research"}
            if TOKEN:
                headers["Authorization"] = "Bearer " + TOKEN
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.load(resp)
        except Exception as exc:  # noqa: BLE001
            if attempt == retries - 1:
                print("  ERR:", query[:60], "->", exc)
                return None
            time.sleep(15)
    return None


def collect(entries, base, lic, langs, src_prefix=""):
    query = base + " license:" + lic
    data = search(query)
    if not data:
        return
    for it in data.get("items", []):
        if it.get("fork"):
            continue
        desc = re.sub(r"\s+", " ", it.get("description") or "").strip()
        if desc and BAD_DESC.search(desc):
            continue
        if it.get("language") not in langs:
            continue
        entries.append({
            "name": it.get("name"),
            "repo_url": it.get("html_url"),
            "description": desc[:200],
            "language": it.get("language"),
            "stars": it.get("stargazers_count", 0),
            "license": lic.upper(),
            "topics": " ".join((it.get("topics") or [])[:10]),
            "last_updated": (it.get("updated_at") or "")[:10],
            "source_query": src_prefix + base,
            "archived": "yes" if it.get("archived") else "no",
        })


def dedupe_sort_cap(entries, cap):
    best = {}
    for e in entries:
        key = e["repo_url"].lower()
        if key not in best or e["stars"] > best[key]["stars"]:
            best[key] = e
    out = sorted(best.values(), key=lambda e: e["stars"], reverse=True)
    return out[:cap]


def stats_for(rows):
    by_lic, by_lang = {}, {}
    for r in rows:
        by_lic[r["license"]] = by_lic.get(r["license"], 0) + 1
        by_lang[r["language"] or "?"] = by_lang.get(r["language"] or "?", 0) + 1
    return {"count": len(rows), "by_license": by_lic, "by_language": by_lang}


def write_csv(path, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=HEADER)
        writer.writeheader()
        writer.writerows(rows)


def main():
    native, web = [], []
    for name, full, url, desc, lang, stars, lic in SEEDS:
        native.append({"name": name, "repo_url": url, "description": desc,
                       "language": lang, "stars": stars, "license": lic.upper(),
                       "topics": "", "last_updated": "", "source_query": "curated-seed",
                       "archived": "no"})

    jobs = []
    for base in NATIVE_BASES:
        for lic in LICENSES:
            jobs.append((native, base, lic, NATIVE_LANGS))
    for base in WEB_BASES:
        for lic in LICENSES:
            jobs.append((web, base, lic, WEB_LANGS))
    for base in WEB_VOLUME_BASES:
        jobs.append((web, base, "mit", WEB_LANGS))

    for i, (entries, base, lic, langs) in enumerate(jobs, 1):
        print(f"[{i}/{len(jobs)}] {base} | {lic}")
        collect(entries, base, lic, langs)
        time.sleep(2.2)  # stay under GitHub's 30 searches/minute limit

    native = dedupe_sort_cap(native, 600)
    web = dedupe_sort_cap(web, 1000)

    write_csv(os.path.join("data", "native_games.csv"), native)
    write_csv(os.path.join("data", "web_games.csv"), web)
    with open(os.path.join("data", "native_games_stats.json"), "w", encoding="utf-8") as fh:
        json.dump(stats_for(native), fh, indent=2)
    with open(os.path.join("data", "web_games_stats.json"), "w", encoding="utf-8") as fh:
        json.dump(stats_for(web), fh, indent=2)

    print(f"Done: {len(native)} native games, {len(web)} web games.")


if __name__ == "__main__":
    main()
