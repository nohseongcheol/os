#!/usr/bin/env python3
"""Compile and execute each country's managed Java tests in its own namespace."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'native'))
from country_naming import names_for_country, validate_edition
from source_names import make_renamer
from verify_country_boots import atomic_json, source_digest


def check(path):
    folder=path.parent;config=json.loads(path.read_text())
    result={'edition':str(folder.relative_to(ROOT)),'country':config['country'],
            'language':config['language'],'passed':False}
    try:
        assert config['identifiers']==names_for_country(config['country'],config['language']),'Stale language/country dictionary'
        assert config['country_naming']==validate_edition(folder,config),'Stale country policy'
        rename=make_renamer(config['identifiers'])
        source=folder/config['source']
        files=sorted((source/rename('원천')).rglob('*.java'))
        assert len(files)==29,'Unexpected managed source inventory'
        before=source_digest(folder,config)
        with tempfile.TemporaryDirectory(prefix='country-namespace-') as temporary:
            command=['javac','-J-XX:-UsePerfData','--release','11','-encoding','UTF-8','-d',temporary]+[str(p) for p in files]
            subprocess.check_output(command,stderr=subprocess.STDOUT,timeout=120)
            main=rename('한국.제이코로스.시험.전체시험')
            output=subprocess.check_output(['java','-XX:-UsePerfData','-cp',temporary,main],stderr=subprocess.STDOUT,timeout=30).decode('utf-8')
            count=re.search(r'(\d+)\s*$',output)
            assert count and int(count.group(1))==47,'Expected all 47 managed assertions: '+output
        assert source_digest(folder,config)==before,'Source changed during testing'
        result.update(passed=True,source_sha256=before,java_files=len(files),main=main,
                      managed_assertions=int(count.group(1)),output=output.strip())
    except subprocess.CalledProcessError as error:
        result['error']=error.output.decode('utf-8','replace')
    except Exception as error:
        result['error']=repr(error)
    print(result['edition'],result['passed'],result.get('error',''),flush=True)
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--countries',nargs='+')
    parser.add_argument('--editions',nargs='*',default=[],help='Additional child edition paths')
    parser.add_argument('--jobs',type=int,default=2,choices=range(1,5))
    parser.add_argument('--output',type=Path,help='Write a separate report for a targeted follow-up check')
    args=parser.parse_args()
    paths=[p for p in sorted((ROOT/'country').glob('*/native.json')) if not args.countries or p.parent.name in args.countries]
    paths+= [ROOT/p/'native.json' for p in args.editions]
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:results=list(pool.map(check,paths))
    report={'passed':all(r['passed'] for r in results),'editions':len(results),'results':results}
    target=args.output or ROOT/'build/localization-round2/managed-country-namespaces.json'
    target.parent.mkdir(parents=True,exist_ok=True)
    atomic_json(target,report)
    if not report['passed']:raise SystemExit(1)


if __name__=='__main__':main()
