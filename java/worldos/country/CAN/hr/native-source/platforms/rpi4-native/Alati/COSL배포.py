#!/usr/bin/env python3
"""redovno_artikl vlastiti ARM64 산출물을 검사하고 LGPL izvor_stablo·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

akcija_korijen = Path(__file__).resolve().parents[1]
spremište_korijen = akcija_korijen.parents[1]
odredište_naziv = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
biblioteka = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def raspršivanje_Datoteka(PUTANJA):
    return hashlib.sha256(Path(PUTANJA).read_bytes()).hexdigest()


def 점검():
    for Ime in ('vendor/wolfssh', 'vendor/wolfssl', 'udaljeno_VALUE/user_settings.h'):
        if (akcija_korijen / Ime).exists():
            raise SystemExit('COSL 배포 Zaustavi: 이전 GPL udaljeno_VALUE 구현이 izvor_stablo 트리에 남아 있습니다: ' + Ime)
    ožičen_VALUE = (akcija_korijen / 'mreža_hrpa/ožičen_mreža.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in ožičen_VALUE or 'SPDX-License-Identifier: GPL' in ožičen_VALUE:
        raise SystemExit('COSL 배포 Zaustavi: BSD GENET 구현·고지 provjeriti 필요')
    for Ime in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (spremište_korijen / Ime).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + Ime)
    simbol_VALUE = subprocess.check_output(['aarch64-linux-gnu-nm', str(akcija_korijen / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', simbol_VALUE):
        raise SystemExit('COSL 배포 Zaustavi: 커널에 이전 GPL lozinka_VALUE/SSH 심볼이 남아 있습니다. pokušati_ponovno_VALUE 빌드하세요.')
    for Ime in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Ime + r'$', simbol_VALUE, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + Ime)
    with tempfile.TemporaryDirectory(dir=str(akcija_korijen / 'build')) as 임시:
        IMAGE_VALUE = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(akcija_korijen / 'build/kernel.elf'), str(IMAGE_VALUE)])
        if raspršivanje_Datoteka(IMAGE_VALUE) != raspršivanje_Datoteka(akcija_korijen / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    izvješće_VALUE = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': raspršivanje_Datoteka(akcija_korijen / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Ime: raspršivanje_Datoteka(akcija_korijen / 'build' / Ime) for Ime in biblioteka}}
    (akcija_korijen / 'build/cosl-distribution-check.json').write_text(json.dumps(izvješće_VALUE, ensure_ascii=False, indent=2) + '\n')
    return izvješće_VALUE


def BIND_sudionik():
    izvješće_VALUE = 점검()
    배포 = akcija_korijen / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(akcija_korijen / 'build')) as 임시:
        Grupa_VALUE = Path(임시) / 'jkoros-native-relink'
        Grupa_VALUE.mkdir()
        def instanca_VALUE(원본, ravnopravan_član_VALUE):
            odredište_VALUE = Grupa_VALUE / ravnopravan_član_VALUE
            odredište_VALUE.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(odredište_VALUE), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(odredište_VALUE))
        for Ime in odredište_naziv:
            instanca_VALUE(akcija_korijen / 'build' / (Ime + '.o'), 'objects/' + Ime + '.o')
        for Ime in biblioteka:
            instanca_VALUE(akcija_korijen / 'build' / Ime, 'objects/' + Path(Ime).name)
        for Ime in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     'C_kompilator', 'korisnik', '명명', 'stroj', 'mreža_hrpa/mreža_hrpa.h', '부팅/veza_Raspored.ld',
                     'udaljeno_VALUE/assh_config.h', 'udaljeno_VALUE/config.h', 'udaljeno_VALUE/ctype.h', 'udaljeno_VALUE/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            instanca_VALUE(akcija_korijen / Ime, Ime)
        for Ime in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            instanca_VALUE(spremište_korijen / Ime, Ime)
        for PUTANJA in sorted((akcija_korijen / 'vendor').glob('LICENSE*')):
            instanca_VALUE(PUTANJA, 'vendor/' + PUTANJA.name)
        instanca_VALUE(akcija_korijen / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        instanca_VALUE(akcija_korijen / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        instanca_VALUE(spremište_korijen / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        instanca_VALUE(akcija_korijen / 'Alati/재연결.py', 'relink.py')
        for PUTANJA in sorted((akcija_korijen / 'build/user').glob('*.elf')):
            instanca_VALUE(PUTANJA, 'build/user/' + PUTANJA.name)
        for Ime in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            instanca_VALUE(akcija_korijen / 'build/user' / (Ime + '.o'), 'build/user/' + Ime + '.o')
        for Ime in ('crt', 'aot-runtime', 'CLR_Podrška', 'Pokreni', '미리번역', 'vratiti_most'):
            instanca_VALUE(akcija_korijen / 'build/ccompiler' / (Ime + '.o'), 'build/ccompiler/' + Ime + '.o')
        명세 = dict(izvješće_VALUE, objects=['objects/' + Ime + '.o' for Ime in odredište_naziv],
                    libraries=['objects/' + Path(PUTANJA).name for PUTANJA in biblioteka])
        (Grupa_VALUE / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (Grupa_VALUE / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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

TinyCC source is included in vendor/tinycc; the native port is in C_kompilator.
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
        cilj = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / cilj.name
        with tarfile.open(str(임시압축), 'w:gz') as Arhiva_VALUE:
            Arhiva_VALUE.add(str(Grupa_VALUE), arcname=Grupa_VALUE.name)
        임시압축.replace(cilj)
    izvješće_VALUE['relink_archive_sha256'] = raspršivanje_Datoteka(cilj)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(izvješće_VALUE, ensure_ascii=False, indent=2) + '\n')
    return cilj


if __name__ == '__main__':
    analizator_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizator_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    VALUE = analizator_48ee4b1b.parse_args()
    if VALUE.command == 'bundle':
        print('COSL source/relink kit:', BIND_sudionik())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
