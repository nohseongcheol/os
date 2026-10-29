#!/usr/bin/env python3
"""Compress the generated installation images and record delivery hashes."""
import gzip
import json
from pathlib import Path
import shutil
from prepare import ROOT, digest


def main():
    dist = ROOT / 'dist'
    for name in ['jkoros-rpi4-system.img', 'jkoros-user.img']:
        source = dist / name
        output = dist / (name + '.gz')
        temporary = dist / (name + '.gz.next')
        with source.open('rb') as src, temporary.open('wb') as dest:
            with gzip.GzipFile(fileobj=dest, mode='wb', compresslevel=1, mtime=0) as packed:
                shutil.copyfileobj(src, packed, length=1024 * 1024)
        temporary.replace(output)
    names = ['jkoros-rpi4-system.img', 'jkoros-rpi4-system.img.gz', 'jkoros-user.img',
             'jkoros-user.img.gz', 'openjdk25-jdk-linux-aarch64-musl.tar.gz',
             'openjdk25-jre-linux-aarch64-musl.tar.gz', '中文Java.jar']
    metadata = []
    for name in names:
        path = dist / name
        metadata.append({'file': name, 'bytes': path.stat().st_size, 'sha256': digest(path)})
    (dist / 'SHA256SUMS').write_text(''.join(item['sha256'] + '  ' + item['file'] + '\n' for item in metadata))
    (dist / 'delivery.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(metadata, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
