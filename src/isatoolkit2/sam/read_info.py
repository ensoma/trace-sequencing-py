from dataclasses import dataclass
from pathlib import Path
import pysam
from typing import Literal

from isatoolkit2.bed.bed_utils import Strand

@dataclass
class ReadLine:
    """Dataclass to hold information about a read line"""

    read_id: str
    seqname: None | str
    integration_site: None | int
    strand: None | Strand
    fragment_length: None | int
    fiveprime_softclip: None | int
    read_mapped: Literal[1, 0]
    pair_mapped: Literal[1, 0]
    supplemental_alignment: Literal[1, 0]
    alternative_alignment: iteral[1, 0]

def read_info(
    infile: Literal["-"] | Path,
) -> SamReadInfo:
    read_lines = []
    with pysam.AlignmentFile(infile) as infile_handle:
        for read in infile_handle:
            read_line = ReadLine(
                seqname=read.reference_name,
            )
            read_lines.append(read_line)
    return SamReadInfo(row=read_lines)
