#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL извор_стабло·재연결 자료를 함께 묶는다."""
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
одредиште_назив = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
библиотека = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def 해시(пут):
    return hashlib.sha256(Path(пут).read_bytes()).hexdigest()


def 점검():
    for назив in ('vendor/wolfssh', 'vendor/wolfssl', 'удаљено_вриједност/user_settings.h'):
        if (기준 / назив).exists():
            raise SystemExit('COSL 배포 стати: 이전 GPL удаљено_вриједност 구현이 извор_стабло 트리에 남아 있습니다: ' + назив)
    ожичен_вриједност = (기준 / '통신망/ожичен_Мрежа.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in ожичен_вриједност or 'SPDX-License-Identifier: GPL' in ожичен_вриједност:
        raise SystemExit('COSL 배포 стати: BSD GENET 구현·고지 потврдити 필요')
    for назив in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (저장소 / назив).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + назив)
    심볼 = subprocess.check_output(['aarch64-linux-gnu-nm', str(기준 / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', 심볼):
        raise SystemExit('COSL 배포 стати: 커널에 이전 GPL лозинка_вриједност/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for назив in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + назив + r'$', 심볼, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + назив)
    with tempfile.TemporaryDirectory(dir=str(기준 / 'build')) as 임시:
        слика_вриједност = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(기준 / 'build/kernel.elf'), str(слика_вриједност)])
        if 해시(слика_вриједност) != 해시(기준 / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    извјештај_вриједност = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': 해시(기준 / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {назив: 해시(기준 / 'build' / назив) for назив in библиотека}}
    (기준 / 'build/cosl-distribution-check.json').write_text(json.dumps(извјештај_вриједност, ensure_ascii=False, indent=2) + '\n')
    return извјештај_вриједност


def повезати_крајња_тачка_bbe6b410():
    извјештај_вриједност = 점검()
    배포 = 기준 / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(기준 / 'build')) as 임시:
        група_вриједност = Path(임시) / 'jkoros-native-relink'
        група_вриједност.mkdir()
        def инстанца_вриједност(원본, peer_вриједност):
            одредиште_вриједност = група_вриједност / peer_вриједност
            одредиште_вриједност.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(одредиште_вриједност), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(одредиште_вриједност))
        for назив in одредиште_назив:
            инстанца_вриједност(기준 / 'build' / (назив + '.o'), 'objects/' + назив + '.o')
        for назив in библиотека:
            инстанца_вриједност(기준 / 'build' / назив, 'objects/' + Path(назив).name)
        for назив in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'корисник', '명명', '기계', '통신망/통신망.h', '부팅/веза_изглед.ld',
                     'удаљено_вриједност/assh_config.h', 'удаљено_вриједност/config.h', 'удаљено_вриједност/ctype.h', 'удаљено_вриједност/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            инстанца_вриједност(기준 / назив, назив)
        for назив in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            инстанца_вриједност(저장소 / назив, назив)
        for пут in sorted((기준 / 'vendor').glob('LICENSE*')):
            инстанца_вриједност(пут, 'vendor/' + пут.name)
        инстанца_вриједност(기준 / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        инстанца_вриједност(기준 / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        инстанца_вриједност(저장소 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        инстанца_вриједност(기준 / '도구/재연결.py', 'relink.py')
        for пут in sorted((기준 / 'build/user').glob('*.elf')):
            инстанца_вриједност(пут, 'build/user/' + пут.name)
        for назив in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            инстанца_вриједност(기준 / 'build/user' / (назив + '.o'), 'build/user/' + назив + '.o')
        for назив in ('crt', 'aot-runtime', '실행지원', '시작', '미리번역', '되돌림'):
            инстанца_вриједност(기준 / 'build/ccompiler' / (назив + '.o'), 'build/ccompiler/' + назив + '.o')
        명세 = dict(извјештај_вриједност, objects=['objects/' + назив + '.o' for назив in одредиште_назив],
                    libraries=['objects/' + Path(пут).name for пут in библиотека])
        (група_вриједност / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (група_вриједност / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        циљ = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / циљ.name
        with tarfile.open(str(임시압축), 'w:gz') as архива_вриједност:
            архива_вриједност.add(str(група_вриједност), arcname=група_вриједност.name)
        임시압축.replace(циљ)
    извјештај_вриједност['relink_archive_sha256'] = 해시(циљ)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(извјештај_вриједност, ensure_ascii=False, indent=2) + '\n')
    return циљ


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    вриједност = 해석기.parse_args()
    if вриједност.command == 'bundle':
        print('COSL source/relink kit:', повезати_крајња_тачка_bbe6b410())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
