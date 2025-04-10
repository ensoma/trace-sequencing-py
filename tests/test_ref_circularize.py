
import pytest

from io import StringIO
from isatoolkit2.ref.circularize import circularize_integration_vector

@pytest.mark.parametrize(
    "input, expected_output, frt_seq, allowed_errors",
    [
        # 2 matches, forward orientation
        (
            ">seq1\nTTTTTTCCTAAAACCTGGGGG\n",
            ">seq1_circularized FRT_site_orientation: forward\nAACCTAA\n",
            "CCT",
            0,
        ),
        # 2 matches, revcomp orientation
        (
            ">seq1\nTTTTTTCCTAAAACCTGGGGG\n",
            ">seq1_circularized FRT_site_orientation: revcomp\nAACCTAA\n",
            "AGG",
            0,
        ),
    ],
    ids=[
        "2 matches, forward orientation",
        "2 matches, revcomp orientation",
    ],
)
def test_valid_circularization(
    input: str,
    expected_output: str,
    frt_seq: str,
    allowed_errors: int,
) -> None:
    """Test circularization of integration vector."""
    # Prepare the input handle
    infile = StringIO(input)
    outfile = StringIO()

    # Call the function to test
    circularize_integration_vector(
        infile=infile,
        outfile=outfile,
        frt_sequence=frt_seq,
        allowed_errors=allowed_errors,
    )

    # Check if the output is as expected
    observed_output = outfile.getvalue()

    assert observed_output == expected_output

@pytest.mark.parametrize(
    "input, expected_error, frt_seq, allowed_errors",
    [
        # No matches
        (
            ">seq1\nTTTTTTCCTAAAACCTGGGGG\n",
            "Expected 2 FRT sites",
            "CCC",
            0,
        ),
        # 1 match, forward orientation
        (
            ">seq1\nTTTTTTCCTAAAACCCGGGGG\n",
            "Expected 2 FRT sites",
            "CCT",
            0,
        ),
        # 3 matches, forward orientation
        (
            ">seq1\nTTTTTTCCTAAAACCTGGGGGCCT\n",
            "Expected 2 FRT sites",
            "CCT",
            0,
        ),
        # 1 match, revcomp orientation
        (
            ">seq1\nTTTTTTCCTAAAACCCGGGGG\n",
            "Expected 2 FRT sites",
            "AGG",
            0,
        ),
        # 3 matches, revcomp orientation
        (
            ">seq1\nTTTTTTCCTAAAACCTGGGGGCCT\n",
            "Expected 2 FRT sites",
            "AGG",
            0,
        ),
        # 1 match forward, 1 match revcomp
        (
            ">seq1\nTTTTTTCCTAAAAAGGGGGGG\n",
            "Expected 2 FRT sites",
            "CCT",
            0,
        ),
    ],
    ids=[
        "No matches",
        "1 match, forward orientation",
        "3 matches, forward orientation",
        "1 match, revcomp orientation",
        "3 maches, revcomp orientation",
        "1 match forward, 1 match revcomp",
    ],
)
def test_invalid_circularization(
    input: str,
    expected_error: str,
    frt_seq: str,
    allowed_errors: int,
) -> None:
    """Test circularization of integration vector with invalid cases."""
    # Prepare the input handle
    infile = StringIO(input)
    outfile = StringIO()

    # Check if the ValueError is raised
    with pytest.raises(ValueError, match=expected_error):
        circularize_integration_vector(
            infile=infile,
            outfile=outfile,
            frt_sequence=frt_seq,
            allowed_errors=allowed_errors,
        )