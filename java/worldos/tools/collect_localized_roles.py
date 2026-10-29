#!/usr/bin/env python3
"""Freeze whole-name translation proposals; builds never call a translator.

Only public English role labels are sent, never project source or user files.
The output is a machine proposal, not a historical/native-speaker certificate.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import html
import json
import os
from pathlib import Path
import re
import sys
import threading
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'native'))
from terms import names

CACHE = ROOT / 'build/country-localization/translation-cache'
DEST = ROOT / 'native/inputs/localized-roles'
REFERENCE = 'https://docs.cloud.google.com/translate/docs/languages'
ENDPOINT = 'https://translation.googleapis.com/language/translate/v2'
LOCK = threading.Lock()
LAST_REQUEST = [0.0]
STOP = threading.Event()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    data = json.dumps(value, ensure_ascii=False, indent=2) + '\n'
    temporary = path.with_suffix(path.suffix + '.new')
    temporary.write_text(data)
    temporary.replace(path)


def phrase(name):
    words = re.findall(r'[A-Z]+(?=[A-Z][a-z]|$)|[A-Z]?[a-z]+|\d+', name)
    return ' '.join(words) or name


def symbol(label):
    label = unicodedata.normalize('NFC', html.unescape(label)).strip()
    value = ''.join(c if c == '_' or unicodedata.category(c)[0] in 'LMN' else '_' for c in label)
    value = re.sub('_+', '_', value).strip('_')
    if value and not value[0].isidentifier():
        value = '_' + value
    if not value or not value.isidentifier():
        raise ValueError('Not a source identifier: ' + repr(label))
    return value


def supported():
    text = (CACHE / 'google-languages.html').read_text()
    return set(html.unescape(code).strip() for code in re.findall(
        r'<td[^>]*>\s*<code[^>]*>([a-zA-Z-]+)</code>', text))


def target(language, available):
    # Explicit script variants must not silently receive another writing system.
    overrides = {'zh': 'zh-CN', 'zh_Hans': 'zh-CN', 'zh_Hant': 'zh-TW',
                 'ms_Latn': 'ms', 'az_Latn': 'az', 'uz_Latn': 'uz',
                 'mn_Cyrl': 'mn', 'ky_Cyrl': 'ky', 'tg_Cyrl': 'tg',
                 'bs_Cyrl': None, 'sr_Cyrl': 'sr', 'mni': 'mni-Mtei',
                 'kok': 'gom', 'nb': 'no', 'fil': 'tl'}
    code = overrides.get(language, language)
    if code in ('zh-CN', 'zh-TW'):
        return code if 'zh-CN' in available or 'zh' in available else None
    return code if code and code in available else None


def translate(language, lines):
    source = '\n'.join(lines)
    key = hashlib.sha256((language + '\0' + source).encode()).hexdigest()
    cached = CACHE / language / (key + '.json')
    if cached.exists():
        return json.loads(cached.read_text())['translations']
    if STOP.is_set():
        raise RuntimeError('Translation service stopped after an access/rate-limit response')
    # Share a conservative request interval across workers. No proxy switching,
    # captcha bypass, or retries after an access/rate-limit rejection.
    with LOCK:
        delay = .4 - (time.monotonic() - LAST_REQUEST[0])
        if delay > 0:
            time.sleep(delay)
        LAST_REQUEST[0] = time.monotonic()
    key_value = os.environ.get('WORLDOS_TRANSLATION_API_KEY')
    if not key_value:
        raise RuntimeError('WORLDOS_TRANSLATION_API_KEY is required for the documented Cloud Translation API; no public-web endpoint fallback is used')
    payload = json.dumps({'source': 'en', 'target': language, 'format': 'text', 'q': lines}).encode()
    request = urllib.request.Request(ENDPOINT, data=payload, headers={
        'Content-Type': 'application/json', 'X-goog-api-key': key_value})
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            result = json.load(response)
    except urllib.error.HTTPError as error:
        if error.code in (401, 403, 429):
            STOP.set()
        raise
    output = [html.unescape(part['translatedText']) for part in result['data']['translations']]
    if len(output) != len(lines):
        raise ValueError('Translation count mismatch')
    write(cached, {'source': lines, 'translations': output, 'endpoint': ENDPOINT})
    return output


def collect(language, code, roles):
    destination = DEST / (language + '.json')
    revision = hashlib.sha256(json.dumps(roles, sort_keys=True).encode()).hexdigest()
    if destination.exists():
        prior = json.loads(destination.read_text())
        if prior.get('role_revision') == revision:
            print('CACHED', language, len(prior['names']), flush=True)
            return {'language': language, 'status': 'cached', 'names': len(prior['names'])}
    base = dict(names(language))
    keys = [key for key in roles if key not in base]
    translated = {}
    batch, length = [], 0
    def flush():
        if not batch:
            return
        result = translate(code, [phrase(roles[key]) for key in batch])
        translated.update(zip(batch, result))
        print('FETCHED', language, len(translated), '/', len(keys), flush=True)
        batch.clear()
    for key in keys:
        size = len(phrase(roles[key])) + 1
        if length + size > 3200 or len(batch) >= 100:
            flush(); length = 0
        batch.append(key); length += size
    flush()
    used = {unicodedata.normalize('NFKC', value) for value in base.values()}
    collisions = []
    for key in keys:
        value = symbol(translated[key])
        original, suffix = value, 2
        # Keep distinct source roles distinct, including Python NFKC aliases.
        while unicodedata.normalize('NFKC', value) in used:
            value = original + '_' + str(suffix); suffix += 1
        if value != original:
            collisions.append({'original': key, 'proposal': original, 'identifier': value})
        used.add(unicodedata.normalize('NFKC', value)); base[key] = value
    document = {'language': language, 'translation_language': code, 'role_revision': revision,
                'status': 'machine-proposal', 'native_review': 'pending', 'etymology_review': 'pending',
                'language_reference': REFERENCE, 'translation_endpoint': ENDPOINT,
                'source_scope': 'Whole English functional labels; no project source text transmitted',
                'names': base, 'translated_labels': translated, 'collisions': collisions}
    write(destination, document)
    print('FROZEN', language, len(base), 'collisions', len(collisions), flush=True)
    return {'language': language, 'status': 'frozen', 'names': len(base), 'collisions': len(collisions)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--languages', nargs='+')
    parser.add_argument('--all', action='store_true')
    parser.add_argument('--jobs', type=int, choices=range(1, 5), default=2)
    parser.add_argument('--plan', action='store_true')
    args = parser.parse_args()
    roles = dict(names('en'))
    roles.setdefault('국가실행기', 'CountryLauncher')
    available = supported()
    paths = list((ROOT / 'country').glob('*/native.json')) + list((ROOT / 'country').glob('*/*/native.json'))
    languages = sorted({json.loads(p.read_text())['language'] for p in paths}) if args.all else (args.languages or ['mr'])
    supported_languages = {language: target(language, available) for language in languages if language not in ('ko', 'en')}
    pending = [language for language, code in supported_languages.items() if not code]
    eligible = [(language, code) for language, code in supported_languages.items() if code]
    plan = {'supported': dict(eligible), 'unsupported': pending, 'reference': REFERENCE}
    write(CACHE / 'plan.json', plan)
    if args.plan:
        print(json.dumps(plan, ensure_ascii=False, indent=2)); return
    def run(item):
        language, code = item
        try:
            return collect(language, code, roles)
        except Exception as error:
            print('FAILED', language, str(error), flush=True)
            return {'language': language, 'status': 'failed', 'error': str(error)}
    with ThreadPoolExecutor(max_workers=args.jobs) as executor:
        results = list(executor.map(run, eligible))
    write(CACHE / 'collection.json', {'results': results, 'unsupported': pending})
    if any(row['status'] == 'failed' for row in results):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
