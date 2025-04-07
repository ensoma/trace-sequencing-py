
import pytest

from pathlib import Path
from isatoolkit2.sam.fiveprime_filter import fiveprime_filter

@pytest.mark.parametrize(
    "input_data, expected_output",
    [
        # Single R1 read, + strand, no filtering
        (
            (
                "@HD\tVN:1.6\tSO:coordinate\n"
                "@SQ\tSN:chr1\tLN:1000\n"
                "read1\t64\tchr1\t100\t60\t10M\t*\t0\t0\tAGCTTCCTAT\t*\n"
            ),
            (
                "@HD\tVN:1.6\tSO:coordinate\n"
                "@SQ\tSN:chr1\tLN:1000\n"
                "read1\t64\tchr1\t100\t60\t10M\t*\t0\t0\tAGCTTCCTAT\t*\n"
            ),
        ),
        # Single R1 read, - strand, no filtering
        (
            (
                "@HD\tVN:1.6\tSO:coordinate\n"
                "@SQ\tSN:chr1\tLN:1000\n"
                "read2\t128\tchr1\t200\t60\t10M\t*\t0\t0\tAGCTTCCTAT\t*\n"
            ),
            (
                "@HD\tVN:1.6\tSO:coordinate\n"
                "@SQ\tSN:chr1\tLN:1000\n"
                "read2\t128\tchr1\t200\t60\t10M\t*\t0\t0\tAGCTTCCTAT\t*\n"
            ),
        ),
    ],
    ids=[
        "Single R1 read, + strand, no filtering",
        "Single R1 read, - strand, no filtering",
    ],
)
def test_fiveprime_filter(
    input_data: str,
    expected_output: str,
    tmp_path: Path,
) -> None:
    """Test the fiveprime_filter function with various inputs."""
    # Create a temporary file to store the input data
    input_file = tmp_path / "input.sam"
    with input_file.open("w") as f:
        f.write(input_data)

    # Create a temporary file to store the output data
    output_file = tmp_path / "output.sam"

    # Run the fiveprime_filter function
    fiveprime_filter(
        input_file, output_file, outfile_format="sam"
    )

    # Read the output file and check its contents
    with output_file.open() as f:
        output_data = f.read()

    assert output_data == expected_output