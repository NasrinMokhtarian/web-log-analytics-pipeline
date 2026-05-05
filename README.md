# Web Log Analytics Pipeline

A production-minded Python project for parsing web server access logs, quarantining malformed records, validating generated outputs, and producing analytics reports.

## Overview

Raw web logs contain valuable operational and analytical information, but they are not directly ready for analysis. They often include semi-structured text, mixed field types, malformed rows, and large numbers of records.

This project transforms a raw web access log into structured, validated outputs that answer practical analytics questions such as:

- Which hosts generated the most requests?
- Which resources consumed the most bandwidth?
- What were the busiest rolling 60-minute traffic windows?
- Which input rows were malformed, and why were they rejected?

The project was designed not only to solve the reporting problem, but also to reflect stronger engineering practices through typing, modularity, validation, testing, and structured logging.

## What the Pipeline Does

The pipeline:

1. reads the raw log file line by line
2. parses valid rows into a typed data model
3. quarantines malformed rows with explicit rejection reasons
4. generates analytics CSV reports
5. validates the final outputs before treating the run as successful

## Analytics Questions This Project Answers

This solution can answer questions such as:

- Which hosts or IP addresses are the most active?
- Which resources drive the highest total bandwidth usage?
- When did traffic peaks occur?
- How many malformed records were found in the raw input?
- What kinds of parsing or validation problems appeared in the source data?

## Output Reports

The pipeline generates the following CSV files:

- **`hosts.csv`** — top hosts by number of requests
- **`resources.csv`** — top resources by total bandwidth
- **`windows.csv`** — busiest rolling 60-minute windows
- **`malformed_lines.csv`** *(optional)* — rejected rows with line number and reason

## Engineering Focus

This version goes beyond a simple scripting solution and includes:

- typed data models with `dataclass`
- modular package structure
- parser validation
- malformed-line quarantine
- automated tests with `pytest`
- structured logging
- final output validation checks
- CLI execution with configurable input and output paths

## Project Structure

```text
web-log-analytics-pipeline/
├── README.md
├── requirements.txt
├── .gitignore
├── pyproject.toml
├── data/
│   └── .gitkeep
├── outputs/
│   └── .gitkeep
├── source/
│   └── log_analysis/
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       ├── models.py
│       ├── parser.py
│       ├── processing.py
│       ├── validation.py
│       └── writers.py
└── tests/
    ├── conftest.py
    ├── test_parser.py
    ├── test_processing.py
    ├── test_validation.py
    └── test_writers.py
```

## Data Model

### `LogRecord`

Represents one valid parsed log row with:

- `host`
- `timestamp`
- `resource`
- `response_size`
- `status_code`

### `MalformedLine`

Represents one quarantined invalid row with:

- `line_number`
- `reason`
- `raw_line`

Using typed data models improves readability, maintainability, and testability compared with passing loose dictionaries throughout the codebase.

## How It Works

### 1. Parsing

Each raw line is parsed into a `LogRecord`. If parsing fails or validation rules are not met, the line is rejected and can be written to a malformed-line report instead of silently disappearing.

### 2. Aggregation

The pipeline calculates:

- host request counts
- total bytes per resource
- rolling 60-minute traffic windows

### 3. Validation

Generated CSV files are validated for:

- correct headers
- row limits
- valid numeric fields
- descending sort order
- unique window start times
- valid timestamp formatting

This helps reduce delivery risk and ensures the final outputs are internally consistent.

## Assumptions and Edge Cases

The solution uses the following assumptions:

- if the response size is `-`, it is treated as `0`
- malformed or irregular lines are rejected from the main analytics flow
- the resource is extracted as the second part of the request string  
  example: `GET /history/apollo/ HTTP/1.0` → `/history/apollo/`
- a 60-minute window is defined as:

```text
[start_time, start_time + 60 minutes)
```

This means the start time is included and the exact end boundary is excluded.

- if multiple requests occur at the same exact timestamp, that timestamp is evaluated once as a window start in the final busiest-window output

## Complexity

- **Time complexity:** `O(n log n)`  
  due to sorting timestamps for rolling-window analysis

- **Space complexity:** approximately `O(n)`  
  due mainly to timestamp storage

## Setup

Install dependencies with:

```bash
python -m pip install -r requirements.txt
```

## How to Run

Place the input log file at:

```text
data/log.txt
```

Because the package is located under `source/`, set `PYTHONPATH` before running.

### Windows PowerShell

```powershell
$env:PYTHONPATH="source"
python -m log_analysis.cli --input data/log.txt --output outputs --write-malformed-lines --log-level INFO
```

### Linux / macOS

```bash
PYTHONPATH=source python -m log_analysis.cli --input data/log.txt --output outputs --write-malformed-lines --log-level INFO
```

## How to Run Tests

### Windows PowerShell

```powershell
$env:PYTHONPATH="source"
python -m pytest -v
```

### Linux / macOS

```bash
PYTHONPATH=source python -m pytest -v
```

## Output Files

### `hosts.csv`

Contains:

- `Host`
- `Number of Requests`

### `resources.csv`

Contains:

- `Resource`
- `Number of Bytes`

### `windows.csv`

Contains:

- `Window Start Time`
- `Number of Requests`

### `malformed_lines.csv`

Contains:

- `Line Number`
- `Reason`
- `Raw Line`

## Design Decisions

### Line-by-line reading

The log file is processed line by line rather than loading the full raw input into memory. This keeps the pipeline more suitable for large files.

### Standard library runtime logic

The runtime implementation uses Python standard library components for parsing, aggregation, and CSV generation. This keeps the execution flow simple and transparent. External dependency usage is currently limited to testing.

### Typed models

Using `dataclass` models improves maintainability and makes the parser contract clearer.

### Separation of concerns

Parsing, processing, output writing, and validation are separated into dedicated modules. This makes the code easier to understand, test, and extend.

### Malformed-line quarantine

Bad rows are separated from the main reporting flow instead of being silently ignored. This improves traceability and data quality visibility.

### Explicit output validation

The pipeline validates generated reports before considering the run complete. This adds a final quality gate before delivery or downstream use.

## Future Improvements

Possible next steps include:

- richer analytics outputs such as status-code summaries and error-rate reporting
- streaming malformed lines directly to disk for very large files
- static type checking with `mypy`
- linting and formatting integration
- packaging as an installable CLI tool
- CI integration for automated test runs
- performance profiling for larger datasets

## What This Project Demonstrates

This project demonstrates:

- Python data-engineering fundamentals
- log parsing and transformation
- rolling-window analytics
- data-quality handling
- output validation before delivery
- modular project structure
- automated testing
- structured logging
- typed data modeling

## Notes

- raw input data is not committed to the repository
- generated CSV outputs are not committed by default
- empty `data/` and `outputs/` directories are preserved with `.gitkeep`

## AI Usage

AI was used as a support tool during the improvement phase of this project, mainly for:

- discussing engineering trade-offs
- refining project structure
- improving validation and testing ideas
- improving documentation quality

Final implementation decisions were reviewed and understood before inclusion in the project.
