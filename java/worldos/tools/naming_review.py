"""Apply function-specific proposals without treating them as native review."""
import hashlib
import json
from pathlib import Path
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
COPYRIGHT = '// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved\n'.encode()


def without_copyright(data):
    return data[len(COPYRIGHT):] if data.startswith(COPYRIGHT) else data


def matches_owned(data, expected):
    return expected is not None and any(hashlib.sha256(value).hexdigest() == expected
                                       for value in (data, without_copyright(data)))


def review():
    return json.loads((ROOT / 'naming/functional-review.json').read_text())


def apply_terms(terms):
    evidence = review()
    for language, entry in evidence['languages'].items():
        if language not in terms:
            continue
        rows = terms[language]
        for concept, text in entry['terms'].items():
            identifier = unicodedata.normalize('NFC', text)
            if not identifier.isidentifier():
                raise ValueError('Invalid reviewed identifier: ' + identifier)
            rows[concept] = dict(rows[concept], text=text, identifier=identifier,
                status='proposal', source='WorldOS function review 2026-10-18; naming/functional-review.json',
                native_review='pending', implementation_role_review='checked',
                etymology_review='pending', references=entry.get('references', []))
        used = {}
        for concept, row in rows.items():
            if row['identifier'] in used:
                raise ValueError('Ambiguous reviewed names: ' + language + '/' + concept + '/' + used[row['identifier']])
            used[row['identifier']] = concept
    return terms
