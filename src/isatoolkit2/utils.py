"""Utility functions for ISAToolkit2 CLI."""

from pathlib import Path
from typing import Literal

import click
from pydantic import BaseModel, FilePath, NewPath, ValidationError, field_validator


# SAM/BAM inputs
class SamBamInputSchema(BaseModel):

    """SAM/BAM file schema."""

    input: Literal["-"] | FilePath

    @field_validator("input", mode="after")
    def check_input(
        cls, value: Literal["-"] | Path,
    ) -> Literal["-"] | Path:
        """Check if the file is a SAM/BAM file."""
        if (
            isinstance(value, Path) and
            value.suffix.lower() not in [".sam", ".bam"]
        ):
                error_msg = f"File {value} is not a SAM/BAM file"
                raise ValueError(error_msg)
        return value

class SamBamInputType(click.ParamType):

    """SAM/BAM file type."""

    name = "sam/bam"

    def convert(
        self,
        value: Literal["-"] | Path,
        param: click.Parameter | None,
        ctx: click.Context | None,
    ) -> Literal["-"] | Path:
        """Check if the file is a SAM/BAM file."""
        try:
            SamBamInputSchema(input=value)
        except ValidationError as e:
            self.fail(f"Invalid input: {e}", param, ctx)
        else:
            return value

# SAM/BAM outputs
class SamBamOutputSchema(BaseModel):

    """SAM/BAM file schema."""

    output: Literal["-"] | FilePath | NewPath

    @field_validator("output", mode="after")
    def check_output(
        cls, value: Literal["-"] | Path,
    ) -> Literal["-"] | Path:
        """Check if the file is a SAM/BAM file."""
        if (
            isinstance(value, Path) and
            value.suffix.lower() not in [".sam", ".bam"]
        ):
            error_msg = f"File {value} is not a SAM/BAM file"
            raise ValueError(error_msg)
        return value

class SamBamOutputType(click.ParamType):

    """SAM/BAM file type."""

    name = "sam/bam"

    def convert(
        self,
        value: Literal["-"] | Path,
        param: click.Parameter | None,
        ctx: click.Context | None,
    ) -> Literal["-"] | Path:
        """Check if the file is a SAM/BAM file."""
        try:
            SamBamOutputSchema(output=value)
        except ValidationError as e:
            self.fail(f"Invalid output: {e}", param, ctx)
        else:
            return value

# SAM/BAM discarded output
class SamBamDiscardedOutputSchema(BaseModel):

    """SAM/BAM discarded output file schema."""

    discarded_output: Literal["-"] | FilePath | NewPath

    @field_validator("discarded_output", mode="after")
    def check_discarded_output(
        cls, value: Literal["-"] | Path,
    ) -> Literal["-"] | Path:
        """Check if the file is a SAM/BAM file."""
        if (
            isinstance(value, Path) and
            value.suffix.lower() not in [".sam", ".bam"]
        ):
            error_msg = f"File {value} is not a SAM/BAM file"
            raise ValueError(error_msg)
        return value

class SamBamDiscardedOutputType(click.ParamType):

    """SAM/BAM discarded output file type."""

    name = "sam/bam"

    def convert(
        self,
        value: Literal["-"] | Path,
        param: click.Parameter | None,
        ctx: click.Context | None,
    ) -> Literal["-"] | Path:
        """Check if the file is a SAM/BAM file."""
        try:
            SamBamDiscardedOutputSchema(discarded_output=value)
        except ValidationError as e:
            self.fail(f"Invalid discarded output: {e}", param, ctx)
        else:
            return value

# FASTA inputs
class FastaInputSchema(BaseModel):

    """FASTA file schema."""

    input: Literal["-"] | FilePath

    @field_validator("input", mode="after")
    def check_input(
        cls, value: Literal["-"] | Path,
    ) -> Literal["-"] | Path:
        """Check if the file is a FASTA file."""
        if (
            isinstance(value, Path) and
            value.suffix.lower() not in [
                ".fasta", ".fa", ".fa.gz", ".fasta.gz",
            ]
        ):
            error_msg = f"File {value} is not a FASTA file"
            raise ValueError(error_msg)
        return value

class FastaInputType(click.ParamType):

    """FASTA file type."""

    name = "fasta"

    def convert(
        self,
        value: Literal["-"] | Path,
        param: click.Parameter | None,
        ctx: click.Context | None,
    ) -> Literal["-"] | Path:
        """Check if the input file is a FASTA file."""
        try:
            FastaInputSchema(input=value)
        except ValidationError as e:
            self.fail(f"Invalid input: {e}", param, ctx)
        else:
            return value

# FASTA outputs
class FastaOutputSchema(BaseModel):

    """FASTA output file schema."""

    output: Literal["-"] | FilePath | NewPath

    @field_validator("output", mode="after")
    def check_fasta_output(
        cls, value: Literal["-"] | Path,
    ) -> Literal["-"] | Path:
        """Check if the output file is a FASTA file."""
        if (
            isinstance(value, Path) and
            value.suffix.lower() not in [
                ".fasta", ".fa", ".fa.gz", ".fasta.gz",
            ]
        ):
            error_msg = f"File {value} is not a FASTA file"
            raise ValueError(error_msg)
        return value

class FastaOutputType(click.ParamType):

    """FASTA output file type."""

    name = "fasta"

    def convert(
        self,
        value: Literal["-"] | Path,
        param: click.Parameter | None,
        ctx: click.Context | None,
    ) -> Literal["-"] | Path:
        """Check if the output file is a FASTA file."""
        try:
            FastaOutputSchema(output=value)
        except ValidationError as e:
            self.fail(f"Invalid output: {e}", param, ctx)
        else:
            return value
