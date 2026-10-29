#!/usr/bin/env python3
"""τρέχων_στοιχείο ίδιο ARM64 산출물을 검사하고 LGPL προέλευση_δέντρο·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

έργο_ρίζα = Path(__file__).resolve().parents[1]
αποθετήριο_ρίζα = έργο_ρίζα.parents[1]
προορισμός_όνομα = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
βιβλιοθήκη = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def κατακερματισμός_Αρχείο(ΔΙΑΔΡΟΜΗ):
    return hashlib.sha256(Path(ΔΙΑΔΡΟΜΗ).read_bytes()).hexdigest()


def 점검():
    for Όνομα in ('vendor/wolfssh', 'vendor/wolfssl', 'απομακρυσμένος_τιμή/user_settings.h'):
        if (έργο_ρίζα / Όνομα).exists():
            raise SystemExit('COSL 배포 Στοπ: 이전 GPL απομακρυσμένος_τιμή 구현이 προέλευση_δέντρο 트리에 남아 있습니다: ' + Όνομα)
    ενσύρματος_τιμή = (έργο_ρίζα / 'δίκτυο_δέσμη/ενσύρματος_δίκτυο.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in ενσύρματος_τιμή or 'SPDX-License-Identifier: GPL' in ενσύρματος_τιμή:
        raise SystemExit('COSL 배포 Στοπ: BSD GENET 구현·고지 επαληθεύω 필요')
    for Όνομα in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (αποθετήριο_ρίζα / Όνομα).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + Όνομα)
    σύμβολο_τιμή = subprocess.check_output(['aarch64-linux-gnu-nm', str(έργο_ρίζα / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', σύμβολο_τιμή):
        raise SystemExit('COSL 배포 Στοπ: 커널에 이전 GPL κωδικός_πρόσβασης_τιμή/SSH 심볼이 남아 있습니다. δοκιμάζω_ξανά_τιμή 빌드하세요.')
    for Όνομα in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Όνομα + r'$', σύμβολο_τιμή, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + Όνομα)
    with tempfile.TemporaryDirectory(dir=str(έργο_ρίζα / 'build')) as 임시:
        εικόνα_τιμή = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(έργο_ρίζα / 'build/kernel.elf'), str(εικόνα_τιμή)])
        if κατακερματισμός_Αρχείο(εικόνα_τιμή) != κατακερματισμός_Αρχείο(έργο_ρίζα / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    έκθεση_τιμή = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': κατακερματισμός_Αρχείο(έργο_ρίζα / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Όνομα: κατακερματισμός_Αρχείο(έργο_ρίζα / 'build' / Όνομα) for Όνομα in βιβλιοθήκη}}
    (έργο_ρίζα / 'build/cosl-distribution-check.json').write_text(json.dumps(έκθεση_τιμή, ensure_ascii=False, indent=2) + '\n')
    return έκθεση_τιμή


def συνδέω_τελικό_σημείο_bbe6b410():
    έκθεση_τιμή = 점검()
    배포 = έργο_ρίζα / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(έργο_ρίζα / 'build')) as 임시:
        Ομάδα_τιμή = Path(임시) / 'jkoros-native-relink'
        Ομάδα_τιμή.mkdir()
        def παρουσία_τιμή(원본, ομότιμος_τιμή):
            προορισμός_τιμή = Ομάδα_τιμή / ομότιμος_τιμή
            προορισμός_τιμή.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(προορισμός_τιμή), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(προορισμός_τιμή))
        for Όνομα in προορισμός_όνομα:
            παρουσία_τιμή(έργο_ρίζα / 'build' / (Όνομα + '.o'), 'objects/' + Όνομα + '.o')
        for Όνομα in βιβλιοθήκη:
            παρουσία_τιμή(έργο_ρίζα / 'build' / Όνομα, 'objects/' + Path(Όνομα).name)
        for Όνομα in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     'Ταχυδρομικός_κώδικας_πρόγραμμα_μεταγλώττισης', 'χρήστης', '명명', 'υπολογιστής_5eb260fa', 'δίκτυο_δέσμη/δίκτυο_δέσμη.h', '부팅/συνδέω_Διάταξη.ld',
                     'απομακρυσμένος_τιμή/assh_config.h', 'απομακρυσμένος_τιμή/config.h', 'απομακρυσμένος_τιμή/ctype.h', 'απομακρυσμένος_τιμή/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            παρουσία_τιμή(έργο_ρίζα / Όνομα, Όνομα)
        for Όνομα in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            παρουσία_τιμή(αποθετήριο_ρίζα / Όνομα, Όνομα)
        for ΔΙΑΔΡΟΜΗ in sorted((έργο_ρίζα / 'vendor').glob('LICENSE*')):
            παρουσία_τιμή(ΔΙΑΔΡΟΜΗ, 'vendor/' + ΔΙΑΔΡΟΜΗ.name)
        παρουσία_τιμή(έργο_ρίζα / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        παρουσία_τιμή(έργο_ρίζα / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        παρουσία_τιμή(αποθετήριο_ρίζα / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        παρουσία_τιμή(έργο_ρίζα / 'Εργαλεία/재연결.py', 'relink.py')
        for ΔΙΑΔΡΟΜΗ in sorted((έργο_ρίζα / 'build/user').glob('*.elf')):
            παρουσία_τιμή(ΔΙΑΔΡΟΜΗ, 'build/user/' + ΔΙΑΔΡΟΜΗ.name)
        for Όνομα in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            παρουσία_τιμή(έργο_ρίζα / 'build/user' / (Όνομα + '.o'), 'build/user/' + Όνομα + '.o')
        for Όνομα in ('crt', 'aot-runtime', 'περιβάλλον_εκτέλεσης_στήριγμα', 'Εκτέλεση_2', '미리번역', 'επιστρέφω_γέφυρα'):
            παρουσία_τιμή(έργο_ρίζα / 'build/ccompiler' / (Όνομα + '.o'), 'build/ccompiler/' + Όνομα + '.o')
        명세 = dict(έκθεση_τιμή, objects=['objects/' + Όνομα + '.o' for Όνομα in προορισμός_όνομα],
                    libraries=['objects/' + Path(ΔΙΑΔΡΟΜΗ).name for ΔΙΑΔΡΟΜΗ in βιβλιοθήκη])
        (Ομάδα_τιμή / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (Ομάδα_τιμή / 'README.md').write_text('''# jkoros native LGPL source and relink kit

This kit accompanies the matching kernel image. Retain it with binary distributions.
Application terms: LICENSE. Library terms: vendor/libassh/COPYING and vendor/tinycc/COPYING.
Other notices: THIRD_PARTY_NOTICES.md. COSL does not override the LGPL permissions.
This product includes software developed by Bill Paul.

Host dependencies: Python 3, Clang supporting aarch64-none-elf, libnewlib-dev headers,
and aarch64-linux-gnu binutils. No Linux kernel is linked into the guest.

From this extracted directory:

    python3 relink.py --verify

This recompiles libassh from the included source/configuration and relinks the kernel.
The original unmodified library must produce the recorded kernel SHA256.
To change libassh, edit vendor/libassh/src, then run without --verify.
Alternatively: python3 relink.py --libassh-archive /path/to/modified/libassh.a

TinyCC source is included in vendor/tinycc; the native port is in Ταχυδρομικός_κώδικας_πρόγραμμα_μεταγλώττισης.
To rebuild a modified TinyCC and replace its embedded executable:

    python3 relink.py --tinycc --sdk /path/to/alpine-arm64-rootfs

Use the same Alpine 3.24.2 ARM64 SDK headers and GCC 15.2.0 libgcc runtime as the
original build (jkoros/platforms/rpi4: make prepare-runtime; see that platform's docs).
The SDK is a host build prerequisite and is not included here. Its libgcc exception
and GPL text are in vendor/LICENSE.libgcc-runtime and vendor/LICENSE.gcc-gpl3.
GCC sources: https://gcc.gnu.org/pub/gcc/releases/gcc-15.2.0/
Both the cc ELF size table and user/program objects are regenerated when --tinycc is used.
Output: build/relinked/kernel8.img. Boot it using the same Pi4 firmware/config or QEMU
runner as the original image. There is no signature lock against modified libraries.

This is a relink kit for one device image. Objects contain the same embedded device
key as that image. Keep personal development images and build/remote credentials
out of public source uploads; provision appropriate images for recipients.
''')
        τιμή_στόχος = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / τιμή_στόχος.name
        with tarfile.open(str(임시압축), 'w:gz') as Αρχειοθήκη_τιμή:
            Αρχειοθήκη_τιμή.add(str(Ομάδα_τιμή), arcname=Ομάδα_τιμή.name)
        임시압축.replace(τιμή_στόχος)
    έκθεση_τιμή['relink_archive_sha256'] = κατακερματισμός_Αρχείο(τιμή_στόχος)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(έκθεση_τιμή, ensure_ascii=False, indent=2) + '\n')
    return τιμή_στόχος


if __name__ == '__main__':
    ανάλυση_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ανάλυση_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    τιμή = ανάλυση_48ee4b1b.parse_args()
    if τιμή.command == 'bundle':
        print('COSL source/relink kit:', συνδέω_τελικό_σημείο_bbe6b410())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
