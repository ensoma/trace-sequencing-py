# ISAToolkit2

ISAToolkit2 (Integration Site Analysis Toolkit 2) is a command-line tool for processing and analyzing integration site data from random transposon insertions. The toolkit provides utilities for manipulating both alignment files (SAM/BAM format) and integration site data (BED format).

## Overview

Integration site analysis involves discovering the locations where transposons have integrated into a genome. This toolkit provides utilities for:

1. **Processing alignment files (SAM/BAM):**
   - Filtering reads based on mapping quality and characteristics
   - Counting integration sites
   - Working with 5' ends of reads

2. **Processing integration sites (BED):**
   - Merging proximal integration sites
   - Sorting sites by position or score

## Installation & Usage

### Option 1: Using Docker (Preferred)

The toolkit is available as a Docker container for easy deployment without worrying about dependencies.

```bash
# Pull the Docker image
docker pull isatoolkit2:0.1.1

# Run a command using the container
docker run --rm -v $(pwd):/data isatoolkit2:latest sam mapping-filter -i /data/input.bam -o /data/output.bam -f bam
```

### Option 2: Local Installation with Poetry

For development purposes or if you prefer to run the toolkit locally:

```bash
# Clone the repository
git clone https://github.com/ensoma/ensoma-trace-toolkit2.git
cd isatoolkit2

# Install dependencies using Poetry
poetry install

# Run the toolkit
poetry run python -m isatoolkit2.main sam mapping-filter -i input.bam -o output.bam -f bam
```

## Commands

The toolkit is organized into two main command groups:

### SAM Commands

Commands for processing SAM/BAM files.

#### `sam mapping-filter`

Filter SAM/BAM files based on ALT and SUP flags.

| Option | Description | Default |
|--------|-------------|---------|
| `-i`, `--infile` | Input SAM/BAM file or stdin (use '-' for stdin) | `-` |
| `-o`, `--outfile` | Output SAM/BAM file or stdout (use '-' for stdout) | `-` |
| `--no-alt-filtering` | Turn off ALT filtering | `False` |
| `--no-sup-filtering` | Turn off SUP filtering | `False` |
| `-f`, `--outfile-format` | Output format (sam or bam) | Required |
| `-u`, `--uncompressed` | Output uncompressed BAM file | `False` |
| `-d`, `--discarded-outfile` | Output discarded reads to a separate file | None |

#### `sam fiveprime-filter`

Filter SAM/BAM files based on 5' softclipping.

| Option | Description | Default |
|--------|-------------|---------|
| `-i`, `--infile` | Input SAM/BAM file or stdin (use '-' for stdin) | `-` |
| `-o`, `--outfile` | Output SAM/BAM file or stdout (use '-' for stdout) | `-` |
| `-f`, `--outfile-format` | Output format (sam or bam) | Required |
| `-u`, `--uncompressed` | Output uncompressed BAM file | `False` |
| `-d`, `--discarded-outfile` | Output discarded reads to a separate file | None |
| `-m`, `--max-softclip` | Maximum softclip length | `5` |

#### `sam count`

Count integration sites in a SAM/BAM file.

| Option | Description | Default |
|--------|-------------|---------|
| `-i`, `--infile` | Input SAM/BAM file or stdin (use '-' for stdin) | `-` |
| `-o`, `--outfile` | Output BED file or stdout (use '-' for stdout) | `-` |

### BED Commands

Commands for processing BED files containing integration site data.

#### `bed sort`

Sort BED file by position or score.

| Option | Description | Default |
|--------|-------------|---------|
| `-i`, `--infile` | Input BED file or stdin (use '-' for stdin) | `-` |
| `-o`, `--outfile` | Output BED file or stdout (use '-' for stdout) | `-` |
| `-s`, `--sort-by` | Sort by position or score | `position` |

#### `bed merge`

Merge proximal integration sites in a BED file.

| Option | Description | Default |
|--------|-------------|---------|
| `-i`, `--infile` | Input BED file or stdin (use '-' for stdin) | `-` |
| `-o`, `--outfile` | Output BED file or stdout (use '-' for stdout) | `-` |
| `-d`, `--distance` | Distance to merge proximal integration sites | `5` |
| `-m`, `--mode` | Mode for merging integration sites (currently only median supported) | `median` |

## Example Usage

### Processing Pipeline Example

```bash
# Filter a BAM file to remove reads with alternative alignments and supplementary alignments
isatoolkit2 sam mapping-filter -i input.bam -o filtered.bam -f bam

# Filter reads based on 5' softclipping
isatoolkit2 sam fiveprime-filter -i filtered.bam -o filtered_5p.bam -f bam -m 5

# Count integration sites and output to BED format
isatoolkit2 sam count -i filtered_5p.bam -o sites.bed

# Merge proximal integration sites
isatoolkit2 bed merge -i sites.bed -o merged_sites.bed -d 5

# Sort the merged sites by score
isatoolkit2 bed sort -i merged_sites.bed -o sorted_sites.bed -s score
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Insert your license information here]
