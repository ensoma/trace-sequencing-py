"""Utility functions for BED file processing."""

import re
from enum import Enum
from typing import Annotated

from annotated_types import Ge, MinLen
from pydantic import BaseModel, ConfigDict


def natural_key(string: str) -> list[str | int]:
    """Generate a key for natural sorting."""
    # Split the string into alternating non-digit and digit parts,
    # adn filter out empty strings.
    return [
        int(s) if s.isdigit()
        else s.lower() for s in re.split(r"(\d+)", string)
        if s
    ]

class Strand(Enum):

    """Strand enumeration."""

    PLUS = "+"
    MINUS = "-"

class BedLine(BaseModel):

    """Dataclass for BED line."""

    seqname: Annotated[str, MinLen(1)]
    start: Annotated[int, Ge(0)]
    end: Annotated[int, Ge(0)]
    name: Annotated[str, MinLen(1)]
    score: Annotated[int, Ge(1)]
    strand: Strand

    model_config = ConfigDict(
        use_enum_values = True,
    )
