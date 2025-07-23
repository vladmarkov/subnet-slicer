#!/usr/bin/python3
"""
Subnet Calculator
Created by Vlad Markov
Version 3.5
==========================================================================

Software License:
MIT
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
==========================================================================
The Subnet Calculator is a tool that identifies a list of subnets from a 
cluster of IP addresses. The --max-gap parameter allows for a granular approach.

Commandline flags and defaults are available by running "python calculate-subnet.py -h"

"""

import ipaddress
import argparse
import csv
from collections import defaultdict

def read_ips_from_csv(file_path, ip_column, aggregate_columns, delimiter, skip_rows):
    """Reads IP addresses and aggregate values from specified columns in a CSV file with a given delimiter, skipping initial rows."""
    ip_list = []
    aggregate_map = defaultdict(set)
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)
        for _ in range(skip_rows):
            next(reader, None)  # Skip the specified number of rows
        for row in reader:
            if len(row) >= ip_column and row[ip_column - 1].strip():  # Check for non-empty IP values
                ip = row[ip_column - 1].strip()
                ip_list.append(ip)
                for col in aggregate_columns:
                    if len(row) >= col:
                        aggregate_value = row[col - 1].strip()
                        if aggregate_value:
                            aggregate_map[ip].add(aggregate_value)
    return ip_list, aggregate_map

def find_network_blocks(ip_list, aggregate_map, max_gap):
    # Convert string IPs to ipaddress objects and remove duplicates using a set
    ip_objects = sorted({ipaddress.ip_address(ip) for ip in ip_list})
    
    # List to hold the network blocks and their corresponding aggregates
    network_blocks = []
    
    # Initialize the first IP as the start of a range
    start_ip = ip_objects[0]
    current_aggregates = aggregate_map[start_ip.exploded]

    # Iterate over the IPs to find contiguous ranges
    for i in range(1, len(ip_objects)):
        # Check if the current IP is within the maximum gap from the previous IP
        if ip_objects[i] > ip_objects[i-1] + max_gap:
            # Calculate the smallest subnet for the current range
            network_blocks.append((calculate_network_block(start_ip, ip_objects[i-1]), current_aggregates))
            start_ip = ip_objects[i]
            current_aggregates = set()
        
        current_aggregates.update(aggregate_map[ip_objects[i].exploded])
    
    # Add the last range
    network_blocks.append((calculate_network_block(start_ip, ip_objects[-1]), current_aggregates))
    
    return network_blocks

def calculate_network_block(first_ip, last_ip):
    # Calculate the smallest subnet that contains both the first and last IP
    for prefix_length in range(32, 22, -1):  # Start from /32 to /23 to find the smallest subnet first
        network = ipaddress.ip_network(f"{first_ip}/{prefix_length}", strict=False)
        if last_ip in network:
            return network
    return None

def main():
    parser = argparse.ArgumentParser(description='Process a list of IP addresses from a CSV file and calculate the network blocks with aggregated values.')
    parser.add_argument('file_path', type=str, help='Path to the file containing IP addresses')
    parser.add_argument('--max-gap', type=int, default=1, help='Maximum gap in size between IPs for the segment (default: 1)')
    parser.add_argument('--csv', action='store_true', help='Indicate that the input file is a CSV file')
    parser.add_argument('--IPcolumn', type=int, default=1, help='Column index for IP addresses in CSV file (default: 1)')
    parser.add_argument('--delimiter', type=str, default=',', help='Delimiter used in the CSV file (default: ",")')
    parser.add_argument('--skip-rows', type=int, default=0, help='Number of rows to skip in the CSV file (default: 0)')
    parser.add_argument('--aggregate-columns', type=str, help='Comma-separated list of column indices for aggregate values in CSV file')
    
    args = parser.parse_args()
    
    if args.csv:
        if args.aggregate_columns:
            aggregate_columns = [int(col) for col in args.aggregate_columns.split(',')]
        else:
            aggregate_columns = []
            
        ip_list, aggregate_map = read_ips_from_csv(args.file_path, args.IPcolumn, aggregate_columns, args.delimiter, args.skip_rows)
    else:
        print("This feature requires the --csv flag and relevant CSV arguments.")
        return

    # Select an aggregate delimiter that does not conflict with the CSV delimiter
    potential_delimiters = [';', '|', '/', ':']
    aggregate_delimiter = next(delim for delim in potential_delimiters if delim != args.delimiter)
    
    network_blocks = find_network_blocks(ip_list, aggregate_map, args.max_gap)
    
    if network_blocks:
        for block, aggregates in network_blocks:
            aggregates_str = aggregate_delimiter.join(sorted(aggregates))
            print(f"{block}{args.delimiter}\"{aggregates_str}\"")
    else:
        print("Could not calculate any network blocks.")

if __name__ == '__main__':
    main()
