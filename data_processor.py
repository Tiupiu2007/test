"""CSV quality checks for the DataPilot demo."""

import csv
import io
from collections import Counter


def analyze_csv(text: str, delimiter: str = ",") -> dict:
    if not text.strip():
        raise ValueError("Il file CSV è vuoto.")
    try:
        rows = list(csv.reader(io.StringIO(text, newline=""), delimiter=delimiter))
    except csv.Error as exc:
        raise ValueError("Il file non sembra essere un CSV valido.") from exc
    if not rows:
        raise ValueError("Il file CSV è vuoto.")

    headers = [item.strip() for item in rows[0]]
    if not any(headers):
        raise ValueError("La prima riga deve contenere le intestazioni delle colonne.")
    counts = Counter(headers)
    duplicate_headers = sorted(h for h, count in counts.items() if h and count > 1)
    data_rows = rows[1:]
    width = len(headers)
    normalized, malformed, missing, whitespace = [], [], [], []

    for row_number, row in enumerate(data_rows, start=2):
        if len(row) != width:
            malformed.append({"row": row_number, "expected": width, "found": len(row)})
        padded = row[:width] + [""] * max(0, width - len(row))
        normalized.append(padded)
        for index, value in enumerate(padded):
            column = headers[index] or f"Colonna {index + 1}"
            if not value.strip():
                missing.append({"row": row_number, "column": column})
            elif value != value.strip():
                whitespace.append({"row": row_number, "column": column})

    seen, duplicate_rows = set(), []
    for row_number, row in enumerate(normalized, start=2):
        key = tuple(value.strip() for value in row)
        if key in seen:
            duplicate_rows.append(row_number)
        else:
            seen.add(key)

    preview = []
    for row in normalized[:8]:
        preview.append({(headers[i] or f"Colonna {i + 1}"): row[i] for i in range(width)})
    issue_count = len(missing) + len(duplicate_rows) + len(whitespace) + len(malformed) + len(duplicate_headers)
    return {
        "row_count": len(data_rows), "column_count": width, "headers": headers,
        "missing_cells": missing, "duplicate_rows": duplicate_rows,
        "whitespace_cells": whitespace, "malformed_rows": malformed,
        "duplicate_headers": duplicate_headers, "preview": preview,
        "issue_count": issue_count,
    }
