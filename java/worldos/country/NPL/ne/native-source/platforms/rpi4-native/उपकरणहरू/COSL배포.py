#!/usr/bin/env python3
"""현재 निज ARM64 산출물을 검사하고 LGPL स्रोत_वृक्ष·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

परियोजना_रूट = Path(__file__).resolve().parents[1]
저장소 = परियोजना_रूट.parents[1]
गन्तव्य_नाम = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
पुस्तकालय = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def ह्यास_फाइल(मार्ग):
    return hashlib.sha256(Path(मार्ग).read_bytes()).hexdigest()


def 점검():
    for नाम in ('vendor/wolfssh', 'vendor/wolfssl', 'दूर_मान/user_settings.h'):
        if (परियोजना_रूट / नाम).exists():
            raise SystemExit('COSL 배포 रोक्नुहोस्: 이전 GPL दूर_मान 구현이 स्रोत_वृक्ष 트리에 남아 있습니다: ' + नाम)
    तार_सहितको_मान = (परियोजना_रूट / 'सञ्जाल_चाङ/तार_सहितको_सञ्जाल.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in तार_सहितको_मान or 'SPDX-License-Identifier: GPL' in तार_सहितको_मान:
        raise SystemExit('COSL 배포 रोक्नुहोस्: BSD GENET 구현·고지 रुजू_गर्नुहोस् 필요')
    for नाम in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (저장소 / नाम).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + नाम)
    चिन्ह_मान = subprocess.check_output(['aarch64-linux-gnu-nm', str(परियोजना_रूट / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', चिन्ह_मान):
        raise SystemExit('COSL 배포 रोक्नुहोस्: 커널에 이전 GPL पासवर्ड_मान/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for नाम in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + नाम + r'$', चिन्ह_मान, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + नाम)
    with tempfile.TemporaryDirectory(dir=str(परियोजना_रूट / 'build')) as 임시:
        छवि_मान = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(परियोजना_रूट / 'build/kernel.elf'), str(छवि_मान)])
        if ह्यास_फाइल(छवि_मान) != ह्यास_फाइल(परियोजना_रूट / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    रिपोर्ट_मान = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': ह्यास_फाइल(परियोजना_रूट / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {नाम: ह्यास_फाइल(परियोजना_रूट / 'build' / नाम) for नाम in पुस्तकालय}}
    (परियोजना_रूट / 'build/cosl-distribution-check.json').write_text(json.dumps(रिपोर्ट_मान, ensure_ascii=False, indent=2) + '\n')
    return रिपोर्ट_मान


def 묶기():
    रिपोर्ट_मान = 점검()
    배포 = परियोजना_रूट / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(परियोजना_रूट / 'build')) as 임시:
        समूह_मान = Path(임시) / 'jkoros-native-relink'
        समूह_मान.mkdir()
        def उद्धरण_मान_37b3d3b1(원본, समान_मान):
            गन्तव्य_मान = समूह_मान / समान_मान
            गन्तव्य_मान.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(गन्तव्य_मान), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(गन्तव्य_मान))
        for नाम in गन्तव्य_नाम:
            उद्धरण_मान_37b3d3b1(परियोजना_रूट / 'build' / (नाम + '.o'), 'objects/' + नाम + '.o')
        for नाम in पुस्तकालय:
            उद्धरण_मान_37b3d3b1(परियोजना_रूट / 'build' / नाम, 'objects/' + Path(नाम).name)
        for नाम in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'प्रयोगकर्ता', '명명', 'मेशिन', 'सञ्जाल_चाङ/सञ्जाल_चाङ.h', '부팅/लिङ्क_लेआउट.ld',
                     'दूर_मान/assh_config.h', 'दूर_मान/config.h', 'दूर_मान/ctype.h', 'दूर_मान/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            उद्धरण_मान_37b3d3b1(परियोजना_रूट / नाम, नाम)
        for नाम in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            उद्धरण_मान_37b3d3b1(저장소 / नाम, नाम)
        for मार्ग in sorted((परियोजना_रूट / 'vendor').glob('LICENSE*')):
            उद्धरण_मान_37b3d3b1(मार्ग, 'vendor/' + मार्ग.name)
        उद्धरण_मान_37b3d3b1(परियोजना_रूट / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        उद्धरण_मान_37b3d3b1(परियोजना_रूट / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        उद्धरण_मान_37b3d3b1(저장소 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        उद्धरण_मान_37b3d3b1(परियोजना_रूट / 'उपकरणहरू/재연결.py', 'relink.py')
        for मार्ग in sorted((परियोजना_रूट / 'build/user').glob('*.elf')):
            उद्धरण_मान_37b3d3b1(मार्ग, 'build/user/' + मार्ग.name)
        for नाम in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            उद्धरण_मान_37b3d3b1(परियोजना_रूट / 'build/user' / (नाम + '.o'), 'build/user/' + नाम + '.o')
        for नाम in ('crt', 'aot-runtime', 'सामान्य_भाषा_चालु_समय_समर्थन', 'चलाउनुहोस्', '미리번역', '되돌림'):
            उद्धरण_मान_37b3d3b1(परियोजना_रूट / 'build/ccompiler' / (नाम + '.o'), 'build/ccompiler/' + नाम + '.o')
        명세 = dict(रिपोर्ट_मान, objects=['objects/' + नाम + '.o' for नाम in गन्तव्य_नाम],
                    libraries=['objects/' + Path(मार्ग).name for मार्ग in पुस्तकालय])
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
        with tarfile.open(str(임시압축), 'w:gz') as सङ्ग्रह_मान:
            सङ्ग्रह_मान.add(str(समूह_मान), arcname=समूह_मान.name)
        임시압축.replace(लक्ष्य)
    रिपोर्ट_मान['relink_archive_sha256'] = ह्यास_फाइल(लक्ष्य)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(रिपोर्ट_मान, ensure_ascii=False, indent=2) + '\n')
    return लक्ष्य


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    मान = 해석기.parse_args()
    if मान.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
