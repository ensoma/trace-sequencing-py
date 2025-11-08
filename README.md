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
docker run \
   --rm \
   -v $(pwd):/workdir \
   -w /workdir \
   ensoma/trace:0.2.2 \
   pixi run --manifest-path /app/pyproject.toml trace sam mapping-filter \
      -i /data/input.bam \
      -o /data/output.bam \
      -f bam
```

### Option 2: Local Installation with Pixi

For development purposes or if you prefer to run the toolkit locally:

```bash
# Clone the repository
git clone https://github.com/ensoma/trace-sequencing-py.git
cd trace-sequencing-py

# Install dependencies
pixi install

# Run the toolkit
pixi run trace sam mapping-filter \
   -i input.bam \
   -o output.bam \
   -f bam
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
trace sam mapping-filter -i input.bam -o filtered.bam -f bam

# Filter reads based on 5' softclipping
trace sam fiveprime-filter -i filtered.bam -o filtered_5p.bam -f bam -m 5

# Count integration sites and output to BED format
trace sam count -i filtered_5p.bam -o sites.bed

# Merge proximal integration sites
trace bed merge -i sites.bed -o merged_sites.bed -d 5

# Sort the merged sites by score
trace bed sort -i merged_sites.bed -o sorted_sites.bed -s score
```

## Contributing

Contributions to isatoolkit2 are welcome. Feel free to submit a pull request, while keeping the following in mind.

### Development Setup

1. **Install Pixi** if you don't have it already.

2. **Install Dependencies**:
   ```bash
   pixi install -e dev
   ```

### Checks

Ensure the following checks pass.

```bash
# Unit tests
pixi run -e dev pytest

# Linting
pixi run -e dev ruff check

# Type checking
pixi run -e dev pyright
```

### Documentation

If you're adding new features, please update the documentation accordingly, including:
- Docstrings for new functions or classes
- Updates to the README.md if necessary
- Comments explaining complex code sections

## License

[Insert your license information here]
