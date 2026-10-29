#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL ماخذ_شجرو·재연결 자료를 함께 묶는다."""
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
منزل_مقصود_نالو = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
لائبريري = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def هيش_فائل(راههه):
    return hashlib.sha256(Path(راههه).read_bytes()).hexdigest()


def 점검():
    for نالو in ('vendor/wolfssh', 'vendor/wolfssl', 'بعيد_قدر/user_settings.h'):
        if (기준 / نالو).exists():
            raise SystemExit('COSL 배포 روڪيو: 이전 GPL بعيد_قدر 구현이 ماخذ_شجرو 트리에 남아 있습니다: ' + نالو)
    유선 = (기준 / 'نيٽ_ورڪ_اڀرڻ/유선망.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in 유선 or 'SPDX-License-Identifier: GPL' in 유선:
        raise SystemExit('COSL 배포 روڪيو: BSD GENET 구현·고지 تصديق_ڪريو 필요')
    for نالو in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (저장소 / نالو).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + نالو)
    نشاني_قدر = subprocess.check_output(['aarch64-linux-gnu-nm', str(기준 / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', نشاني_قدر):
        raise SystemExit('COSL 배포 روڪيو: 커널에 이전 GPL پاس_ورڊ_قدر/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for نالو in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + نالو + r'$', نشاني_قدر, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + نالو)
    with tempfile.TemporaryDirectory(dir=str(기준 / 'build')) as 임시:
        نقش_قدر = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(기준 / 'build/kernel.elf'), str(نقش_قدر)])
        if هيش_فائل(نقش_قدر) != هيش_فائل(기준 / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    رپورٽ_قدر = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': هيش_فائل(기준 / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {نالو: هيش_فائل(기준 / 'build' / نالو) for نالو in لائبريري}}
    (기준 / 'build/cosl-distribution-check.json').write_text(json.dumps(رپورٽ_قدر, ensure_ascii=False, indent=2) + '\n')
    return رپورٽ_قدر


def 묶기():
    رپورٽ_قدر = 점검()
    배포 = 기준 / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(기준 / 'build')) as 임시:
        گروپ_قدر = Path(임시) / 'jkoros-native-relink'
        گروپ_قدر.mkdir()
        def نقل_قدر(원본, همعصر_قدر):
            منزل_مقصود_قدر = گروپ_قدر / همعصر_قدر
            منزل_مقصود_قدر.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(منزل_مقصود_قدر), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(منزل_مقصود_قدر))
        for نالو in منزل_مقصود_نالو:
            نقل_قدر(기준 / 'build' / (نالو + '.o'), 'objects/' + نالو + '.o')
        for نالو in لائبريري:
            نقل_قدر(기준 / 'build' / نالو, 'objects/' + Path(نالو).name)
        for نالو in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'صارف', '명명', 'مشين', 'نيٽ_ورڪ_اڀرڻ/نيٽ_ورڪ_اڀرڻ.h', '부팅/ڪڙي_لي_آئوٽ.ld',
                     'بعيد_قدر/assh_config.h', 'بعيد_قدر/config.h', 'بعيد_قدر/ctype.h', 'بعيد_قدر/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            نقل_قدر(기준 / نالو, نالو)
        for نالو in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            نقل_قدر(저장소 / نالو, نالو)
        for راههه in sorted((기준 / 'vendor').glob('LICENSE*')):
            نقل_قدر(راههه, 'vendor/' + راههه.name)
        نقل_قدر(기준 / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        نقل_قدر(기준 / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        نقل_قدر(저장소 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        نقل_قدر(기준 / 'اوزار/재연결.py', 'relink.py')
        for راههه in sorted((기준 / 'build/user').glob('*.elf')):
            نقل_قدر(راههه, 'build/user/' + راههه.name)
        for نالو in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            نقل_قدر(기준 / 'build/user' / (نالو + '.o'), 'build/user/' + نالو + '.o')
        for نالو in ('crt', 'aot-runtime', 'عام_ٻولي_جو_رن_ٽائيم_معاونت', 'هلائڻ', '미리번역', '되돌림'):
            نقل_قدر(기준 / 'build/ccompiler' / (نالو + '.o'), 'build/ccompiler/' + نالو + '.o')
        명세 = dict(رپورٽ_قدر, objects=['objects/' + نالو + '.o' for نالو in منزل_مقصود_نالو],
                    libraries=['objects/' + Path(راههه).name for راههه in لائبريري])
        (گروپ_قدر / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (گروپ_قدر / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        هدف = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / هدف.name
        with tarfile.open(str(임시압축), 'w:gz') as محفوظ_قدر:
            محفوظ_قدر.add(str(گروپ_قدر), arcname=گروپ_قدر.name)
        임시압축.replace(هدف)
    رپورٽ_قدر['relink_archive_sha256'] = هيش_فائل(هدف)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(رپورٽ_قدر, ensure_ascii=False, indent=2) + '\n')
    return هدف


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    قدر = 해석기.parse_args()
    if قدر.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
