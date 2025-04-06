"""Sort BED file by position or score."""

from typing import Literal, TextIO

import click

from isatoolkit2.bed.bed_utils import BedLine, Strand, natural_key


def sort_bed(
    infile: click.utils.LazyFile | TextIO,
    outfile: click.utils.LazyFile | TextIO,
    sort_by: Literal["position", "score"] = "position",
) -> None:
    """Sort BED file by position or score."""
    # Check if each line in the input file is a valid BED line
    split_lines = [line.strip().split("\t") for line in infile]

    try:
        lines = [
            BedLine(
                seqname=str(split_line[0]),
                start=int(split_line[1]),
                end=int(split_line[2]),
                name=str(split_line[3]),
                score=int(split_line[4]),
                strand=Strand(split_line[5]),
            )
            for split_line in split_lines
        ]
    except IndexError as e:
        error_msg = "Invalid BED line format. Ensure each line has 6 fields."
        raise ValueError(error_msg) from e

    if sort_by == "position":
        # Sort by chromosome (natural sort) and start position (numeric)
        lines.sort(key=lambda line: (
            natural_key(line.seqname),
            line.start,
            line.strand,
        ))
    elif sort_by == "score":
        # Sort by score (fifth column) in descending order
        lines.sort(key=lambda line: line.score, reverse=True)

    # Write sorted lines to output
    for line in lines:
        outfile.write(
            f"{line.seqname}\t"
            f"{line.start}\t"
            f"{line.end}\t"
            f"{line.name}\t"
            f"{line.score}\t"
            f"{line.strand}\n",
        )
