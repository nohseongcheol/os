#!/usr/bin/env python3
"""Fresh build after moving only one country's own files to a new path."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
from export import export_country

ROOT=Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser();parser.add_argument('country');args=parser.parse_args()
    original=ROOT/'country'/args.country
    config=json.loads((original/'native.json').read_text())
    parent=Path(tempfile.mkdtemp(prefix='worldos relocated '))
    target=export_country(original,parent/args.country)
    output=ROOT/'build/native/relocation';output.mkdir(parents=True,exist_ok=True)
    with (output/(args.country+'.log')).open('wb') as log:
        subprocess.check_call(['make','-C',str(target),'build'],stdout=log,stderr=subprocess.STDOUT)
    kernel=target/config['source']/config['native']/'build/kernel8.img'
    report={'passed':True,'country':args.country,'path':str(target),'fresh_build':True,
        'copied_previous_build':False,'copied_other_countries':False,
        'kernel_sha256':hashlib.sha256(kernel.read_bytes()).hexdigest()}
    (output/(args.country+'.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False),flush=True)


if __name__=='__main__':main()
