#!/usr/bin/python3
"""
Subnet Calculator
Created by Vlad Markov
Version 1.1
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

def create_network_block(ip_list):
    # Convert string IPs to ipaddress objects
    ip_objects = [ipaddress.ip_address(ip) for ip in ip_list]
    
    # Sort the IP addresses
    sorted_ips = sorted(ip_objects)
    
    # Create a network from the sorted IPs
    first_ip = sorted_ips[0]
    last_ip = sorted_ips[-1]
    
    # Calculate the smallest subnet that contains both the first and last IP
    for prefix_length in range(32, -1, -1):
        network = ipaddress.ip_network(f"{first_ip}/{prefix_length}", strict=False)
        if last_ip in network:
            return network
    
    return None

def main():
    parser = argparse.ArgumentParser(description='Process a list of IP addresses from a file and calculate the network block.')
    parser.add_argument('file_path', type=str, help='Path to the file containing IP addresses')
    
    args = parser.parse_args()
    
    ip_list = read_ips_from_file(args.file_path)
    network_block = create_network_block(ip_list)
    
    if network_block:
        print(f"Network block: {network_block}")
    else:
        print("Could not calculate a network block.")

if __name__ == '__main__':
    main()
