#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL સ્રોત_ટ્રી·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

પ્રોજેક્ટ_રૂટ = Path(__file__).resolve().parents[1]
저장소 = પ્રોજેક્ટ_રૂટ.parents[1]
ગંતવ્ય_નામ = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
લાઇબ્રેરી = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def હૅશ_ફાઇલ(પથ):
    return hashlib.sha256(Path(પથ).read_bytes()).hexdigest()


def 점검():
    for નામ in ('vendor/wolfssh', 'vendor/wolfssl', 'રિમોટ_મૂલ્ય/user_settings.h'):
        if (પ્રોજેક્ટ_રૂટ / નામ).exists():
            raise SystemExit('COSL 배포 અટકાવો: 이전 GPL રિમોટ_મૂલ્ય 구현이 સ્રોત_ટ્રી 트리에 남아 있습니다: ' + નામ)
    વાયર્ડ_મૂલ્ય = (પ્રોજેક્ટ_રૂટ / 'નેટવર્ક_સ્ટેક/વાયર્ડ_નેટવર્ક.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in વાયર્ડ_મૂલ્ય or 'SPDX-License-Identifier: GPL' in વાયર્ડ_મૂલ્ય:
        raise SystemExit('COSL 배포 અટકાવો: BSD GENET 구현·고지 ચકાસવું 필요')
    for નામ in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (저장소 / નામ).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + નામ)
    પ્રતીક_મૂલ્ય = subprocess.check_output(['aarch64-linux-gnu-nm', str(પ્રોજેક્ટ_રૂટ / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', પ્રતીક_મૂલ્ય):
        raise SystemExit('COSL 배포 અટકાવો: 커널에 이전 GPL પાસવર્ડ_મૂલ્ય/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for નામ in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + નામ + r'$', પ્રતીક_મૂલ્ય, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + નામ)
    with tempfile.TemporaryDirectory(dir=str(પ્રોજેક્ટ_રૂટ / 'build')) as 임시:
        છબી_મૂલ્ય = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(પ્રોજેક્ટ_રૂટ / 'build/kernel.elf'), str(છબી_મૂલ્ય)])
        if હૅશ_ફાઇલ(છબી_મૂલ્ય) != હૅશ_ફાઇલ(પ્રોજેક્ટ_રૂટ / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    અહેવાલ_મૂલ્ય = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': હૅશ_ફાઇલ(પ્રોજેક્ટ_રૂટ / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {નામ: હૅશ_ફાઇલ(પ્રોજેક્ટ_રૂટ / 'build' / નામ) for નામ in લાઇબ્રેરી}}
    (પ્રોજેક્ટ_રૂટ / 'build/cosl-distribution-check.json').write_text(json.dumps(અહેવાલ_મૂલ્ય, ensure_ascii=False, indent=2) + '\n')
    return અહેવાલ_મૂલ્ય


def 묶기():
    અહેવાલ_મૂલ્ય = 점검()
    배포 = પ્રોજેક્ટ_રૂટ / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(પ્રોજેક્ટ_રૂટ / 'build')) as 임시:
        સમૂહ_મૂલ્ય = Path(임시) / 'jkoros-native-relink'
        સમૂહ_મૂલ્ય.mkdir()
        def ઉદાહરણ_મૂલ્ય(원본, પીઅર_મૂલ્ય):
            ગંતવ્ય_મૂલ્ય = સમૂહ_મૂલ્ય / પીઅર_મૂલ્ય
            ગંતવ્ય_મૂલ્ય.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(ગંતવ્ય_મૂલ્ય), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(ગંતવ્ય_મૂલ્ય))
        for નામ in ગંતવ્ય_નામ:
            ઉદાહરણ_મૂલ્ય(પ્રોજેક્ટ_રૂટ / 'build' / (નામ + '.o'), 'objects/' + નામ + '.o')
        for નામ in લાઇબ્રેરી:
            ઉદાહરણ_મૂલ્ય(પ્રોજેક્ટ_રૂટ / 'build' / નામ, 'objects/' + Path(નામ).name)
        for નામ in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'ઉપયોગકર્તા', '명명', 'મશીન', 'નેટવર્ક_સ્ટેક/નેટવર્ક_સ્ટેક.h', '부팅/લિંક_લેઆઉટ.ld',
                     'રિમોટ_મૂલ્ય/assh_config.h', 'રિમોટ_મૂલ્ય/config.h', 'રિમોટ_મૂલ્ય/ctype.h', 'રિમોટ_મૂલ્ય/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            ઉદાહરણ_મૂલ્ય(પ્રોજેક્ટ_રૂટ / નામ, નામ)
        for નામ in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            ઉદાહરણ_મૂલ્ય(저장소 / નામ, નામ)
        for પથ in sorted((પ્રોજેક્ટ_રૂટ / 'vendor').glob('LICENSE*')):
            ઉદાહરણ_મૂલ્ય(પથ, 'vendor/' + પથ.name)
        ઉદાહરણ_મૂલ્ય(પ્રોજેક્ટ_રૂટ / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        ઉદાહરણ_મૂલ્ય(પ્રોજેક્ટ_રૂટ / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        ઉદાહરણ_મૂલ્ય(저장소 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        ઉદાહરણ_મૂલ્ય(પ્રોજેક્ટ_રૂટ / 'ઉપકરણો/재연결.py', 'relink.py')
        for પથ in sorted((પ્રોજેક્ટ_રૂટ / 'build/user').glob('*.elf')):
            ઉદાહરણ_મૂલ્ય(પથ, 'build/user/' + પથ.name)
        for નામ in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            ઉદાહરણ_મૂલ્ય(પ્રોજેક્ટ_રૂટ / 'build/user' / (નામ + '.o'), 'build/user/' + નામ + '.o')
        for નામ in ('crt', 'aot-runtime', 'સામાન્ય_ભાષા_રનટાઇમ_સપોર્ટ', 'ચલાવો_2', '미리번역', '되돌림'):
            ઉદાહરણ_મૂલ્ય(પ્રોજેક્ટ_રૂટ / 'build/ccompiler' / (નામ + '.o'), 'build/ccompiler/' + નામ + '.o')
        명세 = dict(અહેવાલ_મૂલ્ય, objects=['objects/' + નામ + '.o' for નામ in ગંતવ્ય_નામ],
                    libraries=['objects/' + Path(પથ).name for પથ in લાઇબ્રેરી])
        (સમૂહ_મૂલ્ય / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (સમૂહ_મૂલ્ય / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        લક્ષ્ય = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / લક્ષ્ય.name
        with tarfile.open(str(임시압축), 'w:gz') as સંગ્રહ_મૂલ્ય:
            સંગ્રહ_મૂલ્ય.add(str(સમૂહ_મૂલ્ય), arcname=સમૂહ_મૂલ્ય.name)
        임시압축.replace(લક્ષ્ય)
    અહેવાલ_મૂલ્ય['relink_archive_sha256'] = હૅશ_ફાઇલ(લક્ષ્ય)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(અહેવાલ_મૂલ્ય, ensure_ascii=False, indent=2) + '\n')
    return લક્ષ્ય


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    મૂલ્ય = 해석기.parse_args()
    if મૂલ્ય.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
