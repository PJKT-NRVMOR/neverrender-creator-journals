#!/usr/bin/env python3
"""
NeverRender Labs Vision & Color Science — Heavy Studio Grey to Airy Gustavian Chalk Lifter
Transforms heavy mobile-app concrete grey backgrounds (#AEB0B4 wall / #5E6063 floor) into
high-key, luminous Mansour / Eloquence warm gallery chalk (#F6F4F0 wall / #EAE7E1 floor)
while preserving natural floor contact shadows and 100% of warm wood/brass chroma.
"""

import os
import sys
import subprocess

if __name__ == "__main__":
    target = os.getenv(
        "NRL_CHALK_LIFTER_SCRIPT",
        r"C:\Users\Saturn\Desktop\project-marshall-college\scripts\campaigns-and-circulars\lighten_grey_studio_to_gustavian_chalk.py"
    )
    if os.path.exists(target):
        sys.exit(subprocess.call([sys.executable, target] + sys.argv[1:]))
