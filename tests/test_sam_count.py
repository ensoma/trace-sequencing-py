"""Test the count_integration_sites function."""

from io import StringIO
from pathlib import Path

import pytest

from isatoolkit2.sam.count import count_integration_sites


@pytest.mark.parametrize(
    "input_sam, expected_output",
    [
        # Single R1 read, + strand
        (
            (
                "@HD\tVN:1.6\tSO:coordinate\n"
                "@SQ\tSN:chr1\tLN:1000\n"
                "read1\t64\tchr1\t100\t60\t5M\t*\t0\t0\tAGCTT\t*\n"
            ),
            "chr1\t99\t99\t.\t1\t+\n",
        ),
        # Single R1 read, - strand
        (
            (
                "@HD\tVN:1.6\tSO:coordinate\n"
                "@SQ\tSN:chr1\tLN:1000\n"
                "read1\t80\tchr1\t100\t60\t5M\t*\t0\t0\tAGCTT\t*\n"
            ),
            "chr1\t103\t103\t.\t1\t-\n",
        ),
        # 2x R1 reads, same position, + strand
        (
            (
                "@HD\tVN:1.6\tSO:coordinate\n"
                "@SQ\tSN:chr1\tLN:1000\n"
                "read1\t64\tchr1\t100\t60\t5M\t*\t0\t0\tAGCTT\t*\n"
                "read2\t64\tchr1\t100\t60\t5M\t*\t0\t0\tAGCTT\t*\n"
            ),
            "chr1\t99\t99\t.\t2\t+\n",
        ),
        # 2x R1 reads, same position, - strand
        (
            (
                "@HD\tVN:1.6\tSO:coordinate\n"
                "@SQ\tSN:chr1\tLN:1000\n"
                "read1\t80\tchr1\t100\t60\t5M\t*\t0\t0\tAGCTT\t*\n"
                "read2\t80\tchr1\t100\t60\t5M\t*\t0\t0\tAGCTT\t*\n"
            ),
            "chr1\t103\t103\t.\t2\t-\n",
        ),
        # 2x R1 reads, same position, different strands
        (
            (
                "@HD\tVN:1.6\tSO:coordinate\n"
                "@SQ\tSN:chr1\tLN:1000\n"
                "read1\t64\tchr1\t100\t60\t5M\t*\t0\t0\tAGCTT\t*\n"
                "read2\t80\tchr1\t100\t60\t5M\t*\t0\t0\tAGCTT\t*\n"
            ),
            "chr1\t99\t99\t.\t1\t+\n"
            "chr1\t103\t103\t.\t1\t-\n",
        ),
        # 2x R1 reads, same position, different chromosomes
        (
            (
                "@HD\tVN:1.6\tSO:coordinate\n"
                "@SQ\tSN:chr1\tLN:1000\n"
                "@SQ\tSN:chr2\tLN:1000\n"
                "read1\t64\tchr1\t100\t60\t5M\t*\t0\t0\tAGCTT\t*\n"
                "read2\t64\tchr2\t100\t60\t5M\t*\t0\t0\tAGCTT\t*\n"
            ),
            "chr1\t99\t99\t.\t1\t+\n"
            "chr2\t99\t99\t.\t1\t+\n",
        ),
        # 1x R2 read, + strand
        (
            (
                "@HD\tVN:1.6\tSO:coordinate\n"
                "@SQ\tSN:chr1\tLN:1000\n"
                "read1\t128\tchr1\t100\t60\t5M\t*\t0\t0\tAGCTT\t*\n"
            ),
            "",
        ),
        # 1x R2 read, - strand
        (
            (
                "@HD\tVN:1.6\tSO:coordinate\n"
                "@SQ\tSN:chr1\tLN:1000\n"
                "read1\t192\tchr1\t100\t60\t5M\t*\t0\t0\tAGCTT\t*\n"
            ),
            "",
        ),
        # 1x R1 read, 1x R2 read, + strand
        (
            (
                "@HD\tVN:1.6\tSO:coordinate\n"
                "@SQ\tSN:chr1\tLN:1000\n"
                "read1\t64\tchr1\t100\t60\t5M\t*\t0\t0\tAGCTT\t*\n"
                "read2\t128\tchr1\t100\t60\t5M\t*\t0\t0\tAGCTT\t*\n"
            ),
            "chr1\t99\t99\t.\t1\t+\n",
        ),
    ],
    ids=[
        "1x R1 read, + strand",
        "1x R1 read, - strand",
        "2x R1 reads, same position, + strand",
        "2x R1 reads, same position, - strand",
        "2x R1 reads, same position, different strands",
        "2x R1 reads, same position, different chromosomes",
        "1x R2 read, + strand",
        "1x R2 read, - strand",
        "1x R1 read, 1x R2 read, + strand",
    ],
)
def test_sam_count(
    input_sam: str,
    expected_output: str,
    tmp_path: Path,
) -> None:
    """Test the count_integration_sites function."""
    # Create a temporary file for the input SAM
    input_sam_path = tmp_path / "input.sam"
    with input_sam_path.open("w") as f:
        f.write(input_sam)

    # Create a temporary file for the output
    output_bed_file = StringIO()

    # Call the function with the temporary files
    count_integration_sites(input_sam_path, output_bed_file)

    # Get the output as a string
    output_bed = output_bed_file.getvalue()

    # Check if the output matches the expected output
    assert output_bed == expected_output
