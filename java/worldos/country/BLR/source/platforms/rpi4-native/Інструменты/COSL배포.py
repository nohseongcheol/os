#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL крыніца_дрэва·재연결 자료를 함께 묶는다."""
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
прызначэнне_імя = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
бібліятэка = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def хэш_файл(ШЛЯХ):
    return hashlib.sha256(Path(ШЛЯХ).read_bytes()).hexdigest()


def 점검():
    for Назва in ('vendor/wolfssh', 'vendor/wolfssl', 'аддалены_значэнне/user_settings.h'):
        if (기준 / Назва).exists():
            raise SystemExit('COSL 배포 Спыніць: 이전 GPL аддалены_значэнне 구현이 крыніца_дрэва 트리에 남아 있습니다: ' + Назва)
    유선 = (기준 / 'Сетка_Стэк/유선망.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in 유선 or 'SPDX-License-Identifier: GPL' in 유선:
        raise SystemExit('COSL 배포 Спыніць: BSD GENET 구현·고지 праверыць 필요')
    for Назва in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (저장소 / Назва).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + Назва)
    сімвал_значэнне = subprocess.check_output(['aarch64-linux-gnu-nm', str(기준 / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', сімвал_значэнне):
        raise SystemExit('COSL 배포 Спыніць: 커널에 이전 GPL пароль_значэнне/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for Назва in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Назва + r'$', сімвал_значэнне, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + Назва)
    with tempfile.TemporaryDirectory(dir=str(기준 / 'build')) as 임시:
        выява_значэнне = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(기준 / 'build/kernel.elf'), str(выява_значэнне)])
        if хэш_файл(выява_значэнне) != хэш_файл(기준 / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    справаздача_значэнне = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': хэш_файл(기준 / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Назва: хэш_файл(기준 / 'build' / Назва) for Назва in бібліятэка}}
    (기준 / 'build/cosl-distribution-check.json').write_text(json.dumps(справаздача_значэнне, ensure_ascii=False, indent=2) + '\n')
    return справаздача_значэнне


def 묶기():
    справаздача_значэнне = 점검()
    배포 = 기준 / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(기준 / 'build')) as 임시:
        Група_значэнне = Path(임시) / 'jkoros-native-relink'
        Група_значэнне.mkdir()
        def капіяваць_значэнне(원본, аднарангавы_значэнне):
            прызначэнне_значэнне_a0fbc067 = Група_значэнне / аднарангавы_значэнне
            прызначэнне_значэнне_a0fbc067.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(прызначэнне_значэнне_a0fbc067), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(прызначэнне_значэнне_a0fbc067))
        for Назва in прызначэнне_імя:
            капіяваць_значэнне(기준 / 'build' / (Назва + '.o'), 'objects/' + Назва + '.o')
        for Назва in бібліятэка:
            капіяваць_значэнне(기준 / 'build' / Назва, 'objects/' + Path(Назва).name)
        for Назва in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'карыстальнік', '명명', 'камп_ютар', 'Сетка_Стэк/Сетка_Стэк.h', '부팅/сувязь_Макет.ld',
                     'аддалены_значэнне/assh_config.h', 'аддалены_значэнне/config.h', 'аддалены_значэнне/ctype.h', 'аддалены_значэнне/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            капіяваць_значэнне(기준 / Назва, Назва)
        for Назва in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            капіяваць_значэнне(저장소 / Назва, Назва)
        for ШЛЯХ in sorted((기준 / 'vendor').glob('LICENSE*')):
            капіяваць_значэнне(ШЛЯХ, 'vendor/' + ШЛЯХ.name)
        капіяваць_значэнне(기준 / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        капіяваць_значэнне(기준 / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        капіяваць_значэнне(저장소 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        капіяваць_значэнне(기준 / 'Інструменты/재연결.py', 'relink.py')
        for ШЛЯХ in sorted((기준 / 'build/user').glob('*.elf')):
            капіяваць_значэнне(ШЛЯХ, 'build/user/' + ШЛЯХ.name)
        for Назва in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            капіяваць_значэнне(기준 / 'build/user' / (Назва + '.o'), 'build/user/' + Назва + '.o')
        for Назва in ('crt', 'aot-runtime', 'агульнамоўная_серада_выканання_апора', 'Выканаць', '미리번역', '되돌림'):
            капіяваць_значэнне(기준 / 'build/ccompiler' / (Назва + '.o'), 'build/ccompiler/' + Назва + '.o')
        명세 = dict(справаздача_значэнне, objects=['objects/' + Назва + '.o' for Назва in прызначэнне_імя],
                    libraries=['objects/' + Path(ШЛЯХ).name for ШЛЯХ in бібліятэка])
        (Група_значэнне / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (Група_значэнне / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        мэтавы_паказчык = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / мэтавы_паказчык.name
        with tarfile.open(str(임시압축), 'w:gz') as Архіў_значэнне:
            Архіў_значэнне.add(str(Група_значэнне), arcname=Група_значэнне.name)
        임시압축.replace(мэтавы_паказчык)
    справаздача_значэнне['relink_archive_sha256'] = хэш_файл(мэтавы_паказчык)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(справаздача_значэнне, ensure_ascii=False, indent=2) + '\n')
    return мэтавы_паказчык


if __name__ == '__main__':
    аналізатар_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    аналізатар_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    значэнне = аналізатар_48ee4b1b.parse_args()
    if значэнне.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
