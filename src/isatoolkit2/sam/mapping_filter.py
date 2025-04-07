"""Filter SAM/BAM files based on ALT and SUP filtering options."""

from contextlib import ExitStack
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import pysam

from isatoolkit2.sam.sam_utils import get_output_mode


@dataclass
class AltSupCounts:

    """Counts for ALT and SUP filtering."""

    alt_or_sup: int = 0
    total: int = 0
    passing: int = 0

    def __str__(self) -> str:
        """Print the counts in a readable format."""
        return (
            f"Total: {self.total}\n"
            f"Passing: {self.passing}\n"
            f"ALT or SUP: {self.alt_or_sup}\n"
        )

def alt_sup_filtering(
    infile: Literal["-"] | Path,
    outfile: Literal["-"] | Path,
    output_format: Literal["sam", "bam"],
    discarded_outfile: None | Path = None,
    *,
    filter_alt: bool = True,
    filter_sup: bool = True,
    uncompressed: bool = False,
) -> None:
    """Filter SAM/BAM file based on ALT and SUP filtering options."""
    # Set the output mode based on the output format and compression options
    output_mode = get_output_mode(
        output_format, uncompressed=uncompressed,
    )

    # Open the input and output files
    counts = AltSupCounts()

    with ExitStack() as stack:
        infile_handle = stack.enter_context(
            pysam.AlignmentFile(str(infile)),
        )
        outfile_handle = stack.enter_context(
            pysam.AlignmentFile(str(outfile), mode=output_mode, template=infile_handle),
        )
        discarded_handle = (
            stack.enter_context(
                pysam.AlignmentFile(
                    str(discarded_outfile),
                    mode=output_mode,
                    template=infile_handle,
                ),
            )
            if discarded_outfile is not None else None
        )

        # Iterate over each read in the input file
        for read in infile_handle:
            counts.total = counts.total + 1
            # Filter based on ALT and SUP filtering options
            if filter_alt and read.has_tag("XA"):
                counts.alt_or_sup = counts.alt_or_sup + 1
                if discarded_handle:
                    discarded_handle.write(read)
                continue
            if filter_sup and read.has_tag("SA"):
                counts.alt_or_sup = counts.alt_or_sup + 1
                if discarded_handle:
                    discarded_handle.write(read)
                continue

            # Write the read to the output file
            counts.passing = counts.passing + 1
            outfile_handle.write(read)
