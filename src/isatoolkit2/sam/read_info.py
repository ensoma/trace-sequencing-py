from dataclasses import dataclass
from pathlib import Path
import pysam
from typing import Literal

@dataclass
class ReadLine:
    """Dataclass to hold information about a read line"""

    seqname: None | str
    start: int
    end: int

@dataclass
class SamReadInfo:
    """Dataclass to hold information about a SAM reads"""

    row: list[ReadLine]

def integration_site(
    read: psyam.AlignedSegment,
) -> tuple[int, int]:
    """Get the integration site from a read"""
    # Assuming the integration site is at the start of the R1 read.
    

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
