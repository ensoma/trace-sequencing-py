# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ISAToolkit2 is a command-line tool for processing and analyzing integration site data from random transposon insertions. The toolkit manipulates alignment files (SAM/BAM) and integration site data (BED format).

The command-line entry point is `trace` (defined via `pyproject.toml`), not the package name `isatoolkit2`.

## Development Commands

### Setup
```bash
# Install dependencies (including dev environment)
pixi install -e dev
```

### Testing
```bash
# Run all tests
pixi run -e dev pytest

# Run a specific test file
pixi run -e dev pytest tests/test_sam_mapping_filter.py

# Run a specific test function
pixi run -e dev pytest tests/test_sam_mapping_filter.py::test_function_name
```

### Code Quality
```bash
# Linting (runs all ruff checks)
pixi run -e dev ruff check

# Auto-fix linting issues
pixi run -e dev ruff check --fix

# Type checking
pixi run -e dev pyright
```

### Running the CLI
```bash
# Local development
pixi run trace sam mapping-filter -i input.bam -o output.bam -f bam
pixi run trace bed merge -i sites.bed -o merged.bed -d 5
```

### Docker
```bash
# Build Docker image
docker build -t trace:0.2.2 .

# Run via Docker
docker run \
  --rm -v $(pwd):/workdir -w /workdir trace:0.2.2 \
  pixi run --manifest-path /app/pyproject.toml trace sam mapping-filter \
  -i input.bam -o output.bam -f bam
```

## Architecture

### Command Structure
The CLI uses a two-level command hierarchy implemented with Click:
- `trace` → main entry point (`src/isatoolkit2/main.py:cli()`)
  - `sam` → SAM/BAM processing commands
    - `mapping-filter` → Filter based on ALT/SUP flags
    - `fiveprime-filter` → Filter based on 5' softclipping
    - `count` → Count integration sites, output to BED
  - `bed` → BED file processing commands
    - `sort` → Sort by position or score
    - `merge` → Merge proximal integration sites

### Data Flow Pattern
Commands follow a consistent pattern:
1. CLI layer (`main.py`) handles argument parsing and validation using Click
2. Custom Click types (`utils.py`) validate SAM/BAM file paths via Pydantic schemas
3. Implementation modules perform the core logic using pysam/native Python
4. All commands support stdin/stdout (`-` as input/output)

### Key Components

**SAM/BAM Processing** (`src/isatoolkit2/sam/`):
- Uses `pysam` library for SAM/BAM file I/O
- `sam_utils.py` provides output mode helpers (`get_output_mode`)
- Filter functions use `contextlib.ExitStack` to manage multiple file handles
- Filtering logic examines SAM tags (`XA` for alternative alignments, `SA` for supplementary)
- Optional discarded read output via `-d/--discarded-outfile`

**BED Processing** (`src/isatoolkit2/bed/`):
- `BedLine` Pydantic model validates BED format (minimum 6 columns)
- Natural sorting via `natural_key()` for chromosome names (e.g., chr1, chr2, chr10)
- `merge.py` implements chaining algorithm: iteratively merges sites within distance threshold
- Uses median position of highest-scoring entries for merged output

**Custom Click Types** (`src/isatoolkit2/utils.py`):
- `SamBamInputType`/`SamBamOutputType`: Validate .sam/.bam extensions via Pydantic
- Supports `-` for stdin/stdout or file paths
- Validation occurs before command execution

### File Organization
```
src/isatoolkit2/
├── main.py              # CLI entry point with all command definitions
├── utils.py             # Custom Click parameter types
├── sam/
│   ├── sam_utils.py     # Shared SAM/BAM utilities
│   ├── mapping_filter.py
│   ├── fiveprime_filter.py
│   └── count.py
└── bed/
    ├── bed_utils.py     # BedLine model, natural_key sorting
    ├── merge.py
    └── sort.py

tests/
└── test_*.py            # Pytest tests using parametrize for multiple scenarios
```

## Important Implementation Details

### SAM/BAM Handling
- Output mode mapping: `sam` → "w", `bam` + uncompressed → "wbu", `bam` → "wb"
- Always use `str()` when passing paths to pysam (e.g., `pysam.AlignmentFile(str(path))`)
- Template header from input file: `pysam.AlignmentFile(output, mode, template=infile_handle)`

### BED Merging Algorithm
The merge function uses a chaining approach:
- Groups by chromosome and strand
- For each group, maintains a deque of remaining entries
- Iteratively finds entries within `distance` of the *current* position (not initial)
- Updates `current_start` with each match to enable chaining
- Outputs median position of highest-scoring entries with summed scores

### Testing Conventions
- Tests use pytest parametrization for multiple scenarios
- SAM test data includes header: `@HD\tVN:1.6\tSO:coordinate\n@SQ\tSN:chr1\tLN:1000\n`
- Temporary files handled via pytest fixtures

### Ruff Configuration
- Target Python 3.12+
- Selects all rules (`ALL`), ignores `D211`, `D212`
- Per-file ignores: `PLR0913` for functions with many params, `N805` for utils, `S101`/`PT006` for tests
