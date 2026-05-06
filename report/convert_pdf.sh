#!/usr/bin/env bash

# Helper: convert the Markdown report to A4 PDF using pandoc + xelatex
# Usage: chmod +x report/convert_pdf.sh && ./report/convert_pdf.sh

set -euo pipefail

if ! command -v pandoc >/dev/null 2>&1; then
  echo "pandoc not found. Please install pandoc and a TeX engine (texlive-xetex)"
  exit 1
fi

OUT=../blood_all_rl_report.pdf
INPUT=report.md

cd "$(dirname "$0")"

pandoc -V geometry:margin=1in -V papersize:a4 -o "$OUT" "$INPUT" --pdf-engine=xelatex

echo "Created PDF: $(realpath "$OUT")"
