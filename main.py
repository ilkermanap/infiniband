import argparse
import sys
import subprocess
from topology import Topology


parser = argparse.ArgumentParser()
parser.add_argument("--file",
                    help="File name for ibnetdiscover command output",
                    action="store")
parser.add_argument("--run",
                    help="Get information by running ibnetdiscover",
                    action="store_true")
parser.add_argument("--output",
                    help="Name of the output file",
                    action="store")
parser.add_argument("--overwrite",
                    help="Overwrite the output file if exists",
                    action="store_true")


args = parser.parse_args()

if args.file:
    try:
        contents = open(args.file).readlines()
        topology = Topology(contents)
        topology.topology()
    except FileNotFoundError:
        print(f"There is no file named {args.file}")
        sys.exit(1)

if args.run:
    try:
        result = subprocess.run(["ibnetdiscover"], capture_output=True, text=True)
        topology = Topology(result.stdout)
        output = None
        overwrite = False
        if args.output:
            output = args.output
        if args.overwrite:
            overwrite = args.overwrite
        topology.topology(outfile=output, overwrite=overwrite)
    except FileNotFoundError:
        print("Make sure that ibnetdiscover is installed")
        sys.exit(2)
