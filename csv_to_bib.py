#!/usr/bin/env python3
"""
Convert a tab-delimited CSV of paper submissions into a BibTeX (.bib) file.

Usage:
    python csv_to_bib.py input.csv output.bib

Expected CSV header (tab-delimited):
    Paper ID    Paper Title    Abstract    Primary Contact Author Name
    Primary Contact Author Email    Authors    Author Names    Status    Files
"""

import csv
import re
import sys


def escape_bibtex(value: str) -> str:
    """Escape characters that would break BibTeX field parsing."""
    if value is None:
        return ""
    value = value.strip()
    # Balance/escape stray braces so they don't prematurely close a field.
    value = value.replace("{", r"\{").replace("}", r"\}")
    # Collapse internal newlines/tabs into single spaces.
    value = re.sub(r"\s+", " ", value)
    return value


def make_key(paper_id: str) -> str:
    """Turn a Paper ID into a safe BibTeX citation key (no spaces/commas/braces)."""
    key = paper_id.strip()
    key = re.sub(r"[\s,{}]+", "_", key)
    return key


def convert(input_csv: str, output_bib: str, year: str = "2026") -> None:
    with open(input_csv, newline="", encoding="utf-8-sig") as f_in:
        reader = csv.DictReader(f_in, delimiter="\t")

        # Sanity-check that expected columns exist.
        expected = {
            "Paper ID", "Paper Title", "Abstract",
            "Primary Contact Author Name", "Primary Contact Author Email",
            "Authors", "Author Names", "Status", "Files",
        }
        missing = expected - set(reader.fieldnames or [])
        if missing:
            print(f"Warning: missing expected columns: {missing}", file=sys.stderr)

        entries = []
        for row in reader:
            paper_id_raw = row.get("Paper ID", "").strip()
            if not paper_id_raw:
                continue  # skip blank lines

            key = make_key(paper_id_raw)
            title = escape_bibtex(row.get("Paper Title", ""))
            abstract = escape_bibtex(row.get("Abstract", ""))
            status = escape_bibtex(row.get("Status", ""))
            files = escape_bibtex(row.get("Files", ""))
            author = escape_bibtex(row.get("Author Names", "").replace(";", " AND ").replace("*", ""))
            paper_id = escape_bibtex(paper_id_raw)

            entry = (
                f"@article{{{key},\n"
                f"  publicationtype = {{accepted}},\n"
                f"  Postersession = {{undecided}},\n"
                f"  year = {{{year}}},\n"
                f"  pdf = {{submissions/{paper_id}/Submission/{files}}},\n"
                f"  poster = {{}},\n"
                f"  Paper_ID = {{{paper_id}}},\n"
                f"  title = {{{title}}},\n"
                f"  Abstract = {{{abstract}}},\n"
                f"  author = {{{author}}},\n"
                f"  Status = {{Accept}},\n"
                f"}}\n"
            )
            entries.append(entry)

    with open(output_bib, "w", encoding="utf-8") as f_out:
        f_out.write("\n".join(entries))

    print(f"Wrote {len(entries)} entries to {output_bib}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python csv_to_bib.py <input.csv> <output.bib>", file=sys.stderr)
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2])
