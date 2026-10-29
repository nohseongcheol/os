#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL ژێدەر_دار·재연결 자료를 함께 묶는다."""
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
جێمەبەست_ناو = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
کتێبخانە = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def دەرەنجام_فایل(گوزەر):
    return hashlib.sha256(Path(گوزەر).read_bytes()).hexdigest()


def 점검():
    for ناو in ('vendor/wolfssh', 'vendor/wolfssl', 'دوورەدەس_نرخ/user_settings.h'):
        if (기준 / ناو).exists():
            raise SystemExit('COSL 배포 وەستان: 이전 GPL دوورەدەس_نرخ 구현이 ژێدەر_دار 트리에 남아 있습니다: ' + ناو)
    유선 = (기준 / 'تۆڕ_ستاك/유선망.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in 유선 or 'SPDX-License-Identifier: GPL' in 유선:
        raise SystemExit('COSL 배포 وەستان: BSD GENET 구현·고지 سەلماندن 필요')
    for ناو in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (저장소 / ناو).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + ناو)
    سیمبۆل_نرخ = subprocess.check_output(['aarch64-linux-gnu-nm', str(기준 / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', سیمبۆل_نرخ):
        raise SystemExit('COSL 배포 وەستان: 커널에 이전 GPL نهێنوشە_نرخ/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for ناو in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + ناو + r'$', سیمبۆل_نرخ, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + ناو)
    with tempfile.TemporaryDirectory(dir=str(기준 / 'build')) as 임시:
        وێنە_نرخ = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(기준 / 'build/kernel.elf'), str(وێنە_نرخ)])
        if دەرەنجام_فایل(وێنە_نرخ) != دەرەنجام_فایل(기준 / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    ڕاپۆرت_نرخ = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': دەرەنجام_فایل(기준 / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {ناو: دەرەنجام_فایل(기준 / 'build' / ناو) for ناو in کتێبخانە}}
    (기준 / 'build/cosl-distribution-check.json').write_text(json.dumps(ڕاپۆرت_نرخ, ensure_ascii=False, indent=2) + '\n')
    return ڕاپۆرت_نرخ


def 묶기():
    ڕاپۆرت_نرخ = 점검()
    배포 = 기준 / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(기준 / 'build')) as 임시:
        گروپ_نرخ = Path(임시) / 'jkoros-native-relink'
        گروپ_نرخ.mkdir()
        def کۆپی_نرخ(원본, هاوتا_نرخ):
            جێمەبەست_نرخ = گروپ_نرخ / هاوتا_نرخ
            جێمەبەست_نرخ.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(جێمەبەست_نرخ), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(جێمەبەست_نرخ))
        for ناو in جێمەبەست_ناو:
            کۆپی_نرخ(기준 / 'build' / (ناو + '.o'), 'objects/' + ناو + '.o')
        for ناو in کتێبخانە:
            کۆپی_نرخ(기준 / 'build' / ناو, 'objects/' + Path(ناو).name)
        for ناو in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'بەکارهێنەر', '명명', 'مەکینه', 'تۆڕ_ستاك/تۆڕ_ستاك.h', '부팅/لینك_ڕیزبەست.ld',
                     'دوورەدەس_نرخ/assh_config.h', 'دوورەدەس_نرخ/config.h', 'دوورەدەس_نرخ/ctype.h', 'دوورەدەس_نرخ/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            کۆپی_نرخ(기준 / ناو, ناو)
        for ناو in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            کۆپی_نرخ(저장소 / ناو, ناو)
        for گوزەر in sorted((기준 / 'vendor').glob('LICENSE*')):
            کۆپی_نرخ(گوزەر, 'vendor/' + گوزەر.name)
        کۆپی_نرخ(기준 / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        کۆپی_نرخ(기준 / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        کۆپی_نرخ(저장소 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        کۆپی_نرخ(기준 / 'ئامرازەکان/재연결.py', 'relink.py')
        for گوزەر in sorted((기준 / 'build/user').glob('*.elf')):
            کۆپی_نرخ(گوزەر, 'build/user/' + گوزەر.name)
        for ناو in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            کۆپی_نرخ(기준 / 'build/user' / (ناو + '.o'), 'build/user/' + ناو + '.o')
        for ناو in ('crt', 'aot-runtime', 'ڕەنتایمی_زمانی_هاوبەش_پشتیوانی', 'ڕادان', '미리번역', '되돌림'):
            کۆپی_نرخ(기준 / 'build/ccompiler' / (ناو + '.o'), 'build/ccompiler/' + ناو + '.o')
        명세 = dict(ڕاپۆرت_نرخ, objects=['objects/' + ناو + '.o' for ناو in جێمەبەست_ناو],
                    libraries=['objects/' + Path(گوزەر).name for گوزەر in کتێبخانە])
        (گروپ_نرخ / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (گروپ_نرخ / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        مەبەست = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / مەبەست.name
        with tarfile.open(str(임시압축), 'w:gz') as ئەرشیف_نرخ:
            ئەرشیف_نرخ.add(str(گروپ_نرخ), arcname=گروپ_نرخ.name)
        임시압축.replace(مەبەست)
    ڕاپۆرت_نرخ['relink_archive_sha256'] = دەرەنجام_فایل(مەبەست)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(ڕاپۆرت_نرخ, ensure_ascii=False, indent=2) + '\n')
    return مەبەست


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    نرخ = 해석기.parse_args()
    if نرخ.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
