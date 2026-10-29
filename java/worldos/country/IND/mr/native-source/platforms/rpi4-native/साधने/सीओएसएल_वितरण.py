#!/usr/bin/env python3
"""सध्याचे_आयटम स्वकीय ARM64 산출물을 검사하고 LGPL स्रोत_ट्री·पुन्हाजोडा_संचारटोक 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

प्रोजेक्ट_मूळ = Path(__file__).resolve().parents[1]
भांडार_मूळ = प्रोजेक्ट_मूळ.parents[1]
गंतव्यस्थान_नाव = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
लायब्ररी = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def हॅश_संचिका(मार्ग):
    return hashlib.sha256(Path(मार्ग).read_bytes()).hexdigest()


def तपासा_राज्य():
    for नाव in ('vendor/wolfssh', 'vendor/wolfssl', 'दूरस्_थ_मूल्य/user_settings.h'):
        if (प्रोजेक्ट_मूळ / नाव).exists():
            raise SystemExit('COSL वितरण_मूल्य थांबा: मागील_आयटम GPL दूरस्_थ_मूल्य 구현이 स्रोत_ट्री 트리에 남아 있습니다: ' + नाव)
    वायर्ड_मूल्य = (प्रोजेक्ट_मूळ / 'संचारजाळे_स्टॅक/वायर्ड_संचारजाळे.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in वायर्ड_मूल्य or 'SPDX-License-Identifier: GPL' in वायर्ड_मूल्य:
        raise SystemExit('COSL वितरण_मूल्य थांबा: BSD GENET अंमलबजावणी·고지 पडताळा आवश्यक_मूल्य')
    for नाव in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (भांडार_मूळ / नाव).is_file():
            raise SystemExit('COSL वितरण_मूल्य 고지 अनुपस्थित_पद्धत: ' + नाव)
    चिन्ह_मूल्य = subprocess.check_output(['aarch64-linux-gnu-nm', str(प्रोजेक्ट_मूळ / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', चिन्ह_मूल्य):
        raise SystemExit('COSL वितरण_मूल्य थांबा: 커널에 मागील_आयटम GPL पासवर्ड_मूल्य/SSH 심볼이 남아 있습니다. पुनःप्रयत्न_मूल्य 빌드하세요.')
    for नाव in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + नाव + r'$', चिन्ह_मूल्य, re.M):
            raise SystemExit('COSL 대체 अंमलबजावणी 누락: ' + नाव)
    with tempfile.TemporaryDirectory(dir=str(प्रोजेक्ट_मूळ / 'build')) as तात्पुरते_मूल्य:
        चित्र_मूल्य = Path(तात्पुरते_मूल्य) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(प्रोजेक्ट_मूळ / 'build/kernel.elf'), str(चित्र_मूल्य)])
        if हॅश_संचिका(चित्र_मूल्य) != हॅश_संचिका(प्रोजेक्ट_मूळ / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    अहवाल_मूल्य = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': हॅश_संचिका(प्रोजेक्ट_मूळ / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {नाव: हॅश_संचिका(प्रोजेक्ट_मूळ / 'build' / नाव) for नाव in लायब्ररी}}
    (प्रोजेक्ट_मूळ / 'build/cosl-distribution-check.json').write_text(json.dumps(अहवाल_मूल्य, ensure_ascii=False, indent=2) + '\n')
    return अहवाल_मूल्य


def बाइंड_करा_संचारटोक():
    अहवाल_मूल्य = तपासा_राज्य()
    वितरण_मूल्य = प्रोजेक्ट_मूळ / 'dist'
    वितरण_मूल्य.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(प्रोजेक्ट_मूळ / 'build')) as तात्पुरते_मूल्य:
        समूह_मूल्य = Path(तात्पुरते_मूल्य) / 'jkoros-native-relink'
        समूह_मूल्य.mkdir()
        def इन्स्टन्स_मूल्य(मूळ, समकक्ष_मूल्य):
            गंतव्यस्थान_मूल्य = समूह_मूल्य / समकक्ष_मूल्य
            गंतव्यस्थान_मूल्य.parent.mkdir(parents=True, exist_ok=True)
            if मूळ.is_dir():
                shutil.copytree(str(मूळ), str(गंतव्यस्थान_मूल्य), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(मूळ), str(गंतव्यस्थान_मूल्य))
        for नाव in गंतव्यस्थान_नाव:
            इन्स्टन्स_मूल्य(प्रोजेक्ट_मूळ / 'build' / (नाव + '.o'), 'objects/' + नाव + '.o')
        for नाव in लायब्ररी:
            इन्स्टन्स_मूल्य(प्रोजेक्ट_मूळ / 'build' / नाव, 'objects/' + Path(नाव).name)
        for नाव in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     'सी_संकलक', 'प्रयोक्ता', 'नामकरण', 'मशीन', 'संचारजाळे_स्टॅक/संचारजाळे_स्टॅक.h', 'प्रणालीप्रारंभ/लिंक_लेआउट.ld',
                     'दूरस्_थ_मूल्य/assh_config.h', 'दूरस्_थ_मूल्य/config.h', 'दूरस्_थ_मूल्य/ctype.h', 'दूरस्_थ_मूल्य/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'सीओएसएल_वितरण_मार्गदर्शी.md'):
            इन्स्टन्स_मूल्य(प्रोजेक्ट_मूळ / नाव, नाव)
        for नाव in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            इन्स्टन्स_मूल्य(भांडार_मूळ / नाव, नाव)
        for मार्ग in sorted((प्रोजेक्ट_मूळ / 'vendor').glob('LICENSE*')):
            इन्स्टन्स_मूल्य(मार्ग, 'vendor/' + मार्ग.name)
        इन्स्टन्स_मूल्य(प्रोजेक्ट_मूळ / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        इन्स्टन्स_मूल्य(प्रोजेक्ट_मूळ / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        इन्स्टन्स_मूल्य(भांडार_मूळ / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        इन्स्टन्स_मूल्य(प्रोजेक्ट_मूळ / 'साधने/पुन्हाजोडा_संचारटोक.py', 'relink.py')
        for मार्ग in sorted((प्रोजेक्ट_मूळ / 'build/user').glob('*.elf')):
            इन्स्टन्स_मूल्य(मार्ग, 'build/user/' + मार्ग.name)
        for नाव in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            इन्स्टन्स_मूल्य(प्रोजेक्ट_मूळ / 'build/user' / (नाव + '.o'), 'build/user/' + नाव + '.o')
        for नाव in ('crt', 'aot-runtime', 'सामान्य_भाषा_रनटाइम_समर्थन', 'सुरू_करा', 'आगाऊ_संबंधित_वेळ', 'परतकरा_ब्रिज'):
            इन्स्टन्स_मूल्य(प्रोजेक्ट_मूळ / 'build/ccompiler' / (नाव + '.o'), 'build/ccompiler/' + नाव + '.o')
        विनिर्देश = dict(अहवाल_मूल्य, objects=['objects/' + नाव + '.o' for नाव in गंतव्यस्थान_नाव],
                    libraries=['objects/' + Path(मार्ग).name for मार्ग in लायब्ररी])
        (समूह_मूल्य / 'relink.json').write_text(json.dumps(विनिर्देश, ensure_ascii=False, indent=2) + '\n')
        (समूह_मूल्य / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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

TinyCC source is included in vendor/tinycc; the native port is in सी_संकलक.
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
        लक्ष्य = वितरण_मूल्य / 'jkoros-native-relink.tar.gz'
        तात्पुरते_संग्रह = Path(तात्पुरते_मूल्य) / लक्ष्य.name
        with tarfile.open(str(तात्पुरते_संग्रह), 'w:gz') as संग्रह_मूल्य:
            संग्रह_मूल्य.add(str(समूह_मूल्य), arcname=समूह_मूल्य.name)
        तात्पुरते_संग्रह.replace(लक्ष्य)
    अहवाल_मूल्य['relink_archive_sha256'] = हॅश_संचिका(लक्ष्य)
    (वितरण_मूल्य / 'cosl-distribution.json').write_text(json.dumps(अहवाल_मूल्य, ensure_ascii=False, indent=2) + '\n')
    return लक्ष्य


if __name__ == '__main__':
    व्याकरणविश्लेषक_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    व्याकरणविश्लेषक_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    मूल्य = व्याकरणविश्लेषक_48ee4b1b.parse_args()
    if मूल्य.command == 'bundle':
        print('COSL source/relink kit:', बाइंड_करा_संचारटोक())
    else:
        print(json.dumps(तपासा_राज्य(), ensure_ascii=False, indent=2))
