Report conversion and notes

Files created:

- `report/report.md` - the main Markdown report (contains embedded images referencing `../figures/`)
- `report/convert_pdf.sh` - helper script that attempts to convert the Markdown to PDF using pandoc + xelatex

Conversion instructions (recommended):

1. Install pandoc and a TeX engine (e.g., texlive or a minimal xelatex/pdflatex distribution).

Debian/Ubuntu example:

```bash
sudo apt update
sudo apt install -y pandoc texlive-xetex
```

2. From the project root run:

```bash
# create PDF (A4) using xelatex
pandoc -V geometry:margin=1in -V papersize:a4 -o blood_all_rl_report.pdf report/report.md --pdf-engine=xelatex
```

3. If pandoc/latex isn't available, open `report/report.md` in a markdown editor (Typora, VS Code) and export to PDF using the editor's "Export to PDF" feature.

Notes:
- The report references images in `figures/` by relative paths. Ensure `figures/` is present and contains the generated PNGs before converting.
- If you prefer a different PDF engine (pdflatex, wkhtmltopdf), adapt the `--pdf-engine` flag accordingly.

