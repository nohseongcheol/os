#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL ಮೂಲ_ವೃಕ್ಷ·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

ಬಿಂಬಿಸು_ಮೂಲ = Path(__file__).resolve().parents[1]
ಸಂಗ್ರಹಣೆ_ಮೂಲ = ಬಿಂಬಿಸು_ಮೂಲ.parents[1]
ಗಮ್ಯಸ್ಥಾನ_ಹೆಸರು = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
ಲೈಬ್ರರಿ = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def ಹ್ಯಾಶ್_ಫೈಲ್(ಮಾರ್ಗ):
    return hashlib.sha256(Path(ಮಾರ್ಗ).read_bytes()).hexdigest()


def 점검():
    for ಹೆಸರು in ('vendor/wolfssh', 'vendor/wolfssl', 'ರಿಮೋಟ್_ಮೌಲ್ಯ/user_settings.h'):
        if (ಬಿಂಬಿಸು_ಮೂಲ / ಹೆಸರು).exists():
            raise SystemExit('COSL 배포 ನಿಲ್ಲು: 이전 GPL ರಿಮೋಟ್_ಮೌಲ್ಯ 구현이 ಮೂಲ_ವೃಕ್ಷ 트리에 남아 있습니다: ' + ಹೆಸರು)
    ವಾಯರ್ಡ್_ಮೌಲ್ಯ = (ಬಿಂಬಿಸು_ಮೂಲ / 'ನೆಟ್_ವರ್ಕ್_ಸ್ಟ್ಯಾಕ್/ವಾಯರ್ಡ್_ನೆಟ್_ವರ್ಕ್.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in ವಾಯರ್ಡ್_ಮೌಲ್ಯ or 'SPDX-License-Identifier: GPL' in ವಾಯರ್ಡ್_ಮೌಲ್ಯ:
        raise SystemExit('COSL 배포 ನಿಲ್ಲು: BSD GENET 구현·고지 ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು 필요')
    for ಹೆಸರು in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (ಸಂಗ್ರಹಣೆ_ಮೂಲ / ಹೆಸರು).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + ಹೆಸರು)
    ಚಿಹ್ನೆ_ಮೌಲ್ಯ = subprocess.check_output(['aarch64-linux-gnu-nm', str(ಬಿಂಬಿಸು_ಮೂಲ / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', ಚಿಹ್ನೆ_ಮೌಲ್ಯ):
        raise SystemExit('COSL 배포 ನಿಲ್ಲು: 커널에 이전 GPL ಪಾಸ್_ವರ್ಡ್_ಮೌಲ್ಯ/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for ಹೆಸರು in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + ಹೆಸರು + r'$', ಚಿಹ್ನೆ_ಮೌಲ್ಯ, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + ಹೆಸರು)
    with tempfile.TemporaryDirectory(dir=str(ಬಿಂಬಿಸು_ಮೂಲ / 'build')) as 임시:
        ಇಮೇಜ್_ಮೌಲ್ಯ = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(ಬಿಂಬಿಸು_ಮೂಲ / 'build/kernel.elf'), str(ಇಮೇಜ್_ಮೌಲ್ಯ)])
        if ಹ್ಯಾಶ್_ಫೈಲ್(ಇಮೇಜ್_ಮೌಲ್ಯ) != ಹ್ಯಾಶ್_ಫೈಲ್(ಬಿಂಬಿಸು_ಮೂಲ / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    ವರದಿ_ಮೌಲ್ಯ = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': ಹ್ಯಾಶ್_ಫೈಲ್(ಬಿಂಬಿಸು_ಮೂಲ / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {ಹೆಸರು: ಹ್ಯಾಶ್_ಫೈಲ್(ಬಿಂಬಿಸು_ಮೂಲ / 'build' / ಹೆಸರು) for ಹೆಸರು in ಲೈಬ್ರರಿ}}
    (ಬಿಂಬಿಸು_ಮೂಲ / 'build/cosl-distribution-check.json').write_text(json.dumps(ವರದಿ_ಮೌಲ್ಯ, ensure_ascii=False, indent=2) + '\n')
    return ವರದಿ_ಮೌಲ್ಯ


def 묶기():
    ವರದಿ_ಮೌಲ್ಯ = 점검()
    배포 = ಬಿಂಬಿಸು_ಮೂಲ / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(ಬಿಂಬಿಸು_ಮೂಲ / 'build')) as 임시:
        ಸಮೂಹ_ಮೌಲ್ಯ = Path(임시) / 'jkoros-native-relink'
        ಸಮೂಹ_ಮೌಲ್ಯ.mkdir()
        def ನಕಲಿಸು_ಮೌಲ್ಯ(원본, ಪೀರ್_ಮೌಲ್ಯ):
            ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ = ಸಮೂಹ_ಮೌಲ್ಯ / ಪೀರ್_ಮೌಲ್ಯ
            ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ))
        for ಹೆಸರು in ಗಮ್ಯಸ್ಥಾನ_ಹೆಸರು:
            ನಕಲಿಸು_ಮೌಲ್ಯ(ಬಿಂಬಿಸು_ಮೂಲ / 'build' / (ಹೆಸರು + '.o'), 'objects/' + ಹೆಸರು + '.o')
        for ಹೆಸರು in ಲೈಬ್ರರಿ:
            ನಕಲಿಸು_ಮೌಲ್ಯ(ಬಿಂಬಿಸು_ಮೂಲ / 'build' / ಹೆಸರು, 'objects/' + Path(ಹೆಸರು).name)
        for ಹೆಸರು in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'ಬಳಕೆದಾರ', '명명', 'ಯಂತ್ರ', 'ನೆಟ್_ವರ್ಕ್_ಸ್ಟ್ಯಾಕ್/ನೆಟ್_ವರ್ಕ್_ಸ್ಟ್ಯಾಕ್.h', '부팅/ಜೋಡಣೆ_ಲೇಔಟ್.ld',
                     'ರಿಮೋಟ್_ಮೌಲ್ಯ/assh_config.h', 'ರಿಮೋಟ್_ಮೌಲ್ಯ/config.h', 'ರಿಮೋಟ್_ಮೌಲ್ಯ/ctype.h', 'ರಿಮೋಟ್_ಮೌಲ್ಯ/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            ನಕಲಿಸು_ಮೌಲ್ಯ(ಬಿಂಬಿಸು_ಮೂಲ / ಹೆಸರು, ಹೆಸರು)
        for ಹೆಸರು in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            ನಕಲಿಸು_ಮೌಲ್ಯ(ಸಂಗ್ರಹಣೆ_ಮೂಲ / ಹೆಸರು, ಹೆಸರು)
        for ಮಾರ್ಗ in sorted((ಬಿಂಬಿಸು_ಮೂಲ / 'vendor').glob('LICENSE*')):
            ನಕಲಿಸು_ಮೌಲ್ಯ(ಮಾರ್ಗ, 'vendor/' + ಮಾರ್ಗ.name)
        ನಕಲಿಸು_ಮೌಲ್ಯ(ಬಿಂಬಿಸು_ಮೂಲ / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        ನಕಲಿಸು_ಮೌಲ್ಯ(ಬಿಂಬಿಸು_ಮೂಲ / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        ನಕಲಿಸು_ಮೌಲ್ಯ(ಸಂಗ್ರಹಣೆ_ಮೂಲ / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        ನಕಲಿಸು_ಮೌಲ್ಯ(ಬಿಂಬಿಸು_ಮೂಲ / 'ಪರಿಕರಗಳು/재연결.py', 'relink.py')
        for ಮಾರ್ಗ in sorted((ಬಿಂಬಿಸು_ಮೂಲ / 'build/user').glob('*.elf')):
            ನಕಲಿಸು_ಮೌಲ್ಯ(ಮಾರ್ಗ, 'build/user/' + ಮಾರ್ಗ.name)
        for ಹೆಸರು in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            ನಕಲಿಸು_ಮೌಲ್ಯ(ಬಿಂಬಿಸು_ಮೂಲ / 'build/user' / (ಹೆಸರು + '.o'), 'build/user/' + ಹೆಸರು + '.o')
        for ಹೆಸರು in ('crt', 'aot-runtime', 'ಸಾಮಾನ್ಯ_ಭಾಷೆಯ_ಚಾಲ್ತಿ_ಸಮಯ_ಬೆಂಬಲ', 'ಚಲಾಯಿಸು_2', '미리번역', '되돌림'):
            ನಕಲಿಸು_ಮೌಲ್ಯ(ಬಿಂಬಿಸು_ಮೂಲ / 'build/ccompiler' / (ಹೆಸರು + '.o'), 'build/ccompiler/' + ಹೆಸರು + '.o')
        명세 = dict(ವರದಿ_ಮೌಲ್ಯ, objects=['objects/' + ಹೆಸರು + '.o' for ಹೆಸರು in ಗಮ್ಯಸ್ಥಾನ_ಹೆಸರು],
                    libraries=['objects/' + Path(ಮಾರ್ಗ).name for ಮಾರ್ಗ in ಲೈಬ್ರರಿ])
        (ಸಮೂಹ_ಮೌಲ್ಯ / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (ಸಮೂಹ_ಮೌಲ್ಯ / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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

TinyCC source is included in vendor/tinycc; the native port is in 시언어번역기.
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
        ಲಕ್ಷ್ಯ = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / ಲಕ್ಷ್ಯ.name
        with tarfile.open(str(임시압축), 'w:gz') as ಅರ್ಖೀವ್_ಮೌಲ್ಯ:
            ಅರ್ಖೀವ್_ಮೌಲ್ಯ.add(str(ಸಮೂಹ_ಮೌಲ್ಯ), arcname=ಸಮೂಹ_ಮೌಲ್ಯ.name)
        임시압축.replace(ಲಕ್ಷ್ಯ)
    ವರದಿ_ಮೌಲ್ಯ['relink_archive_sha256'] = ಹ್ಯಾಶ್_ಫೈಲ್(ಲಕ್ಷ್ಯ)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(ವರದಿ_ಮೌಲ್ಯ, ensure_ascii=False, indent=2) + '\n')
    return ಲಕ್ಷ್ಯ


if __name__ == '__main__':
    ಪಾರ್ಸರ್_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ಪಾರ್ಸರ್_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    ಮೌಲ್ಯ = ಪಾರ್ಸರ್_48ee4b1b.parse_args()
    if ಮೌಲ್ಯ.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
