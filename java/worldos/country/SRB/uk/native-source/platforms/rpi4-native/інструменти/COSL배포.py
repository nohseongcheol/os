#!/usr/bin/env python3
"""чинний_елемент своє ARM64 산출물을 검사하고 LGPL джерело_дерево·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

Дії_корінь = Path(__file__).resolve().parents[1]
репозиторій_корінь = Дії_корінь.parents[1]
місце_ім_я = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
бібліотека = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def геш_код_Файл(шлях):
    return hashlib.sha256(Path(шлях).read_bytes()).hexdigest()


def 점검():
    for Назва in ('vendor/wolfssh', 'vendor/wolfssl', 'віддалений_значення/user_settings.h'):
        if (Дії_корінь / Назва).exists():
            raise SystemExit('COSL 배포 Зупинити: 이전 GPL віддалений_значення 구현이 джерело_дерево 트리에 남아 있습니다: ' + Назва)
    проводовий_значення = (Дії_корінь / 'мережа_Стіс/проводовий_мережа.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in проводовий_значення or 'SPDX-License-Identifier: GPL' in проводовий_значення:
        raise SystemExit('COSL 배포 Зупинити: BSD GENET реалізація·고지 перевіряти 필요')
    for Назва in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (репозиторій_корінь / Назва).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + Назва)
    символ_значення = subprocess.check_output(['aarch64-linux-gnu-nm', str(Дії_корінь / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', символ_значення):
        raise SystemExit('COSL 배포 Зупинити: 커널에 이전 GPL пароль_значення/SSH 심볼이 남아 있습니다. пробувати_знову_значення 빌드하세요.')
    for Назва in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Назва + r'$', символ_значення, re.M):
            raise SystemExit('COSL 대체 реалізація 누락: ' + Назва)
    with tempfile.TemporaryDirectory(dir=str(Дії_корінь / 'build')) as 임시:
        фото_значення = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(Дії_корінь / 'build/kernel.elf'), str(фото_значення)])
        if геш_код_Файл(фото_значення) != геш_код_Файл(Дії_корінь / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    звіт_значення = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': геш_код_Файл(Дії_корінь / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Назва: геш_код_Файл(Дії_корінь / 'build' / Назва) for Назва in бібліотека}}
    (Дії_корінь / 'build/cosl-distribution-check.json').write_text(json.dumps(звіт_значення, ensure_ascii=False, indent=2) + '\n')
    return звіт_значення


def зв_язувати_учасник():
    звіт_значення = 점검()
    배포 = Дії_корінь / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(Дії_корінь / 'build')) as 임시:
        Група_значення = Path(임시) / 'jkoros-native-relink'
        Група_значення.mkdir()
        def екземпляр_значення(원본, точка_значення):
            місце_значення = Група_значення / точка_значення
            місце_значення.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(місце_значення), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(місце_значення))
        for Назва in місце_ім_я:
            екземпляр_значення(Дії_корінь / 'build' / (Назва + '.o'), 'objects/' + Назва + '.o')
        for Назва in бібліотека:
            екземпляр_значення(Дії_корінь / 'build' / Назва, 'objects/' + Path(Назва).name)
        for Назва in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'простір_користувача', '명명', 'комп_ютер', 'мережа_Стіс/мережа_Стіс.h', 'запуск_машини/схема_компонування.ld',
                     'віддалений_значення/assh_config.h', 'віддалений_значення/config.h', 'віддалений_значення/ctype.h', 'віддалений_значення/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            екземпляр_значення(Дії_корінь / Назва, Назва)
        for Назва in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            екземпляр_значення(репозиторій_корінь / Назва, Назва)
        for шлях in sorted((Дії_корінь / 'vendor').glob('LICENSE*')):
            екземпляр_значення(шлях, 'vendor/' + шлях.name)
        екземпляр_значення(Дії_корінь / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        екземпляр_значення(Дії_корінь / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        екземпляр_значення(репозиторій_корінь / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        екземпляр_значення(Дії_корінь / 'інструменти/재연결.py', 'relink.py')
        for шлях in sorted((Дії_корінь / 'build/user').glob('*.elf')):
            екземпляр_значення(шлях, 'build/user/' + шлях.name)
        for Назва in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            екземпляр_значення(Дії_корінь / 'build/user' / (Назва + '.o'), 'build/user/' + Назва + '.o')
        for Назва in ('crt', 'aot-runtime', 'загальномовне_середовище_виконання_опора', 'запустити', '미리번역', 'повернути_міст'):
            екземпляр_значення(Дії_корінь / 'build/ccompiler' / (Назва + '.o'), 'build/ccompiler/' + Назва + '.o')
        명세 = dict(звіт_значення, objects=['objects/' + Назва + '.o' for Назва in місце_ім_я],
                    libraries=['objects/' + Path(шлях).name for шлях in бібліотека])
        (Група_значення / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (Група_значення / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        мета = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / мета.name
        with tarfile.open(str(임시압축), 'w:gz') as Архів_значення:
            Архів_значення.add(str(Група_значення), arcname=Група_значення.name)
        임시압축.replace(мета)
    звіт_значення['relink_archive_sha256'] = геш_код_Файл(мета)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(звіт_значення, ensure_ascii=False, indent=2) + '\n')
    return мета


if __name__ == '__main__':
    аналізатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    аналізатор_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    значення = аналізатор_48ee4b1b.parse_args()
    if значення.command == 'bundle':
        print('COSL source/relink kit:', зв_язувати_учасник())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
