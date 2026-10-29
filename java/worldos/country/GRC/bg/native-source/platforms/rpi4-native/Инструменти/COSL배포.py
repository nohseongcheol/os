#!/usr/bin/env python3
"""в_срок_артикул 자체 ARM64 산출물을 검사하고 LGPL източник_дърво·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

проект_корен = Path(__file__).resolve().parents[1]
хранилище_корен = проект_корен.parents[1]
местоназначение_препратка_към_клетка = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
библиотека = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def хеширане_Файл(ПЪТ):
    return hashlib.sha256(Path(ПЪТ).read_bytes()).hexdigest()


def 점검():
    for Име in ('vendor/wolfssh', 'vendor/wolfssl', 'отдалечен_стойност/user_settings.h'):
        if (проект_корен / Име).exists():
            raise SystemExit('COSL 배포 Спиране: 이전 GPL отдалечен_стойност 구현이 източник_дърво 트리에 남아 있습니다: ' + Име)
    кабелен_стойност = (проект_корен / 'мрежа_стек/кабелен_мрежа.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in кабелен_стойност or 'SPDX-License-Identifier: GPL' in кабелен_стойност:
        raise SystemExit('COSL 배포 Спиране: BSD GENET 구현·고지 проверявам 필요')
    for Име in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (хранилище_корен / Име).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + Име)
    символ_стойност = subprocess.check_output(['aarch64-linux-gnu-nm', str(проект_корен / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', символ_стойност):
        raise SystemExit('COSL 배포 Спиране: 커널에 이전 GPL парола_стойност/SSH 심볼이 남아 있습니다. опитвам_повторно_стойност 빌드하세요.')
    for Име in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Име + r'$', символ_стойност, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + Име)
    with tempfile.TemporaryDirectory(dir=str(проект_корен / 'build')) as 임시:
        снимка_стойност = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(проект_корен / 'build/kernel.elf'), str(снимка_стойност)])
        if хеширане_Файл(снимка_стойност) != хеширане_Файл(проект_корен / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    отчет_стойност = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': хеширане_Файл(проект_корен / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Име: хеширане_Файл(проект_корен / 'build' / Име) for Име in библиотека}}
    (проект_корен / 'build/cosl-distribution-check.json').write_text(json.dumps(отчет_стойност, ensure_ascii=False, indent=2) + '\n')
    return отчет_стойност


def обвързвам_участник():
    отчет_стойност = 점검()
    배포 = проект_корен / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(проект_корен / 'build')) as 임시:
        Група_стойност = Path(임시) / 'jkoros-native-relink'
        Група_стойност.mkdir()
        def копирам_стойност(원본, крайно_устройство_стойност):
            местоназначение_стойност = Група_стойност / крайно_устройство_стойност
            местоназначение_стойност.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(местоназначение_стойност), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(местоназначение_стойност))
        for Име in местоназначение_препратка_към_клетка:
            копирам_стойност(проект_корен / 'build' / (Име + '.o'), 'objects/' + Име + '.o')
        for Име in библиотека:
            копирам_стойност(проект_корен / 'build' / Име, 'objects/' + Path(Име).name)
        for Име in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'потребител', '명명', 'машина', 'мрежа_стек/мрежа_стек.h', '부팅/Връзка_схема.ld',
                     'отдалечен_стойност/assh_config.h', 'отдалечен_стойност/config.h', 'отдалечен_стойност/ctype.h', 'отдалечен_стойност/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            копирам_стойност(проект_корен / Име, Име)
        for Име in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            копирам_стойност(хранилище_корен / Име, Име)
        for ПЪТ in sorted((проект_корен / 'vendor').glob('LICENSE*')):
            копирам_стойност(ПЪТ, 'vendor/' + ПЪТ.name)
        копирам_стойност(проект_корен / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        копирам_стойност(проект_корен / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        копирам_стойност(хранилище_корен / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        копирам_стойност(проект_корен / 'Инструменти/재연결.py', 'relink.py')
        for ПЪТ in sorted((проект_корен / 'build/user').glob('*.elf')):
            копирам_стойност(ПЪТ, 'build/user/' + ПЪТ.name)
        for Име in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            копирам_стойност(проект_корен / 'build/user' / (Име + '.o'), 'build/user/' + Име + '.o')
        for Име in ('crt', 'aot-runtime', 'обща_езикова_среда_Поддръжка', 'Стартиране', '미리번역', 'връщам_мост'):
            копирам_стойност(проект_корен / 'build/ccompiler' / (Име + '.o'), 'build/ccompiler/' + Име + '.o')
        명세 = dict(отчет_стойност, objects=['objects/' + Име + '.o' for Име in местоназначение_препратка_към_клетка],
                    libraries=['objects/' + Path(ПЪТ).name for ПЪТ in библиотека])
        (Група_стойност / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (Група_стойност / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        цел = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / цел.name
        with tarfile.open(str(임시압축), 'w:gz') as Архив_стойност:
            Архив_стойност.add(str(Група_стойност), arcname=Група_стойност.name)
        임시압축.replace(цел)
    отчет_стойност['relink_archive_sha256'] = хеширане_Файл(цел)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(отчет_стойност, ensure_ascii=False, indent=2) + '\n')
    return цел


if __name__ == '__main__':
    анализатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    анализатор_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    стойност = анализатор_48ee4b1b.parse_args()
    if стойност.command == 'bundle':
        print('COSL source/relink kit:', обвързвам_участник())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
