#!/usr/bin/env python3
"""Fetch pinned distribution inputs; never install packages on the host."""
import argparse
import concurrent.futures
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    'alpine-virt-3.24.1-x86_64.iso': ('https://dl-cdn.alpinelinux.org/alpine/v3.24/releases/x86_64/alpine-virt-3.24.1-x86_64.iso', 'e73a6241bd5f3c5c2d4d38c02cc52c378c0415a7c888bd292066bf36e0f41a39'),
    'alpine-minirootfs-3.24.1-x86_64.tar.gz': ('https://dl-cdn.alpinelinux.org/alpine/v3.24/releases/x86_64/alpine-minirootfs-3.24.1-x86_64.tar.gz', '41f73e3cf5fa919b8aa5ca6b30dc48f0da2720776d7423e2a7748211456fe081'),
    'main-APKINDEX.tar.gz': ('https://dl-cdn.alpinelinux.org/alpine/v3.24/main/x86_64/APKINDEX.tar.gz', None),
    'community-APKINDEX.tar.gz': ('https://dl-cdn.alpinelinux.org/alpine/v3.24/community/x86_64/APKINDEX.tar.gz', None),
    'cldr48-supplementalData.xml': ('https://raw.githubusercontent.com/unicode-org/cldr/release-48/common/supplemental/supplementalData.xml', None),
    'apk-tools-static-3.0.8-r0.apk': ('https://dl-cdn.alpinelinux.org/alpine/v3.24/main/x86_64/apk-tools-static-3.0.8-r0.apk', None),
}

def fetch(name, url, expected=None):
    target = ROOT / 'vendor' / name
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        if expected and digest != expected:
            raise ValueError('Cached hash mismatch: ' + name)
        return {'file': name, 'url': url, 'sha256': digest}
    request = urllib.request.Request(url, headers={'User-Agent': 'WorldOS-build/1.0'})
    temporary = target.with_name(target.name + '.download')
    digest = hashlib.sha256()
    with urllib.request.urlopen(request, timeout=60) as response, temporary.open('wb') as output:
        while True:
            block = response.read(1024 * 1024)
            if not block:
                break
            output.write(block)
            digest.update(block)
    if expected and digest.hexdigest() != expected:
        raise ValueError('Downloaded hash mismatch: ' + name)
    temporary.replace(target)
    print('FETCHED', name, target.stat().st_size, flush=True)
    return {'file': name, 'url': url, 'sha256': digest.hexdigest()}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url')
    parser.add_argument('--name')
    args = parser.parse_args()
    if args.url:
        print(json.dumps(fetch(args.name, args.url), ensure_ascii=False))
        return
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(fetch, name, url, digest) for name, (url, digest) in SOURCES.items()]
        results = [future.result() for future in futures]
    (ROOT / 'vendor/sources.json').write_text(json.dumps(results, indent=2) + '\n')

if __name__ == '__main__':
    main()
