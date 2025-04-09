"""Circularize integration vector around the FRT site."""

from contextlib import ExitStack
from pathlib import Path
from sys import stdin, stdout
from typing import Annotated, Literal, TextIO

import regex
from annotated_types import Ge, Le, MinLen
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from pydantic import Field

EXPECTED_FRT_SITES = 2

def find_frt_sites(
    seq: Annotated[
        str,
        MinLen(10),
        Field(pattern=r"^[ACGTNacgtn]+"),
    ],
    frt_sequence: Annotated[
        str,
        MinLen(5),
        Field(pattern=r"^[ACGTNacgtn]+"),
    ],
    allowed_errors: Annotated[int, Ge(0), Le(5)],
) -> tuple[regex.Match, regex.Match, Literal["forward", "revcomp"]]:
    """Find the FRT sites in the sequence."""
    # The regex patterns to find the FRT sites.
    # Also the reverse complement.
    pattern = f"({frt_sequence}){{e<={allowed_errors}}}"

    rev_frt_sequence = str(
        Seq(frt_sequence).reverse_complement(),
    )
    pattern_revcomp = f"({rev_frt_sequence}){{e<={allowed_errors}}}"

    # Find the FRT sites
    matches = list(regex.finditer(pattern, seq))
    matches_revcomp = list(
        regex.finditer(pattern_revcomp, seq),
    )

    # Check if we found exactly two FRT sites.
    # Can either both be in the forward or revcomp.
    orientation = check_orientation(
        matches,
        matches_revcomp,
    )

    # Return the matches for the correct orientation.
    if orientation == "forward":
        return matches[0], matches[1], orientation
    return matches_revcomp[0], matches_revcomp[1], orientation

def check_orientation(
    forward_matches: list[regex.Match],
    reverse_matches: list[regex.Match],
) -> Literal["forward", "revcomp"]:
    """Check if we found exactly two FRT sites."""
    # Must have two sites on either the forward or reverse strand.
    if (
        len(forward_matches) != EXPECTED_FRT_SITES and
        len(reverse_matches) != EXPECTED_FRT_SITES
    ):
        error_msg = (
            f"Expected 2 FRT sites on either the forward or reverse strand, "
            f"found {len(forward_matches)} forward "
            f"and {len(reverse_matches)} reverse."
        )
        raise ValueError(error_msg)

    # Check if matches are all either on the forward or reverse strand.
    if (
        (
            len(forward_matches) == EXPECTED_FRT_SITES and
            len(reverse_matches) > 0
        ) or
        (
            len(reverse_matches) == EXPECTED_FRT_SITES and
            len(forward_matches) > 0
        )
    ):
        error_msg = (
            f"FRT sites must be either on the forward or reverse strand."
            f"found {len(forward_matches)} forward "
            f"and {len(reverse_matches)} reverse."
        )
        raise ValueError(error_msg)

    # Return if the matches are on the forward or reverse strand.
    return "forward" if len(forward_matches) == EXPECTED_FRT_SITES else "revcomp"

def circularize_integration_vector(
    infile: Literal["-"] | Path | TextIO,
    outfile: Literal["-"] | Path | TextIO,
    frt_sequence: Annotated[
        str,
        MinLen(5),
        Field(pattern=r"^[ACGTNacgtn]+"),
    ],
    allowed_errors: Annotated[int, Ge(0), Le(5)] = 0,
) -> None:
    """Circularize a sequence around the FRT site."""
    with ExitStack() as stack:
        # Prepare the input handle
        if infile == "-":
            input_stream = stdin
        elif isinstance(infile, TextIO):
            input_stream = infile
        else:
            input_stream = stack.enter_context(
                infile.open("r"),
            )

        infile_handle = SeqIO.parse(input_stream, "fasta")

        # Prepare the output handle
        if outfile == "-":
            output_stream = stdout
        elif isinstance(outfile, TextIO):
            output_stream = outfile
        else:
            output_stream = stack.enter_context(
                outfile.open("w"),
            )

        # Retrieve the records in the input file
        fasta_records = list(infile_handle)

        if len(fasta_records) != 1:
            error_msg = "Input file must contain exactly one FASTA record."
            raise ValueError(error_msg)

        seq_id = fasta_records[0].id
        seq = str(fasta_records[0].seq).upper()

        # Find the FRT sites
        left_match, right_match, orientation = find_frt_sites(
            seq,
            frt_sequence.upper(),
            allowed_errors,
        )

        # extract the internal sequence.
        # Then split the sequence into two parts.
        internal_seq = seq[left_match.end():right_match.start()]

        midpoint = len(internal_seq) // 2
        left_half = internal_seq[:midpoint]
        right_half = internal_seq[midpoint:]

        # Create the new sequence
        circularized_seq = right_half + left_match.group() + left_half

        # Create the new record and write it to the output file
        circularized_record = SeqRecord(
            Seq(circularized_seq),
            id=f"{seq_id}_circularized",
        )

        SeqIO.write(
            circularized_record,
            output_stream,
            "fasta",
        )
