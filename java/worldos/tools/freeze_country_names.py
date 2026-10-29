#!/usr/bin/env python3
"""Freeze territory names from the project's pinned CLDR 48 release.

Unknown translations retain an explicit ISO identifier and a pending status.
They never borrow the name of another country or another language.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'native'))
from country_naming import country_policy, identifier

# A country namespace and a language namespace must stay distinct when CLDR's
# short country name is also used by the language API in the same source tree.
COUNTRY_IDENTIFIERS = {
    ('EST', 'et'): 'Eesti_Vabariik',
    ('IDN', 'id'): 'Republik_Indonesia',
    ('MNG', 'mn'): 'Монгол_Улс',
    ('THA', 'th'): 'ประเทศไทย',
    ('MMR', 'my'): 'မြန်မာနိုင်ငံ',
}


def freeze(archive):
    with zipfile.ZipFile(str(archive)) as bundle:
        files = set(bundle.namelist())
        parents = {}
        supplemental = ET.fromstring(bundle.read('common/supplemental/supplementalData.xml'))
        for row in supplemental.findall('./parentLocales/parentLocale'):
            if row.get('component'):
                continue
            for locale in row.get('locales', '').split():
                parents[locale] = row.get('parent')
        documents = {}

        def territory(locale, code, seen=()):
            if not locale or locale == 'root' or locale in seen:
                return None
            filename = 'common/main/' + locale + '.xml'
            if filename in files:
                if locale not in documents:
                    documents[locale] = ET.fromstring(bundle.read(filename))
                document = documents[locale]
                alias = document.find('./alias')
                if alias is not None and alias.get('source') != 'locale':
                    return territory(alias.get('source'), code, seen + (locale,))
                for row in document.findall('./localeDisplayNames/territories/territory'):
                    if row.get('type') == code and not row.get('alt') and row.text not in ('↑↑↑', '∅∅∅', None):
                        return row.text, locale
            parent = parents.get(locale, locale.rpartition('_')[0])
            return territory(parent, code, seen + (locale,))

        rows = {}
        for country, policy in sorted(country_policy().items()):
            for language in policy['languages']:
                found = territory(language, policy['alpha2'])
                label, source = found if found else (country, None)
                symbol = COUNTRY_IDENTIFIERS.get((country, language), identifier(label))
                supported = symbol.isidentifier()
                if not supported:
                    # Python 3.6's Unicode tables predate some CLDR scripts.
                    # Keep their real display name; do not emit invalid code.
                    symbol = country
                rows[country + '/' + language] = {
                    'label': label, 'identifier': symbol,
                    'source_locale': source,
                    'identifier_policy': 'country-name-with-namespace-disambiguation' if (country, language) in COUNTRY_IDENTIFIERS else 'cldr-name-as-code-identifier',
                    'status': ('pending-identifier-toolchain-support' if not supported else
                               'cldr-territory-name' if found else 'pending-country-name-translation'),
                    'os_name': 'J' + country.title() + 'OS'}
        license_name = next(name for name in files if name.lower() in ('license.txt', 'license'))
        license_text = bundle.read(license_name).decode('utf-8')
    result = {'version': 1, 'release': 'CLDR 48',
              'source': 'https://unicode.org/Public/cldr/48/cldr-common-48.zip',
              'archive_sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
              'namespace_policy': 'Country ISO identity; edition language determines country-name spelling. OS names are project proper names formed from J + titlecase ISO alpha-3 + OS.',
              'names': rows}
    destination = ROOT / 'native/inputs/country-names.json'
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    destination.with_name('country-names-LICENSE.txt').write_text(license_text)
    print('Country/language names:', len(rows), 'pending:', sum(r['source_locale'] is None for r in rows.values()))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    freeze(parser.parse_args().archive)
