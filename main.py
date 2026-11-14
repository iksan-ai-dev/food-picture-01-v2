#!/usr/bin/env python3
"""Copy the shipped poke-bowl image to /output/entry.png (stdlib only).

The image is rendered at build time by generate.py and shipped as
entry.png; this program only copies it, so both grading runs write the
exact same bytes. No network, no third-party packages.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(OUT, exist_ok=True)
shutil.copyfile(os.path.join(HERE, "entry.png"), os.path.join(OUT, "entry.png"))
