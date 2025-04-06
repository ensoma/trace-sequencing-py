"""Merge proximal integration sites."""

from collections import deque
from itertools import groupby
from typing import Annotated, Literal, TextIO

import click
from annotated_types import Ge, Le

from isatoolkit2.bed.bed_utils import BedLine, Strand, natural_key

MIN_BED_COLS = 6

def read_lines(
    infile: click.utils.LazyFile | TextIO,
) -> list[BedLine]:
    """Read lines from a BED file."""
    lines = []
    for line in infile:
        # Skip empty lines or comment lines
        stripped_line = line.strip()
        if not stripped_line or stripped_line.startswith("#"):
            continue

        split_line = stripped_line.split("\t")
        # Check if line has the expected format
        if len(split_line) >= MIN_BED_COLS:
            lines.append(
                BedLine(
                    seqname=str(split_line[0]),
                    start=int(split_line[1]),
                    end=int(split_line[2]),
                    name=str(split_line[3]),
                    score=int(split_line[4]),
                    strand=Strand(split_line[5]),
                ),
            )
    return lines

def merge_integration_sites(
    infile: click.utils.LazyFile | TextIO,
    outfile: click.utils.LazyFile | TextIO,
    distance: Annotated[int, Ge(0), Le(100)] = 5,
    mode: Literal["median"] = "median",
) -> None:
    """Merge proximal integration sites."""
    # Currently ony supports median mode.
    # Will add a merge mode in the future.
    if mode != "median":
        error_msg = "Only median mode is supported."
        raise ValueError(error_msg)

    # Read the input file and position sort.
    #   - The sorting is version/natural sorting of the chromosome and
    #     and numeric sorting of the start position.
    lines = read_lines(infile)

    # Sort the lines by chromosome, strand, and then position
    lines.sort(
        key=lambda line: (
            natural_key(line.seqname),
            line.strand,  # Use strand directly without natural_key
            int(line.start),
        ),
    )

    # Group by chromosome and strand, but collect the groups into a dictionary
    # to avoid iterator consumption issues
    grouped_data = {}
    for key, group in groupby(lines, key=lambda line: (line.seqname, line.strand)):
        grouped_data[key] = list(group)  # Convert iterator to list to preserve items

    # Process each group.
    for entries_list in grouped_data.values():
        entries = deque(entries_list)  # A deque of BedLine objects

        # Iterate over all integration sites in the same chromosome and strand.
        while entries:
            current_entry = entries.popleft() # The first entry in the deque

            # Initialize variables for the current entry.
            proximal_entries = [current_entry] # List of proximal entries
            total_score = current_entry.score # Total score of proximal entries
            max_score = current_entry.score # Maximum score of proximal entries
            highest_entries = [current_entry] # List of highest scoring entries
            current_start = current_entry.start # Current start position

            # Find all entries within distance - implement proper chaining
            i = 0
            while i < len(entries):
                next_entry = entries[i]

                # Check if the next entry is within the specified distance
                # from CURRENT position
                # This is the key fix
                #   - we compare with current_start which is updated for each match
                if abs(next_entry.start - current_start) <= distance:
                    # Remove the entry from the queue and don't increment i
                    entries.remove(next_entry)
                    proximal_entries.append(next_entry) # Add to proximal entries
                    total_score += next_entry.score # Update total score

                    # Update current_start for chaining behavior - this is critical
                    current_start = next_entry.start

                    # Update max score if proximal entry has a higher score
                    if next_entry.score > max_score:
                        max_score = next_entry.score
                        highest_entries = [next_entry]
                    # If the score is equal to the max score,
                    # add position to highest scores
                    elif next_entry.score == max_score:
                        highest_entries.append(next_entry)
                else:
                    # Only increment i if we don't find a match,
                    # since removing entries changes indices
                    i += 1

            # Select the median entry
            positions = sorted(entry.start for entry in highest_entries)
            median_pos = positions[len(positions) // 2]
            median_entry = next(e for e in highest_entries if e.start == median_pos)

            output_line = (
                f"{median_entry.seqname}\t"
                f"{median_pos}\t"
                f"{median_pos}\t"
                f"{median_entry.name}\t"
                f"{total_score}\t"
                f"{median_entry.strand}\n"
            )

            # Write the merged entry to the output file
            outfile.write(output_line)

    # Final flush to ensure all data is written
    outfile.flush()
