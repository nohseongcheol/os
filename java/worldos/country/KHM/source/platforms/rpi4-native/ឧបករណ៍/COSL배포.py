#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL ប្រភព_មែកធាង·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

បញ្ចាំង_ឬស = Path(__file__).resolve().parents[1]
ឃ្លាំង_ផ្ទុក_ឬស = បញ្ចាំង_ឬស.parents[1]
ទិសដៅ_ឈ្មោះ = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
បណ្ណាល័យ = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def ហាស_ឯកសារ(ផ្លូវ):
    return hashlib.sha256(Path(ផ្លូវ).read_bytes()).hexdigest()


def 점검():
    for ឈ្មោះ in ('vendor/wolfssh', 'vendor/wolfssl', 'ពីចម្ងាយ_តំលៃ/user_settings.h'):
        if (បញ្ចាំង_ឬស / ឈ្មោះ).exists():
            raise SystemExit('COSL 배포 បញ្ឈប់: 이전 GPL ពីចម្ងាយ_តំលៃ 구현이 ប្រភព_មែកធាង 트리에 남아 있습니다: ' + ឈ្មោះ)
    ដែលប្រើខ្សែ_តំលៃ = (បញ្ចាំង_ឬស / 'ណិតវឺក_គរ/ដែលប្រើខ្សែ_ណិតវឺក.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in ដែលប្រើខ្សែ_តំលៃ or 'SPDX-License-Identifier: GPL' in ដែលប្រើខ្សែ_តំលៃ:
        raise SystemExit('COSL 배포 បញ្ឈប់: BSD GENET 구현·고지 ផ្ទៀងផ្ទាត់ 필요')
    for ឈ្មោះ in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (ឃ្លាំង_ផ្ទុក_ឬស / ឈ្មោះ).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + ឈ្មោះ)
    និមិត្ត_សញ្ញា_តំលៃ = subprocess.check_output(['aarch64-linux-gnu-nm', str(បញ្ចាំង_ឬស / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', និមិត្ត_សញ្ញា_តំលៃ):
        raise SystemExit('COSL 배포 បញ្ឈប់: 커널에 이전 GPL លេខសម្ងាត់_តំលៃ/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for ឈ្មោះ in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + ឈ្មោះ + r'$', និមិត្ត_សញ្ញា_តំលៃ, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + ឈ្មោះ)
    with tempfile.TemporaryDirectory(dir=str(បញ្ចាំង_ឬស / 'build')) as 임시:
        រូបថត_តំលៃ = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(បញ្ចាំង_ឬស / 'build/kernel.elf'), str(រូបថត_តំលៃ)])
        if ហាស_ឯកសារ(រូបថត_តំលៃ) != ហាស_ឯកសារ(បញ្ចាំង_ឬស / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    រាយការណ៍_តំលៃ = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': ហាស_ឯកសារ(បញ្ចាំង_ឬស / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {ឈ្មោះ: ហាស_ឯកសារ(បញ្ចាំង_ឬស / 'build' / ឈ្មោះ) for ឈ្មោះ in បណ្ណាល័យ}}
    (បញ្ចាំង_ឬស / 'build/cosl-distribution-check.json').write_text(json.dumps(រាយការណ៍_តំលៃ, ensure_ascii=False, indent=2) + '\n')
    return រាយការណ៍_តំលៃ


def 묶기():
    រាយការណ៍_តំលៃ = 점검()
    배포 = បញ្ចាំង_ឬស / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(បញ្ចាំង_ឬស / 'build')) as 임시:
        ក្រុម_តំលៃ = Path(임시) / 'jkoros-native-relink'
        ក្រុម_តំលៃ.mkdir()
        def ចំលង_តំលៃ(원본, សិទ្ធស្មើ_តំលៃ):
            ទិសដៅ_តំលៃ = ក្រុម_តំលៃ / សិទ្ធស្មើ_តំលៃ
            ទិសដៅ_តំលៃ.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(ទិសដៅ_តំលៃ), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(ទិសដៅ_តំលៃ))
        for ឈ្មោះ in ទិសដៅ_ឈ្មោះ:
            ចំលង_តំលៃ(បញ្ចាំង_ឬស / 'build' / (ឈ្មោះ + '.o'), 'objects/' + ឈ្មោះ + '.o')
        for ឈ្មោះ in បណ្ណាល័យ:
            ចំលង_តំលៃ(បញ្ចាំង_ឬស / 'build' / ឈ្មោះ, 'objects/' + Path(ឈ្មោះ).name)
        for ឈ្មោះ in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'អ្នកប្រើ', '명명', 'ម៉ាស៊ីន', 'ណិតវឺក_គរ/ណិតវឺក_គរ.h', '부팅/តំណ_ប្លង់.ld',
                     'ពីចម្ងាយ_តំលៃ/assh_config.h', 'ពីចម្ងាយ_តំលៃ/config.h', 'ពីចម្ងាយ_តំលៃ/ctype.h', 'ពីចម្ងាយ_តំលៃ/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            ចំលង_តំលៃ(បញ្ចាំង_ឬស / ឈ្មោះ, ឈ្មោះ)
        for ឈ្មោះ in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            ចំលង_តំលៃ(ឃ្លាំង_ផ្ទុក_ឬស / ឈ្មោះ, ឈ្មោះ)
        for ផ្លូវ in sorted((បញ្ចាំង_ឬស / 'vendor').glob('LICENSE*')):
            ចំលង_តំលៃ(ផ្លូវ, 'vendor/' + ផ្លូវ.name)
        ចំលង_តំលៃ(បញ្ចាំង_ឬស / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        ចំលង_តំលៃ(បញ្ចាំង_ឬស / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        ចំលង_តំលៃ(ឃ្លាំង_ផ្ទុក_ឬស / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        ចំលង_តំលៃ(បញ្ចាំង_ឬស / 'ឧបករណ៍/재연결.py', 'relink.py')
        for ផ្លូវ in sorted((បញ្ចាំង_ឬស / 'build/user').glob('*.elf')):
            ចំលង_តំលៃ(ផ្លូវ, 'build/user/' + ផ្លូវ.name)
        for ឈ្មោះ in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            ចំលង_តំលៃ(បញ្ចាំង_ឬស / 'build/user' / (ឈ្មោះ + '.o'), 'build/user/' + ឈ្មោះ + '.o')
        for ឈ្មោះ in ('crt', 'aot-runtime', 'ដំណើរការភាសាទូទៅ_ទម្រ', 'រត់', '미리번역', '되돌림'):
            ចំលង_តំលៃ(បញ្ចាំង_ឬស / 'build/ccompiler' / (ឈ្មោះ + '.o'), 'build/ccompiler/' + ឈ្មោះ + '.o')
        명세 = dict(រាយការណ៍_តំលៃ, objects=['objects/' + ឈ្មោះ + '.o' for ឈ្មោះ in ទិសដៅ_ឈ្មោះ],
                    libraries=['objects/' + Path(ផ្លូវ).name for ផ្លូវ in បណ្ណាល័យ])
        (ក្រុម_តំលៃ / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (ក្រុម_តំលៃ / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        គោលដៅ = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / គោលដៅ.name
        with tarfile.open(str(임시압축), 'w:gz') as ប័ណ្ណសារ_តំលៃ:
            ប័ណ្ណសារ_តំលៃ.add(str(ក្រុម_តំលៃ), arcname=ក្រុម_តំលៃ.name)
        임시압축.replace(គោលដៅ)
    រាយការណ៍_តំលៃ['relink_archive_sha256'] = ហាស_ឯកសារ(គោលដៅ)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(រាយការណ៍_តំលៃ, ensure_ascii=False, indent=2) + '\n')
    return គោលដៅ


if __name__ == '__main__':
    មុខងារ_ញែក_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    មុខងារ_ញែក_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    តំលៃ = មុខងារ_ញែក_48ee4b1b.parse_args()
    if តំលៃ.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
