#!/usr/bin/env python3
"""अद्यतित_आइटम निज ARM64 산출물을 검사하고 LGPL स्रोत_ट्री·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

प्रोजेक्ट_करें_मूल = Path(__file__).resolve().parents[1]
संग्रह_मूल = प्रोजेक्ट_करें_मूल.parents[1]
गंतव्य_नाम = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
लाइब्रेरी = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def हैश_फ़ाइल(पथ):
    return hashlib.sha256(Path(पथ).read_bytes()).hexdigest()


def 점검():
    for नाम in ('vendor/wolfssh', 'vendor/wolfssl', 'दूरस्थ_मान/user_settings.h'):
        if (प्रोजेक्ट_करें_मूल / नाम).exists():
            raise SystemExit('COSL 배포 रोकें: 이전 GPL दूरस्थ_मान 구현이 स्रोत_ट्री 트리에 남아 있습니다: ' + नाम)
    वायर्ड_मान = (प्रोजेक्ट_करें_मूल / 'नेटवर्क_स्टैक/वायर्ड_नेटवर्क.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in वायर्ड_मान or 'SPDX-License-Identifier: GPL' in वायर्ड_मान:
        raise SystemExit('COSL 배포 रोकें: BSD GENET 구현·고지 सत्यापित_करें 필요')
    for नाम in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (संग्रह_मूल / नाम).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + नाम)
    प्रतीक_मान = subprocess.check_output(['aarch64-linux-gnu-nm', str(प्रोजेक्ट_करें_मूल / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', प्रतीक_मान):
        raise SystemExit('COSL 배포 रोकें: 커널에 이전 GPL पासवर्ड_मान/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for नाम in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + नाम + r'$', प्रतीक_मान, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + नाम)
    with tempfile.TemporaryDirectory(dir=str(प्रोजेक्ट_करें_मूल / 'build')) as 임시:
        छवि_मान = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(प्रोजेक्ट_करें_मूल / 'build/kernel.elf'), str(छवि_मान)])
        if हैश_फ़ाइल(छवि_मान) != हैश_फ़ाइल(प्रोजेक्ट_करें_मूल / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    रिपोर्ट_मान = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': हैश_फ़ाइल(प्रोजेक्ट_करें_मूल / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {नाम: हैश_फ़ाइल(प्रोजेक्ट_करें_मूल / 'build' / नाम) for नाम in लाइब्रेरी}}
    (प्रोजेक्ट_करें_मूल / 'build/cosl-distribution-check.json').write_text(json.dumps(रिपोर्ट_मान, ensure_ascii=False, indent=2) + '\n')
    return रिपोर्ट_मान


def बाइंड_करें_एंडपॉइंट():
    रिपोर्ट_मान = 점검()
    배포 = प्रोजेक्ट_करें_मूल / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(प्रोजेक्ट_करें_मूल / 'build')) as 임시:
        समूह_मान = Path(임시) / 'jkoros-native-relink'
        समूह_मान.mkdir()
        def आवृत्ति_मान(원본, पीअर_मान):
            गंतव्य_मान = समूह_मान / पीअर_मान
            गंतव्य_मान.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(गंतव्य_मान), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(गंतव्य_मान))
        for नाम in गंतव्य_नाम:
            आवृत्ति_मान(प्रोजेक्ट_करें_मूल / 'build' / (नाम + '.o'), 'objects/' + नाम + '.o')
        for नाम in लाइब्रेरी:
            आवृत्ति_मान(प्रोजेक्ट_करें_मूल / 'build' / नाम, 'objects/' + Path(नाम).name)
        for नाम in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     'सी_कंपाइलर', 'उपयोगकर्ता', '명명', 'यंत्र', 'नेटवर्क_स्टैक/नेटवर्क_स्टैक.h', '부팅/लिंक_लेआउट.ld',
                     'दूरस्थ_मान/assh_config.h', 'दूरस्थ_मान/config.h', 'दूरस्थ_मान/ctype.h', 'दूरस्थ_मान/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            आवृत्ति_मान(प्रोजेक्ट_करें_मूल / नाम, नाम)
        for नाम in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            आवृत्ति_मान(संग्रह_मूल / नाम, नाम)
        for पथ in sorted((प्रोजेक्ट_करें_मूल / 'vendor').glob('LICENSE*')):
            आवृत्ति_मान(पथ, 'vendor/' + पथ.name)
        आवृत्ति_मान(प्रोजेक्ट_करें_मूल / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        आवृत्ति_मान(प्रोजेक्ट_करें_मूल / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        आवृत्ति_मान(संग्रह_मूल / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        आवृत्ति_मान(प्रोजेक्ट_करें_मूल / 'उपकरण/재연결.py', 'relink.py')
        for पथ in sorted((प्रोजेक्ट_करें_मूल / 'build/user').glob('*.elf')):
            आवृत्ति_मान(पथ, 'build/user/' + पथ.name)
        for नाम in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            आवृत्ति_मान(प्रोजेक्ट_करें_मूल / 'build/user' / (नाम + '.o'), 'build/user/' + नाम + '.o')
        for नाम in ('crt', 'aot-runtime', 'निष्पादनसहायता', 'चलाएँ', '미리번역', 'वापस_करें_ब्रिज'):
            आवृत्ति_मान(प्रोजेक्ट_करें_मूल / 'build/ccompiler' / (नाम + '.o'), 'build/ccompiler/' + नाम + '.o')
        명세 = dict(रिपोर्ट_मान, objects=['objects/' + नाम + '.o' for नाम in गंतव्य_नाम],
                    libraries=['objects/' + Path(पथ).name for पथ in लाइब्रेरी])
        (समूह_मान / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (समूह_मान / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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

TinyCC source is included in vendor/tinycc; the native port is in सी_कंपाइलर.
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
        लक्ष्य = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / लक्ष्य.name
        with tarfile.open(str(임시압축), 'w:gz') as संग्रह_मान:
            संग्रह_मान.add(str(समूह_मान), arcname=समूह_मान.name)
        임시압축.replace(लक्ष्य)
    रिपोर्ट_मान['relink_archive_sha256'] = हैश_फ़ाइल(लक्ष्य)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(रिपोर्ट_मान, ensure_ascii=False, indent=2) + '\n')
    return लक्ष्य


if __name__ == '__main__':
    पार्सर_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    पार्सर_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    मान = पार्सर_48ee4b1b.parse_args()
    if मान.command == 'bundle':
        print('COSL source/relink kit:', बाइंड_करें_एंडपॉइंट())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
