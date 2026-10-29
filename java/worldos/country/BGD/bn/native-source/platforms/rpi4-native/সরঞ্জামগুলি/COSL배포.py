#!/usr/bin/env python3
"""현재 নিজ ARM64 산출물을 검사하고 LGPL উত্স_ট্রী·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

প্রকল্প_মূল = Path(__file__).resolve().parents[1]
সংগ্রহস্থলের_মূল = প্রকল্প_মূল.parents[1]
গন্তব্য_নাম = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
লাইব্রেরি = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def হ্যাশ_ফাইল(পথ_2):
    return hashlib.sha256(Path(পথ_2).read_bytes()).hexdigest()


def 점검():
    for নাম in ('vendor/wolfssh', 'vendor/wolfssl', 'দূরবর্তী_মান/user_settings.h'):
        if (প্রকল্প_মূল / নাম).exists():
            raise SystemExit('COSL 배포 বন্ধ_করুন_2: 이전 GPL দূরবর্তী_মান 구현이 উত্স_ট্রী 트리에 남아 있습니다: ' + নাম)
    ওয়্যার্ড_মান = (প্রকল্প_মূল / 'নেটওয়ার্ক_গাদা/ওয়্যার্ড_নেটওয়ার্ক.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in ওয়্যার্ড_মান or 'SPDX-License-Identifier: GPL' in ওয়্যার্ড_মান:
        raise SystemExit('COSL 배포 বন্ধ_করুন_2: BSD GENET 구현·고지 যাচাই_করা 필요')
    for নাম in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (সংগ্রহস্থলের_মূল / নাম).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + নাম)
    প্রতীক_মান = subprocess.check_output(['aarch64-linux-gnu-nm', str(প্রকল্প_মূল / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', প্রতীক_মান):
        raise SystemExit('COSL 배포 বন্ধ_করুন_2: 커널에 이전 GPL পাসওয়ার্ড_মান/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for নাম in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + নাম + r'$', প্রতীক_মান, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + নাম)
    with tempfile.TemporaryDirectory(dir=str(প্রকল্প_মূল / 'build')) as 임시:
        ছবি_মান = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(প্রকল্প_মূল / 'build/kernel.elf'), str(ছবি_মান)])
        if হ্যাশ_ফাইল(ছবি_মান) != হ্যাশ_ফাইল(প্রকল্প_মূল / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    রিপোর্ট_মান = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': হ্যাশ_ফাইল(প্রকল্প_মূল / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {নাম: হ্যাশ_ফাইল(প্রকল্প_মূল / 'build' / নাম) for নাম in লাইব্রেরি}}
    (প্রকল্প_মূল / 'build/cosl-distribution-check.json').write_text(json.dumps(রিপোর্ট_মান, ensure_ascii=False, indent=2) + '\n')
    return রিপোর্ট_মান


def 묶기():
    রিপোর্ট_মান = 점검()
    배포 = প্রকল্প_মূল / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(প্রকল্প_মূল / 'build')) as 임시:
        দল_মান = Path(임시) / 'jkoros-native-relink'
        দল_মান.mkdir()
        def নজির_মান(원본, পিয়ার_মান):
            গন্তব্য_মান = দল_মান / পিয়ার_মান
            গন্তব্য_মান.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(গন্তব্য_মান), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(গন্তব্য_মান))
        for নাম in গন্তব্য_নাম:
            নজির_মান(প্রকল্প_মূল / 'build' / (নাম + '.o'), 'objects/' + নাম + '.o')
        for নাম in লাইব্রেরি:
            নজির_মান(প্রকল্প_মূল / 'build' / নাম, 'objects/' + Path(নাম).name)
        for নাম in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'ব্যবহারকারী', '명명', 'মেশিন', 'নেটওয়ার্ক_গাদা/নেটওয়ার্ক_গাদা.h', '부팅/লিংক_লেআউট.ld',
                     'দূরবর্তী_মান/assh_config.h', 'দূরবর্তী_মান/config.h', 'দূরবর্তী_মান/ctype.h', 'দূরবর্তী_মান/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            নজির_মান(প্রকল্প_মূল / নাম, নাম)
        for নাম in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            নজির_মান(সংগ্রহস্থলের_মূল / নাম, নাম)
        for পথ_2 in sorted((প্রকল্প_মূল / 'vendor').glob('LICENSE*')):
            নজির_মান(পথ_2, 'vendor/' + পথ_2.name)
        নজির_মান(প্রকল্প_মূল / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        নজির_মান(প্রকল্প_মূল / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        নজির_মান(সংগ্রহস্থলের_মূল / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        নজির_মান(প্রকল্প_মূল / 'সরঞ্জামগুলি/재연결.py', 'relink.py')
        for পথ_2 in sorted((প্রকল্প_মূল / 'build/user').glob('*.elf')):
            নজির_মান(পথ_2, 'build/user/' + পথ_2.name)
        for নাম in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            নজির_মান(প্রকল্প_মূল / 'build/user' / (নাম + '.o'), 'build/user/' + নাম + '.o')
        for নাম in ('crt', 'aot-runtime', 'সাধারণ_ভাষা_রানটাইম_সমর্থন', 'চালনা', '미리번역', '되돌림'):
            নজির_মান(প্রকল্প_মূল / 'build/ccompiler' / (নাম + '.o'), 'build/ccompiler/' + নাম + '.o')
        명세 = dict(রিপোর্ট_মান, objects=['objects/' + নাম + '.o' for নাম in গন্তব্য_নাম],
                    libraries=['objects/' + Path(পথ_2).name for পথ_2 in লাইব্রেরি])
        (দল_মান / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (দল_মান / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        লক্ষ্য = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / লক্ষ্য.name
        with tarfile.open(str(임시압축), 'w:gz') as সংগ্রহ_করা_মান:
            সংগ্রহ_করা_মান.add(str(দল_মান), arcname=দল_মান.name)
        임시압축.replace(লক্ষ্য)
    রিপোর্ট_মান['relink_archive_sha256'] = হ্যাশ_ফাইল(লক্ষ্য)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(রিপোর্ট_মান, ensure_ascii=False, indent=2) + '\n')
    return লক্ষ্য


if __name__ == '__main__':
    পার্সার_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    পার্সার_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    মান = পার্সার_48ee4b1b.parse_args()
    if মান.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
