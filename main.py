"""News image entry for make.fun: news-image-20261123.

Sums up the world news of Monday 23 November 2026 in one image.

The image itself is entry.png beside this file. It was drawn for this
entry as a one-page newspaper front page: masthead plus the date,
then five stories -- the Iran war widening to Bahrain and the Strait
of Hormuz, the COP31 climate talks collapsing in Antalya, Russian
strikes killing civilians in Ukraine, Ukrainian naval drones sinking
a Russian warship off Libya, and the Democrats winning the US House.

This program only copies that image to the output path. It uses the
standard library only, makes no network call, and reads nothing
outside its own directory, so running it twice writes the same bytes.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def main() -> None:
    if not SOURCE.is_file():
        raise FileNotFoundError(f"entry image missing: {SOURCE}")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(SOURCE, target)
    if target.stat().st_size > 1_048_576:
        raise ValueError("entry image is over the 1 MiB limit")


if __name__ == "__main__":
    main()
