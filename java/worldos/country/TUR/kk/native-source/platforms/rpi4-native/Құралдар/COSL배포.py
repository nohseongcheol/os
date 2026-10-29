#!/usr/bin/env python3
"""ток_элемент 자체 ARM64 산출물을 검사하고 LGPL көз_дарақ·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

жоба_түбір = Path(__file__).resolve().parents[1]
репозиторий_түбір = жоба_түбір.parents[1]
тағайындау_аты = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
кітапхана = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def хэш_файл(Жол_2):
    return hashlib.sha256(Path(Жол_2).read_bytes()).hexdigest()


def 점검():
    for Аты in ('vendor/wolfssh', 'vendor/wolfssl', '원격/user_settings.h'):
        if (жоба_түбір / Аты).exists():
            raise SystemExit('COSL 배포 Тоқтату: 이전 GPL 원격 구현이 көз_дарақ 트리에 남아 있습니다: ' + Аты)
    сымды_мән = (жоба_түбір / 'желі_Бума/сымды_желі.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in сымды_мән or 'SPDX-License-Identifier: GPL' in сымды_мән:
        raise SystemExit('COSL 배포 Тоқтату: BSD GENET 구현·고지 тексеру 필요')
    for Аты in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (репозиторий_түбір / Аты).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + Аты)
    символ_мән = subprocess.check_output(['aarch64-linux-gnu-nm', str(жоба_түбір / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', символ_мән):
        raise SystemExit('COSL 배포 Тоқтату: 커널에 이전 GPL құпиясөз_мән/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for Аты in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Аты + r'$', символ_мән, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + Аты)
    with tempfile.TemporaryDirectory(dir=str(жоба_түбір / 'build')) as 임시:
        сурет_мән = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(жоба_түбір / 'build/kernel.elf'), str(сурет_мән)])
        if хэш_файл(сурет_мән) != хэш_файл(жоба_түбір / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    есеп_мән = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': хэш_файл(жоба_түбір / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Аты: хэш_файл(жоба_түбір / 'build' / Аты) for Аты in кітапхана}}
    (жоба_түбір / 'build/cosl-distribution-check.json').write_text(json.dumps(есеп_мән, ensure_ascii=False, indent=2) + '\n')
    return есеп_мән


def байланыстыру_қатысушы():
    есеп_мән = 점검()
    배포 = жоба_түбір / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(жоба_түбір / 'build')) as 임시:
        Топ_мән = Path(임시) / 'jkoros-native-relink'
        Топ_мән.mkdir()
        def дана_мән(원본, бір_рангілі_мән):
            тағайындау_мән = Топ_мән / бір_рангілі_мән
            тағайындау_мән.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(тағайындау_мән), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(тағайындау_мән))
        for Аты in тағайындау_аты:
            дана_мән(жоба_түбір / 'build' / (Аты + '.o'), 'objects/' + Аты + '.o')
        for Аты in кітапхана:
            дана_мән(жоба_түбір / 'build' / Аты, 'objects/' + Path(Аты).name)
        for Аты in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'пайдаланушы', '명명', 'компьютер', 'желі_Бума/желі_Бума.h', '부팅/Cілтеме_макет.ld',
                     '원격/assh_config.h', '원격/config.h', '원격/ctype.h', '원격/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            дана_мән(жоба_түбір / Аты, Аты)
        for Аты in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            дана_мән(репозиторий_түбір / Аты, Аты)
        for Жол_2 in sorted((жоба_түбір / 'vendor').glob('LICENSE*')):
            дана_мән(Жол_2, 'vendor/' + Жол_2.name)
        дана_мән(жоба_түбір / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        дана_мән(жоба_түбір / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        дана_мән(репозиторий_түбір / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        дана_мән(жоба_түбір / 'Құралдар/재연결.py', 'relink.py')
        for Жол_2 in sorted((жоба_түбір / 'build/user').glob('*.elf')):
            дана_мән(Жол_2, 'build/user/' + Жол_2.name)
        for Аты in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            дана_мән(жоба_түбір / 'build/user' / (Аты + '.o'), 'build/user/' + Аты + '.o')
        for Аты in ('crt', 'aot-runtime', 'CLR_ортасы_тіреу', 'Орындау_2', '미리번역', 'қайтару_көпір'):
            дана_мән(жоба_түбір / 'build/ccompiler' / (Аты + '.o'), 'build/ccompiler/' + Аты + '.o')
        сипаттама = dict(есеп_мән, objects=['objects/' + Аты + '.o' for Аты in тағайындау_аты],
                    libraries=['objects/' + Path(Жол_2).name for Жол_2 in кітапхана])
        (Топ_мән / 'relink.json').write_text(json.dumps(сипаттама, ensure_ascii=False, indent=2) + '\n')
        (Топ_мән / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        мақсатты_мән = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / мақсатты_мән.name
        with tarfile.open(str(임시압축), 'w:gz') as Мұрағат_мән:
            Мұрағат_мән.add(str(Топ_мән), arcname=Топ_мән.name)
        임시압축.replace(мақсатты_мән)
    есеп_мән['relink_archive_sha256'] = хэш_файл(мақсатты_мән)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(есеп_мән, ensure_ascii=False, indent=2) + '\n')
    return мақсатты_мән


if __name__ == '__main__':
    талдау_құралы_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    талдау_құралы_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    мән = талдау_құралы_48ee4b1b.parse_args()
    if мән.command == 'bundle':
        print('COSL source/relink kit:', байланыстыру_қатысушы())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
