#!/usr/bin/env python3
"""현재 بومی ARM64 산출물을 검사하고 LGPL منبع_درخت·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

نمایش_دادن_جذر = Path(__file__).resolve().parents[1]
مخزن_جذر = نمایش_دادن_جذر.parents[1]
مقصد_نام = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
کتابخانه = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def هاشور_فایل(مسیر):
    return hashlib.sha256(Path(مسیر).read_bytes()).hexdigest()


def 점검():
    for نام in ('vendor/wolfssh', 'vendor/wolfssl', 'راه_دور_مقدار/user_settings.h'):
        if (نمایش_دادن_جذر / نام).exists():
            raise SystemExit('COSL 배포 توقف: 이전 GPL راه_دور_مقدار 구현이 منبع_درخت 트리에 남아 있습니다: ' + نام)
    سیم_دار_مقدار = (نمایش_دادن_جذر / 'شبکه_پشته/سیم_دار_شبکه.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in سیم_دار_مقدار or 'SPDX-License-Identifier: GPL' in سیم_دار_مقدار:
        raise SystemExit('COSL 배포 توقف: BSD GENET 구현·고지 تأیید_صحت 필요')
    for نام in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (مخزن_جذر / نام).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + نام)
    نماد_مقدار = subprocess.check_output(['aarch64-linux-gnu-nm', str(نمایش_دادن_جذر / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', نماد_مقدار):
        raise SystemExit('COSL 배포 توقف: 커널에 이전 GPL رمز_عبور_مقدار/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for نام in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + نام + r'$', نماد_مقدار, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + نام)
    with tempfile.TemporaryDirectory(dir=str(نمایش_دادن_جذر / 'build')) as 임시:
        عکس_مقدار = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(نمایش_دادن_جذر / 'build/kernel.elf'), str(عکس_مقدار)])
        if هاشور_فایل(عکس_مقدار) != هاشور_فایل(نمایش_دادن_جذر / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    گزارش_مقدار = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': هاشور_فایل(نمایش_دادن_جذر / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {نام: هاشور_فایل(نمایش_دادن_جذر / 'build' / نام) for نام in کتابخانه}}
    (نمایش_دادن_جذر / 'build/cosl-distribution-check.json').write_text(json.dumps(گزارش_مقدار, ensure_ascii=False, indent=2) + '\n')
    return گزارش_مقدار


def 묶기():
    گزارش_مقدار = 점검()
    배포 = نمایش_دادن_جذر / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(نمایش_دادن_جذر / 'build')) as 임시:
        گروه_مقدار = Path(임시) / 'jkoros-native-relink'
        گروه_مقدار.mkdir()
        def کپی_مقدار(원본, مشابه_مقدار):
            مقصد_مقدار = گروه_مقدار / مشابه_مقدار
            مقصد_مقدار.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(مقصد_مقدار), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(مقصد_مقدار))
        for نام in مقصد_نام:
            کپی_مقدار(نمایش_دادن_جذر / 'build' / (نام + '.o'), 'objects/' + نام + '.o')
        for نام in کتابخانه:
            کپی_مقدار(نمایش_دادن_جذر / 'build' / نام, 'objects/' + Path(نام).name)
        for نام in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'کاربر', '명명', 'دستگاه', 'شبکه_پشته/شبکه_پشته.h', '부팅/پیوند_پیمایش.ld',
                     'راه_دور_مقدار/assh_config.h', 'راه_دور_مقدار/config.h', 'راه_دور_مقدار/ctype.h', 'راه_دور_مقدار/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            کپی_مقدار(نمایش_دادن_جذر / نام, نام)
        for نام in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            کپی_مقدار(مخزن_جذر / نام, نام)
        for مسیر in sorted((نمایش_دادن_جذر / 'vendor').glob('LICENSE*')):
            کپی_مقدار(مسیر, 'vendor/' + مسیر.name)
        کپی_مقدار(نمایش_دادن_جذر / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        کپی_مقدار(نمایش_دادن_جذر / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        کپی_مقدار(مخزن_جذر / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        کپی_مقدار(نمایش_دادن_جذر / 'ابزارها/재연결.py', 'relink.py')
        for مسیر in sorted((نمایش_دادن_جذر / 'build/user').glob('*.elf')):
            کپی_مقدار(مسیر, 'build/user/' + مسیر.name)
        for نام in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            کپی_مقدار(نمایش_دادن_جذر / 'build/user' / (نام + '.o'), 'build/user/' + نام + '.o')
        for نام in ('crt', 'aot-runtime', 'زمان_اجرای_زبان_مشترک_پشتیبان', 'اجرا_2', '미리번역', 'بازگرداندن_پل'):
            کپی_مقدار(نمایش_دادن_جذر / 'build/ccompiler' / (نام + '.o'), 'build/ccompiler/' + نام + '.o')
        명세 = dict(گزارش_مقدار, objects=['objects/' + نام + '.o' for نام in مقصد_نام],
                    libraries=['objects/' + Path(مسیر).name for مسیر in کتابخانه])
        (گروه_مقدار / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (گروه_مقدار / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        with tarfile.open(str(임시압축), 'w:gz') as آرشیو_مقدار:
            آرشیو_مقدار.add(str(گروه_مقدار), arcname=گروه_مقدار.name)
        임시압축.replace(هدف)
    گزارش_مقدار['relink_archive_sha256'] = هاشور_فایل(هدف)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(گزارش_مقدار, ensure_ascii=False, indent=2) + '\n')
    return هدف


if __name__ == '__main__':
    مفسر_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    مفسر_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    مقدار = مفسر_48ee4b1b.parse_args()
    if مقدار.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
