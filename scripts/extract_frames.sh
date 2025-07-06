#!/usr/bin/env bash

INPUT_VIDEO="$1"
OUT_DIR="../dataset/images/raw"
FPS=5           # кадров в секунду
START_NUM=1434    # с какого кадра начинать нумерацию

mkdir -p "$OUT_DIR"

ffmpeg -i "$INPUT_VIDEO" -vf fps=$FPS -start_number $START_NUM \
       "$OUT_DIR/frame_%05d.jpg"

