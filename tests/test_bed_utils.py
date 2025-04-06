"""Bed utils tests."""

import pytest

from isatoolkit2.bed.bed_utils import natural_key


@pytest.mark.parametrize(
    "input_str, expected_output",
    [
        ("a", ["a"]),
        ("a1", ["a", 1]),
        ("a10", ["a", 10]),
        ("a2", ["a", 2]),
        ("a1b", ["a", 1, "b"]),
        ("a1.5", ["a", 1, ".", 5]),
    ],
    ids=[
        "single_char",
        "single_char_digit",
        "single_char_digit_10",
        "single_char_digit_2",
        "single_char_digit_1b",
        "single_char_digit_float",
    ],
)
def test_natural_key(
    input_str: str,
    expected_output: list[str | int | float],
) -> None:
    """Test the natural_key function with various input strings."""
    result = natural_key(input_str)
    assert result == expected_output
