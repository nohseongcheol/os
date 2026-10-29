#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL উৎস_ট্ৰি·재연결 자료를 함께 묶는다."""
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
গন্তব্য_স্থান_নাম = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
লাইব্ৰেৰী = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def হেচ_ফাইল(পথ):
    return hashlib.sha256(Path(পথ).read_bytes()).hexdigest()


def 점검():
    for নাম in ('vendor/wolfssh', 'vendor/wolfssl', 'দূৰবৰ্তী_মান/user_settings.h'):
        if (기준 / নাম).exists():
            raise SystemExit('COSL 배포 বন্ধ_কৰক_2: 이전 GPL দূৰবৰ্তী_মান 구현이 উৎস_ট্ৰি 트리에 남아 있습니다: ' + নাম)
    তাঁৰযুক্ত_মান = (기준 / 'নেটৱৰ্ক_ষ্টেক/তাঁৰযুক্ত_নেটৱৰ্ক.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in তাঁৰযুক্ত_মান or 'SPDX-License-Identifier: GPL' in তাঁৰযুক্ত_মান:
        raise SystemExit('COSL 배포 বন্ধ_কৰক_2: BSD GENET 구현·고지 প্ৰমাণিত_কৰক 필요')
    for নাম in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (저장소 / নাম).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + নাম)
    প্ৰতীক_মান = subprocess.check_output(['aarch64-linux-gnu-nm', str(기준 / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', প্ৰতীক_মান):
        raise SystemExit('COSL 배포 বন্ধ_কৰক_2: 커널에 이전 GPL পাছৱৰ্ড_মান/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for নাম in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + নাম + r'$', প্ৰতীক_মান, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + নাম)
    with tempfile.TemporaryDirectory(dir=str(기준 / 'build')) as 임시:
        ছবি_মান = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(기준 / 'build/kernel.elf'), str(ছবি_মান)])
        if হেচ_ফাইল(ছবি_মান) != হেচ_ফাইল(기준 / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    ৰিপ_ৰ্ট_মান = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': হেচ_ফাইল(기준 / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {নাম: হেচ_ফাইল(기준 / 'build' / নাম) for নাম in লাইব্ৰেৰী}}
    (기준 / 'build/cosl-distribution-check.json').write_text(json.dumps(ৰিপ_ৰ্ট_মান, ensure_ascii=False, indent=2) + '\n')
    return ৰিপ_ৰ্ট_মান


def 묶기():
    ৰিপ_ৰ্ট_মান = 점검()
    배포 = 기준 / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(기준 / 'build')) as 임시:
        দল_মান = Path(임시) / 'jkoros-native-relink'
        দল_মান.mkdir()
        def নজিৰ_মান(원본, পীয়েৰ_মান):
            গন্তব্য_স্থান_মান = দল_মান / পীয়েৰ_মান
            গন্তব্য_স্থান_মান.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(গন্তব্য_স্থান_মান), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(গন্তব্য_স্থান_মান))
        for নাম in গন্তব্য_স্থান_নাম:
            নজিৰ_মান(기준 / 'build' / (নাম + '.o'), 'objects/' + নাম + '.o')
        for নাম in লাইব্ৰেৰী:
            নজিৰ_মান(기준 / 'build' / নাম, 'objects/' + Path(নাম).name)
        for নাম in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'ব্যৱহাৰকৰ্তা', '명명', 'মেচিন', 'নেটৱৰ্ক_ষ্টেক/নেটৱৰ্ক_ষ্টেক.h', '부팅/লিংক_লেআউট.ld',
                     'দূৰবৰ্তী_মান/assh_config.h', 'দূৰবৰ্তী_মান/config.h', 'দূৰবৰ্তী_মান/ctype.h', 'দূৰবৰ্তী_মান/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            নজিৰ_মান(기준 / নাম, নাম)
        for নাম in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            নজিৰ_মান(저장소 / নাম, নাম)
        for পথ in sorted((기준 / 'vendor').glob('LICENSE*')):
            নজিৰ_মান(পথ, 'vendor/' + পথ.name)
        নজিৰ_মান(기준 / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        নজিৰ_মান(기준 / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        নজিৰ_মান(저장소 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        নজিৰ_মান(기준 / 'সঁজুলিসমূহ/재연결.py', 'relink.py')
        for পথ in sorted((기준 / 'build/user').glob('*.elf')):
            নজিৰ_মান(পথ, 'build/user/' + পথ.name)
        for নাম in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            নজিৰ_মান(기준 / 'build/user' / (নাম + '.o'), 'build/user/' + নাম + '.o')
        for নাম in ('crt', 'aot-runtime', 'উমৈহতীয়া_ভাষা_ৰানটাইম_সমর্থন', 'সঞ্চালন', '미리번역', '되돌림'):
            নজিৰ_মান(기준 / 'build/ccompiler' / (নাম + '.o'), 'build/ccompiler/' + নাম + '.o')
        명세 = dict(ৰিপ_ৰ্ট_মান, objects=['objects/' + নাম + '.o' for নাম in গন্তব্য_স্থান_নাম],
                    libraries=['objects/' + Path(পথ).name for পথ in লাইব্ৰেৰী])
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
        with tarfile.open(str(임시압축), 'w:gz') as অভিলেখাগাৰ_মান:
            অভিলেখাগাৰ_মান.add(str(দল_মান), arcname=দল_মান.name)
        임시압축.replace(লক্ষ্য)
    ৰিপ_ৰ্ট_মান['relink_archive_sha256'] = হেচ_ফাইল(লক্ষ্য)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(ৰিপ_ৰ্ট_মান, ensure_ascii=False, indent=2) + '\n')
    return লক্ষ্য


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    মান = 해석기.parse_args()
    if মান.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
