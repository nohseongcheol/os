#!/usr/bin/env python3
"""Report Korean Java names and whole comments separately from literal fixtures."""
import argparse
from collections import Counter
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'native'))
from generate import identifiers
from java_prose import TOKENS

HANGUL=re.compile('[\u1100-\u11ff\u3130-\u318f\uac00-\ud7af]')
LEGAL=re.compile(r'copyright|spdx-license|licensed under|저작권',re.I)


@lru_cache(maxsize=4096)
def inspect(digest, data):
    assert hashlib.sha256(data).hexdigest()==digest,'Source changed outside its manifest'
    text=data.decode('utf-8')
    names=sorted({t for t in identifiers('source.java',text) if HANGUL.search(t)})
    comments=[m.group() for m in TOKENS.finditer(text)
              if m.group().startswith(('//','/*')) and not LEGAL.search(m.group()) and HANGUL.search(m.group())]
    literals=[m.group() for m in TOKENS.finditer(text) if m.group().startswith('"') and HANGUL.search(m.group())]
    return names, comments, literals


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--languages',nargs='+')
    parser.add_argument('--output',type=Path,default=ROOT/'build/localization-round2/java-localization-audit.json')
    args=parser.parse_args()
    paths=list((ROOT/'country').glob('*/native.json'))+list((ROOT/'country').glob('*/*/native.json'))
    editions=[];errors=[];total=0
    configs=sorted(((p,json.loads(p.read_text())) for p in paths),key=lambda item:(item[1]['language'],str(item[0])))
    for path,c in configs:
        if args.languages and c['language'] not in args.languages:continue
        manifest_bytes=(path.parent/'native-generated.json').read_bytes()
        manifest=json.loads(manifest_bytes.decode('utf-8'))
        entries=sorted((n,h) for n,h in manifest.items() if n.endswith('.java'))
        pending_names=set();pending_paths=[];pending_comments=[];pending_messages=[]
        library='/'+c['native']+'/'+c['identifiers'].get('한국어자바','한국어자바')+'/'
        for name,digest in entries:
            try:
                names,comments,literals=inspect(digest,(path.parent/name).read_bytes())
                total+=1
                if c['language']=='ko':continue
                pending_names.update(names)
                if HANGUL.search(name):pending_paths.append(name)
                if comments:pending_comments.append({'path':name,'comments':comments})
                if library in '/'+name and literals:pending_messages.append({'path':name,'messages':literals})
            except (AssertionError,OSError,UnicodeError) as error:
                errors.append({'edition':str(path.parent.relative_to(ROOT)),'path':name,'error':str(error)})
        editions.append({'edition':str(path.parent.relative_to(ROOT)),'country':c['country'],'language':c['language'],
                         'manifest_sha256':hashlib.sha256(manifest_bytes).hexdigest(),
                         'java_files':len(entries),'remaining_identifiers':sorted(pending_names),
                         'remaining_paths':pending_paths,'remaining_comments':pending_comments,'remaining_library_messages':pending_messages})
    report={'integrity_passed':not errors,'editions':len(editions),'java_files_checked':total,'errors':errors,
            'scope':'Owned Java identifiers, paths and complete comments. Copyright authors and literal character/string fixtures are not translation failures. Not a complete prose or non-Java audit.',
            'fully_localized_in_this_scope':sum(not(r['remaining_identifiers'] or r['remaining_paths'] or r['remaining_comments'] or r['remaining_library_messages']) for r in editions),
            'language_tags_with_pending':dict(Counter(r['language'] for r in editions if r['remaining_identifiers'] or r['remaining_paths'] or r['remaining_comments'] or r['remaining_library_messages'])),
            'results':editions}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('results','language_tags_with_pending','errors')},ensure_ascii=False),flush=True)
    if errors:raise SystemExit(1)


if __name__=='__main__':main()
