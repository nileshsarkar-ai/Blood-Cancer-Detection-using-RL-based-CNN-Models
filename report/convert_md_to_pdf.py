#!/usr/bin/env python3
"""
Simple Markdown -> PDF converter using reportlab.
Designed for the project's report/report.md which references images in ../figures/.
Produces blood_all_rl_report_python.pdf at project root.

This is a pragmatic converter (supports headers '#','##','###', paragraphs, and image embeds of form ![alt](path)).
"""

import re
import os
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from PIL import Image as PILImage

ROOT = Path(__file__).resolve().parents[1]
MD_PATH = ROOT / 'report' / 'report.md'
OUT_PDF = ROOT / 'blood_all_rl_report_python.pdf'

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = inch
CONTENT_WIDTH = PAGE_WIDTH - 2 * MARGIN

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleCenter', parent=styles['Title'], alignment=TA_CENTER))
styles.add(ParagraphStyle(name='H1', parent=styles['Heading1'], spaceAfter=12))
styles.add(ParagraphStyle(name='H2', parent=styles['Heading2'], spaceAfter=8))
styles.add(ParagraphStyle(name='Body', parent=styles['BodyText'], spaceAfter=6))

img_pattern = re.compile(r'!\[.*?\]\((.*?)\)')

flowables = []

with open(MD_PATH, 'r', encoding='utf-8') as f:
    lines = [ln.rstrip() for ln in f.readlines()]

buf = []

def flush_paragraph():
    global buf
    if not buf:
        return
    text = ' '.join(buf).strip()
    if text:
        # simple replacements to keep basic markup inline
        text = text.replace('\n', '<br/>')
        flowables.append(Paragraph(text, styles['Body']))
        flowables.append(Spacer(1, 6))
    buf = []

for ln in lines:
    if not ln.strip():
        flush_paragraph()
        continue
    # headings
    if ln.startswith('# '):
        flush_paragraph()
        hdr = ln.lstrip('# ').strip()
        flowables.append(Paragraph(hdr, styles['TitleCenter']))
        flowables.append(Spacer(1, 12))
        continue
    if ln.startswith('## '):
        flush_paragraph()
        hdr = ln.lstrip('#').strip()
        flowables.append(Paragraph(hdr, styles['H1']))
        continue
    if ln.startswith('### '):
        flush_paragraph()
        hdr = ln.lstrip('#').strip()
        flowables.append(Paragraph(hdr, styles['H2']))
        continue
    # image
    m = img_pattern.search(ln)
    if m:
        flush_paragraph()
        img_path = m.group(1)
        # resolve relative paths from report/ directory
        img_file = (Path(__file__).resolve().parent / img_path).resolve()
        if not img_file.exists():
            # try relative to project root
            alt = (ROOT / img_path).resolve()
            if alt.exists():
                img_file = alt
        if img_file.exists():
            try:
                pil = PILImage.open(img_file)
                iw, ih = pil.size
                max_w = CONTENT_WIDTH
                # scale to fit width
                scale = min(1.0, max_w / iw)
                new_w = iw * scale
                new_h = ih * scale
                img = Image(str(img_file), width=new_w, height=new_h)
                flowables.append(img)
                flowables.append(Spacer(1,12))
            except Exception as e:
                flowables.append(Paragraph(f'Image could not be loaded: {img_file} ({e})', styles['Body']))
        else:
            flowables.append(Paragraph(f'Image not found: {img_path}', styles['Body']))
        continue
    # normal text (collect into paragraph)
    buf.append(ln)

flush_paragraph()

# Build PDF
print(f'Writing PDF to: {OUT_PDF}')
doc = SimpleDocTemplate(str(OUT_PDF), pagesize=A4,
                        leftMargin=MARGIN, rightMargin=MARGIN,
                        topMargin=MARGIN, bottomMargin=MARGIN)

try:
    doc.build(flowables)
    print('PDF generation successful.')
except Exception as e:
    print('PDF generation failed:', e)
    raise
