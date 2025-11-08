"""Test the bed_merge function."""

from io import StringIO

import pytest

from isatoolkit2.bed.merge import merge_integration_sites


@pytest.mark.parametrize(
    "input_bed, expected_output",
    [
        # No merging needed - distance too far
        (
            ("chr1\t100\t100\t.\t1\t+\nchr1\t200\t200\t.\t1\t+\n"),
            ("chr1\t100\t100\t.\t1\t+\nchr1\t200\t200\t.\t1\t+\n"),
        ),
        # No merging needed - different chromosomes
        (
            ("chr1\t100\t100\t.\t1\t+\nchr2\t100\t100\t.\t1\t+\n"),
            ("chr1\t100\t100\t.\t1\t+\nchr2\t100\t100\t.\t1\t+\n"),
        ),
        # No merging needed - different strands
        (
            ("chr1\t100\t100\t.\t1\t+\nchr1\t100\t100\t.\t1\t-\n"),
            ("chr1\t100\t100\t.\t1\t+\nchr1\t100\t100\t.\t1\t-\n"),
        ),
        # Merge entries - distance of 1
        (
            ("chr1\t100\t100\t.\t1\t+\nchr1\t101\t101\t.\t2\t+\n"),
            ("chr1\t101\t101\t.\t3\t+\n"),
        ),
        # Merge entries - distance of 5
        (
            ("chr1\t100\t100\t.\t1\t+\nchr1\t105\t105\t.\t2\t+\n"),
            ("chr1\t105\t105\t.\t3\t+\n"),
        ),
        # Don't merge entries - distance of 6
        (
            ("chr1\t100\t100\t.\t1\t+\nchr1\t106\t106\t.\t1\t+\n"),
            ("chr1\t100\t100\t.\t1\t+\nchr1\t106\t106\t.\t1\t+\n"),
        ),
        # Merge 3 entries
        (
            (
                "chr1\t100\t100\t.\t1\t+\n"
                "chr1\t101\t101\t.\t2\t+\n"
                "chr1\t102\t102\t.\t3\t+\n"
            ),
            ("chr1\t102\t102\t.\t6\t+\n"),
        ),
        # Merge two entries with median position
        (
            ("chr1\t100\t100\t.\t1\t+\nchr1\t102\t102\t.\t1\t+\n"),
            ("chr1\t101\t101\t.\t2\t+\n"),
        ),
        # Merge three entries with median position
        (
            (
                "chr1\t100\t100\t.\t1\t+\n"
                "chr1\t103\t103\t.\t1\t+\n"
                "chr1\t104\t104\t.\t1\t+\n"
            ),
            ("chr1\t103\t103\t.\t3\t+\n"),
        ),
    ],
    ids=[
        "no merge, too far",
        "no merge, different chromosome",
        "no merge, different strand",
        "merge, distance of 1",
        "merge, distance of 5",
        "no merge, distance of 6",
        "merge 3 entries",
        "merge, 2 entries median position",
        "merge, 3 entries median position",
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
