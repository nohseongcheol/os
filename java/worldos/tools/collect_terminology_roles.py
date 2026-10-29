#!/usr/bin/env python3
"""Freeze offline, attributed IT terminology proposals by explicit language.

No network requests and no related-language fallback. A compound is a modern
project proposal, not evidence for a historical term or a native-speaker review.
Uncovered whole roles stay pending; never fill them with English or phonetics.
"""
import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'native'))
from terms import names, RESERVED
from paths import jkoros_root
from source_names import make_renamer, rename_source

REFERENCE = 'https://learn.microsoft.com/en-us/globalization/reference/microsoft-terminology'
XML_LANG = '{http://www.w3.org/XML/1998/namespace}lang'
NON_LATIN = set('am ar as be bg bn bo brx dz el fa gu he hi hy ja ka kk km kn ko ks ky lo mai ml mn mr my ne or pa ps sa sd si sr ta te tg th ti ug uk ur zh'.split())


def words(value):
    return re.findall(r'[A-Z]+(?=[A-Z][a-z]|$)|[A-Z]?[a-z]+|\d+', value.replace('_', ' '))


def key(value):
    return ' '.join(re.findall(r'[^\W_]+', value.casefold()))


def symbol(label):
    value = unicodedata.normalize('NFKC', label)
    value = ''.join(c if c == '_' or unicodedata.category(c)[0] in 'LMN' else '_' for c in value)
    value = re.sub('_+', '_', value).strip('_')
    if value and value[0].isdigit():
        value = '_' + value
    return value if value.isidentifier() else None


def proposal(parts, vocabulary, verb_last=False):
    """Prefer complete technical expressions over individual constituents."""
    output, evidence = [], []
    offset = 0
    # Marathi functional identifiers put an initial action after its object.
    verbs = {'read', 'write', 'send', 'receive', 'get', 'set', 'check', 'verify',
             'test', 'open', 'close', 'create', 'remove', 'delete', 'find',
             'parse', 'load', 'save', 'build', 'execute', 'invoke', 'draw',
             'allocate', 'release', 'compile', 'show', 'print', 'make'}
    if verb_last and len(parts) > 1 and parts[0].lower() in verbs:
        parts = parts[1:] + parts[:1]
    while offset < len(parts):
        for end in range(len(parts), offset, -1):
            phrase = key(' '.join(parts[offset:end]))
            if phrase in vocabulary:
                output.append(vocabulary[phrase]); evidence.append(phrase)
                offset = end
                break
        else:
            if parts[offset].isdigit():
                output.append(parts[offset]); offset += 1
            else:
                return None, []
    return symbol('_'.join(output)), evidence


def targets(code, member):
    # Script variants are explicit. Never assign Hindi to Marathi, or a
    # language to a neighbouring language because their alphabets overlap.
    code = code.replace('_', '-').lower()
    base = code.split('-')[0]
    if base == 'zh':
        return ['zh', 'zh_Hans'] if 'SIMPLIFIED' in member else ['zh_Hant']
    if base == 'sr':
        return ['sr_Cyrl'] if 'CYRILLIC' in member else ['sr_Latn']
    if base == 'bs':
        return ['bs_Cyrl'] if 'CYRILLIC' in member else ['bs', 'bs_Latn']
    if base == 'pa' and 'ARABIC' in member:
        return ['pa_Arab']
    variants = {'az': 'az_Latn', 'ms': 'ms_Latn', 'ky': 'ky_Cyrl',
                'mn': 'mn_Cyrl', 'tg': 'tg_Cyrl', 'uz': 'uz_Latn',
                'tk': 'tk_Latn', 'ha': 'ha_Latn', 'ff': 'ff_Latn'}
    if base == 'uz' and 'CYRILLIC' in member:
        return ['uz_Cyrl']
    return [base, variants[base]] if base in variants else [base]


def read_terms(stream, wanted, non_latin):
    candidates = collections.defaultdict(collections.Counter)
    language = None
    for event, entry in ET.iterparse(stream, events=('end',)):
        if entry.tag != 'termEntry':
            continue
        sections = entry.findall('langSet')
        source = next((s for s in sections if s.get(XML_LANG, '').startswith('en')), None)
        target = next((s for s in sections if not s.get(XML_LANG, '').startswith('en')), None)
        if source is not None and target is not None:
            language = target.get(XML_LANG)
            source_term = key(source.findtext('.//term', ''))
            target_term = target.findtext('.//term', '')
            value = symbol(target_term)
            if source_term in wanted and value and (not non_latin or any(ord(c) > 127 for c in value)):
                definition = source.findtext('.//descrip', '').lower()
                # Reject obvious non-computing senses of overloaded headwords.
                irrelevant = any(w in definition for w in ('social network', 'conversation thread', 'discussion thread'))
                if not irrelevant:
                    candidates[source_term][value] += 1
        entry.clear()
    # A repeated entry is not an additional vote by a translator. Prefer the
    # compact lexical form; retain the ambiguity in the snapshot for review.
    vocabulary = {term: min(options, key=lambda s: (len(s), s)) for term, options in candidates.items()}
    ambiguous = {term: sorted(options) for term, options in candidates.items() if len(options) > 1}
    return language, vocabulary, ambiguous


def freeze(language, roles, vocabulary, ambiguous, archive_hash, member):
    base = dict(names(language, include_snapshot=False))
    evidence = {}
    endonyms = json.loads((ROOT / 'native/inputs/language-endonyms.json').read_text())
    # The package stands for the edition's own language, not the English
    # translation of the word "English" in the intermediate role inventory.
    if language in endonyms['names']:
        base['한국어'] = endonyms['names'][language]
    overrides = json.loads((ROOT / 'native/inputs/functional-overrides.json').read_text())
    base.update(overrides['languages'].get(language, {}))
    protected = set(base)
    if language == 'mr':
        with (ROOT / 'native/inputs/marathi-role-words.tsv').open() as stream:
            vocabulary.update({row['word']: row['proposal'] for row in csv.DictReader(stream, delimiter='\t')})
    used = {unicodedata.normalize('NFKC', v) for v in base.values()}
    for original, role in roles.items():
        if original in base:
            continue
        if original == '한국어':
            continue
        phrase = key(' '.join(words(role)))
        if phrase in vocabulary:
            value, matched = vocabulary[phrase], [phrase]
        else:
            value, matched = proposal(words(role), vocabulary, language == 'mr')
        if not value:
            continue
        # Source files also carry these names. Reserve room for .java and
        # filesystem component limits; an oversized proposal stays pending.
        if len(value.encode()) > 220:
            continue
        if unicodedata.normalize('NFKC', value) in used:
            value += '_' + hashlib.sha256(original.encode()).hexdigest()[:8]
        if value in RESERVED:
            continue
        used.add(unicodedata.normalize('NFKC', value))
        base[original] = value
        evidence[original] = {'role': role, 'constituents': matched,
                              'status': 'whole-term-proposal' if len(matched) == 1 else 'functional-compound-proposal'}
    rejected = fit_guest_limits(base, protected)
    for original in rejected:
        evidence.pop(original, None)
    document = {'language': language, 'status': 'terminology-based-proposals',
                'native_review': 'pending', 'etymology_review': 'pending',
                'references': [REFERENCE], 'archive_sha256': archive_hash,
                'archive_member': member, 'names': base, 'roles': evidence,
                'ambiguities_for_review': ambiguous,
                'runtime_limit_pending': rejected,
                'pending_roles': {k: v for k, v in roles.items() if k not in base},
                'scope': 'Modern functional identifiers, not historically attested compounds. No related-language or English fallback.'}
    path = ROOT / 'native/inputs/localized-roles' / (language + '.json')
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.json.new')
    temporary.write_text(json.dumps(document, ensure_ascii=False, indent=2) + '\n')
    temporary.replace(path)
    return {'language': language, 'mapped': len(base), 'added': len(evidence),
            'pending': len(document['pending_roles'])}


def fit_guest_limits(mapping, protected):
    """Do not introduce names that break the existing guest filesystem.

Keep a whole role untranslated if its new spelling exceeds a real guest
limit. The original source and known working aliases remain unchanged.
Rejection is explicit coverage debt, not a silently truncated identifier.
"""
    root = jkoros_root()
    rejected = {}
    for path in sorted((root / 'example').rglob('*')):
        if not path.is_file():
            continue
        relative = '/' + str(path.relative_to(root))
        rename = make_renamer(mapping)
        if len(rename(relative).encode()) <= 62:
            continue
        for original in list(mapping):
            if original not in protected and original in path.name:
                rejected[original] = 'guest-path-63-byte-limit'
                mapping.pop(original)
    libraries = list((root / 'platforms/rpi4-native/파이썬연결/라이브러리').glob('*.py'))
    libraries += [root / 'example/python/한국어.py']
    for path in libraries:
        rename = make_renamer(mapping)
        if len(('/lib/'+rename(path.name)).encode()) > 63:
            if path.stem in protected:
                raise ValueError('Protected Python module name exceeds guest /lib path limit: '+rename(path.name))
            if path.stem in mapping:
                mapping.pop(path.stem)
                rejected[path.stem] = 'guest-library-path-63-byte-limit'
        text = path.read_text()
        translated = rename_source(str(path), text, make_renamer(mapping))
        excess = len(translated.encode()) - 16384
        if excess <= 0:
            continue
        tokens = collections.Counter(re.findall(r'[^\W\d]\w*', text))
        savings = sorted(((tokens[k] * (len(v.encode()) - len(k.encode())), k)
                          for k, v in mapping.items() if k not in protected), reverse=True)
        for saving, original in savings:
            if saving <= 0 or excess <= 0:
                break
            mapping.pop(original)
            rejected[original] = 'embedded-python-16384-byte-limit'
            excess -= saving
        # Account for symbolic names embedded in strings as well as code.
        while len(rename_source(str(path), text, make_renamer(mapping)).encode()) > 16384:
            candidate = next((k for saving, k in savings if saving > 0 and k in mapping), None)
            if candidate is None:
                raise ValueError('Existing protected aliases already exceed guest Python limit: ' + str(path))
            mapping.pop(candidate); rejected[candidate] = 'embedded-python-16384-byte-limit'
    return rejected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', type=Path, default=ROOT / 'build/country-localization/translation-cache/MicrosoftTermCollection.zip')
    parser.add_argument('--languages', nargs='+')
    args = parser.parse_args()
    roles = dict(names('en'))
    paths = list((ROOT / 'country').glob('*/native.json')) + list((ROOT / 'country').glob('*/*/native.json'))
    selected = set(args.languages or {json.loads(p.read_text())['language'] for p in paths}) - {'en', 'ko'}
    wanted = set()
    for role in roles.values():
        parts = words(role)
        wanted.update(key(' '.join(parts[a:b])) for a in range(len(parts)) for b in range(a + 1, len(parts) + 1))
    archive_hash = hashlib.sha256(args.archive.read_bytes()).hexdigest()
    report = []
    with zipfile.ZipFile(args.archive) as archive:
        for member in archive.namelist():
            if not member.endswith('.tbx'):
                continue
            with archive.open(member) as stream:
                # Detect the declared target without loading an entire TBX.
                sample = stream.read(16384).decode('utf-8-sig', errors='ignore')
            codes = re.findall(r'<langSet xml:lang="([^"]+)"', sample)
            code = next((c for c in codes if not c.startswith('en')), None)
            if code is None:
                continue
            languages = selected.intersection(targets(code, member))
            if not languages:
                continue
            with archive.open(member) as stream:
                non_latin = code.split('-')[0] in NON_LATIN and 'LATIN' not in member
                unused, vocabulary, ambiguous = read_terms(stream, wanted, non_latin)
            for language in sorted(languages):
                row = freeze(language, roles, dict(vocabulary), ambiguous, archive_hash, member)
                report.append(row); print(json.dumps(row), flush=True)
                selected.remove(language)
    result = {'results': report, 'languages_without_terminology_source': sorted(selected),
              'all_native_reviews_complete': False, 'all_etymologies_verified': False}
    destination = ROOT / 'build/localization-fix/terminology-collection.json'
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
