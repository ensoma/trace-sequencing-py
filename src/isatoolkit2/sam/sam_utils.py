"""SAM utilities for handling SAM/BAM files."""

from typing import Literal


def get_output_mode(
    output_format: Literal["sam", "bam"],
    *,
    uncompressed: bool,
) -> Literal["w", "wu", "wb"]:
    """Get the output mode based on the output format and compression options."""
    return "w" if output_format == "sam" else "wu" if uncompressed else "wb"
