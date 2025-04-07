"""Filter R1 reads with too many softclipped bases on the 5' end."""

from contextlib import ExitStack
from pathlib import Path
from typing import Annotated, Literal

import pysam
from annotated_types import Ge, Le

from isatoolkit2.sam.sam_utils import get_output_mode

SOFTCLIP_INDEX = 4

def softclipped_bases(
    read: pysam.AlignedSegment,
) -> int | None:
    """Get the number of softclipped bases from the R1 5' end."""
    if not read.cigartuples:
        return None
    if read.is_reverse:
        if read.cigartuples[-1][0] == SOFTCLIP_INDEX:  # Soft clip at end
            return read.cigartuples[-1][1]
    elif read.cigartuples[0][0] == SOFTCLIP_INDEX:  # Soft clip at start
        return read.cigartuples[0][1]
    return 0

def fiveprime_filter(
    infile: Literal["-"] | Path,
    outfile: Literal["-"] | Path,
    outfile_format: Literal["sam", "bam"],
    discarded_outfile: None | Path = None,
    max_softclip: Annotated[int, Ge(1), Le(100)] = 5,
    *,
    uncompressed: bool = False,
) -> None:
    """Filter R1 reads with too many softclipped bases on the 5' end."""
    # Set the output mode based on the output format and compression options
    output_mode = get_output_mode(
        outfile_format, uncompressed=uncompressed,
    )

    with ExitStack() as stack:
        infile_handle = stack.enter_context(
            pysam.AlignmentFile(str(infile)),
        )
        outfile_handle = stack.enter_context(
            pysam.AlignmentFile(
                str(outfile),
                mode=output_mode,
                template=infile_handle,
            ),
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
            # Move to the next read if it's not R1
            if not read.is_read1:
                outfile_handle.write(read)
                continue

            # Move onto the next read if it's not mapped
            if read.is_unmapped:
                continue

            # If the read is R1, check if there are too many softclipped bases.
            # Needs to be strand-aware.
            softclipped = softclipped_bases(read)
            if softclipped is not None and softclipped <= max_softclip:
                outfile_handle.write(read)
                continue

            # If the R1 read is mapped and has too many softclipped bases,
            # write it to the discard file.
            if discarded_handle:
                discarded_handle.write(read)
