# -*- coding: utf-8 -*-
"""
Writes access-gate/rooms.json — the room list the gate's map picker searches.

Generated from build_room_images.ROOMS, the same source the images and kb.md are
built from, so a room can never appear in the picker without its map existing
(or vice versa). Re-run after adding or renaming a room.

    python3 build-rooms-json.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.abspath(os.path.join(HERE, os.pardir, "yarmouk-clinic-emergency-gpt"))
sys.path.insert(0, BUILD)

from build_room_images import ROOMS  # noqa: E402

OUT = os.path.join(HERE, "rooms.json")
IMAGES = os.path.join(HERE, "m")


def main():
    rooms, missing = [], []
    for r in ROOMS:
        if not os.path.exists(os.path.join(IMAGES, r["filename"])):
            missing.append(r["filename"])
            continue
        rooms.append({
            "en": r["en"],
            "ar": r["ar"],
            "floor": "Ground" if r["floor"] == "ground" else "First",
            "f": r["filename"],
        })

    if missing:
        sys.exit("no image for: %s" % ", ".join(missing))

    rooms.sort(key=lambda x: (x["floor"], x["en"].lower()))
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(rooms, fh, ensure_ascii=False, separators=(",", ":"))

    print("%d rooms -> %s (%.1f KB)" % (len(rooms), OUT, os.path.getsize(OUT) / 1024))


if __name__ == "__main__":
    main()
