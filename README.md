Here is a detailed README for the `calculate-subnet.py` script, including an explanation about the incoming file:

---

# Subnet Calculator

## Overview

The Subnet Calculator is a Python tool designed to identify and calculate network subnets from a list of IP addresses. This tool is particularly useful for network administrators and engineers who need to organize IP addresses into subnets efficiently. The script allows for customized segmentation using the `--max-gap` parameter, providing a granular approach to subnet calculation.

## Features

- Identifies contiguous IP address ranges and calculates the smallest subnet for each range.
- Supports specifying a maximum allowable gap between IP addresses for them to be considered part of the same segment.
- Outputs network blocks in CIDR notation.
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
./calculate-subnet.py <file_path> [--max-gap MAX_GAP]
```

### Arguments

- `<file_path>`: The path to the file containing IP addresses. Each IP address should be on a separate line.
- `--max-gap MAX_GAP`: (Optional) The maximum number of IP addresses that can be skipped for two IPs to be considered part of the same segment. Default is `1`.

### Example

```bash
./calculate-subnet.py ip_list.txt --max-gap 2
```

This command processes the IP addresses in `ip_list.txt` and calculates network blocks, allowing for a maximum gap of 2 IP addresses between addresses in a segment.

## Incoming File Format

- The incoming file should be a plain text file with one IP address per line.
- Example contents of `ip_list.txt`:

  ```
  10.10.10.10
  10.10.10.11
  10.10.10.12
  10.10.5.13
  10.10.5.16
  10.10.10.16
  ```

- The script will ignore empty lines and duplicate IP addresses automatically.

