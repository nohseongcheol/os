#!/usr/bin/env python3
"""Expose missing script editions; CLDR secondary is not a modern-use verdict."""
from pathlib import Path
import unicodedata
from generate_script_variants import profiles, rows, table
from variant_terms import INDIA
from native_source import local_path

root = Path(__file__).resolve().parents[1]
scripts = {}
for row in rows(root / '명명/cldr48-language-script.tsv'):
    if not row or row[0].startswith('#') or len(row) < 5:
        continue
    language, label, status, script, script_label = row[:5]
    scripts.setdefault(language, []).append((script, status, script_label))
country_locales = {row[0]: row[3] for row in rows(root / '나라-소스-언어선택.tsv')[1:]}
selected = {(country, locale.split('_')[0]) for country, locale in country_locales.items()}
selected.update(('IND', language) for language, _, _, _ in INDIA)
implemented = {(record[0], record[1]) for record in profiles()}
coverage = []
name_cache = {}


def has_existing_script(country, language, script, script_label):
    locale = country_locales.get(country, '')
    if locale.split('_')[0] != language:
        return False
    explicit = locale.split('_')[1:] or [item[0] for item in scripts.get(language, []) if item[1] == 'primary']
    if explicit != [script]:
        return False
    if country not in name_cache:
        name_cache[country] = ''.join(row[1] for row in rows(local_path(local_path(root / '나라' / country, '소스'), '이름대응표.tsv'))[1:])
    prefix = {'Latn': 'LATIN', 'Cyrl': 'CYRILLIC', 'Arab': 'ARABIC', 'Deva': 'DEVANAGARI',
              'Beng': 'BENGALI', 'Hans': 'CJK', 'Hant': 'CJK', 'Jpan': 'CJK',
              'Hang': 'HANGUL', 'Kore': 'HANGUL', 'Orya': 'ORIYA', 'Guru': 'GURMUKHI',
              'Ethi': 'ETHIOPIC', 'Nkoo': 'NKO'}.get(script, script_label.upper())
    return any(unicodedata.name(ch, '').startswith(prefix + ' ') for ch in name_cache[country])
for country, language in sorted(selected):
    choices = scripts.get(language, [])
    if len(choices) < 2 and (country, language) != ('JPN', 'ja'):
        continue
    if language == 'ja':
        choices = choices + [('Hira', 'project-script-edition', 'Hiragana'), ('Kana', 'project-script-edition', 'Katakana')]
    for script, classification, label in choices:
        profile = language + '_' + script
        available = (country, profile) in implemented
        existing = has_existing_script(country, language, script, label)
        status = 'source-added-language-review-pending' if available else ('existing-country-source-language-review-pending' if existing else 'not-implemented')
        coverage.append([country, profile, classification, label, status,
                         'CLDR secondary may include historical usage; review before implementation'])
represented = {(row[0], row[1]) for row in coverage}
for country, profile in sorted(implemented - represented):
    coverage.append([country, profile, 'project-script-edition', profile.split('_')[1],
                     'source-added-language-review-pending', 'Independent edition; terminology incomplete'])
coverage.sort()
header = ['country', 'profile', 'cldr_classification', 'script_name', 'implementation_status', 'note']
(root / '문자판-범위점검.tsv').write_text(table(header, coverage), encoding='utf-8')
pending = [row for row in coverage if row[4] == 'not-implemented']
(root / '문자판-미구현.tsv').write_text(table(header, pending), encoding='utf-8')
print(len(coverage), 'script candidates;', len(pending), 'not implemented (includes historical-script candidates)')
