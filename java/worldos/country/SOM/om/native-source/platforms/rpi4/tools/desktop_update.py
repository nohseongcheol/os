"""Build a small desktop update for images that are already in use."""
import hashlib
import json
from pathlib import Path
import subprocess

from prepare import ROOT


def payload():
    project = ROOT.parents[1]
    library = project / '한국어자바'
    subprocess.run(['make', '-s', '--no-print-directory', '-C', str(library)], check=True)
    mapping = [
        (ROOT / 'runtime/profile', 'etc/profile.d/jkoros.sh', 0o644),
        (ROOT / 'runtime/session', 'usr/local/bin/jkoros-session', 0o755),
        (ROOT / 'runtime/terminal', 'usr/local/bin/jkoros-terminal', 0o755),
        (ROOT / 'runtime/desktop-settings.py', 'usr/local/lib/jkoros/desktop-settings.py', 0o755),
        (ROOT / 'runtime/fonts.conf', 'etc/fonts/conf.d/60-jkoros-desktop.conf', 0o644),
        (ROOT / 'runtime/Xresources', 'etc/jkoros/Xresources', 0o644),
        (library / 'build/한국어자바.jar', 'opt/jkoros/lib/한국어자바.jar', 0o644),
    ]
    files = {}
    records = []
    for source, target, mode in mapping:
        data = source.read_bytes()
        files['files/' + target] = (mode, data)
        records.append({'path': target, 'mode': mode, 'sha256': hashlib.sha256(data).hexdigest()})
    installer = (ROOT / 'runtime/apply-desktop-update.py').read_bytes()
    identity = hashlib.sha256(json.dumps(records, sort_keys=True).encode() + installer).hexdigest()[:20]
    manifest = {'version': 'korean-desktop-' + identity,
                'base_id': json.loads((ROOT / 'dist/manifest.json').read_text())['base_id'],
                'files': records}
    files['manifest.json'] = (0o644, json.dumps(manifest, ensure_ascii=False, indent=2).encode() + b'\n')
    files['apply.py'] = (0o755, installer)
    return files
