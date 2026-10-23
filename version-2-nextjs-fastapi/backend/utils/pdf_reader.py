"""Robust text extraction for text-based PDF resumes.

Uses pdfplumber's layout-aware extraction first, with a regular extraction
fallback for pages where layout mode returns little usable text. OCR is not
performed here; scanned image-only PDFs need an OCR engine installed.
"""

from __future__ import annotations

import logging
import re
import unicodedata
from pathlib import Path
from typing import BinaryIO, Union

import pdfplumber

logger = logging.getLogger(__name__)
PdfInput = Union[str, Path, BinaryIO]


def _clean_text(text: str) -> str:
    """Normalize common PDF extraction artifacts without flattening sections."""
    if not text:
        return ""

    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\u00ad", "")  # soft hyphen
    text = text.replace("\x00", " ")
    # Join words split by a line-ending hyphen, but keep genuine hyphenated terms.
    text = re.sub(r"(?<=\w)-\s*\n\s*(?=\w)", "", text)

    cleaned_lines = []
    for line in text.splitlines():
        line = line.replace("\t", " ")
        line = re.sub(r"[ \u00a0]{2,}", " ", line).strip()
        if line:
            cleaned_lines.append(line)
        elif cleaned_lines and cleaned_lines[-1] != "":
            # Keep one blank line as a weak section boundary.
            cleaned_lines.append("")

    return "\n".join(cleaned_lines).strip()


def _usable_text_score(text: str) -> tuple[int, int]:
    """Prefer extractable, mostly textual output over layout whitespace."""
    compact = re.sub(r"\s+", "", text)
    alphanumeric = sum(char.isalnum() for char in compact)
    return alphanumeric, len(compact)


def read_pdf(file: PdfInput) -> str:
    """Extract readable text from a PDF file or binary file-like object.

    Each page is extracted separately to preserve page boundaries. Layout mode
    can help with resumes that use columns; regular mode is used as a fallback
    when it produces more meaningful text.
    """
    page_texts: list[str] = []

    try:
        with pdfplumber.open(file) as pdf:
            if not pdf.pages:
                return ""

            for page_number, page in enumerate(pdf.pages, start=1):
                layout_text = ""
                regular_text = ""

                try:
                    layout_text = page.extract_text(
                        layout=True,
                        x_tolerance=2,
                        y_tolerance=3,
                    ) or ""
                except Exception:
                    logger.debug("Layout extraction failed on PDF page %s", page_number, exc_info=True)

                try:
                    regular_text = page.extract_text(
                        x_tolerance=2,
                        y_tolerance=3,
                    ) or ""
                except Exception:
                    logger.debug("Regular extraction failed on PDF page %s", page_number, exc_info=True)

                layout_clean = _clean_text(layout_text)
                regular_clean = _clean_text(regular_text)

                # Layout output is preferred when it retains most of the useful
                # text; otherwise use the regular extractor for that page.
                layout_score = _usable_text_score(layout_clean)
                regular_score = _usable_text_score(regular_clean)
                if layout_score[0] >= regular_score[0] * 0.70 and layout_score[0] > 0:
                    selected = layout_clean
                else:
                    selected = regular_clean or layout_clean

                if selected:
                    page_texts.append(selected)

    except Exception as exc:
        logger.exception("Failed to read PDF resume")
        raise ValueError("Could not read this PDF. Check that it is a valid, unencrypted PDF.") from exc

    result = "\n\n".join(page_texts).strip()
    # Avoid sending an image-only/scanned PDF's near-empty extraction downstream.
    if len(re.sub(r"\s", "", result)) < 20:
        logger.info("PDF extraction returned too little text; the PDF may be scanned or image-only")
        return ""
    return result
