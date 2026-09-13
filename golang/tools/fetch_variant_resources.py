#!/usr/bin/env python3
"""Fetch public, pinned generation-only resources; never needed by OS builds."""
import hashlib
import json
from pathlib import Path
import sys
import urllib.request
import zipfile
import io
import tarfile

destination = Path(sys.argv[1]).resolve()
destination.mkdir(parents=True, exist_ok=True)
url = 'https://raw.githubusercontent.com/unicode-org/cldr/release-48/tools/cldr-code/src/main/resources/org/unicode/cldr/util/data/language_script.tsv'
data = urllib.request.urlopen(url, timeout=40).read()
(destination / 'language_script.tsv').write_bytes(data)
for package, version in [('pykakasi', '2.0.8'), ('jaconv', '0.3.4'), ('klepto', '0.2.4'), ('dill', '0.3.4'), ('pox', '0.3.0')]:
    metadata = json.load(urllib.request.urlopen('https://pypi.org/pypi/{}/{}/json'.format(package, version), timeout=40))
    wheels = [item for item in metadata['urls'] if item['filename'].endswith('.whl') and ('none-any' in item['filename'])]
    if not wheels:
        item = next(item for item in metadata['urls'] if item['filename'].endswith('.tar.gz'))
        contents = urllib.request.urlopen(item['url'], timeout=40).read()
        assert hashlib.sha256(contents).hexdigest() == item['digests']['sha256']
        with tarfile.open(fileobj=io.BytesIO(contents), mode='r:gz') as archive:
            for member in archive:
                parts = Path(member.name).parts
                if member.isfile() and len(parts) > 1 and (parts[1] == package or 'LICENSE' in parts[-1].upper()):
                    if '..' in parts or member.name.startswith('/'):
                        raise RuntimeError('Unsafe source path')
                    target = destination / 'python' / Path(*parts[1:])
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(archive.extractfile(member).read())
        print(package, version, item['digests']['sha256'], flush=True)
        continue
    item = wheels[0]
    contents = urllib.request.urlopen(item['url'], timeout=40).read()
    assert hashlib.sha256(contents).hexdigest() == item['digests']['sha256']
    with zipfile.ZipFile(io.BytesIO(contents)) as archive:
        for name in archive.namelist():
            path = Path(name)
            if path.is_absolute() or '..' in path.parts:
                raise RuntimeError('Unsafe wheel path')
        archive.extractall(str(destination / 'python'))
    print(package, version, item['digests']['sha256'], flush=True)
