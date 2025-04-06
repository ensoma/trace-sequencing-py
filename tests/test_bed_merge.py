"""Test the bed_merge function."""

from io import StringIO

import pytest

from isatoolkit2.bed.merge import merge_integration_sites


@pytest.mark.parametrize(
    "input_bed, expected_output",
    [
        # No merging needed
        (
            (
                "chr1\t100\t100\t.\t1\t+\n"
                "chr1\t200\t200\t.\t1\t+\n"
            ),
            (
                "chr1\t100\t100\t.\t1\t+\n"
                "chr1\t200\t200\t.\t1\t+\n"
            ),
        ),
    ],
    ids=[
        "no_merge",
    ],
)
def test_merge_bed(
    input_bed: str,
    expected_output: str,
) -> None:
    """Test the bed_merge function with various input scenarios."""
    # Convert input strings to list of lines
    input_bed_file = StringIO(input_bed)
    output_bed_file = StringIO()

    # Call the bed_merge function
    merge_integration_sites(input_bed_file, output_bed_file)
    output_bed = output_bed_file.getvalue()

    # Assert that the output matches the expected output
    assert output_bed == expected_output
