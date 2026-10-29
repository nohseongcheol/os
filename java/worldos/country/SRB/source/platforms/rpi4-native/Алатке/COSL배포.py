#!/usr/bin/env python3
"""актуелно_ставка 자체 ARM64 산출물을 검사하고 LGPL извор_стабло·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

пројектовати_корен = Path(__file__).resolve().parents[1]
депо_корен = пројектовати_корен.parents[1]
одредиште_име = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
библиотека = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def хеш_фајл(ПУТАЊА):
    return hashlib.sha256(Path(ПУТАЊА).read_bytes()).hexdigest()


def 점검():
    for Назив in ('vendor/wolfssh', 'vendor/wolfssl', 'удаљен_вриједност/user_settings.h'):
        if (пројектовати_корен / Назив).exists():
            raise SystemExit('COSL 배포 Заустави: 이전 GPL удаљен_вриједност 구현이 извор_стабло 트리에 남아 있습니다: ' + Назив)
    ожичен_вриједност = (пројектовати_корен / 'Мрежа_комплет/ожичен_Мрежа.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in ожичен_вриједност or 'SPDX-License-Identifier: GPL' in ожичен_вриједност:
        raise SystemExit('COSL 배포 Заустави: BSD GENET 구현·고지 потврдити 필요')
    for Назив in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (депо_корен / Назив).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + Назив)
    симбол_вриједност = subprocess.check_output(['aarch64-linux-gnu-nm', str(пројектовати_корен / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', симбол_вриједност):
        raise SystemExit('COSL 배포 Заустави: 커널에 이전 GPL лозинка_вриједност/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for Назив in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Назив + r'$', симбол_вриједност, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + Назив)
    with tempfile.TemporaryDirectory(dir=str(пројектовати_корен / 'build')) as 임시:
        слика_вриједност = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(пројектовати_корен / 'build/kernel.elf'), str(слика_вриједност)])
        if хеш_фајл(слика_вриједност) != хеш_фајл(пројектовати_корен / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    извештај_вриједност = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': хеш_фајл(пројектовати_корен / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Назив: хеш_фајл(пројектовати_корен / 'build' / Назив) for Назив in библиотека}}
    (пројектовати_корен / 'build/cosl-distribution-check.json').write_text(json.dumps(извештај_вриједност, ensure_ascii=False, indent=2) + '\n')
    return извештај_вриједност


def повезати_крајња_тачка():
    извештај_вриједност = 점검()
    배포 = пројектовати_корен / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(пројектовати_корен / 'build')) as 임시:
        Група_вриједност = Path(임시) / 'jkoros-native-relink'
        Група_вриједност.mkdir()
        def инстанца_вриједност(원본, 상대):
            одредиште_вриједност = Група_вриједност / 상대
            одредиште_вриједност.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(одредиште_вриједност), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(одредиште_вриједност))
        for Назив in одредиште_име:
            инстанца_вриједност(пројектовати_корен / 'build' / (Назив + '.o'), 'objects/' + Назив + '.o')
        for Назив in библиотека:
            инстанца_вриједност(пројектовати_корен / 'build' / Назив, 'objects/' + Path(Назив).name)
        for Назив in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'корисник', '명명', 'рачунар', 'Мрежа_комплет/Мрежа_комплет.h', '부팅/Веза_изглед.ld',
                     'удаљен_вриједност/assh_config.h', 'удаљен_вриједност/config.h', 'удаљен_вриједност/ctype.h', 'удаљен_вриједност/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            инстанца_вриједност(пројектовати_корен / Назив, Назив)
        for Назив in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            инстанца_вриједност(депо_корен / Назив, Назив)
        for ПУТАЊА in sorted((пројектовати_корен / 'vendor').glob('LICENSE*')):
            инстанца_вриједност(ПУТАЊА, 'vendor/' + ПУТАЊА.name)
        инстанца_вриједност(пројектовати_корен / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        инстанца_вриједност(пројектовати_корен / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        инстанца_вриједност(депо_корен / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        инстанца_вриједност(пројектовати_корен / 'Алатке/재연결.py', 'relink.py')
        for ПУТАЊА in sorted((пројектовати_корен / 'build/user').glob('*.elf')):
            инстанца_вриједност(ПУТАЊА, 'build/user/' + ПУТАЊА.name)
        for Назив in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            инстанца_вриједност(пројектовати_корен / 'build/user' / (Назив + '.o'), 'build/user/' + Назив + '.o')
        for Назив in ('crt', 'aot-runtime', 'заједничка_извршна_језичка_компонента_Подршка', 'Покрени', '미리번역', 'вратити_мост'):
            инстанца_вриједност(пројектовати_корен / 'build/ccompiler' / (Назив + '.o'), 'build/ccompiler/' + Назив + '.o')
        명세 = dict(извештај_вриједност, objects=['objects/' + Назив + '.o' for Назив in одредиште_име],
                    libraries=['objects/' + Path(ПУТАЊА).name for ПУТАЊА in библиотека])
        (Група_вриједност / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (Група_вриједност / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        with tarfile.open(str(임시압축), 'w:gz') as Архива_вриједност:
            Архива_вриједност.add(str(Група_вриједност), arcname=Група_вриједност.name)
        임시압축.replace(циљ)
    извештај_вриједност['relink_archive_sha256'] = хеш_фајл(циљ)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(извештај_вриједност, ensure_ascii=False, indent=2) + '\n')
    return циљ


if __name__ == '__main__':
    анализатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    анализатор_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    вриједност = анализатор_48ee4b1b.parse_args()
    if вриједност.command == 'bundle':
        print('COSL source/relink kit:', повезати_крајња_тачка())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
