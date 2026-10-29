#!/usr/bin/env python3
"""현재 اپنا ARM64 산출물을 검사하고 LGPL ماخذ_شجر·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

عکس_ڈالنا_روٹ = Path(__file__).resolve().parents[1]
저장소 = عکس_ڈالنا_روٹ.parents[1]
منزل_مقصود_نام = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
لائبریری = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def ہيش_فائل(راستہ_2):
    return hashlib.sha256(Path(راستہ_2).read_bytes()).hexdigest()


def 점검():
    for نام in ('vendor/wolfssh', 'vendor/wolfssl', 'بعید_قدر/user_settings.h'):
        if (عکس_ڈالنا_روٹ / نام).exists():
            raise SystemExit('COSL 배포 روکیں: 이전 GPL بعید_قدر 구현이 ماخذ_شجر 트리에 남아 있습니다: ' + نام)
    بذریعہ_تار_قدر = (عکس_ڈالنا_روٹ / 'نیٹ_ورک_اسٹیک/بذریعہ_تار_نیٹ_ورک.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in بذریعہ_تار_قدر or 'SPDX-License-Identifier: GPL' in بذریعہ_تار_قدر:
        raise SystemExit('COSL 배포 روکیں: BSD GENET 구현·고지 تصدیق_کریں 필요')
    for نام in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (저장소 / نام).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + نام)
    علامت_قدر = subprocess.check_output(['aarch64-linux-gnu-nm', str(عکس_ڈالنا_روٹ / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', علامت_قدر):
        raise SystemExit('COSL 배포 روکیں: 커널에 이전 GPL پاس_ورڈ_قدر/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for نام in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + نام + r'$', علامت_قدر, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + نام)
    with tempfile.TemporaryDirectory(dir=str(عکس_ڈالنا_روٹ / 'build')) as 임시:
        نقش_قدر = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(عکس_ڈالنا_روٹ / 'build/kernel.elf'), str(نقش_قدر)])
        if ہيش_فائل(نقش_قدر) != ہيش_فائل(عکس_ڈالنا_روٹ / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    رپورٹ_قدر = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': ہيش_فائل(عکس_ڈالنا_روٹ / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {نام: ہيش_فائل(عکس_ڈالنا_روٹ / 'build' / نام) for نام in لائبریری}}
    (عکس_ڈالنا_روٹ / 'build/cosl-distribution-check.json').write_text(json.dumps(رپورٹ_قدر, ensure_ascii=False, indent=2) + '\n')
    return رپورٹ_قدر


def 묶기():
    رپورٹ_قدر = 점검()
    배포 = عکس_ڈالنا_روٹ / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(عکس_ڈالنا_روٹ / 'build')) as 임시:
        گروپ_قدر = Path(임시) / 'jkoros-native-relink'
        گروپ_قدر.mkdir()
        def نقل_قدر(원본, ساتھی_قدر):
            منزل_مقصود_قدر = گروپ_قدر / ساتھی_قدر
            منزل_مقصود_قدر.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(منزل_مقصود_قدر), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(منزل_مقصود_قدر))
        for نام in منزل_مقصود_نام:
            نقل_قدر(عکس_ڈالنا_روٹ / 'build' / (نام + '.o'), 'objects/' + نام + '.o')
        for نام in لائبریری:
            نقل_قدر(عکس_ڈالنا_روٹ / 'build' / نام, 'objects/' + Path(نام).name)
        for نام in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'صارف', '명명', 'مشین', 'نیٹ_ورک_اسٹیک/نیٹ_ورک_اسٹیک.h', '부팅/ربط_ترتیب.ld',
                     'بعید_قدر/assh_config.h', 'بعید_قدر/config.h', 'بعید_قدر/ctype.h', 'بعید_قدر/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            نقل_قدر(عکس_ڈالنا_روٹ / نام, نام)
        for نام in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            نقل_قدر(저장소 / نام, نام)
        for راستہ_2 in sorted((عکس_ڈالنا_روٹ / 'vendor').glob('LICENSE*')):
            نقل_قدر(راستہ_2, 'vendor/' + راستہ_2.name)
        نقل_قدر(عکس_ڈالنا_روٹ / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        نقل_قدر(عکس_ڈالنا_روٹ / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        نقل_قدر(저장소 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        نقل_قدر(عکس_ڈالنا_روٹ / 'ٹولز/재연결.py', 'relink.py')
        for راستہ_2 in sorted((عکس_ڈالنا_روٹ / 'build/user').glob('*.elf')):
            نقل_قدر(راستہ_2, 'build/user/' + راستہ_2.name)
        for نام in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            نقل_قدر(عکس_ڈالنا_روٹ / 'build/user' / (نام + '.o'), 'build/user/' + نام + '.o')
        for نام in ('crt', 'aot-runtime', 'عام_زبان_چلت_عرصہ_معاونت', 'چلائیں', '미리번역', '되돌림'):
            نقل_قدر(عکس_ڈالنا_روٹ / 'build/ccompiler' / (نام + '.o'), 'build/ccompiler/' + نام + '.o')
        명세 = dict(رپورٹ_قدر, objects=['objects/' + نام + '.o' for نام in منزل_مقصود_نام],
                    libraries=['objects/' + Path(راستہ_2).name for راستہ_2 in لائبریری])
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
        ہدف = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / ہدف.name
        with tarfile.open(str(임시압축), 'w:gz') as محفوظ_قدر:
            محفوظ_قدر.add(str(گروپ_قدر), arcname=گروپ_قدر.name)
        임시압축.replace(ہدف)
    رپورٹ_قدر['relink_archive_sha256'] = ہيش_فائل(ہدف)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(رپورٹ_قدر, ensure_ascii=False, indent=2) + '\n')
    return ہدف


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    قدر = 해석기.parse_args()
    if قدر.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
