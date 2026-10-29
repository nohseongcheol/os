#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL ଉତ୍ସ_ବୃକ୍ଷ·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ = Path(__file__).resolve().parents[1]
저장소 = ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍.parents[1]
ଲକ୍ଷସ୍ଥଳ_ନାମ = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
ଲାଇବ୍ରେରୀ = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def ହାସ୍_ଫାଇଲ୍(ପଥ):
    return hashlib.sha256(Path(ପଥ).read_bytes()).hexdigest()


def 점검():
    for ନାମ in ('vendor/wolfssh', 'vendor/wolfssl', 'ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ/user_settings.h'):
        if (ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / ନାମ).exists():
            raise SystemExit('COSL 배포 ଅଟକାନ୍ତୁ: 이전 GPL ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ 구현이 ଉତ୍ସ_ବୃକ୍ଷ 트리에 남아 있습니다: ' + ନାମ)
    ତାରଯୁକ୍ତ_ମୂଲ୍ୟ = (ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'ନେଟ୍_ୱାର୍କ୍_ଗଦା/ତାରଯୁକ୍ତ_ନେଟ୍_ୱାର୍କ୍.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in ତାରଯୁକ୍ତ_ମୂଲ୍ୟ or 'SPDX-License-Identifier: GPL' in ତାରଯୁକ୍ତ_ମୂଲ୍ୟ:
        raise SystemExit('COSL 배포 ଅଟକାନ୍ତୁ: BSD GENET 구현·고지 ଯାଞ୍ଚ୍_କରିବା 필요')
    for ନାମ in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (저장소 / ନାମ).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + ନାମ)
    ସଙ୍କେତ_ମୂଲ୍ୟ = subprocess.check_output(['aarch64-linux-gnu-nm', str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', ସଙ୍କେତ_ମୂଲ୍ୟ):
        raise SystemExit('COSL 배포 ଅଟକାନ୍ତୁ: 커널에 이전 GPL ପାସ୍_ୱାର୍ଡ୍_ମୂଲ୍ୟ/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for ନାମ in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + ନାମ + r'$', ସଙ୍କେତ_ମୂଲ୍ୟ, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + ନାମ)
    with tempfile.TemporaryDirectory(dir=str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build')) as 임시:
        ଚିତ୍ର_ମୂଲ୍ୟ = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build/kernel.elf'), str(ଚିତ୍ର_ମୂଲ୍ୟ)])
        if ହାସ୍_ଫାଇଲ୍(ଚିତ୍ର_ମୂଲ୍ୟ) != ହାସ୍_ଫାଇଲ୍(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    ରିପୋର୍ଟ_ମୂଲ୍ୟ = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': ହାସ୍_ଫାଇଲ୍(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {ନାମ: ହାସ୍_ଫାଇଲ୍(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build' / ନାମ) for ନାମ in ଲାଇବ୍ରେରୀ}}
    (ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build/cosl-distribution-check.json').write_text(json.dumps(ରିପୋର୍ଟ_ମୂଲ୍ୟ, ensure_ascii=False, indent=2) + '\n')
    return ରିପୋର୍ଟ_ମୂଲ୍ୟ


def 묶기():
    ରିପୋର୍ଟ_ମୂଲ୍ୟ = 점검()
    배포 = ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build')) as 임시:
        ଗୋଷ୍ଠୀ_ମୂଲ୍ୟ = Path(임시) / 'jkoros-native-relink'
        ଗୋଷ୍ଠୀ_ମୂଲ୍ୟ.mkdir()
        def କପି_ମୂଲ୍ୟ(원본, ସମକକ୍ଷ_ମୂଲ୍ୟ):
            ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ = ଗୋଷ୍ଠୀ_ମୂଲ୍ୟ / ସମକକ୍ଷ_ମୂଲ୍ୟ
            ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ))
        for ନାମ in ଲକ୍ଷସ୍ଥଳ_ନାମ:
            କପି_ମୂଲ୍ୟ(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build' / (ନାମ + '.o'), 'objects/' + ନାମ + '.o')
        for ନାମ in ଲାଇବ୍ରେରୀ:
            କପି_ମୂଲ୍ୟ(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build' / ନାମ, 'objects/' + Path(ନାମ).name)
        for ନାମ in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'ଉପଭୋକ୍ତା', '명명', 'ମେସିନ୍', 'ନେଟ୍_ୱାର୍କ୍_ଗଦା/ନେଟ୍_ୱାର୍କ୍_ଗଦା.h', '부팅/ଲିଙ୍କ୍_ଲେଆଉଟ୍.ld',
                     'ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ/assh_config.h', 'ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ/config.h', 'ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ/ctype.h', 'ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            କପି_ମୂଲ୍ୟ(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / ନାମ, ନାମ)
        for ନାମ in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            କପି_ମୂଲ୍ୟ(저장소 / ନାମ, ନାମ)
        for ପଥ in sorted((ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'vendor').glob('LICENSE*')):
            କପି_ମୂଲ୍ୟ(ପଥ, 'vendor/' + ପଥ.name)
        କପି_ମୂଲ୍ୟ(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        କପି_ମୂଲ୍ୟ(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        କପି_ମୂଲ୍ୟ(저장소 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        କପି_ମୂଲ୍ୟ(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'ଉପକରଣସମୂହ/재연결.py', 'relink.py')
        for ପଥ in sorted((ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build/user').glob('*.elf')):
            କପି_ମୂଲ୍ୟ(ପଥ, 'build/user/' + ପଥ.name)
        for ନାମ in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            କପି_ମୂଲ୍ୟ(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build/user' / (ନାମ + '.o'), 'build/user/' + ନାମ + '.o')
        for ନାମ in ('crt', 'aot-runtime', 'ସାଧାରଣ_ଭାଷା_ରନ୍_ଟାଇମ୍_ସମର୍ଥନ', 'ଚଳାନ୍ତୁ', '미리번역', '되돌림'):
            କପି_ମୂଲ୍ୟ(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build/ccompiler' / (ନାମ + '.o'), 'build/ccompiler/' + ନାମ + '.o')
        명세 = dict(ରିପୋର୍ଟ_ମୂଲ୍ୟ, objects=['objects/' + ନାମ + '.o' for ନାମ in ଲକ୍ଷସ୍ଥଳ_ନାମ],
                    libraries=['objects/' + Path(ପଥ).name for ପଥ in ଲାଇବ୍ରେରୀ])
        (ଗୋଷ୍ଠୀ_ମୂଲ୍ୟ / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (ଗୋଷ୍ଠୀ_ମୂଲ୍ୟ / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        ଲକ୍ଷ୍ୟସ୍ଥଳ = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / ଲକ୍ଷ୍ୟସ୍ଥଳ.name
        with tarfile.open(str(임시압축), 'w:gz') as ଅଭିଲେଖାଗାର_ମୂଲ୍ୟ:
            ଅଭିଲେଖାଗାର_ମୂଲ୍ୟ.add(str(ଗୋଷ୍ଠୀ_ମୂଲ୍ୟ), arcname=ଗୋଷ୍ଠୀ_ମୂଲ୍ୟ.name)
        임시압축.replace(ଲକ୍ଷ୍ୟସ୍ଥଳ)
    ରିପୋର୍ଟ_ମୂଲ୍ୟ['relink_archive_sha256'] = ହାସ୍_ଫାଇଲ୍(ଲକ୍ଷ୍ୟସ୍ଥଳ)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(ରିପୋର୍ଟ_ମୂଲ୍ୟ, ensure_ascii=False, indent=2) + '\n')
    return ଲକ୍ଷ୍ୟସ୍ଥଳ


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    ମୂଲ୍ୟ = 해석기.parse_args()
    if ମୂଲ୍ୟ.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
