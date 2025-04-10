"""CLI for ISAToolkit2."""

from pathlib import Path
from typing import Annotated, Literal, TextIO

import click
from annotated_types import Ge, Le

from isatoolkit2.utils import FastaInputType, SamBamInputType, SamBamOutputType

# Custom click types
SAMBAM_INPUT = SamBamInputType()
SAMBAM_OUTPUT = SamBamOutputType()
DISCARDED_SAMBAM_OUTPUT = SamBamOutputType()
FASTA_INPUT = FastaInputType()
FASTA_OUTPUT = FastaInputType()

# The ref subcommand group
@click.group()
def ref() -> None:
    """Initialize reference file CLI."""

@ref.command("circularize")
@click.option(
    "-i", "--infile",
    "infile",
    type=FASTA_INPUT,
    default="-", show_default=True,
    help="Input reference file or stdin (use '-' for stdin)",
)
@click.option(
    "-o", "--outfile",
    "outfile",
    type=FASTA_OUTPUT,
    default="-", show_default=True,
    help="Output reference file or stdout (use '-' for stdout)",
)
@click.option(
    "-f", "--frt-sequence",
    "frt_sequence",
    type=str,
    default="GAAGTTCCTATTCCGAAGTTCCTATTCTCTAGAAAGTATAGGAACTTC",
    show_default=True,
    help="FRT sequence to add to the reference",
)
@click.option(
    "-e", "--allowed-errors",
    "allowed_errors",
    type=int,
    default=0, show_default=True,
    help="Allowed errors in the FRT sequence",
)
def circularize_cmd(
    infile: Literal["-"] | Path,
    outfile: Literal["-"] | Path,
    frt_sequence: str = "GAAGTTCCTATTCCGAAGTTCCTATTCTCTAGAAAGTATAGGAACTTC",
    allowed_errors: Annotated[int, Ge(0), Le(10)] = 0,
) -> None:
    """Circularize a reference FASTA file."""
    from isatoolkit2.ref.circularize import circularize_integration_vector
    circularize_integration_vector(
        infile=infile,
        outfile=outfile,
        frt_sequence=frt_sequence,
        allowed_errors=allowed_errors,
    )

# The bed subcommand group
@click.group()
def bed() -> None:
    """BED file CLI."""

@bed.command("sort")
@click.option(
    "-i", "--infile",
    "infile",
    type=click.File("r"),
    default="-", show_default=True,
    help="Input BED file or stdin (use '-' for stdin)",
)
@click.option(
    "-o", "--outfile",
    "outfile",
    type=click.File("w"),
    default="-", show_default=True,
    help="Output BED file or stdout (use '-' for stdout)",
)
@click.option(
    "-s", "--sort-by",
    "sort_by",
    type=click.Choice(["position", "score"], case_sensitive=False),
    default="position", show_default=True,
    help="Sort by position or score",
)
def sort_cmd(
    infile: click.utils.LazyFile | TextIO,
    outfile: click.utils.LazyFile | TextIO,
    sort_by: Literal["position", "score"],
) -> None:
    """Sort BED file by position or score."""
    from isatoolkit2.bed.sort import sort_bed
    sort_bed(
        infile=infile,
        outfile=outfile,
        sort_by=sort_by,
    )

@bed.command("merge")
@click.option(
    "-i", "--infile",
    "infile",
    type=click.File("r"),
    default="-", show_default=True,
    help="Input BED file or stdin (use '-' for stdin)",
)
@click.option(
    "-o", "--outfile",
    "outfile",
    type=click.File("w"),
    default="-", show_default=True,
    help="Output BED file or stdout (use '-' for stdout)",
)
@click.option(
    "-d", "--distance",
    "distance",
    type=int,
    default=5, show_default=True,
    help="Distance to merge proximal integration sites",
)
@click.option(
    "-m", "--mode",
    "mode",
    type=click.Choice(["median"], case_sensitive=False),
    default="median", show_default=True,
    help=(
        "Mode for merging integration sites "
        "(currently only median supported)"
    ),
)
def merge_cmd(
    infile: click.utils.LazyFile | TextIO,
    outfile: click.utils.LazyFile | TextIO,
    distance: Annotated[int, Ge(0), Le(100)] = 5,
    mode: Literal["median"] = "median",
) -> None:
    """Merge proximal integration sites in a BED file."""
    from isatoolkit2.bed.merge import merge_integration_sites
    merge_integration_sites(
        infile=infile,
        outfile=outfile,
        distance=distance,
        mode=mode,
    )

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
    from isatoolkit2.sam.mapping_filter import alt_sup_filtering
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
    from isatoolkit2.sam.fiveprime_filter import fiveprime_filter
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
    outfile: click.utils.LazyFile | TextIO,
) -> None:
    """Count integration sites in a SAM/BAM file."""
    from isatoolkit2.sam.count import count_integration_sites
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
cli.add_command(ref)

if __name__ == "__main__":
    # Run the CLI
    cli()
