#!/usr/bin/env python3
"""текущий_товар свой ARM64 산출물을 검사하고 LGPL источник_дерево·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

задача_корень = Path(__file__).resolve().parents[1]
корень_репозитория = задача_корень.parents[1]
цель_имя = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
библиотека = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def хэш_файл(путь):
    return hashlib.sha256(Path(путь).read_bytes()).hexdigest()


def 점검():
    for Название in ('vendor/wolfssh', 'vendor/wolfssl', 'удаленный_ЗНАЧЕН/user_settings.h'):
        if (задача_корень / Название).exists():
            raise SystemExit('COSL распределение_ЗНАЧЕН Остановить: Назад_товар GPL удаленный_ЗНАЧЕН 구현이 источник_дерево 트리에 남아 있습니다: ' + Название)
    проводной_ЗНАЧЕН = (задача_корень / 'сеть_стек/проводной_сеть.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in проводной_ЗНАЧЕН or 'SPDX-License-Identifier: GPL' in проводной_ЗНАЧЕН:
        raise SystemExit('COSL распределение_ЗНАЧЕН Остановить: BSD GENET реализация·고지 проверять 필요')
    for Название in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (корень_репозитория / Название).is_file():
            raise SystemExit('COSL распределение_ЗНАЧЕН 고지 없음: ' + Название)
    символ_ЗНАЧЕН = subprocess.check_output(['aarch64-linux-gnu-nm', str(задача_корень / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', символ_ЗНАЧЕН):
        raise SystemExit('COSL распределение_ЗНАЧЕН Остановить: 커널에 Назад_товар GPL пароль_ЗНАЧЕН/SSH 심볼이 남아 있습니다. повторить_попытку_ЗНАЧЕН 빌드하세요.')
    for Название in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Название + r'$', символ_ЗНАЧЕН, re.M):
            raise SystemExit('COSL 대체 реализация 누락: ' + Название)
    with tempfile.TemporaryDirectory(dir=str(задача_корень / 'build')) as 임시:
        фото_ЗНАЧЕН = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(задача_корень / 'build/kernel.elf'), str(фото_ЗНАЧЕН)])
        if хэш_файл(фото_ЗНАЧЕН) != хэш_файл(задача_корень / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    Отчет_ЗНАЧЕН = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': хэш_файл(задача_корень / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Название: хэш_файл(задача_корень / 'build' / Название) for Название in библиотека}}
    (задача_корень / 'build/cosl-distribution-check.json').write_text(json.dumps(Отчет_ЗНАЧЕН, ensure_ascii=False, indent=2) + '\n')
    return Отчет_ЗНАЧЕН


def BIND_участник():
    Отчет_ЗНАЧЕН = 점검()
    распределение_ЗНАЧЕН = задача_корень / 'dist'
    распределение_ЗНАЧЕН.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(задача_корень / 'build')) as 임시:
        Группа_ЗНАЧЕН = Path(임시) / 'jkoros-native-relink'
        Группа_ЗНАЧЕН.mkdir()
        def экземпляр_ЗНАЧЕН(원본, одноранговый_ЗНАЧЕН):
            цель_ЗНАЧЕН = Группа_ЗНАЧЕН / одноранговый_ЗНАЧЕН
            цель_ЗНАЧЕН.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(цель_ЗНАЧЕН), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(цель_ЗНАЧЕН))
        for Название in цель_имя:
            экземпляр_ЗНАЧЕН(задача_корень / 'build' / (Название + '.o'), 'objects/' + Название + '.o')
        for Название in библиотека:
            экземпляр_ЗНАЧЕН(задача_корень / 'build' / Название, 'objects/' + Path(Название).name)
        for Название in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     'C_компилятор', 'пространство_пользователя', '명명', 'компьютер_5eb260fa', 'сеть_стек/сеть_стек.h', 'запуск_машины/схема_компоновки.ld',
                     'удаленный_ЗНАЧЕН/assh_config.h', 'удаленный_ЗНАЧЕН/config.h', 'удаленный_ЗНАЧЕН/ctype.h', 'удаленный_ЗНАЧЕН/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            экземпляр_ЗНАЧЕН(задача_корень / Название, Название)
        for Название in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            экземпляр_ЗНАЧЕН(корень_репозитория / Название, Название)
        for путь in sorted((задача_корень / 'vendor').glob('LICENSE*')):
            экземпляр_ЗНАЧЕН(путь, 'vendor/' + путь.name)
        экземпляр_ЗНАЧЕН(задача_корень / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        экземпляр_ЗНАЧЕН(задача_корень / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        экземпляр_ЗНАЧЕН(корень_репозитория / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        экземпляр_ЗНАЧЕН(задача_корень / 'инструменты/재연결.py', 'relink.py')
        for путь in sorted((задача_корень / 'build/user').glob('*.elf')):
            экземпляр_ЗНАЧЕН(путь, 'build/user/' + путь.name)
        for Название in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            экземпляр_ЗНАЧЕН(задача_корень / 'build/user' / (Название + '.o'), 'build/user/' + Название + '.o')
        for Название in ('crt', 'aot-runtime', 'ПоддержкаВыполнения', 'запустить', '미리번역', 'Возврат_мост'):
            экземпляр_ЗНАЧЕН(задача_корень / 'build/ccompiler' / (Название + '.o'), 'build/ccompiler/' + Название + '.o')
        спецификация = dict(Отчет_ЗНАЧЕН, objects=['objects/' + Название + '.o' for Название in цель_имя],
                    libraries=['objects/' + Path(путь).name for путь in библиотека])
        (Группа_ЗНАЧЕН / 'relink.json').write_text(json.dumps(спецификация, ensure_ascii=False, indent=2) + '\n')
        (Группа_ЗНАЧЕН / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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

TinyCC source is included in vendor/tinycc; the native port is in C_компилятор.
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
        целевое_значение = распределение_ЗНАЧЕН / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / целевое_значение.name
        with tarfile.open(str(임시압축), 'w:gz') as Архив_ЗНАЧЕН:
            Архив_ЗНАЧЕН.add(str(Группа_ЗНАЧЕН), arcname=Группа_ЗНАЧЕН.name)
        임시압축.replace(целевое_значение)
    Отчет_ЗНАЧЕН['relink_archive_sha256'] = хэш_файл(целевое_значение)
    (распределение_ЗНАЧЕН / 'cosl-distribution.json').write_text(json.dumps(Отчет_ЗНАЧЕН, ensure_ascii=False, indent=2) + '\n')
    return целевое_значение


if __name__ == '__main__':
    анализатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    анализатор_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    ЗНАЧЕН = анализатор_48ee4b1b.parse_args()
    if ЗНАЧЕН.command == 'bundle':
        print('COSL source/relink kit:', BIND_участник())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
