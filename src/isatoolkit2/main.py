"""CLI for ISAToolkit2."""

from pathlib import Path
from typing import Annotated, Literal

import click
from annotated_types import Ge, Le

from isatoolkit2.sam.fiveprime_filter import fiveprime_filter
from isatoolkit2.sam.mapping_filter import alt_sup_filtering
from isatoolkit2.utils import SamBamInputType, SamBamOutputType
from isatoolkit2.sam.count import count_integration_sites

# Custom click types
SAMBAM_INPUT = SamBamInputType()
SAMBAM_OUTPUT = SamBamOutputType()
DISCARDED_SAMBAM_OUTPUT = SamBamOutputType()

# The bed subcommand group
@click.group()
def bed() -> None:
    """BED file CLI."""

# The sam subcommand group
@click.group()
def sam() -> None:
    """SAM file CLI."""

@sam.command("mapping-filter")
@click.option(
    "-i", "--infile",
    "infile",
    type=SAMBAM_INPUT,
    default="-", show_default=True,
    help="Input SAM/BAM file or stdin (use '-' for stdin)",
)
@click.option(
    "-o", "--outfile",
    "outfile",
    type=SAMBAM_OUTPUT,
    default="-", show_default=True,
    help="Output SAM/BAM file or stdout (use '-' for stdout)",
)
@click.option(
    "--no-alt-filtering",
    "no_alt_filtering",
    is_flag=True,
    type=bool,
    default=False, show_default=True,
    help="Turn off ALT filtering",
)
@click.option(
    "--no-sup-filtering",
    "no_sup_filtering",
    is_flag=True,
    type=bool,
    default=False, show_default=True,
    help="Turn off SUP filtering",
)
@click.option(
    "-f", "--outfile-format",
    "outfile_format",
    type=click.Choice(["sam", "bam"], case_sensitive=False),
    required=True,
    help="Output format (sam or bam)",
)
@click.option(
    "-u", "--uncompressed",
    "uncompressed",
    is_flag=True,
    type=bool,
    default=False, show_default=True,
    help="Output uncompressed BAM file",
)
@click.option(
    "-d", "--discarded-outfile",
    "discarded_outfile",
    type=DISCARDED_SAMBAM_OUTPUT,
    help="Output discarded reads to a separate file",
)
def mapping_filter_cmd(
    infile: Literal["-"] | Path,
    outfile: Literal["-"] | Path,
    outfile_format: Literal["sam", "bam"],
    discarded_outfile: None | Path = None,
    *,
    no_alt_filtering: bool = False,
    no_sup_filtering: bool = False,
    uncompressed: bool = False,
) -> None:
    """Filter SAM/BAM file."""
    alt_sup_filtering(
        infile=infile,
        outfile=outfile,
        filter_alt=not no_alt_filtering,
        filter_sup=not no_sup_filtering,
        output_format=outfile_format,
        uncompressed=uncompressed,
        discarded_outfile=discarded_outfile,
    )

@sam.command("fiveprime-filter")
@click.option(
    "-i", "--infile",
    "infile",
    type=SAMBAM_INPUT,
    default="-", show_default=True,
    help="Input SAM/BAM file or stdin (use '-' for stdin)",
)
@click.option(
    "-o", "--outfile",
    "outfile",
    type=SAMBAM_OUTPUT,
    default="-", show_default=True,
    help="Output SAM/BAM file or stdout (use '-' for stdout)",
)
@click.option(
    "-f", "--outfile-format",
    "outfile_format",
    type=click.Choice(["sam", "bam"], case_sensitive=False),
    required=True,
    help="Output format (sam or bam)",
)
@click.option(
    "-u", "--uncompressed",
    "uncompressed",
    is_flag=True,
    type=bool,
    default=False, show_default=True,
    help="Output uncompressed BAM file",
)
@click.option(
    "-d", "--discarded-outfile",
    "discarded_outfile",
    type=DISCARDED_SAMBAM_OUTPUT,
    help="Output discarded reads to a separate file",
)
@click.option(
    "-m", "--max-softclip",
    "max_softclip",
    type=int,
    default=5, show_default=True,
    help="Maximum softclip length",
)
def fiveprime_filter_cmd(
    infile: Literal["-"] | Path,
    outfile: Literal["-"] | Path,
    outfile_format: Literal["sam", "bam"],
    max_softclip: Annotated[int, Ge(1), Le(100)] = 5,
    discarded_outfile: None | Path = None,
    *,
    uncompressed: bool = False,
) -> None:
    """Filter SAM/BAM file based on 5' softclipping."""
    fiveprime_filter(
        infile=infile,
        outfile=outfile,
        max_softclip=max_softclip,
        outfile_format=outfile_format,
        uncompressed=uncompressed,
        discarded_outfile=discarded_outfile,
    )

@sam.command("count")
@click.option(
    "-i", "--infile",
    "infile",
    type=SAMBAM_INPUT,
    default="-", show_default=True,
    help="Input SAM/BAM file or stdin (use '-' for stdin)",
)
@click.option(
    "-o", "--outfile",
    "outfile",
    type=click.File("w"),
    default="-", show_default=True,
    help="Output BED file or stdout (use '-' for stdout)",
)
def count_cmd(
    infile: Literal["-"] | Path,
    outfile: Literal["-"] | Path,
) -> None:
    """Count integration sites in a SAM/BAM file."""

    count_integration_sites(
        infile=infile,
        outfile=outfile,
    )

# The CLI entry point
@click.group()
def cli() -> None:
    """ISA Toolkit 2 - Tools for processing sequencing data."""

# Add the subcommands to the main CLI group
cli.add_command(sam)
cli.add_command(bed)

if __name__ == "__main__":
    # Run the CLI
    cli()
