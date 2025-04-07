"""Test the sam_mapping_filter module."""

from pathlib import Path

import pytest

from isatoolkit2.sam.mapping_filter import alt_sup_filtering

SAM_HEADER = (
    "@HD\tVN:1.6\tSO:coordinate\n"
    "@SQ\tSN:chr1\tLN:1000\n"
)

@pytest.mark.parametrize(
    "input_data, expected_output",
    [
        # Single R1 read, + strand, no filtering
        (
            (
                f"{SAM_HEADER}"
                "read1\t64\tchr1\t100\t60\t5M\t*\t0\t0\t*\t*\n"
            ),
            (
                f"{SAM_HEADER}"
                "read1\t64\tchr1\t100\t60\t5M\t*\t0\t0\t*\t*\n"
            ),
        ),
        # Single R2 read, + strand, no filtering
        (
            (
                f"{SAM_HEADER}"
                "read1\t128\tchr1\t100\t60\t5M\t*\t0\t0\t*\t*\n"
            ),
            (
                f"{SAM_HEADER}"
                "read1\t128\tchr1\t100\t60\t5M\t*\t0\t0\t*\t*\n"
            ),
        ),
        # Single R1 read, - strand, no filtering
        (
            (
                f"{SAM_HEADER}"
                "read1\t80\tchr1\t100\t60\t5M\t*\t0\t0\t*\t*\n"
            ),
            (
                f"{SAM_HEADER}"
                "read1\t80\tchr1\t100\t60\t5M\t*\t0\t0\t*\t*\n"
            ),
        ),
        # Single R2 read, - strand, no filtering
        (
            (
                f"{SAM_HEADER}"
                "read1\t144\tchr1\t100\t60\t5M\t*\t0\t0\t*\t*\n"
            ),
            (
                f"{SAM_HEADER}"
                "read1\t144\tchr1\t100\t60\t5M\t*\t0\t0\t*\t*\n"
            ),
        ),
        # Single R1 read, + strand, filter supplemental
        (
            (
                f"{SAM_HEADER}"
                "read1\t64\tchr1\t100\t60\t5M\t*\t0\t0\t*\t*\tSA:Z:*\n"
            ),
            SAM_HEADER,
        ),
        # Single R2 read, + strand, filter supplemental
        (
            (
                f"{SAM_HEADER}"
                "read1\t128\tchr1\t100\t60\t5M\t*\t0\t0\t*\t*\tSA:Z:*\n"
            ),
            SAM_HEADER,
        ),
        # Single R1 read, - strand, filter supplemental
        (
            (
                f"{SAM_HEADER}"
                "read1\t80\tchr1\t100\t60\t5M\t*\t0\t0\t*\t*\tSA:Z:*\n"
            ),
            SAM_HEADER,
        ),
        # Single R2 read, - strand, filter supplemental
        (
            (
                f"{SAM_HEADER}"
                "read1\t144\tchr1\t100\t60\t5M\t*\t0\t0\t*\t*\tSA:Z:*\n"
            ),
            SAM_HEADER,
        ),
        # Single R1 read, + strand, filter alternate
        (
            (
                f"{SAM_HEADER}"
                "read1\t64\tchr1\t100\t60\t5M\t*\t0\t0\t*\t*\tXA:Z:*\n"
            ),
            SAM_HEADER,
        ),
        # Single R2 read, + strand, filter alternate
        (
            (
                f"{SAM_HEADER}"
                "read1\t128\tchr1\t100\t60\t5M\t*\t0\t0\t*\t*\tXA:Z:*\n"
            ),
            SAM_HEADER,
        ),
        # Single R1 read, - strand, filter alternate
        (
            (
                f"{SAM_HEADER}"
                "read1\t80\tchr1\t100\t60\t5M\t*\t0\t0\t*\t*\tXA:Z:*\n"
            ),
            SAM_HEADER,
        ),
        # Single R2 read, - strand, filter alternate
        (
            (
                f"{SAM_HEADER}"
                "read1\t144\tchr1\t100\t60\t5M\t*\t0\t0\t*\t*\tXA:Z:*\n"
            ),
            SAM_HEADER,
        ),
        # Single R1 read, + strand, filter alternate and supplemental
        (
            (
                f"{SAM_HEADER}"
                "read1\t64\tchr1\t100\t60\t5M\t*\t0\t0\t*\t*\tXA:Z:*\tSA:Z:*\n"
            ),
            SAM_HEADER,
        ),
        # Single R2 read, + strand, filter alternate and supplemental
        (
            (
                f"{SAM_HEADER}"
                "read1\t128\tchr1\t100\t60\t5M\t*\t0\t0\t*\t*\tXA:Z:*\tSA:Z:*\n"
            ),
            SAM_HEADER,
        ),
        # Single R1 read, - strand, filter alternate and supplemental
        (
            (
                f"{SAM_HEADER}"
                "read1\t80\tchr1\t100\t60\t5M\t*\t0\t0\t*\t*\tXA:Z:*\tSA:Z:*\n"
            ),
            SAM_HEADER,
        ),
        # Single R2 read, - strand, filter alternate and supplemental
        (
            (
                f"{SAM_HEADER}"
                "read1\t144\tchr1\t100\t60\t5M\t*\t0\t0\t*\t*\tXA:Z:*\tSA:Z:*\n"
            ),
            SAM_HEADER,
        ),
    ],
    ids=[
        "single R1 read, + strand, no filtering",
        "single R2 read, + strand, no filtering",
        "single R1 read, - strand, no filtering",
        "single R2 read, - strand, no filtering",
        "single R1 read, + strand, filter sup",
        "single R2 read, + strand, filter sup",
        "single R1 read, - strand, filter sup",
        "single R2 read, - strand, filter sup",
        "single R1 read, + strand, filter alt",
        "single R2 read, + strand, filter alt",
        "single R1 read, - strand, filter alt",
        "single R2 read, - strand, filter alt",
        "single R1 read, + strand, filter alt sup",
        "single R2 read, + strand, filter alt sup",
        "single R1 read, - strand, filter alt sup",
        "single R2 read, - strand, filter alt sup",
    ],
)
def test_alt_sup_filtering(
    input_data: str,
    expected_output: str,
    tmp_path: Path,
) -> None:
    """Test the alt_sup_filtering function."""
    # Create a temporary file to store the input data
    input_file = tmp_path / "input.sam"
    with input_file.open("w") as f:
        f.write(input_data)

    # Create a temporary file to store the output data
    output_file = tmp_path / "output.sam"

    # Run the fiveprime_filter function
    alt_sup_filtering(
        input_file, output_file, output_format="sam",
    )

    # Read the output file and check its contents
    with output_file.open() as f:
        output_data = f.read()

    assert output_data == expected_output
