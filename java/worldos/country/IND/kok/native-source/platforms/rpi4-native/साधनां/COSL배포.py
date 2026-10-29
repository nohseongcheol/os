#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL स्त्रोत_ट्री·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

प्रॉजॅक्ट_रूट = Path(__file__).resolve().parents[1]
저장소 = प्रॉजॅक्ट_रूट.parents[1]
नियुक्त_स्थान_नांव = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
लायब्ररी = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def हॅश_फायल(पाथ):
    return hashlib.sha256(Path(पाथ).read_bytes()).hexdigest()


def 점검():
    for नांव in ('vendor/wolfssh', 'vendor/wolfssl', 'दुर्मीळ_मोल/user_settings.h'):
        if (प्रॉजॅक्ट_रूट / नांव).exists():
            raise SystemExit('COSL 배포 थांबचें: 이전 GPL दुर्मीळ_मोल 구현이 स्त्रोत_ट्री 트리에 남아 있습니다: ' + नांव)
    वायर्ड_मोल = (प्रॉजॅक्ट_रूट / 'नॅटवर्क_स्टॅक/वायर्ड_नॅटवर्क.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in वायर्ड_मोल or 'SPDX-License-Identifier: GPL' in वायर्ड_मोल:
        raise SystemExit('COSL 배포 थांबचें: BSD GENET 구현·고지 पुनर्तपासणी_करची 필요')
    for नांव in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (저장소 / नांव).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + नांव)
    चिन्न_मोल = subprocess.check_output(['aarch64-linux-gnu-nm', str(प्रॉजॅक्ट_रूट / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', चिन्न_मोल):
        raise SystemExit('COSL 배포 थांबचें: 커널에 이전 GPL पासवर्ड_मोल/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for नांव in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + नांव + r'$', चिन्न_मोल, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + नांव)
    with tempfile.TemporaryDirectory(dir=str(प्रॉजॅक्ट_रूट / 'build')) as 임시:
        IMAGE_मोल = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(प्रॉजॅक्ट_रूट / 'build/kernel.elf'), str(IMAGE_मोल)])
        if हॅश_फायल(IMAGE_मोल) != हॅश_फायल(प्रॉजॅक्ट_रूट / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    अहवाल_मोल = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': हॅश_फायल(प्रॉजॅक्ट_रूट / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {नांव: हॅश_फायल(प्रॉजॅक्ट_रूट / 'build' / नांव) for नांव in लायब्ररी}}
    (प्रॉजॅक्ट_रूट / 'build/cosl-distribution-check.json').write_text(json.dumps(अहवाल_मोल, ensure_ascii=False, indent=2) + '\n')
    return अहवाल_मोल


def 묶기():
    अहवाल_मोल = 점검()
    배포 = प्रॉजॅक्ट_रूट / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(प्रॉजॅक्ट_रूट / 'build')) as 임시:
        गट_मोल = Path(임시) / 'jkoros-native-relink'
        गट_मोल.mkdir()
        def इन्सटन्स_मोल(원본, पीयर_मोल):
            नियुक्त_स्थान_मोल = गट_मोल / पीयर_मोल
            नियुक्त_स्थान_मोल.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(नियुक्त_स्थान_मोल), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(नियुक्त_स्थान_मोल))
        for नांव in नियुक्त_स्थान_नांव:
            इन्सटन्स_मोल(प्रॉजॅक्ट_रूट / 'build' / (नांव + '.o'), 'objects/' + नांव + '.o')
        for नांव in लायब्ररी:
            इन्सटन्स_मोल(प्रॉजॅक्ट_रूट / 'build' / नांव, 'objects/' + Path(नांव).name)
        for नांव in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'उपेगकर्तो', '명명', 'यंत्र', 'नॅटवर्क_स्टॅक/नॅटवर्क_स्टॅक.h', '부팅/लिंक_रचणाय.ld',
                     'दुर्मीळ_मोल/assh_config.h', 'दुर्मीळ_मोल/config.h', 'दुर्मीळ_मोल/ctype.h', 'दुर्मीळ_मोल/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            इन्सटन्स_मोल(प्रॉजॅक्ट_रूट / नांव, नांव)
        for नांव in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            इन्सटन्स_मोल(저장소 / नांव, नांव)
        for पाथ in sorted((प्रॉजॅक्ट_रूट / 'vendor').glob('LICENSE*')):
            इन्सटन्स_मोल(पाथ, 'vendor/' + पाथ.name)
        इन्सटन्स_मोल(प्रॉजॅक्ट_रूट / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        इन्सटन्स_मोल(प्रॉजॅक्ट_रूट / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        इन्सटन्स_मोल(저장소 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        इन्सटन्स_मोल(प्रॉजॅक्ट_रूट / 'साधनां/재연결.py', 'relink.py')
        for पाथ in sorted((प्रॉजॅक्ट_रूट / 'build/user').glob('*.elf')):
            इन्सटन्स_मोल(पाथ, 'build/user/' + पाथ.name)
        for नांव in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            इन्सटन्स_मोल(प्रॉजॅक्ट_रूट / 'build/user' / (नांव + '.o'), 'build/user/' + नांव + '.o')
        for नांव in ('crt', 'aot-runtime', 'सामान्य_भास_रनटायम_तेंको', 'चलोवप', '미리번역', 'return_ब्रिज'):
            इन्सटन्स_मोल(प्रॉजॅक्ट_रूट / 'build/ccompiler' / (नांव + '.o'), 'build/ccompiler/' + नांव + '.o')
        명세 = dict(अहवाल_मोल, objects=['objects/' + नांव + '.o' for नांव in नियुक्त_स्थान_नांव],
                    libraries=['objects/' + Path(पाथ).name for पाथ in लायब्ररी])
        (गट_मोल / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (गट_मोल / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        लक्ष्य = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / लक्ष्य.name
        with tarfile.open(str(임시압축), 'w:gz') as संग्रह_मोल:
            संग्रह_मोल.add(str(गट_मोल), arcname=गट_मोल.name)
        임시압축.replace(लक्ष्य)
    अहवाल_मोल['relink_archive_sha256'] = हॅश_फायल(लक्ष्य)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(अहवाल_मोल, ensure_ascii=False, indent=2) + '\n')
    return लक्ष्य


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    मोल = 해석기.parse_args()
    if मोल.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
