"""Sort BED file by position or score."""

import re
from typing import Annotated, Literal, TextIO

import click
from pydantic import Field


def natural_key(string: str) -> list[str | int]:
    """Generate a key for natural sorting."""
    return [int(s) if s.isdigit() else s.lower() for s in re.split(r"(\d+)", string)]

def sort_bed(
    infile: click.utils.LazyFile | TextIO,
    outfile: click.utils.LazyFile | TextIO,
    sort_by: Literal["position", "score"] = "position",
) -> None:
    """Sort BED file by position or score."""
    lines = [line.strip() for line in infile]

    if sort_by == "position":
        # Sort by chromosome (natural sort) and start position (numeric)
        lines.sort(key=lambda line: (
            natural_key(line.split("\t")[0]),
            int(line.split("\t")[1]),
        ))
    elif sort_by == "score":
        # Sort by score (fifth column) in descending order
        lines.sort(key=lambda line: int(line.split("\t")[4]), reverse=True)

    # Write sorted lines to output
    for line in lines:
        outfile.write(f"{line}\n")
