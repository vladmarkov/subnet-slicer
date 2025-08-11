# Subnet Slicer

## Overview

Subnet Slicer is a Python tool designed to identify and calculate network subnets from a list of IP addresses found in a CSV file. This tool is especially useful for network administrators who need to organize IP addresses into subnets efficiently. It provides the flexibility to extract and concatenate values from specific columns, allowing for customized data processing.

## Features

- Identifies contiguous IP address ranges and calculates the smallest subnet for each range.
- Supports specifying maximum allowable gaps between IP addresses for them to be considered part of the same segment.
- Outputs network blocks in CIDR notation.
- Extracts and concatenates values from specified columns using character ranges.
- Dynamically adjusts output format based on the order of specified arguments.
- Supports CSV input with customizable delimiters.
- Allows printing only subnets when no aggregation columns are specified.

## Requirements

- Python 3.x

## Installation

1. Clone or download the script to your local machine.
2. Ensure the script is executable:
   ```bash
   chmod +x calculate-subnet.py
   ```

## Usage

```bash
python3 calculate-subnet.py <file_path> [options]
```

### Options

- `<file_path>`: The path to the CSV file containing IP addresses.
- `--skip-rows SKIP_ROWS`: Number of rows to skip at the beginning of the CSV file (default: `0`).
- `--csv DELIMITER`: Indicate that the input file is a CSV file and optionally specify a delimiter (default: `,`).
- `--max-gap MAX_GAP`: The maximum number of IP addresses that can be skipped for two IPs to be considered part of the same segment.
- `--IPcolumn IPCOLUMN`: Column index for IP addresses in CSV file.
- `--aggregate-columns AGGREGATE_COLUMNS`: Comma-separated list of column indices for aggregate values in CSV file, with optional extraction format `column:start-end`.

### Example

Given the following CSV file `sample.csv`:

```
1;10.10.1.10;Office1;of001pod501vm001.internal.mycompany.com
2;10.10.1.11;Office1;of001pod501vm007.internal.mycompany.com
3;10.10.2.12;DC1;dc101pod208vm131.external.mycompany.com
4;10.10.5.10;DC2;dc201pod603vm351.external.mycompany.com
5;10.10.5.11;DC2;dc201pod603vm381.external.mycompany.com
6;10.10.2.13;DC1;dc101pod216vm133.external.mycompany.com
```

To calculate subnets and extract values, run:

```bash
python3 calculate-subnet.py sample.csv --skip-rows 1 --csv ";" --max-gap 120 --IPcolumn 2 --aggregate-columns 3,4:1-11
```

Expected Output:
```
10.10.1.10/31;"Office1";"of001pod501"
10.10.2.12/31;"DC1";"dc101pod208|dc101pod216"
10.10.5.10/31;"DC2";"dc201pod603"
```

For a different order:

```bash
python3 calculate-subnet.py sample.csv --skip-rows 1 --csv ";" --max-gap 120 --aggregate-columns 3,4:1-11 --IPcolumn 2
```

Expected Output:
```
"Office1";"of001pod501";10.10.1.10/31
"DC1";"dc101pod208|dc101pod216";10.10.2.12/31
"DC2";"dc201pod603";10.10.5.10/31
```

To print only subnets:

```bash
python3 calculate-subnet.py sample.csv --skip-rows 1 --csv ";" --max-gap 120 --IPcolumn 2
```

Expected Output:
```
10.10.1.10/31
10.10.2.12/31
10.10.5.10/31
```

