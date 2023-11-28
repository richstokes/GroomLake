#!/bin/bash
set -e

pyxel package . main.py
pyxel app2html GroomLake.pyxapp

mkdir dist || true
mv GroomLake.html dist/index.html
rm GroomLake.pyxapp
