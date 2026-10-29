#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL 소스·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]
목적이름 = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
라이브러리 = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def 해시(Percors):
    return hashlib.sha256(Path(Percors).read_bytes()).hexdigest()


def 점검():
    for Nom in ('vendor/wolfssh', 'vendor/wolfssl', '원격/user_settings.h'):
        if (기준 / Nom).exists():
            raise SystemExit('COSL 배포 Ferme: 이전 GPL 원격 구현이 소스 트리에 남아 있습니다: ' + Nom)
    유선 = (기준 / '통신망/유선망.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in 유선 or 'SPDX-License-Identifier: GPL' in 유선:
        raise SystemExit('COSL 배포 Ferme: BSD GENET 구현·고지 확인 필요')
    for Nom in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (저장소 / Nom).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + Nom)
    심볼 = subprocess.check_output(['aarch64-linux-gnu-nm', str(기준 / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', 심볼):
        raise SystemExit('COSL 배포 Ferme: 커널에 이전 GPL 암호/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for Nom in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Nom + r'$', 심볼, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + Nom)
    with tempfile.TemporaryDirectory(dir=str(기준 / 'build')) as 임시:
        영상 = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(기준 / 'build/kernel.elf'), str(영상)])
        if 해시(영상) != 해시(기준 / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    보고 = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': 해시(기준 / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Nom: 해시(기준 / 'build' / Nom) for Nom in 라이브러리}}
    (기준 / 'build/cosl-distribution-check.json').write_text(json.dumps(보고, ensure_ascii=False, indent=2) + '\n')
    return 보고


def 묶기():
    보고 = 점검()
    배포 = 기준 / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(기준 / 'build')) as 임시:
        묶음 = Path(임시) / 'jkoros-native-relink'
        묶음.mkdir()
        def 복사(원본, 상대):
            목적 = 묶음 / 상대
            목적.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(목적), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(목적))
        for Nom in 목적이름:
            복사(기준 / 'build' / (Nom + '.o'), 'objects/' + Nom + '.o')
        for Nom in 라이브러리:
            복사(기준 / 'build' / Nom, 'objects/' + Path(Nom).name)
        for Nom in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', '사용자', '명명', '기계', '통신망/통신망.h', '부팅/배치.ld',
                     '원격/assh_config.h', '원격/config.h', '원격/ctype.h', '원격/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            복사(기준 / Nom, Nom)
        for Nom in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            복사(저장소 / Nom, Nom)
        for Percors in sorted((기준 / 'vendor').glob('LICENSE*')):
            복사(Percors, 'vendor/' + Percors.name)
        복사(기준 / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        복사(기준 / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        복사(저장소 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        복사(기준 / '도구/재연결.py', 'relink.py')
        for Percors in sorted((기준 / 'build/user').glob('*.elf')):
            복사(Percors, 'build/user/' + Percors.name)
        for Nom in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            복사(기준 / 'build/user' / (Nom + '.o'), 'build/user/' + Nom + '.o')
        for Nom in ('crt', 'aot-runtime', '실행지원', 'Eseguis', '미리번역', '되돌림'):
            복사(기준 / 'build/ccompiler' / (Nom + '.o'), 'build/ccompiler/' + Nom + '.o')
        명세 = dict(보고, objects=['objects/' + Nom + '.o' for Nom in 목적이름],
                    libraries=['objects/' + Path(Percors).name for Percors in 라이브러리])
        (묶음 / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (묶음 / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        대상 = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / 대상.name
        with tarfile.open(str(임시압축), 'w:gz') as 압축:
            압축.add(str(묶음), arcname=묶음.name)
        임시압축.replace(대상)
    보고['relink_archive_sha256'] = 해시(대상)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(보고, ensure_ascii=False, indent=2) + '\n')
    return 대상


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    값 = 해석기.parse_args()
    if 값.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
