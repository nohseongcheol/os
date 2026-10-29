#!/usr/bin/env python3
"""Boot each country's own current image and exercise localized guest programs.

Serial UART avoids exposing VNC/network ports. A boot pass is deliberately
separate from complete naming or a translated UI. Evidence is source/image
bound and resumable; stale reports never count as a pass for a renamed build.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import os
from pathlib import Path
import re
import selectors
import shutil
import signal
import subprocess
import threading
import time

ROOT = Path(__file__).resolve().parents[1]
PROBE_VERSION = 4
KERNEL_CACHE_LOCK = threading.Lock()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_digest(folder, config):
    result = hashlib.sha256()
    for name in sorted(config['owned_files']):
        result.update(name.encode())
        result.update((folder / config['source'] / name).read_bytes())
    from importlib.util import spec_from_file_location, module_from_spec
    spec = spec_from_file_location('ip_config', str(ROOT/'tools/ip_config.py'))
    module = module_from_spec(spec); spec.loader.exec_module(module)
    effective = module.config_path(folder/config['source']/config['native'])
    result.update(b'ip.conf\0')
    result.update(effective.read_bytes() if effective else b'')
    return result.hexdigest()


def kernel_input_files(config):
    """Conservative input set for the native ARM64 builder.

    Include every owned file except the separate hosted managed-Java tree,
    its root make include and three root architecture/introduction documents.
    In particular all native tools, examples (including README), data, build
    scripts and compiler/ABI files remain inputs. Dependency archives are
    hashed separately. This exclusion never implies a managed-Java test pass.
    """
    from source_names import make_renamer
    rename = make_renamer(config['identifiers'])
    managed = rename('원천') + '/'
    documents = {rename(p) for p in ('만들기.mk', '안내.md', '문서/구조.md', '문서/기능대응.md')}
    return sorted(name for name in config['owned_files'] if not name.startswith(managed) and name not in documents)


def kernel_input_digest(config, read):
    result = hashlib.sha256()
    for name in kernel_input_files(config):
        result.update(name.encode())
        result.update(read(name))
    return result.hexdigest()


def reuse_namespace_kernel(cache, folder, config, source_hash):
    """Namespace-only historical proofs predate externally selected ip.conf.

    Full-source/configuration-bound cache entries remain usable. A namespace
    baseline cannot establish which external configuration its image used.
    """
    return None


def launcher_digest(folder, config):
    result = hashlib.sha256()
    for name in ('native-launch.sh', 'native-java/'+config['identifiers'].get('국가실행기','국가실행기')+'.java'):
        result.update(name.encode())
        result.update((folder/name).read_bytes())
    return result.hexdigest()


def atomic_json(path, value):
    temporary = path.with_suffix(path.suffix + '.new')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    temporary.replace(path)


def reuse_kernel(cache, build, source_hash, vendor_hash):
    """Reuse only a proven image for exactly equal owned bytes and dependencies.

    The target must still boot and pass all probes. This caches compilation,
    never verification, and makes independent copies instead of hard links.
    """
    marker = build / 'worldos-source.sha256'
    if (build / 'kernel8.img').is_file() and marker.is_file() and marker.read_text().strip() == source_hash:
        return None
    with KERNEL_CACHE_LOCK:
        candidates = (cache / (source_hash + '-' + vendor_hash + '.img'), cache / (source_hash + '.img'))
        for image in candidates:
            try:
                evidence = json.loads(image.with_suffix('.json').read_text())
                if evidence.get('source_sha256') != source_hash or evidence.get('vendor_sha256') != vendor_hash:
                    continue
                proof = evidence.get('origin_pass_report')
                if proof is None:  # Older cache entries require their original live report.
                    proof = json.loads((ROOT / evidence['origin_report']).read_text())
                if not (proof.get('passed') and proof.get('probe_version') in (2, PROBE_VERSION) and
                        proof.get('source_sha256') == source_hash and
                        proof.get('kernel_sha256') == evidence['kernel_sha256']):
                    continue
                if digest(image) != evidence['kernel_sha256']:
                    continue
                build.mkdir(parents=True, exist_ok=True)
                temporary = build / 'kernel8.img.new'
                shutil.copyfile(str(image), str(temporary))
                assert digest(temporary) == evidence['kernel_sha256']
                temporary.replace(build / 'kernel8.img')
                atomic_json(build / 'worldos-kernel-cache.json', evidence)
                temporary_marker = marker.with_suffix('.sha256.new')
                temporary_marker.write_text(source_hash + '\n')
                temporary_marker.replace(marker)
                return {'origin_country': evidence['origin_country'],
                        'source_sha256': source_hash, 'kernel_sha256': evidence['kernel_sha256']}
            except (OSError, ValueError, KeyError):
                continue
    return None


def cache_verified_kernel(cache, kernel, config, report):
    """Keep immutable evidence with the verified image for future equal trees."""
    if not report.get('passed') or digest(kernel) != report.get('kernel_sha256'):
        return
    with KERNEL_CACHE_LOCK:
        cache.mkdir(parents=True, exist_ok=True)
        image = cache / (report['source_sha256'] + '-' + config['vendor_sha256'] + '.img')
        temporary = image.with_suffix('.img.new')
        shutil.copyfile(str(kernel), str(temporary))
        assert digest(temporary) == report['kernel_sha256']
        temporary.replace(image)
        atomic_json(image.with_suffix('.json'), {
            'source_sha256': report['source_sha256'], 'kernel_sha256': report['kernel_sha256'],
            'vendor_sha256': config['vendor_sha256'], 'origin_country': report['country'],
            'origin_pass_report': report,
            'scope': 'Independent compiled-image copy for exactly equal owned source/dependencies. Each target requires its own boot verification.'})


def verify(folder, output, qemu, resume=True, keep_new_builds=False):
    config = json.loads((folder / 'native.json').read_text())
    native = folder / config['source'] / config['native']
    build = native / 'build'
    new_build = not build.exists()
    kernel = build / 'kernel8.img'
    output.mkdir(parents=True, exist_ok=True)
    target = output / 'report.json'
    source_hash = source_digest(folder, config)
    launch_hash = launcher_digest(folder, config)
    if resume and target.is_file() and kernel.is_file():
        prior = json.loads(target.read_text())
        if (prior.get('passed') and prior.get('probe_version') == PROBE_VERSION and
                prior.get('source_sha256') == source_hash and
                prior.get('launcher_sha256') == launch_hash and
                prior.get('kernel_sha256') == digest(kernel)):
            return dict(prior, cached=True)
    report = {'country': config['country'], 'language': config['language'],
              'edition': str(folder.relative_to(ROOT)), 'passed': False, 'booted': False,
              'probe_version': PROBE_VERSION, 'source_sha256': source_hash,
              'launcher_sha256': launch_hash,
              'linux_loaded': False, 'physical_board_tested': False,
              'language_help_translated': bool(config.get('help_sentence_translated')),
              'remaining_native_identifiers': config['naming']['untranslated_identifiers'],
              'complete_localization_certified': False}
    cache = output.parent / 'equal-source-kernels'
    reused = reuse_kernel(cache, build, source_hash, config['vendor_sha256'])
    if not reused:
        reused = reuse_namespace_kernel(cache, folder, config, source_hash)
    if reused:
        report['kernel_build_reused'] = reused
    if qemu:
        report['qemu_launcher_sha256'] = digest(qemu)
    environment = dict(os.environ)
    if qemu:
        environment['QEMU_AARCH64'] = str(qemu)
    transcript = bytearray()
    process = None
    selector = selectors.DefaultSelector()
    started = time.monotonic()
    try:
        process = subprocess.Popen(['sh', str(folder / 'native-launch.sh'), 'run',
                                    '--display', 'none', '--resolution', '640x480'],
                                   cwd=str(folder), env=environment, stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                   bufsize=0, start_new_session=True)
        selector.register(process.stdout, selectors.EVENT_READ)

        def until(marker, offset=0, timeout=90):
            deadline = time.monotonic() + timeout
            while marker not in transcript[offset:]:
                if time.monotonic() > deadline or process.poll() is not None:
                    raise AssertionError('Missing ' + repr(marker) + '\n' +
                                         transcript[max(0, len(transcript)-5000):].decode('utf-8', 'replace'))
                for key, _ in selector.select(.1):
                    part = key.fileobj.read(65536)
                    if part:
                        transcript.extend(part)
            return transcript[offset:].decode('utf-8', 'replace')

        sequence = [0]

        def shell(command):
            sequence[0] += 1
            marker = '__COUNTRY_BOOT_DONE_' + str(sequence[0]) + '__'
            offset = len(transcript)
            process.stdin.write((command + '; echo; echo ' + marker + '\n').encode())
            process.stdin.flush()
            return until(('\r\n' + marker + '\r\njkoros-native> ').encode(), offset)

        until(b'jkoros-native> ', timeout=600)
        for marker in (b'JAVA AOT PASS', b'TASK PASS', b'USER PROTECTION PASS', b'NATIVE READY'):
            assert marker in transcript, repr(marker)
        boot_start = transcript.find(b'JAVA AOT PASS')
        assert not re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', transcript[boot_start:])
        report.update(booted=True, kernel_sha256=digest(kernel))
        assert source_digest(folder, config) == source_hash, 'Source changed during verification'
        help_text = shell('help input')
        assert config['help'] in help_text, 'Edition input help mismatch'
        report['edition_input_help_present'] = True
        sample = config['input']['sample']
        quoted = json.dumps(sample, ensure_ascii=False)
        echoed = shell('echo ' + quoted)
        assert '\r\n' + sample + '\r\n' in echoed, 'UTF-8 echo mismatch'
        shell('echo ' + quoted + ' > country-utf8.txt')
        saved = shell('cat country-utf8.txt')
        assert '\r\n' + sample + '\r\n' in saved, 'UTF-8 file roundtrip mismatch'
        report['locale_sample_utf8_file_roundtrip'] = True
        name = config['examples']['출력예제']
        shell('example java')
        shell('cd /example/java')
        compiled = shell('javac ' + name + '.java')
        assert 'exit 0' in compiled, compiled
        ran = shell('java ' + name)
        assert 'exit 0' in ran and '42' in ran, ran
        report['localized_guest_javac_java'] = True
        shell('cd /; example python; cd /example/python')
        ran = shell('python ' + name + '.py')
        assert 'exit 0' in ran and '42' in ran, ran
        report['localized_guest_python'] = True
        shell('cd /; example c; cd /example/c')
        compiled = shell('cc ' + name + '.c -o country-demo')
        assert 'exit 0' in compiled, compiled
        ran = shell('./country-demo')
        assert 'exit 0' in ran, ran
        report['localized_guest_c'] = True
        assert source_digest(folder, config) == source_hash, 'Source changed during guest probes'
        assert launcher_digest(folder, config) == launch_hash, 'Launcher changed during guest probes'
        report['passed'] = True
    except Exception as error:
        report['error'] = str(error)
    finally:
        if process and process.poll() is None:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
        selector.close()
        report['elapsed_seconds'] = round(time.monotonic()-started, 2)
        (output / 'serial.log').write_bytes(transcript)
        # Only our own newly created compiler intermediates are disposable.
        # Existing user builds are retained; all tested images remain available.
        if new_build and report['passed'] and not keep_new_builds:
            retained = {'kernel8.img', 'worldos-source.sha256', 'build.json', 'worldos-kernel-cache.json'}
            for path in build.iterdir():
                if path.name not in retained:
                    if path.is_dir() and not path.is_symlink():
                        shutil.rmtree(str(path))
                    else:
                        path.unlink()
            report['new_build_intermediates_removed'] = True
        target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
        if report['passed']:
            cache_verified_kernel(cache, kernel, config, report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument('--all', action='store_true')
    selection.add_argument('--countries', nargs='+')
    parser.add_argument('--jobs', type=int, choices=(1, 2), default=1)
    parser.add_argument('--qemu', type=Path)
    parser.add_argument('--no-resume', action='store_true')
    parser.add_argument('--keep-new-builds', action='store_true')
    args = parser.parse_args()
    folders = sorted(p.parent for p in (ROOT / 'country').glob('*/native.json'))
    if args.countries:
        selected = set(args.countries)
        unknown = selected - {p.name for p in folders}
        if unknown:
            parser.error('Unknown countries: ' + ','.join(sorted(unknown)))
        folders = [p for p in folders if p.name in selected]
    qemu = args.qemu.resolve() if args.qemu else None
    if qemu and not qemu.is_file():
        parser.error('Missing QEMU launcher')
    output = ROOT / 'build/native/country-boots'
    output.mkdir(parents=True, exist_ok=True)
    results = []
    with ThreadPoolExecutor(max_workers=args.jobs) as executor:
        futures = {executor.submit(verify, folder, output / folder.name, qemu,
                                   not args.no_resume, args.keep_new_builds): folder for folder in folders}
        for future in as_completed(futures):
            report = future.result()
            results.append(report)
            summary = {'passed': all(r['passed'] for r in results),
                       'requested_countries': len(folders), 'checked': len(results),
                       'booted': sum(r['booted'] for r in results),
                       'complete': len(results) == len(folders),
                       'complete_localization_certified': False,
                       'scope': 'Actual per-country current-image boot, input help, UTF-8 file roundtrip and localized Java/Python/C examples. No assertion of complete translation or all input-method key sequences.',
                       'results': sorted(results, key=lambda r: r['country'])}
            target = output / 'summary.json'
            temporary = target.with_suffix('.json.new')
            temporary.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
            temporary.replace(target)
            print(report['country'], report['language'], 'PASS' if report['passed'] else 'FAIL',
                  len(results), '/', len(folders), report.get('error', '')[-600:], flush=True)
    if any(not r['passed'] for r in results):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
