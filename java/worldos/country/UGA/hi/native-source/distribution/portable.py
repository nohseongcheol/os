#!/usr/bin/env python3
"""Portable source release: exclude reproducible inputs, restore them on Ubuntu."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import platform
import posixpath
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
STATE = '.portable-state.json'
SKIP_DIRS = {'.git', '.vbox', '__pycache__', '.pytest_cache', '.cache',
             '.download-cache', 'build', 'dist', 'परिणाम'}
APT = ['build-essential', 'clang', 'binutils-aarch64-linux-gnu', 'libnewlib-dev',
       'default-jdk-headless', 'python3', 'python3-pil', 'curl', 'ca-certificates',
       'xz-utils', 'grub-common', 'grub-pc-bin', 'xorriso', 'mtools', 'dosfstools',
       'squashfs-tools', 'kmod', 'busybox-static', 'e2fsprogs', 'fontconfig',
       'qemu-system-arm', 'qemu-system-x86']


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def safe_name(name):
    p = PurePosixPath(name)
    if not name or p.is_absolute() or '..' in p.parts or '\\' in name:
        raise ValueError('Unsafe package path: ' + name)
    return str(p)


def safe_link(name, target):
    if not target or target.startswith('/') or '\\' in target:
        raise ValueError('External archive link: ' + name)
    resolved = posixpath.normpath(posixpath.join(posixpath.dirname(name), target))
    safe_name(resolved)


def config(root):
    return json.loads((root / 'distribution/dependencies.json').read_text(encoding='utf-8'))


def vendor_index(root):
    """Map reproducible extracted WorldOS files; retain any local modifications."""
    indexes, mapping = {}, {}
    for path in sorted((root / 'कंट्री_मान').glob('*/native.json')):
        data = json.loads(path.read_text())
        archive = path.parent / 'native-vendor.tar.gz'
        digest = data['vendor_sha256']
        if digest not in indexes:
            if sha(archive) != digest:
                raise ValueError('Vendor archive checksum mismatch: ' + str(archive))
            with tarfile.open(str(archive)) as stream:
                indexes[digest] = {m.name: hashlib.sha256(stream.extractfile(m).read()).hexdigest()
                                   for m in stream if m.isfile()}
        prefix = str((path.parent / data['source']).relative_to(root)) + '/'
        mapping[prefix] = (indexes[digest], str(path.parent.relative_to(root)))
    return mapping


def pack(root, output, level=9):
    cfg = config(root)
    output = output.absolute()
    output.parent.mkdir(parents=True, exist_ok=True)
    selected, downloadable = [], {}
    for dependency in cfg['downloads']:
        files = []
        for entry in dependency['files']:
            p = root / entry['path']
            if not p.exists() or (p.is_file() and not p.is_symlink() and sha(p) == entry['sha256']):
                files.append(entry)
                downloadable[entry['path']] = True
        if files:
            selected.append(dict(dependency, files=files))
    stock = vendor_index(root) if cfg['project'] == 'worldos' else {}
    overrides, payload, skipped = set(), {}, {}
    files = []
    for directory, folders, names in os.walk(str(root), followlinks=False):
        folders.sort(); names.sort()
        parent = Path(directory)
        for name in list(folders):
            p = parent / name
            rel = str(p.relative_to(root))
            special = (cfg['project'] == 'worldos' and len(p.relative_to(root).parts) == 3
                       and p.relative_to(root).parts[0] == 'कंट्री_मान' and name == 'host')
            if name in SKIP_DIRS or special or rel in cfg.get('exclude_dirs', []):
                folders.remove(name); skipped[rel + '/'] = 'cache/output'
            elif p.is_symlink():
                folders.remove(name); names.append(name)
        for name in sorted(names):
            p = parent / name
            rel = str(p.relative_to(root))
            if p.absolute() in (output, Path(str(output) + '.sha256'), Path(str(output) + '.report.json')) or rel == STATE or name.endswith(('.pyc', '.pyo', '.log')):
                skipped[rel] = 'generated'; continue
            if rel in cfg.get('exclude_files', []) or name == '.vendor-sha256':
                skipped[rel] = 'regenerated'; continue
            if rel in downloadable:
                skipped[rel] = 'download'; continue
            if p.is_symlink():
                target = os.readlink(str(p))
                if os.path.isabs(target):
                    resolved = p.resolve()
                    if root not in resolved.parents:
                        raise ValueError('Cannot package external symlink: ' + rel)
                    target = os.path.relpath(str(resolved), str(p.parent))
                safe_link(rel, target)
                payload[rel] = {'link': target}
            elif p.is_file():
                digest = sha(p)
                omitted = False
                for prefix, (index, country) in stock.items():
                    if rel.startswith(prefix + 'platforms/rpi4-native/vendor/'):
                        if index.get(rel[len(prefix):]) == digest:
                            skipped[rel] = 'bundled dependency'; omitted = True
                        else:
                            overrides.add(country)
                        break
                if omitted:
                    continue
                payload[rel] = {'sha256': digest}
            else:
                raise ValueError('Unsupported source file: ' + rel)
            files.append((p, rel))
    state = {'format': 1, 'project': cfg['project'], 'files': payload,
             'downloads': selected, 'vendor_overrides': sorted(overrides)}
    with tempfile.TemporaryDirectory(prefix='portable-pack-') as temporary:
        staged = Path(temporary) / output.name
        with tarfile.open(str(staged), 'w:xz', preset=level) as archive:
            for p, rel in files:
                info = archive.gettarinfo(str(p), arcname=rel)
                info.uid = info.gid = 0; info.uname = info.gname = ''; info.mtime = 0
                if 'link' in payload[rel]:
                    info.type = tarfile.SYMTYPE; info.linkname = payload[rel]['link']; info.size = 0
                    archive.addfile(info)
                else:
                    info.type = tarfile.REGTYPE; info.linkname = ''; info.size = p.stat().st_size
                    with p.open('rb') as stream:
                        archive.addfile(info, stream)
            data = (json.dumps(state, ensure_ascii=False, separators=(',', ':')) + '\n').encode('utf-8')
            info = tarfile.TarInfo(STATE); info.size = len(data); info.mode = 0o644
            archive.addfile(info, io.BytesIO(data))
        if staged.stat().st_size > 2_000_000_000:
            raise ValueError('Archive exceeds the 2 GB release limit')
        # Same-filesystem final replacement, even when /tmp is a separate mount.
        with tempfile.NamedTemporaryFile(prefix='.pack-', dir=str(output.parent), delete=False) as stream:
            pending = Path(stream.name)
        try:
            shutil.copyfile(str(staged), str(pending)); pending.replace(output)
        finally:
            if pending.exists(): pending.unlink()
    checksum = sha(output)
    Path(str(output) + '.sha256').write_text(checksum + '  ' + output.name + '\n')
    launcher = output.parent / 'unpack.sh'
    if launcher.resolve() != (root / 'unpack.sh').resolve():
        shutil.copy2(str(root / 'unpack.sh'), str(launcher))
    report = {'archive': str(output), 'bytes': output.stat().st_size, 'sha256': checksum,
              'included_files': len(files), 'excluded_entries': len(skipped),
              'download_groups': len(selected), 'excluded': skipped}
    Path(str(output) + '.report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print('Packed {}: {:,} bytes; {} files; {} exclusions'.format(output, report['bytes'], len(files), len(skipped)))


def unpack(archive, destination):
    archive, destination = archive.absolute(), destination.absolute()
    if destination.exists() or destination.is_symlink():
        raise ValueError('Destination already exists: ' + str(destination))
    checksum = Path(str(archive) + '.sha256')
    if checksum.exists() and sha(archive) != checksum.read_text().split()[0]:
        raise ValueError('Release archive checksum mismatch')
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.unpack-', dir=str(destination.parent)) as temporary:
        staged = Path(temporary) / 'project'; staged.mkdir()
        with tarfile.open(str(archive)) as stream:
            members = stream.getmembers(); by_name = {}
            for item in members:
                name = safe_name(item.name)
                if name in by_name or not (item.isfile() or item.isdir() or item.issym()):
                    raise ValueError('Duplicate or unsupported archive member: ' + name)
                by_name[name] = item
                if item.issym(): safe_link(name, item.linkname)
            links = {name for name, item in by_name.items() if item.issym()}
            for name in by_name:
                if any(str(parent) in links for parent in PurePosixPath(name).parents):
                    raise ValueError('Archive member below symlink: ' + name)
            state = json.loads(stream.extractfile(by_name[STATE]).read().decode('utf-8'))
            if state.get('format') != 1 or set(state['files']) != set(by_name) - {STATE}:
                raise ValueError('Package manifest does not match archive')
            for name, item in by_name.items():
                target = staged / name; target.parent.mkdir(parents=True, exist_ok=True)
                if item.issym():
                    if state['files'][name].get('link') != item.linkname:
                        raise ValueError('Link manifest mismatch: ' + name)
                    continue
                if item.isdir(): target.mkdir(exist_ok=True); continue
                with stream.extractfile(item) as source, target.open('wb') as output:
                    shutil.copyfileobj(source, output)
                target.chmod(item.mode & 0o777)
                if name != STATE and sha(target) != state['files'][name]['sha256']:
                    raise ValueError('Payload checksum mismatch: ' + name)
            for name in sorted(links):
                (staged / name).symlink_to(by_name[name].linkname)
            for name in links:
                try:
                    resolved = (staged / name).resolve()
                except RuntimeError:
                    raise ValueError('Cyclic archive symlink: ' + name)
                if resolved != staged and staged not in resolved.parents:
                    raise ValueError('Archive symlink chain escapes project: ' + name)
        staged.rename(destination)
    print('Extracted to ' + str(destination), flush=True)
    return destination


def download(dependency, cache):
    cache.mkdir(parents=True, exist_ok=True)
    expected = dependency['sha256']; target = cache / expected
    if target.is_file() and sha(target) == expected:
        return target
    mirror = os.environ.get('PORTABLE_DOWNLOAD_CACHE')
    if mirror:
        candidate = Path(mirror) / expected
        if candidate.is_file() and sha(candidate) == expected:
            shutil.copyfile(str(candidate), str(target)); return target
    for attempt in range(3):
        try:
            print('Download: ' + dependency['url'], flush=True)
            request = urllib.request.Request(dependency['url'], headers={'User-Agent': 'Portable-OS-source/1.0'})
            with tempfile.NamedTemporaryFile(prefix='.download-', dir=str(cache), delete=False) as output:
                temporary = Path(output.name)
                try:
                    with urllib.request.urlopen(request, timeout=60) as response:
                        shutil.copyfileobj(response, output)
                except Exception:
                    temporary.unlink(); raise
            try:
                if sha(temporary) != expected:
                    raise ValueError('Downloaded checksum mismatch: ' + dependency['url'])
                temporary.replace(target)
            finally:
                if temporary.exists(): temporary.unlink()
            return target
        except (OSError, ValueError):
            if attempt == 2: raise
            time.sleep(attempt + 1)


def restore_downloads(root, dependencies, profile):
    for dependency in dependencies:
        if profile == 'native' and dependency.get('profile') == 'linux': continue
        needed = []
        for entry in dependency['files']:
            path = root / safe_name(entry['path'])
            if path.is_file() and sha(path) == entry['sha256']: continue
            if path.exists() or path.is_symlink():
                raise ValueError('Preserving modified dependency: ' + str(path))
            needed.append(entry)
        if not needed: continue
        cached = download(dependency, root / '.download-cache')
        archive = tarfile.open(str(cached)) if any('member' in x for x in needed) else None
        try:
            for entry in needed:
                path = root / entry['path']; path.parent.mkdir(parents=True, exist_ok=True)
                with tempfile.NamedTemporaryFile(prefix='.restore-', dir=str(path.parent), delete=False) as output:
                    temporary = Path(output.name)
                    try:
                        if 'member' in entry:
                            member = archive.getmember(entry['member'])
                            if not member.isfile(): raise ValueError('Dependency member is not a regular file')
                            source = archive.extractfile(member)
                        else: source = cached.open('rb')
                        with source: shutil.copyfileobj(source, output)
                    except Exception:
                        temporary.unlink(); raise
                try:
                    if sha(temporary) != entry['sha256']: raise ValueError('Restored dependency checksum mismatch')
                    temporary.chmod(entry.get('mode', 0o644)); temporary.replace(path)
                finally:
                    if temporary.exists(): temporary.unlink()
        finally:
            if archive is not None: archive.close()


def host_tools(install):
    if platform.system() != 'Linux' or platform.machine() not in ('x86_64', 'amd64'):
        raise ValueError('This release build environment requires Ubuntu Linux x86_64')
    if install:
        text = Path('/etc/os-release').read_text()
        if 'ubuntu' not in text.lower(): raise ValueError('Automatic host setup supports Ubuntu')
        missing = []
        for package in APT:
            result = subprocess.run(['dpkg-query', '-W', '-f=${Status}', package], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            if result.stdout.decode().strip() != 'install ok installed': missing.append(package)
        if missing:
            privilege = [] if os.geteuid() == 0 else ['sudo']
            subprocess.check_call(privilege + ['apt-get', 'update'])
            subprocess.check_call(privilege + ['apt-get', 'install', '-y'] + missing)
    required = ['make', 'javac', 'jar', 'gcc', 'clang', 'clang++', 'aarch64-linux-gnu-ld', 'aarch64-linux-gnu-ar', 'aarch64-linux-gnu-objcopy']
    missing = [name for name in required if not shutil.which(name)]
    if missing: raise ValueError('Missing host build tools: ' + ', '.join(missing))
    if not Path('/usr/include/newlib/stdio.h').is_file(): raise ValueError('Install libnewlib-dev')


def prepare(root, profile='all', install=True):
    cfg = config(root)
    state_path = root / STATE
    state = json.loads(state_path.read_text()) if state_path.exists() else {'downloads': cfg['downloads'], 'vendor_overrides': []}
    host_tools(install)
    restore_downloads(root, state['downloads'], profile)
    if cfg['project'] == 'jkoros':
        command = [sys.executable, 'tools/prepare.py'] + (['--sdk-only'] if profile == 'native' else [])
        subprocess.check_call(command, cwd=str(root / 'platforms/rpi4'))
        if profile == 'all':
            subprocess.check_call(['make', 'prepare-host'], cwd=str(root / 'platforms/rpi4'))
            subprocess.check_call(['make', 'runtimes'], cwd=str(root / 'platforms/rpi4'))
    else:
        # Generated vendor copies are recovered from the pinned shared archive.
        for country in state.get('vendor_overrides', []):
            folder = root / safe_name(country)
            data = json.loads((folder / 'native.json').read_text())
            source = folder / data['source']; vendor = source / data['native'] / 'vendor'
            kept = {p.relative_to(source): (p.read_bytes(), p.stat().st_mode & 0o777)
                    for p in vendor.rglob('*') if p.is_file()}
            with tarfile.open(str(folder / 'native-vendor.tar.gz')) as archive:
                for item in archive:
                    target = source / safe_name(item.name)
                    if not item.isfile(): raise ValueError('Unexpected vendor archive entry')
                    target.parent.mkdir(parents=True, exist_ok=True)
                    with archive.extractfile(item) as stream, target.open('wb') as output:
                        shutil.copyfileobj(stream, output)
                    target.chmod(item.mode & 0o777)
            for rel, (content, mode) in kept.items():
                (source / rel).write_bytes(content); (source / rel).chmod(mode)
            (source / '.vendor-sha256').write_text(data['vendor_sha256'] + '\n')
        if profile == 'all':
            subprocess.check_call(['make', 'prepare-runtime'], cwd=str(root))
            subprocess.check_call(['make', 'runtime'], cwd=str(root))
    print('Preparation complete: {} ({})'.format(root, profile), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='action')
    p = commands.add_parser('pack'); p.add_argument('--root', type=Path, default=ROOT)
    p.add_argument('--output', type=Path); p.add_argument('--level', type=int, choices=range(10), default=9)
    p = commands.add_parser('unpack'); p.add_argument('archive', type=Path); p.add_argument('destination', type=Path)
    p.add_argument('--no-prepare', action='store_true', help='Extract only; default automatically downloads/prepares dependencies')
    p.add_argument('--profile', choices=['all', 'native'], default='all')
    p.add_argument('--no-host-install', action='store_true')
    p = commands.add_parser('prepare'); p.add_argument('--root', type=Path, default=ROOT)
    p.add_argument('--profile', choices=['all', 'native'], default='all'); p.add_argument('--no-host-install', action='store_true')
    args = parser.parse_args()
    if args.action == 'pack':
        root = args.root.resolve(); name = config(root)['project']
        pack(root, args.output or root / 'dist' / (name + '-source.tar.xz'), args.level)
    elif args.action == 'unpack':
        root = unpack(args.archive, args.destination)
        if not args.no_prepare:
            command = [sys.executable, str(root / 'distribution/portable.py'), 'prepare', '--profile', args.profile]
            if args.no_host_install: command.append('--no-host-install')
            subprocess.check_call(command)
    elif args.action == 'prepare': prepare(args.root.resolve(), args.profile, not args.no_host_install)
    else: parser.error('Choose pack, unpack, or prepare')


if __name__ == '__main__':
    try: main()
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print('ERROR: ' + str(error), file=sys.stderr)
        print('After fixing preparation errors, run ./unpack.sh --prepare inside the extracted project.', file=sys.stderr)
        sys.exit(1)
