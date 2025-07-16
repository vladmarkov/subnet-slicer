#!/usr/bin/python3
"""
Subnet Calculator
Created by Vlad Markov
Version 2.1
==========================================================================

Software License:
MIT
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
==========================================================================
import ipaddress
import argparse

def read_ips_from_file(file_path):
    """Reads IP addresses from a file, one per line."""
    with open(file_path, 'r') as file:
        ip_list = [line.strip() for line in file if line.strip()]
    return ip_list

def find_network_blocks(ip_list, max_gap):
    # Convert string IPs to ipaddress objects and remove duplicates using a set
    ip_objects = sorted({ipaddress.ip_address(ip) for ip in ip_list})
    
    # List to hold the network blocks
    network_blocks = []
    
    # Initialize the first IP as the start of a range
    start_ip = ip_objects[0]
    
    # Iterate over the IPs to find contiguous ranges
    for i in range(1, len(ip_objects)):
        # Check if the current IP is within the maximum gap from the previous IP
        if ip_objects[i] > ip_objects[i-1] + max_gap:
            # Calculate the smallest subnet for the current range
            network_blocks.append(calculate_network_block(start_ip, ip_objects[i-1]))
            start_ip = ip_objects[i]
    
    # Add the last range
    network_blocks.append(calculate_network_block(start_ip, ip_objects[-1]))
    
    return network_blocks

def calculate_network_block(first_ip, last_ip):
    # Calculate the smallest subnet that contains both the first and last IP
    for prefix_length in range(32, 22, -1):  # Start from /32 to /23 to find the smallest subnet first
        network = ipaddress.ip_network(f"{first_ip}/{prefix_length}", strict=False)
        if last_ip in network:
            return network
    return None

def main():
    parser = argparse.ArgumentParser(description='Process a list of IP addresses from a file and calculate the network blocks.')
    parser.add_argument('file_path', type=str, help='Path to the file containing IP addresses')
    parser.add_argument('--max-gap', type=int, default=1, help='Maximum gap in size between IPs for the segment (default: 1)')
    
    args = parser.parse_args()
    
    ip_list = read_ips_from_file(args.file_path)
    network_blocks = find_network_blocks(ip_list, args.max_gap)
    
    if network_blocks:
        for block in network_blocks:
            print(f"Network block: {block}")
    else:
        print("Could not calculate any network blocks.")

if __name__ == '__main__':
    main()
