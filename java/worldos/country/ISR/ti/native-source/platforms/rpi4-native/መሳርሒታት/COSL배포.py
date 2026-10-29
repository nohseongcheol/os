#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL ምንጪ_ገረብ·재연결 자료를 함께 묶는다."""
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
መዓልቦ_ሽም = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
ቤት_ንባብ = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def 해시(መገዲ):
    return hashlib.sha256(Path(መገዲ).read_bytes()).hexdigest()


def 점검():
    for ሽም in ('vendor/wolfssh', 'vendor/wolfssl', 'ርሑቕ_ዋጋ/user_settings.h'):
        if (기준 / ሽም).exists():
            raise SystemExit('COSL 배포 ኣቑም: 이전 GPL ርሑቕ_ዋጋ 구현이 ምንጪ_ገረብ 트리에 남아 있습니다: ' + ሽም)
    유선 = (기준 / 'ማሕበራዊ_ኔትወርክ_ድርደራ/유선망.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in 유선 or 'SPDX-License-Identifier: GPL' in 유선:
        raise SystemExit('COSL 배포 ኣቑም: BSD GENET 구현·고지 ኣረጋግጽ 필요')
    for ሽም in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (저장소 / ሽም).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + ሽም)
    ምልክት_ዋጋ = subprocess.check_output(['aarch64-linux-gnu-nm', str(기준 / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', ምልክት_ዋጋ):
        raise SystemExit('COSL 배포 ኣቑም: 커널에 이전 GPL መሕለፊ_ቃል_ዋጋ/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for ሽም in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + ሽም + r'$', ምልክት_ዋጋ, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + ሽም)
    with tempfile.TemporaryDirectory(dir=str(기준 / 'build')) as 임시:
        ምስሊ_ዋጋ = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(기준 / 'build/kernel.elf'), str(ምስሊ_ዋጋ)])
        if 해시(ምስሊ_ዋጋ) != 해시(기준 / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    ጸብጻብ_ዋጋ = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': 해시(기준 / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {ሽም: 해시(기준 / 'build' / ሽም) for ሽም in ቤት_ንባብ}}
    (기준 / 'build/cosl-distribution-check.json').write_text(json.dumps(ጸብጻብ_ዋጋ, ensure_ascii=False, indent=2) + '\n')
    return ጸብጻብ_ዋጋ


def 묶기():
    ጸብጻብ_ዋጋ = 점검()
    배포 = 기준 / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(기준 / 'build')) as 임시:
        ጉጅለ_ዋጋ = Path(임시) / 'jkoros-native-relink'
        ጉጅለ_ዋጋ.mkdir()
        def ቅዳሕ_ዋጋ(원본, መዘና_ዋጋ):
            መዓልቦ_ዋጋ = ጉጅለ_ዋጋ / መዘና_ዋጋ
            መዓልቦ_ዋጋ.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(መዓልቦ_ዋጋ), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(መዓልቦ_ዋጋ))
        for ሽም in መዓልቦ_ሽም:
            ቅዳሕ_ዋጋ(기준 / 'build' / (ሽም + '.o'), 'objects/' + ሽም + '.o')
        for ሽም in ቤት_ንባብ:
            ቅዳሕ_ዋጋ(기준 / 'build' / ሽም, 'objects/' + Path(ሽም).name)
        for ሽም in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'ተጠቃሚ', '명명', 'ማሽን', 'ማሕበራዊ_ኔትወርክ_ድርደራ/ማሕበራዊ_ኔትወርክ_ድርደራ.h', '부팅/መጋጠሚ_ኣቀማምጣ.ld',
                     'ርሑቕ_ዋጋ/assh_config.h', 'ርሑቕ_ዋጋ/config.h', 'ርሑቕ_ዋጋ/ctype.h', 'ርሑቕ_ዋጋ/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            ቅዳሕ_ዋጋ(기준 / ሽም, ሽም)
        for ሽም in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            ቅዳሕ_ዋጋ(저장소 / ሽም, ሽም)
        for መገዲ in sorted((기준 / 'vendor').glob('LICENSE*')):
            ቅዳሕ_ዋጋ(መገዲ, 'vendor/' + መገዲ.name)
        ቅዳሕ_ዋጋ(기준 / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        ቅዳሕ_ዋጋ(기준 / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        ቅዳሕ_ዋጋ(저장소 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        ቅዳሕ_ዋጋ(기준 / 'መሳርሒታት/재연결.py', 'relink.py')
        for መገዲ in sorted((기준 / 'build/user').glob('*.elf')):
            ቅዳሕ_ዋጋ(መገዲ, 'build/user/' + መገዲ.name)
        for ሽም in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            ቅዳሕ_ዋጋ(기준 / 'build/user' / (ሽም + '.o'), 'build/user/' + ሽም + '.o')
        for ሽም in ('crt', 'aot-runtime', 'ግዜ_ስራሕ_ናይ_ሓባር_ቛንቛ_ሓገዝ', 'ኣኺድ', '미리번역', '되돌림'):
            ቅዳሕ_ዋጋ(기준 / 'build/ccompiler' / (ሽም + '.o'), 'build/ccompiler/' + ሽም + '.o')
        명세 = dict(ጸብጻብ_ዋጋ, objects=['objects/' + ሽም + '.o' for ሽም in መዓልቦ_ሽም],
                    libraries=['objects/' + Path(መገዲ).name for መገዲ in ቤት_ንባብ])
        (ጉጅለ_ዋጋ / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (ጉጅለ_ዋጋ / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        ዕላማ = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / ዕላማ.name
        with tarfile.open(str(임시압축), 'w:gz') as ሰንድ_ዋጋ:
            ሰንድ_ዋጋ.add(str(ጉጅለ_ዋጋ), arcname=ጉጅለ_ዋጋ.name)
        임시압축.replace(ዕላማ)
    ጸብጻብ_ዋጋ['relink_archive_sha256'] = 해시(ዕላማ)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(ጸብጻብ_ዋጋ, ensure_ascii=False, indent=2) + '\n')
    return ዕላማ


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    ዋጋ = 해석기.parse_args()
    if ዋጋ.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
