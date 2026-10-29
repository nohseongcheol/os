#!/usr/bin/env python3
"""aktuelno_stavka 자체 ARM64 산출물을 검사하고 LGPL izvor_stablo·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

radnja_koren = Path(__file__).resolve().parents[1]
depo_koren = radnja_koren.parents[1]
odredište_ime = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
biblioteka = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def heš_Datoteka(putanja):
    return hashlib.sha256(Path(putanja).read_bytes()).hexdigest()


def 점검():
    for ime in ('vendor/wolfssh', 'vendor/wolfssl', 'udaljen_VALUE/user_settings.h'):
        if (radnja_koren / ime).exists():
            raise SystemExit('COSL 배포 Stani: 이전 GPL udaljen_VALUE 구현이 izvor_stablo 트리에 남아 있습니다: ' + ime)
    žični_VALUE = (radnja_koren / 'Mreža_stek/žični_Mreža.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in žični_VALUE or 'SPDX-License-Identifier: GPL' in žični_VALUE:
        raise SystemExit('COSL 배포 Stani: BSD GENET 구현·고지 verifikovati 필요')
    for ime in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (depo_koren / ime).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + ime)
    simbol_VALUE = subprocess.check_output(['aarch64-linux-gnu-nm', str(radnja_koren / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', simbol_VALUE):
        raise SystemExit('COSL 배포 Stani: 커널에 이전 GPL lozinka_VALUE/SSH 심볼이 남아 있습니다. pokušati_ponovo_VALUE 빌드하세요.')
    for ime in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + ime + r'$', simbol_VALUE, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + ime)
    with tempfile.TemporaryDirectory(dir=str(radnja_koren / 'build')) as 임시:
        IMAGE_VALUE = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(radnja_koren / 'build/kernel.elf'), str(IMAGE_VALUE)])
        if heš_Datoteka(IMAGE_VALUE) != heš_Datoteka(radnja_koren / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    izveštaj_VALUE = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': heš_Datoteka(radnja_koren / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {ime: heš_Datoteka(radnja_koren / 'build' / ime) for ime in biblioteka}}
    (radnja_koren / 'build/cosl-distribution-check.json').write_text(json.dumps(izveštaj_VALUE, ensure_ascii=False, indent=2) + '\n')
    return izveštaj_VALUE


def povezati_učesnik():
    izveštaj_VALUE = 점검()
    배포 = radnja_koren / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(radnja_koren / 'build')) as 임시:
        Grupa_VALUE = Path(임시) / 'jkoros-native-relink'
        Grupa_VALUE.mkdir()
        def instanca_VALUE(원본, ravnopravni_uređaj_VALUE):
            odredište_VALUE = Grupa_VALUE / ravnopravni_uređaj_VALUE
            odredište_VALUE.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(odredište_VALUE), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(odredište_VALUE))
        for ime in odredište_ime:
            instanca_VALUE(radnja_koren / 'build' / (ime + '.o'), 'objects/' + ime + '.o')
        for ime in biblioteka:
            instanca_VALUE(radnja_koren / 'build' / ime, 'objects/' + Path(ime).name)
        for ime in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     'C_kompajler', 'korisnik', '명명', 'računar', 'Mreža_stek/Mreža_stek.h', '부팅/Veza_Raspored.ld',
                     'udaljen_VALUE/assh_config.h', 'udaljen_VALUE/config.h', 'udaljen_VALUE/ctype.h', 'udaljen_VALUE/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            instanca_VALUE(radnja_koren / ime, ime)
        for ime in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            instanca_VALUE(depo_koren / ime, ime)
        for putanja in sorted((radnja_koren / 'vendor').glob('LICENSE*')):
            instanca_VALUE(putanja, 'vendor/' + putanja.name)
        instanca_VALUE(radnja_koren / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        instanca_VALUE(radnja_koren / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        instanca_VALUE(depo_koren / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        instanca_VALUE(radnja_koren / 'Alatke/재연결.py', 'relink.py')
        for putanja in sorted((radnja_koren / 'build/user').glob('*.elf')):
            instanca_VALUE(putanja, 'build/user/' + putanja.name)
        for ime in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            instanca_VALUE(radnja_koren / 'build/user' / (ime + '.o'), 'build/user/' + ime + '.o')
        for ime in ('crt', 'aot-runtime', 'CLR_komponenta_Podrška', 'koristiti', '미리번역', 'vratiti_most'):
            instanca_VALUE(radnja_koren / 'build/ccompiler' / (ime + '.o'), 'build/ccompiler/' + ime + '.o')
        명세 = dict(izveštaj_VALUE, objects=['objects/' + ime + '.o' for ime in odredište_ime],
                    libraries=['objects/' + Path(putanja).name for putanja in biblioteka])
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

TinyCC source is included in vendor/tinycc; the native port is in C_kompajler.
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
    izveštaj_VALUE['relink_archive_sha256'] = heš_Datoteka(cilj)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(izveštaj_VALUE, ensure_ascii=False, indent=2) + '\n')
    return cilj


if __name__ == '__main__':
    analizator_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizator_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    VALUE = analizator_48ee4b1b.parse_args()
    if VALUE.command == 'bundle':
        print('COSL source/relink kit:', povezati_učesnik())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
