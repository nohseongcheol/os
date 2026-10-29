#!/usr/bin/env python3
"""Compose complete role names from a maintained, language-specific glossary.

Collision reports require explicit semantic corrections. Never invent hash or
numeric suffixes, borrow another language's dictionary, or certify etymology.
"""
import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path
import sys
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'native'))
from terms import names, RESERVED
from collect_terminology_roles import words, fit_guest_limits

GLOSSARIES = {'ja': 'japanese-role-words.tsv',
              'zh_Hans': 'chinese-role-words.tsv',
              'zh_Hant': 'traditional-chinese-role-words.tsv',
              'vi': 'vietnamese-role-words.tsv',
              'de': 'de-role-words.tsv', 'fr': 'fr-role-words.tsv', 'es': 'es-role-words.tsv'}
VERBS = set('read write get set add remove create delete find search parse emit generate '
            'compile execute run stop check verify validate open close load save send receive '
            'show draw fill allocate release invoke call wait await accept bind connect listen '
            'decode encode extract skip localize compare append insert print build reset clear '
            'copy copyWith change prepare initialize translate test start finish register '
            'unregister preserve restore recover collect gather inspect allow reject ignore '
            'protect rename synchronize assemble install apply convert analyze enable disable '
            'deactivate refresh replace extend truncate throw catch yield seek put push pop '
            'capture visit identify increase subtract calculate join split compose normalize '
            'erase discard reserve retain reallocate grant acquire distribute relay configure '
            'consume modify decrypt encrypt'.split())


def compose(role, glossary, language='ja'):
    parts = words(role)
    # Preserve the processor family as one proper technical name. The 'x'
    # here is not the coordinate variable used by drawing functions.
    index = 0
    while index + 1 < len(parts):
        if parts[index].lower() == 'x' and parts[index+1] == '86':
            parts[index:index+2] = ['x86']
        index += 1
    # Japanese technical compounds put the operation after its object.
    if language in ('ja', 'de', 'my') and len(parts) > 1 and parts[0].lower() in VERBS and role[0].islower():
        parts = parts[1:] + parts[:1]
    if language in ('fr', 'es', 'vi'):
        if len(parts) > 1 and role[0].islower() and parts[0].lower() in VERBS | {'is','has','does','can','should','will'}:
            parts = parts[:1] + list(reversed(parts[1:]))
        else:
            parts = list(reversed(parts))
    if language in ('de', 'fr', 'es', 'vi'):
        values = [p if p.isdigit() or p == 'x86' else glossary[p.lower()] for p in parts]
        value = ''.join(v[:1].upper()+v[1:] for v in values)
        return value[:1].lower()+value[1:] if role[:1].islower() else value
    return ''.join(p if p.isdigit() or p == 'x86' else glossary[p.lower()] for p in parts)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--language', choices=sorted(GLOSSARIES), required=True)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    glossary_path = ROOT / 'native/inputs' / GLOSSARIES[args.language]
    correction_path = ROOT / 'native/inputs/reviewed-roles' / (args.language + '.json')
    glossary = {r['word']: r['proposal'] for r in csv.DictReader(glossary_path.open(), delimiter='\t')}
    corrections = json.loads(correction_path.read_text())
    roles = names('en')
    mapping = {}
    missing = {}
    invalid = {}
    for original, role in roles.items():
        try:
            value = corrections['names'].get(original) or compose(role, glossary, args.language)
        except KeyError as error:
            missing[original] = str(error)
            continue
        value = unicodedata.normalize('NFKC', value)
        if not value.isidentifier() or value in RESERVED or len(value.encode()) > 220:
            invalid[original] = value
        mapping[original] = value
    reverse = collections.defaultdict(list)
    for original, value in mapping.items():
        reverse[value].append(original)
    collisions = {value: [{'original': k, 'role': roles[k]} for k in keys]
                  for value, keys in reverse.items() if len(keys) > 1}
    report = {'language': args.language, 'roles': len(roles), 'mapped': len(mapping),
              'missing': missing, 'invalid': invalid, 'collisions': collisions}
    output = ROOT / 'build/localization-round2'
    output.mkdir(parents=True, exist_ok=True)
    (output / (args.language + '-composition.json')).write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print('ROLES', len(roles), 'MAPPED', len(mapping), 'MISSING', len(missing),
          'INVALID', len(invalid), 'COLLISIONS', len(collisions))
    if not args.write:
        return
    if missing or invalid or collisions:
        raise SystemExit('Resolve the semantic review report before writing a dictionary.')
    trial = dict(mapping)
    rejected = fit_guest_limits(trial, set())
    if rejected:
        (output / (args.language + '-runtime-limits.json')).write_text(json.dumps(rejected, ensure_ascii=False, indent=2) + '\n')
        raise SystemExit('Shorten the reported names without dropping their translations.')
    document = {'language': args.language, 'status': 'function-based-project-proposals',
                'native_review': 'pending', 'etymology_review': 'pending',
                'references': corrections['references'],
                'manual_glossary_sha256': hashlib.sha256(glossary_path.read_bytes()).hexdigest(),
                'whole_role_corrections_sha256': hashlib.sha256(correction_path.read_bytes()).hexdigest(),
                'scope': 'Original code roles composed using this language glossary. Modern proposals, not historically attested compounds. No related-language fallback or opaque collision suffix.',
                'naming_principles': corrections.get('naming_principles'),
                'verified_lexeme_history': corrections.get('verified_lexeme_history', []),
                'rationale': corrections.get('rationale', {}), 'names': mapping,
                'roles': {k: {'role': role, 'status': 'reviewed-whole-role-proposal' if k in corrections['names'] else 'functional-compound-proposal'} for k, role in roles.items()},
                'pending_roles': {}, 'runtime_limit_pending': {}}
    target = ROOT / 'native/inputs/localized-roles' / (args.language + '.json')
    temporary = target.with_suffix('.json.new')
    temporary.write_text(json.dumps(document, ensure_ascii=False, indent=2) + '\n')
    temporary.replace(target)
    print('WROTE', target.relative_to(ROOT))
    if args.language == 'zh_Hans':
        alias = ROOT / 'native/inputs/localized-roles/zh.json'
        temporary = alias.with_suffix('.json.new')
        temporary.write_text(json.dumps(dict(document, language='zh', alias_of='zh_Hans'), ensure_ascii=False, indent=2) + '\n')
        temporary.replace(alias)


if __name__ == '__main__':
    main()
