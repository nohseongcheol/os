#!/usr/bin/env python3
"""Run current-source ARM64 boot probes for explicitly selected child editions."""
import argparse
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'native'))
from country_naming import validate_edition
from verify_country_boots import verify, atomic_json


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('editions',nargs='+')
    parser.add_argument('--qemu',type=Path)
    args=parser.parse_args()
    qemu=args.qemu.resolve() if args.qemu else None
    if qemu and not qemu.is_file():parser.error('Missing QEMU executable')
    output=ROOT/'build/native/edition-boots'
    results=[]
    for edition in args.editions:
        folder=(ROOT/edition).resolve()
        relative=folder.relative_to(ROOT/'country')
        if len(relative.parts)!=2:parser.error('Select a country/language edition')
        config=json.loads((folder/'native.json').read_text())
        validate_edition(folder,config)
        destination=output/('-'.join(relative.parts))
        report=verify(folder,destination,qemu)
        report['edition']=str(folder.relative_to(ROOT))
        atomic_json(destination/'report.json',report)
        results.append(report)
        print(edition,'PASS' if report['passed'] else 'FAIL',report.get('error',''),flush=True)
    report={'passed':all(r['passed'] for r in results),'editions':len(results),'results':results,
            'scope':'Actual selected ARM64 child-edition boot, UTF-8 file roundtrip and guest Java/Python/C execution. Translation completeness and native-script rendering are separate.'}
    atomic_json(output/'summary.json',report)
    if not report['passed']:raise SystemExit(1)


if __name__=='__main__':main()
