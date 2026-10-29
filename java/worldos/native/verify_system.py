#!/usr/bin/env python3
"""Build and boot selected independent editions; retain per-kernel evidence."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser();parser.add_argument('countries',nargs='+');args=parser.parse_args()
    for code in args.countries:
        if len(code)!=3 or not code.isupper() or not code.isalpha():raise SystemExit('Expected a country code: '+code)
        folder=ROOT/'country'/code;output=ROOT/'build/native/system'/code;output.mkdir(parents=True,exist_ok=True)
        subprocess.check_call(['make','-C',str(folder),'test-system','ARGS=--output '+str(output)])
        report=json.loads((output/'report.json').read_text());config=json.loads((folder/'native.json').read_text())
        native=folder/config['source']/config['native'];kernel=native/'build/kernel8.img'
        assert report['passed'] and report['country']==code and report['kernel_sha256']==hashlib.sha256(kernel.read_bytes()).hexdigest(),code
        print('SYSTEM COMMANDS VERIFIED',code,flush=True)


if __name__=='__main__':main()
