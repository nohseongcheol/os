#!/usr/bin/env python3
"""Inspect an existing JDK without executing it; report native-kernel ABI blockers."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
import zipfile


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def inspect_elf(path):
    data = Path(path).read_bytes()
    if len(data) < 64 or data[:6] != b'\x7fELF\x02\x01':
        raise ValueError('ELF64 little-endian file required: ' + str(path))
    typ, machine = struct.unpack_from('<HH', data, 16)
    entry, phoff = struct.unpack_from('<QQ', data, 24)
    ehsize, phsize, count = struct.unpack_from('<HHH', data, 52)
    if ehsize != 64 or phsize != 56 or count > 65535 or phoff + count * phsize > len(data):
        raise ValueError('Invalid ELF program headers: ' + str(path))
    segments, interpreter, abi = [], None, False
    for i in range(count):
        kind, flags, offset, address, physical, size, memory, align = struct.unpack_from('<IIQQQQQQ', data, phoff + i * phsize)
        if size and offset + size > len(data):
            raise ValueError('ELF segment outside file: ' + str(path))
        if kind == 3:
            interpreter = data[offset:offset + size].rstrip(b'\0').decode('utf-8', 'replace')
        if kind == 4:
            notes, at = data[offset:offset + size], 0
            while at + 12 <= len(notes):
                namesz, descsz, note_type = struct.unpack_from('<III', notes, at)
                at += 12
                end_name, end_desc = at + (namesz + 3 & ~3), at + (namesz + 3 & ~3) + (descsz + 3 & ~3)
                if end_desc > len(notes):
                    break
                if notes[at:at + namesz] == b'JKOROS\0' and descsz == 4 and note_type == 1:
                    abi = struct.unpack_from('<I', notes, end_name)[0] == 1 or abi
                at = end_desc
        segments.append({'type': kind, 'flags': flags, 'address': address, 'offset': offset,
                         'file_bytes': size, 'memory_bytes': memory, 'alignment': align})
    # This is a compatibility screen, not a replacement for user_validate_elf().
    reasons = []
    if machine != 183: reasons.append('CPU is not AArch64')
    if typ != 2: reasons.append('ELF is not ET_EXEC (PIE/shared objects need a dynamic loader)')
    if interpreter: reasons.append('Requires program interpreter: ' + interpreter)
    if not abi: reasons.append('Missing JKOROS ABI v1 note')
    if count > 16: reasons.append('More than 16 program headers')
    for p in segments:
        kind = p['type']
        if kind in (2, 7): reasons.append('Unsupported ' + {2: 'PT_DYNAMIC', 7: 'PT_TLS'}[kind])
        elif kind not in (0, 1, 4, 6, 0x6474e551): reasons.append('Unsupported segment type 0x{:x}'.format(kind))
        if kind == 1 and p['memory_bytes']:
            if p['address'] < 0x02000000 or p['address'] + p['memory_bytes'] > 0x02c00000:
                reasons.append('Load segment outside fixed 12 MiB user image region')
            if p['alignment'] != 4096 or p['address'] % 4096 or p['offset'] % 4096:
                reasons.append('Load segment does not satisfy 4 KiB page alignment')
            if p['flags'] & 3 == 3: reasons.append('Writable and executable load segment')
    output = subprocess.check_output(['readelf', '-dW', str(path)], universal_newlines=True)
    needed = re.findall(r'\(NEEDED\).*?\[([^]]+)\]', output)
    symbols = subprocess.check_output(['readelf', '--dyn-syms', '-W', str(path)], universal_newlines=True)
    imports = sorted(set(m.group(1).split('@')[0] for m in re.finditer(r'\bUND\s+(\S+)', symbols)))
    reasons = sorted(set(reasons))
    return {'path': str(path), 'sha256': digest(path), 'bytes': len(data), 'machine': machine,
            'elf_type': typ, 'entry': entry, 'interpreter': interpreter, 'needed_libraries': needed,
            'undefined_dynamic_symbols': imports, 'segments': segments, 'jkoros_abi_v1': abi,
            'native_abi_blockers': reasons, 'native_abi_screen_passed': not reasons,
            'fits_shell_upload': len(data) <= 16384}


def inspect_jdk(jdk):
    jdk = Path(jdk).resolve()
    java, jvm, modules = jdk / 'bin/java', jdk / 'lib/server/libjvm.so', jdk / 'lib/modules'
    for p in (jdk / 'release', java, jvm, modules):
        if not p.is_file(): raise ValueError('Missing modular OpenJDK image file: ' + str(p))
    release = dict(re.findall(r'^([A-Z_]+)="(.*)"$', (jdk / 'release').read_text(), re.M))
    binaries = {name: inspect_elf(p) for name, p in [('java', java), ('libjvm', jvm)]}
    version = None
    jmod = jdk / 'jmods/java.base.jmod'
    if jmod.is_file():
        with zipfile.ZipFile(str(jmod)) as z:
            data = z.read('classes/java/lang/Object.class')
            if data[:4] != b'\xca\xfe\xba\xbe': raise ValueError('Invalid Object.class')
            version = struct.unpack_from('>H', data, 6)[0]
    requirements = {
        'memory_mapping': ['mmap', 'munmap', 'mprotect', 'madvise'],
        'native_threads_tls': ['pthread_create', 'pthread_join', 'pthread_key_create', 'pthread_getspecific', 'pthread_setspecific'],
        'synchronization': ['pthread_mutex_lock', 'pthread_cond_wait', 'pthread_cond_timedwait', 'sem_wait'],
        'signals': ['sigaction', 'sigaltstack', 'pthread_sigmask'],
        'dynamic_libraries': ['dlopen', 'dlsym', 'dlclose'],
        'clocks': ['clock_gettime', 'nanosleep'],
    }
    imports = set(binaries['libjvm']['undefined_dynamic_symbols'])
    return {'kind': 'OpenJDK native port assessment', 'inspected_only': True, 'executed': False,
            'jdk': str(jdk), 'release': release, 'java_base_class_version': version,
            'binaries': binaries, 'module_image': {'bytes': modules.stat().st_size, 'sha256': digest(modules)},
            'observed_os_imports': {k: [s for s in names if s in imports] for k, names in requirements.items()},
            'native_kernel_port_complete': False,
            'direct_copy_runnable': False,
            'reason': 'Current JKOROS ABI does not implement the OpenJDK OS runtime contract. A successful host build is not a kernel port.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--jdk', type=Path, required=True)
    p.add_argument('-o', '--output', type=Path, required=True)
    p.add_argument('--require-native', action='store_true', help='Exit 3 if the runtime cannot run on the own kernel')
    args = p.parse_args()
    try:
        report = inspect_jdk(args.jdk)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    except (ValueError, OSError, subprocess.CalledProcessError, zipfile.BadZipFile) as exc:
        p.exit(1, str(exc) + '\n')
    print('검사 완료: {}; oma tuum_VALUE 직접 Täida_käsk 불가'.format(args.output))
    return 3 if args.require_native else 0


if __name__ == '__main__':
    raise SystemExit(main())
