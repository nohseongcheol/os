#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL чыганак_агач·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

экранга_җибәрү_тамыр = Path(__file__).resolve().parents[1]
저장소 = экранга_җибәрү_тамыр.parents[1]
күчерү_урыны_исем = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
библиотека = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def Хәш_файл(Yul):
    return hashlib.sha256(Path(Yul).read_bytes()).hexdigest()


def 점검():
    for исем in ('vendor/wolfssh', 'vendor/wolfssl', 'читтәге_VALUE/user_settings.h'):
        if (экранга_җибәрү_тамыр / исем).exists():
            raise SystemExit('COSL 배포 туктату: 이전 GPL читтәге_VALUE 구현이 чыганак_агач 트리에 남아 있습니다: ' + исем)
    чыбыклы_VALUE = (экранга_җибәрү_тамыр / 'Челтәр_Стәк/чыбыклы_Челтәр.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in чыбыклы_VALUE or 'SPDX-License-Identifier: GPL' in чыбыклы_VALUE:
        raise SystemExit('COSL 배포 туктату: BSD GENET 구현·고지 раслау 필요')
    for исем in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (저장소 / исем).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + исем)
    символ_VALUE = subprocess.check_output(['aarch64-linux-gnu-nm', str(экранга_җибәрү_тамыр / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', символ_VALUE):
        raise SystemExit('COSL 배포 туктату: 커널에 이전 GPL серсүз_VALUE/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for исем in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + исем + r'$', символ_VALUE, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + исем)
    with tempfile.TemporaryDirectory(dir=str(экранга_җибәрү_тамыр / 'build')) as 임시:
        IMAGE_VALUE = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(экранга_җибәрү_тамыр / 'build/kernel.elf'), str(IMAGE_VALUE)])
        if Хәш_файл(IMAGE_VALUE) != Хәш_файл(экранга_җибәрү_тамыр / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    отчет_VALUE = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': Хәш_файл(экранга_җибәрү_тамыр / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {исем: Хәш_файл(экранга_җибәрү_тамыр / 'build' / исем) for исем in библиотека}}
    (экранга_җибәрү_тамыр / 'build/cosl-distribution-check.json').write_text(json.dumps(отчет_VALUE, ensure_ascii=False, indent=2) + '\n')
    return отчет_VALUE


def 묶기():
    отчет_VALUE = 점검()
    배포 = экранга_җибәрү_тамыр / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(экранга_җибәрү_тамыр / 'build')) as 임시:
        төркем_VALUE = Path(임시) / 'jkoros-native-relink'
        төркем_VALUE.mkdir()
        def экземпляр_VALUE(원본, тиңдәш_VALUE):
            күчерү_урыны_VALUE = төркем_VALUE / тиңдәш_VALUE
            күчерү_урыны_VALUE.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(күчерү_урыны_VALUE), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(күчерү_урыны_VALUE))
        for исем in күчерү_урыны_исем:
            экземпляр_VALUE(экранга_җибәрү_тамыр / 'build' / (исем + '.o'), 'objects/' + исем + '.o')
        for исем in библиотека:
            экземпляр_VALUE(экранга_җибәрү_тамыр / 'build' / исем, 'objects/' + Path(исем).name)
        for исем in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'кулланучы', '명명', 'машина', 'Челтәр_Стәк/Челтәр_Стәк.h', '부팅/бәйләү_план.ld',
                     'читтәге_VALUE/assh_config.h', 'читтәге_VALUE/config.h', 'читтәге_VALUE/ctype.h', 'читтәге_VALUE/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            экземпляр_VALUE(экранга_җибәрү_тамыр / исем, исем)
        for исем in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            экземпляр_VALUE(저장소 / исем, исем)
        for Yul in sorted((экранга_җибәрү_тамыр / 'vendor').glob('LICENSE*')):
            экземпляр_VALUE(Yul, 'vendor/' + Yul.name)
        экземпляр_VALUE(экранга_җибәрү_тамыр / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        экземпляр_VALUE(экранга_җибәрү_тамыр / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        экземпляр_VALUE(저장소 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        экземпляр_VALUE(экранга_җибәрү_тамыр / 'Кораллар/재연결.py', 'relink.py')
        for Yul in sorted((экранга_җибәрү_тамыр / 'build/user').glob('*.elf')):
            экземпляр_VALUE(Yul, 'build/user/' + Yul.name)
        for исем in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            экземпляр_VALUE(экранга_җибәрү_тамыр / 'build/user' / (исем + '.o'), 'build/user/' + исем + '.o')
        for исем in ('crt', 'aot-runtime', 'CLR_мохите_ярдәм', 'эшләтү', '미리번역', 'кайтару_күпер'):
            экземпляр_VALUE(экранга_җибәрү_тамыр / 'build/ccompiler' / (исем + '.o'), 'build/ccompiler/' + исем + '.o')
        명세 = dict(отчет_VALUE, objects=['objects/' + исем + '.o' for исем in күчерү_урыны_исем],
                    libraries=['objects/' + Path(Yul).name for Yul in библиотека])
        (төркем_VALUE / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (төркем_VALUE / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        максат_кыйммәт = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / максат_кыйммәт.name
        with tarfile.open(str(임시압축), 'w:gz') as Архив_VALUE:
            Архив_VALUE.add(str(төркем_VALUE), arcname=төркем_VALUE.name)
        임시압축.replace(максат_кыйммәт)
    отчет_VALUE['relink_archive_sha256'] = Хәш_файл(максат_кыйммәт)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(отчет_VALUE, ensure_ascii=False, indent=2) + '\n')
    return максат_кыйммәт


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    VALUE = 해석기.parse_args()
    if VALUE.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
