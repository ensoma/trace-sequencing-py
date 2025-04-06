"""Test sorting of BED files."""

from io import StringIO

import pytest

from isatoolkit2.bed.sort import sort_bed


@pytest.mark.parametrize(
    "input_bed, expected_output",
    [
        # No sorting
        (
            (
                "chr1\t100\t100\t.\t1\t+\n"
                "chr1\t101\t101\t.\t1\t+\n"
            ),
            (
                "chr1\t100\t100\t.\t1\t+\n"
                "chr1\t101\t101\t.\t1\t+\n"
            ),
        ),
        # Position sorting only
        (
            (
                "chr1\t101\t101\t.\t1\t+\n"
                "chr1\t100\t100\t.\t1\t+\n"
            ),
            (
                "chr1\t100\t100\t.\t1\t+\n"
                "chr1\t101\t101\t.\t1\t+\n"
            ),
        ),
        # Chromosome sorting only
        (
            (
                "chr2\t100\t100\t.\t1\t+\n"
                "chr1\t100\t100\t.\t1\t+\n"
            ),
            (
                "chr1\t100\t100\t.\t1\t+\n"
                "chr2\t100\t100\t.\t1\t+\n"
            ),
        ),
        # Strand sorting only
        (
            (
                "chr1\t100\t100\t.\t1\t-\n"
                "chr1\t100\t100\t.\t1\t+\n"
            ),
            (
                "chr1\t100\t100\t.\t1\t+\n"
                "chr1\t100\t100\t.\t1\t-\n"
            ),
        ),
        # Chromosome, position, and strand sorting
        (
            (
                "chr2\t101\t101\t.\t1\t+\n"
                "chr2\t100\t100\t.\t1\t-\n"
                "chr2\t100\t100\t.\t1\t+\n"
                "chr1\t101\t101\t.\t1\t+\n"
                "chr1\t100\t100\t.\t1\t+\n"
            ),
            (
                "chr1\t100\t100\t.\t1\t+\n"
                "chr1\t101\t101\t.\t1\t+\n"
                "chr2\t100\t100\t.\t1\t+\n"
                "chr2\t100\t100\t.\t1\t-\n"
                "chr2\t101\t101\t.\t1\t+\n"
            ),
        ),
    ],
    ids=[
        "no sorting",
        "position sorting only",
        "chromosome sorting only",
        "strand sorting only",
        "chromosome, position, and strand sorting",
    ],
)
def test_valid_position_sorting(
    input_bed: str,
    expected_output: str,
) -> None:
    """Test that the bed file is sorted correctly."""
    # Create StringIO objects for the input anbd output.
    input_bed_file = StringIO(input_bed)
    output_bed_file = StringIO()

    # Call the sort_bed function with the StringIO objects
    # And capture the output
    sort_bed(input_bed_file, output_bed_file)
    output_bed = output_bed_file.getvalue()

    # Assert that the output matches the expected output
    assert output_bed == expected_output

@pytest.mark.parametrize(
    "input_bed, expected_output",
    [
        # No sorting
        (
            (
                "chr1\t100\t100\t.\t1\t+\n"
                "chr1\t101\t101\t.\t1\t+\n"
            ),
            (
                "chr1\t100\t100\t.\t1\t+\n"
                "chr1\t101\t101\t.\t1\t+\n"
            ),
        ),
        # Score sorting same chromosome
        (
            (
                "chr1\t101\t101\t.\t1\t+\n"
                "chr1\t100\t100\t.\t2\t+\n"
            ),
            (
                "chr1\t100\t100\t.\t2\t+\n"
                "chr1\t101\t101\t.\t1\t+\n"
            ),
        ),
        # Score sorting different chromosomes same position
        (
            (
                "chr1\t100\t100\t.\t1\t+\n"
                "chr2\t100\t100\t.\t2\t+\n"
            ),
            (
                "chr2\t100\t100\t.\t2\t+\n"
                "chr1\t100\t100\t.\t1\t+\n"
            ),
        ),
        # Score sorting different chromosomes different position
        (
            (
                "chr1\t100\t100\t.\t1\t+\n"
                "chr2\t101\t101\t.\t2\t+\n"
            ),
            (
                "chr2\t101\t101\t.\t2\t+\n"
                "chr1\t100\t100\t.\t1\t+\n"
            ),
        ),
    ],
    ids=[
        "no sorting",
        "score sorting same chromosome",
        "score sorting different chromosomes same position",
        "score sorting different chromosomes different position",
    ],
)
def test_valid_score_sorting(
    input_bed: str,
    expected_output: str,
) -> None:
    """Test that the bed file is sorted correctly."""
    # Create StringIO objects for the input and output.
    input_bed_file = StringIO(input_bed)
    output_bed_file = StringIO()

    # Call the sort_bed function with the StringIO objects
    # And capture the output
    sort_bed(input_bed_file, output_bed_file, sort_by="score")
    output_bed = output_bed_file.getvalue()

    # Assert that the output matches the expected output
    assert output_bed == expected_output

@pytest.mark.parametrize(
    "input_bed, error_type, error_msg",
    [
        # Missing last column
        (
            "chr1\t100\t100\t.\t1\n",
            ValueError,
            "Invalid BED line format.",
        ),
    ],
    ids=[
        "missing last column",
    ],
)
def test_invalid_bed_file(
    input_bed: str,
    error_type: type[ValueError],
    error_msg: str,
) -> None:
    """Test that the bed file is sorted correctly."""
    # Create StringIO objects for the input and output.
    input_bed_file = StringIO(input_bed)
    output_bed_file = StringIO()

    # Call the sort_bed function with the StringIO objects
    # And capture the output
    with pytest.raises(error_type, match=error_msg):
        sort_bed(input_bed_file, output_bed_file)
