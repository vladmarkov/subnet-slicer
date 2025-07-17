Here's an updated version of the README to reflect the recent changes, including support for CSV files, custom delimiters, and skipping rows:

---

# Subnet Calculator

## Overview

The Subnet Calculator is a Python tool designed to identify and calculate network subnets from a list of IP addresses. This tool is particularly useful for network administrators and engineers who need to organize IP addresses into subnets efficiently. The script allows for customized segmentation using the `--max-gap` parameter, providing a granular approach to subnet calculation.

## Features

- Identifies contiguous IP address ranges and calculates the smallest subnet for each range.
- Supports specifying a maximum allowable gap between IP addresses for them to be considered part of the same segment.
- Outputs network blocks in CIDR notation.
- Supports reading from text files or CSV files with customizable delimiters.
- Allows skipping initial rows in a CSV file, useful for ignoring headers.
- Licensed under the MIT License, making it free for personal and commercial use.

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
./calculate-subnet.py <file_path> [options]
```

### Options

- `<file_path>`: The path to the file containing IP addresses.
- `--max-gap MAX_GAP`: (Optional) The maximum number of IP addresses that can be skipped for two IPs to be considered part of the same segment. Default is `1`.
- `--csv`: (Optional) Indicate that the input file is a CSV file.
- `--IPcolumn IP_COLUMN`: (Optional) The column index for IP addresses in the CSV file. Default is `0`.
- `--delimiter DELIMITER`: (Optional) The delimiter used in the CSV file. Default is `,`.
- `--skip-rows SKIP_ROWS`: (Optional) The number of rows to skip at the beginning of the CSV file. Useful for skipping headers. Default is `0`.

### Example

Process a CSV file with the 6th column containing IP addresses, using a `;` delimiter, and skip the first row:

```bash
./calculate-subnet.py data.csv --csv --IPcolumn 5 --delimiter ";" --skip-rows 1 --max-gap 2
```

## Incoming File Format

- **Text File**: One IP address per line.
- - Example contents of `ip_list.txt`:

  ```
  10.10.10.10
  10.10.10.11
  10.10.10.12
  10.10.5.13
  10.10.5.16
  10.10.10.16
  ```
- **CSV File**: Specify the column with IP addresses and optionally the delimiter and rows to skip.

### Example CSV Content

```
ID;IP Address;Location
1;10.10.10.10;Office
2;10.10.10.11;Office
3;10.10.10.12;Data Center
```

In this case, use `--IPcolumn 1` and `--delimiter ";"`.
