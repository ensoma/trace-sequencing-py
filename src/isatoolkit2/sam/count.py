"""Count integration sites."""

from collections import defaultdict
from contextlib import ExitStack
from dataclasses import dataclass, field
from pathlib import Path
from typing import Annotated, Literal, TextIO

import click
import pysam
from annotated_types import Ge, MinLen


@dataclass
class PositionCounts:

    """Counts for integration sites."""

    r1_total: Annotated[int, Ge(0)] = 0
    integration_sites: dict[
        tuple[
            Annotated[str, MinLen(1)],
            Annotated[int, Ge(0)],
            Literal["+", "-"],
        ],
        Annotated[int, Ge(0)],
    ] = field(
        default_factory=lambda: defaultdict(int),
    )

def count_integration_sites(
    infile: Literal["-"] | Path,
    outfile: click.utils.LazyFile | TextIO,
) -> None:
    """Count integration sites in a SAM/BAM file."""
    # Open the input and output files
    with ExitStack() as stack:
        infile_handle = stack.enter_context(
            pysam.AlignmentFile(str(infile)),
        )

        # Initialize counts
        counts = PositionCounts()

        # Iterate through each read in the input file
        for read in infile_handle:
            # Skip unmapped reads and R2 reads
            if read.is_unmapped or read.is_read2:
                continue
            counts.r1_total += 1

            # Get the 5' most position of the R1 read
            if read.is_reverse:
                strand = "-"
                # For reverse reads, the 5' end is the rightmost position (reference_end - 1)
                # reference_end is one past the last aligned base
                pos = read.reference_end - 1 if read.reference_end else None
            else:
                strand = "+"
                # For forward reads, the 5' end is the leftmost position (reference_start)
                pos = read.reference_start if read.reference_start else None

            # Increment the count for this integration site
            if pos and read.reference_name:
                counts.integration_sites[(read.reference_name, pos, strand)] += 1

        # Write the counts to the output file
        for coords, count in counts.integration_sites.items():
            seqname, start, strand = coords
            outfile.write(
                f"{seqname}\t{start}\t{start}\t.\t{count}\t{strand}\n",
            )
