"""Merge proximal integration sites."""

from collections import deque
from itertools import groupby
from typing import Annotated, Literal, TextIO

import click
from annotated_types import Ge, Le

from isatoolkit2.bed.bed_utils import BedLine, Strand, natural_key


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
    lines = []
    for line in infile:
        split_line = line.strip().split("\t")
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

    lines.sort(
        key=lambda line: (
            natural_key(line.seqname),
            int(line.start),
            natural_key(line.strand),
        ),
    )

    # Group by chromosome and strand.
    grouped_lines = list(
        groupby(lines, key=lambda line: (line.seqname, line.strand)),
    )

    # Process each group.
    for group in grouped_lines:
        entries = deque(group[1]) # A deque of BedLine objects

        # Iterate over all integration sites in the same chromosome and strand.
        while entries:
            current_entry = entries.popleft() # The first entry in the deque

            # Initialize variables for the current entry.
            proximal_entries = [current_entry] # List of proximal entries
            total_score = current_entry.score # Total score of proximal entries
            max_score = current_entry.score # Maximum score of proximal entries
            highest_entries = [current_entry] # List of highest scoring entries
            current_start = current_entry.start # Current start position

            # Find all entries within distance
            while entries:
                next_entry = entries[0] # Peek at the next entry in the deque

                # Check if the next entry is within the specified distance
                if abs(next_entry.start - current_start) <= distance:
                    entries.popleft() # Allow iteration to next item in inner while loop
                    proximal_entries.append(next_entry) # Add to proximal entries
                    total_score += next_entry.score # Update total score
                    current_start = next_entry.start # Update current start position

                    # Update max score if proximal entry has a higher score
                    # Reset the position of the highest scoring entries
                    if next_entry.score > max_score:
                        max_score = next_entry.score
                        highest_entries = [next_entry]
                    # If the score is equal to the max score,
                    # add position to highest scores
                    elif next_entry.score == max_score:
                        highest_entries.append(next_entry)
                # If the next entry is not within distance, break the inner loop
                else:
                    break

            # Select the median entry
            positions = sorted(entry.start for entry in highest_entries)
            median_pos = positions[len(positions) // 2]
            median_entry = next(e for e in highest_entries if e.start == median_pos)

            # Write the merged entry to the output file
            outfile.write(
                f"{median_entry.seqname}\t"
                f"{median_pos}\t"
                f"{median_pos}\t"
                f"{median_entry.name}\t"
                f"{total_score}\t"
                f"{median_entry.strand}\n",
            )
