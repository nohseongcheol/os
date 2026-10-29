#!/usr/bin/env python3
"""Freeze explicitly written whole-role corrections, with collision checks."""
import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path
import sys
import unicodedata

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'native'))
from terms import names, RESERVED
from collect_terminology_roles import fit_guest_limits
from compose_reviewed_roles import compose


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--language',required=True)
    parser.add_argument('--write',action='store_true')
    args=parser.parse_args()
    path=ROOT/'native/inputs/reviewed-roles'/(args.language+'.json')
    corrections=json.loads(path.read_text())
    mapping=names(args.language)
    mapping.update(corrections['names'])
    glossary_path=ROOT/'native/inputs/burmese-role-words.tsv'
    generated={}
    rejected_compounds={}
    if args.language=='my' and glossary_path.is_file():
        # Only this language's explicitly maintained words may compose roles.
        # Unknown or ambiguous roles remain visible in pending_roles.
        mapping=dict(corrections['names'])
        glossary={r['word']:r['proposal'] for r in csv.DictReader(glossary_path.open(),delimiter='\t')}
        groups=collections.defaultdict(list)
        for original,role in names('en').items():
            if original in mapping:continue
            try:value=unicodedata.normalize('NFKC',compose(role,glossary,args.language))
            except KeyError:continue
            if not value.isidentifier() or value in RESERVED or len(value.encode())>220:
                rejected_compounds[original]='identifier-or-filesystem-limit';continue
            groups[value].append(original)
        used=set(mapping.values())
        for value,originals in groups.items():
            if value in used or len(originals)>1:
                for original in originals:rejected_compounds[original]='semantic-disambiguation-required'
                continue
            generated[originals[0]]=value
        mapping.update(generated)
    mapping={k:unicodedata.normalize('NFKC',v) for k,v in mapping.items()}
    reverse=collections.defaultdict(list)
    for k,v in mapping.items():reverse[v].append(k)
    invalid={k:v for k,v in mapping.items() if not v.isidentifier() or v in RESERVED or len(v.encode())>220}
    collisions={v:ks for v,ks in reverse.items() if len(ks)>1}
    trial=dict(mapping)
    limits=fit_guest_limits(trial,set())
    if args.language=='my':
        # Curated whole names must fit. Composed candidates that exceed the
        # real guest path/module limits remain untranslated until shortened.
        for original in set(mapping)-set(trial):
            if original in corrections['names']:continue
            mapping.pop(original);rejected_compounds[original]='guest-runtime-limit'
        limits=fit_guest_limits(dict(mapping),set())
    report={'language':args.language,'roles':len(mapping),'invalid':invalid,'collisions':collisions,'runtime_limits':limits,
            'composed_candidates':len(generated),'rejected_compounds':rejected_compounds,
            'uncorrected_legacy_roles':sorted(set(names(args.language))-set(corrections['names']))}
    target=ROOT/'build/localization-round2'/(args.language+'-corrections.json')
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('ROLES',len(mapping),'INVALID',len(invalid),'COLLISIONS',len(collisions),'LIMITS',len(limits),flush=True)
    if args.write:
        if invalid or collisions or limits:raise SystemExit('Resolve corrections before applying them')
        document=dict(corrections,names=mapping,
                      whole_role_corrections_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                      scope='Explicit whole-role proposals; uncovered roles remain pending.',
                      pending_roles={k:en for k,en in names('en').items() if k not in mapping})
        if args.language=='my':
            document['manual_glossary_sha256']=hashlib.sha256(glossary_path.read_bytes()).hexdigest()
            document['rejected_compounds']=rejected_compounds
        (ROOT/'native/inputs/localized-roles'/(args.language+'.json')).write_text(json.dumps(document,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':main()
