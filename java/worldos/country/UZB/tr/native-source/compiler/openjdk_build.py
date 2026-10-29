#!/usr/bin/env python3
"""Build OpenJDK sources with the official javac/C/C++ build; never label it a kernel port."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import time
from openjdk_probe import digest, inspect_jdk


class BuildError(Exception):
    pass


def build(source, output, boot_jdk, jobs=2, target=None, sysroot=None, cc=None, cxx=None, configure_args=()):
    source, output, boot_jdk = (Path(p).resolve() for p in (source, output, boot_jdk))
    if output == source or source in output.parents:
        raise BuildError('Use a separate build directory outside the source tree')
    if output in source.parents:
        raise BuildError('Build directory must not contain the source tree')
    if any(re.search(r'\s', str(p)) for p in (source, output, boot_jdk)):
        raise BuildError('OpenJDK build paths must not contain whitespace')
    version_file = next((n for n in ('make/conf/version-numbers.conf', 'make/autoconf/version-numbers') if (source / n).is_file()), None)
    if version_file is None: raise BuildError('Incomplete OpenJDK sources: version-numbers')
    for name in ('configure', 'src/hotspot/share/runtime/os.hpp', 'src/java.base/share/classes/java/lang/Object.java'):
        if not (source / name).is_file(): raise BuildError('Incomplete OpenJDK sources: ' + name)
    for name in ('java', 'javac'):
        if not (boot_jdk / 'bin' / name).is_file(): raise BuildError('Boot JDK lacks bin/' + name)
    if jobs < 1 or jobs > 256: raise BuildError('jobs must be between 1 and 256')
    if target and (not re.fullmatch('[A-Za-z0-9_.+-]+', target) or 'linux' not in target):
        raise BuildError('This build route currently supports Linux targets; JKOROS needs an OS port first')
    if sysroot and not Path(sysroot).is_dir(): raise BuildError('Target sysroot does not exist')
    # Protect existing projects; failed OpenJDK builds can be resumed in their own directory.
    marker = output / 'jkoros-openjdk-build.json'
    if output.exists() and any(output.iterdir()) and not marker.is_file():
        raise BuildError('Nonempty directory is not a managed OpenJDK build: ' + str(output))
    if marker.is_file():
        old = json.loads(marker.read_text())
        if old.get('source') != str(source): raise BuildError('Build directory belongs to another source tree')
    output.mkdir(parents=True, exist_ok=True)
    config = ['bash', str(source / 'configure'), '--with-boot-jdk=' + str(boot_jdk),
              '--with-debug-level=release', '--with-jvm-variants=server', '--with-native-debug-symbols=none',
              '--disable-warnings-as-errors', '--with-jobs=' + str(jobs)]
    if target: config += ['--openjdk-target=' + target]
    if sysroot: config += ['--with-sysroot=' + str(Path(sysroot).resolve())]
    config += list(configure_args)
    env = os.environ.copy()
    if cc: env['CC'] = cc
    if cxx: env['CXX'] = cxx
    report = {'source': str(source), 'build_directory': str(output), 'boot_jdk': str(boot_jdk),
              'route': 'official OpenJDK javac plus C/C++ toolchain', 'self_aot_compiler': False,
              'target': target or 'build host', 'native_kernel_port_complete': False,
              'passed': False, 'stage': 'configure', 'commands': [],
              'source_identity': {n: digest(source / n) for n in ('configure', version_file)}}
    def record(): marker.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    def run(args, log):
        report['commands'].append(args); record()
        print('OpenJDK {} → {}'.format(report['stage'], output / log), flush=True)
        with (output / log).open('wb') as stream:
            p = subprocess.run(args, cwd=str(output), env=env, stdout=stream, stderr=subprocess.STDOUT)
        if p.returncode: raise BuildError('{} failed ({}); see {}'.format(report['stage'], p.returncode, output / log))
    record()
    try:
        run(config, 'driver-configure.log')
        report['stage'] = 'images'
        run(['make', 'images', 'JOBS=' + str(jobs)], 'images.log')
        image = output / 'images/jdk'
        report['runtime_assessment'] = inspect_jdk(image)
        # Cross-built images must never be executed as if they were host executables.
        report['image_built'] = True
        report['runtime_executed'] = False
        report['stage'] = 'complete'; report['passed'] = True
        report['completed_unix_time'] = int(time.time())
    except BaseException as exc:
        report['error'] = str(exc); raise
    finally:
        record()
    print('OpenJDK image: {} (Öz çekirdek_değer 이식은 별도)'.format(image), flush=True)
    return report


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--build-dir', type=Path, required=True)
    p.add_argument('--boot-jdk', type=Path, required=True)
    p.add_argument('--jobs', type=int, default=2)
    p.add_argument('--openjdk-target')
    p.add_argument('--sysroot')
    p.add_argument('--cc')
    p.add_argument('--cxx')
    p.add_argument('--configure-arg', action='append', default=[])
    args = p.parse_args()
    try:
        build(args.source, args.build_dir, args.boot_jdk, args.jobs, args.openjdk_target,
              args.sysroot, args.cc, args.cxx, args.configure_arg)
    except (BuildError, OSError, ValueError, subprocess.CalledProcessError) as exc:
        p.exit(1, str(exc) + '\n')


if __name__ == '__main__':
    main()
