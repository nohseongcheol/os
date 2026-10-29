"""Country codes select territories; language tags select whole-role names.

The tables contain project proposals. A dictionary etymology is evidence about
a word, never certification of every new compound containing that word.
"""
import csv
from functools import lru_cache
import importlib.util
import json
from pathlib import Path
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[1]


@lru_cache(maxsize=8)
def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def identifier(label):
    # Keep marks used by Indic and other writing systems. Spaces separate
    # complete words; do not invent translations by splitting identifiers.
    value = unicodedata.normalize('NFC', label)
    value = ''.join(c if c == '_' or unicodedata.category(c)[0] in 'LMN' else '_' for c in value)
    return re.sub('_+', '_', value).strip('_')


CORE_ROLES = {
    '동적기억공간': 'heap', '쌓임공간': 'stack', '저장기': 'register',
    '화면요소': 'widget', '주부트기록': 'boot_record',
}
PATH_ROLES = {'구현': 'implementation', '체계호출': 'system_call',
              '오류번호': 'errno', '파일제어': 'file_control', '파일상태': 'file_status'}
SHELL_ROLES = {'명령해석기': 'shell_name', '글길이': 'text_length',
               '글같음': 'text_equal', '줄읽기': 'read_line', '도움말': 'print_help'}


@lru_cache(maxsize=None)
def additions(language):
    if language == 'ko':
        return {}
    lexicon = load_module('country_native_lexicon', ROOT / 'native/inputs/naming_lexicon.py')
    shell = load_module('country_shell_lexicon', ROOT / 'naming/upstream/shell_terms.py')
    words = lexicon.lexicon().get(language, {})
    roles = dict(CORE_ROLES, **PATH_ROLES)
    result = {old: identifier(words[role]) for old, role in roles.items() if role in words}
    shell_words = shell.vocabulary(language)
    result.update({old: identifier(shell_words[role]) for old, role in SHELL_ROLES.items() if role in shell_words})
    if language == 'en':
        frozen = json.loads((ROOT / 'native/inputs/english-source-names.json').read_text())
        result.update(frozen['names'])
        compounds = json.loads((ROOT / 'native/inputs/english-composed-names.json').read_text())
        result.update(compounds['names'])
        with (ROOT / 'native/inputs/english-functional-names.tsv').open() as stream:
            result.update({row['original']: row['localized'] for row in csv.DictReader(stream, delimiter='\t')})
    return result


@lru_cache(maxsize=1)
def country_policy():
    countries = {c['alpha_3']: c for c in json.loads((ROOT / 'naming/countries.json').read_text())['3166-1']}
    with (ROOT / 'native/inputs/representatives.tsv').open() as stream:
        representatives = {r['country_alpha3']: r for r in csv.DictReader(stream, delimiter='\t')}
    languages = {}
    for edition in json.loads((ROOT / 'editions.json').read_text()):
        languages.setdefault(edition['country'], []).append(edition['language'])
    return {code: {'alpha2': country['alpha_2'], 'name': country['name'],
                   'representative_language': representatives[code]['language'],
                   'cldr_language_editions': sorted(set(languages[code])),
                   'languages': sorted(set(languages[code]) | {representatives[code]['language']})}
            for code, country in countries.items()}


@lru_cache(maxsize=1)
def country_names():
    return json.loads((ROOT / 'native/inputs/country-names.json').read_text())['names']


@lru_cache(maxsize=2048)
def names_for_country(country, language):
    """Country namespaces are independent of the edition's language glossary."""
    from terms import names
    result = dict(names(language))
    identity = country_names()[country + '/' + language]
    result.update({'한국': identity['identifier'], '제이코로스': identity['os_name']})
    if len(set(result.values())) != len(result):
        raise ValueError('Country namespace collides with a code role: ' + country + '/' + language)
    return result


def country_source_identity(original, text, mapping):
    """Brand the managed system's own reported name; preserve native ABI names."""
    if original.startswith('원천/') and original.endswith('.java'):
        return text.replace('"jkoros"', '"' + mapping['제이코로스'] + '"')
    return text


def validate_edition(folder, config):
    relative = folder.relative_to(ROOT / 'country')
    code = relative.parts[0]
    policy = country_policy()[code]
    if config['country'] != code:
        raise ValueError('Country code does not match folder: ' + str(folder))
    expected = policy['representative_language'] if len(relative.parts) == 1 else relative.parts[1]
    if config['language'] != expected or expected not in policy['languages']:
        raise ValueError('Language does not match territory edition: ' + str(folder))
    return {'country_code': code, 'country_name': policy['name'],
            'language': expected, 'selection': 'representative' if len(relative.parts) == 1 else 'explicit-language-edition',
            'country_source': 'naming/countries.json (ISO 3166-1)',
            'language_source': 'Unicode CLDR 48; native/inputs/representatives.tsv; editions.json',
            'namespace': country_names()[code + '/' + expected],
            'native_review': 'pending', 'etymology_review': 'partial; see term evidence'}
