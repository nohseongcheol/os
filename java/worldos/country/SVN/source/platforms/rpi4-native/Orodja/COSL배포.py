#!/usr/bin/env python3
"""sprotno_element lastno ARM64 산출물을 검사하고 LGPL vir_drevo·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

pobuda_koren = Path(__file__).resolve().parents[1]
shramba_koren = pobuda_koren.parents[1]
cilj_ime = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
knjižnica = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def zgoščena_vrednost_Datoteka(POT):
    return hashlib.sha256(Path(POT).read_bytes()).hexdigest()


def 점검():
    for Ime in ('vendor/wolfssh', 'vendor/wolfssl', 'oddaljen_VALUE/user_settings.h'):
        if (pobuda_koren / Ime).exists():
            raise SystemExit('COSL 배포 Zaustavi: 이전 GPL oddaljen_VALUE 구현이 vir_drevo 트리에 남아 있습니다: ' + Ime)
    žičen_VALUE = (pobuda_koren / 'mreža_Sklad/žičen_mreža.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in žičen_VALUE or 'SPDX-License-Identifier: GPL' in žičen_VALUE:
        raise SystemExit('COSL 배포 Zaustavi: BSD GENET 구현·고지 확인 필요')
    for Ime in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (shramba_koren / Ime).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + Ime)
    simbol_VALUE = subprocess.check_output(['aarch64-linux-gnu-nm', str(pobuda_koren / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', simbol_VALUE):
        raise SystemExit('COSL 배포 Zaustavi: 커널에 이전 GPL geslo_VALUE/SSH 심볼이 남아 있습니다. znova_poskusiti_VALUE 빌드하세요.')
    for Ime in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Ime + r'$', simbol_VALUE, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + Ime)
    with tempfile.TemporaryDirectory(dir=str(pobuda_koren / 'build')) as 임시:
        IMAGE_VALUE = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(pobuda_koren / 'build/kernel.elf'), str(IMAGE_VALUE)])
        if zgoščena_vrednost_Datoteka(IMAGE_VALUE) != zgoščena_vrednost_Datoteka(pobuda_koren / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    prijavi_VALUE = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': zgoščena_vrednost_Datoteka(pobuda_koren / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Ime: zgoščena_vrednost_Datoteka(pobuda_koren / 'build' / Ime) for Ime in knjižnica}}
    (pobuda_koren / 'build/cosl-distribution-check.json').write_text(json.dumps(prijavi_VALUE, ensure_ascii=False, indent=2) + '\n')
    return prijavi_VALUE


def BIND_končna_točka():
    prijavi_VALUE = 점검()
    배포 = pobuda_koren / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(pobuda_koren / 'build')) as 임시:
        Skupina_VALUE = Path(임시) / 'jkoros-native-relink'
        Skupina_VALUE.mkdir()
        def kopirati_VALUE(원본, enakovreden_VALUE):
            cilj_VALUE = Skupina_VALUE / enakovreden_VALUE
            cilj_VALUE.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(cilj_VALUE), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(cilj_VALUE))
        for Ime in cilj_ime:
            kopirati_VALUE(pobuda_koren / 'build' / (Ime + '.o'), 'objects/' + Ime + '.o')
        for Ime in knjižnica:
            kopirati_VALUE(pobuda_koren / 'build' / Ime, 'objects/' + Path(Ime).name)
        for Ime in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     'C_prevajalnik', 'uporabnik', '명명', 'računalnik', 'mreža_Sklad/mreža_Sklad.h', '부팅/Povezava_Krmarjenje.ld',
                     'oddaljen_VALUE/assh_config.h', 'oddaljen_VALUE/config.h', 'oddaljen_VALUE/ctype.h', 'oddaljen_VALUE/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            kopirati_VALUE(pobuda_koren / Ime, Ime)
        for Ime in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            kopirati_VALUE(shramba_koren / Ime, Ime)
        for POT in sorted((pobuda_koren / 'vendor').glob('LICENSE*')):
            kopirati_VALUE(POT, 'vendor/' + POT.name)
        kopirati_VALUE(pobuda_koren / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        kopirati_VALUE(pobuda_koren / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        kopirati_VALUE(shramba_koren / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        kopirati_VALUE(pobuda_koren / 'Orodja/재연결.py', 'relink.py')
        for POT in sorted((pobuda_koren / 'build/user').glob('*.elf')):
            kopirati_VALUE(POT, 'build/user/' + POT.name)
        for Ime in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            kopirati_VALUE(pobuda_koren / 'build/user' / (Ime + '.o'), 'build/user/' + Ime + '.o')
        for Ime in ('crt', 'aot-runtime', 'skupni_jezikovni_izvajalnik_Podpora', 'Zaženi', '미리번역', 'vrni_most'):
            kopirati_VALUE(pobuda_koren / 'build/ccompiler' / (Ime + '.o'), 'build/ccompiler/' + Ime + '.o')
        명세 = dict(prijavi_VALUE, objects=['objects/' + Ime + '.o' for Ime in cilj_ime],
                    libraries=['objects/' + Path(POT).name for POT in knjižnica])
        (Skupina_VALUE / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (Skupina_VALUE / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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

TinyCC source is included in vendor/tinycc; the native port is in C_prevajalnik.
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
        tarča = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / tarča.name
        with tarfile.open(str(임시압축), 'w:gz') as Arhiv_VALUE:
            Arhiv_VALUE.add(str(Skupina_VALUE), arcname=Skupina_VALUE.name)
        임시압축.replace(tarča)
    prijavi_VALUE['relink_archive_sha256'] = zgoščena_vrednost_Datoteka(tarča)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(prijavi_VALUE, ensure_ascii=False, indent=2) + '\n')
    return tarča


if __name__ == '__main__':
    razčlenjevalnik_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    razčlenjevalnik_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    VALUE = razčlenjevalnik_48ee4b1b.parse_args()
    if VALUE.command == 'bundle':
        print('COSL source/relink kit:', BIND_končna_točka())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
