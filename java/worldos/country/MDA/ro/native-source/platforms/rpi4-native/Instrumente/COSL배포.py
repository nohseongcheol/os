#!/usr/bin/env python3
"""curent_element propriu ARM64 산출물을 검사하고 LGPL sursă_arborescență·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

Project_rădăcină = Path(__file__).resolve().parents[1]
depozit_rădăcină = Project_rădăcină.parents[1]
destinație_nume = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
bibliotecă = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def cod_hash_Fișier(Cale):
    return hashlib.sha256(Path(Cale).read_bytes()).hexdigest()


def 점검():
    for Nume in ('vendor/wolfssh', 'vendor/wolfssl', 'la_distanță_VALUE/user_settings.h'):
        if (Project_rădăcină / Nume).exists():
            raise SystemExit('COSL 배포 Oprește: Anteriorul_element GPL la_distanță_VALUE 구현이 sursă_arborescență 트리에 남아 있습니다: ' + Nume)
    cu_fir_VALUE = (Project_rădăcină / 'rețea_Teanc/cu_fir_rețea.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in cu_fir_VALUE or 'SPDX-License-Identifier: GPL' in cu_fir_VALUE:
        raise SystemExit('COSL 배포 Oprește: BSD GENET 구현·고지 verifica 필요')
    for Nume in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (depozit_rădăcină / Nume).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + Nume)
    simbol_VALUE = subprocess.check_output(['aarch64-linux-gnu-nm', str(Project_rădăcină / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', simbol_VALUE):
        raise SystemExit('COSL 배포 Oprește: 커널에 Anteriorul_element GPL parolă_VALUE/SSH 심볼이 남아 있습니다. reîncerca_VALUE 빌드하세요.')
    for Nume in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Nume + r'$', simbol_VALUE, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + Nume)
    with tempfile.TemporaryDirectory(dir=str(Project_rădăcină / 'build')) as 임시:
        IMAGE_VALUE = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(Project_rădăcină / 'build/kernel.elf'), str(IMAGE_VALUE)])
        if cod_hash_Fișier(IMAGE_VALUE) != cod_hash_Fișier(Project_rădăcină / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    raport_VALUE = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': cod_hash_Fișier(Project_rădăcină / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Nume: cod_hash_Fișier(Project_rădăcină / 'build' / Nume) for Nume in bibliotecă}}
    (Project_rădăcină / 'build/cosl-distribution-check.json').write_text(json.dumps(raport_VALUE, ensure_ascii=False, indent=2) + '\n')
    return raport_VALUE


def BIND_participant():
    raport_VALUE = 점검()
    배포 = Project_rădăcină / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(Project_rădăcină / 'build')) as 임시:
        grup_VALUE = Path(임시) / 'jkoros-native-relink'
        grup_VALUE.mkdir()
        def copia_VALUE(원본, pereche_VALUE):
            destinație_VALUE = grup_VALUE / pereche_VALUE
            destinație_VALUE.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(destinație_VALUE), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(destinație_VALUE))
        for Nume in destinație_nume:
            copia_VALUE(Project_rădăcină / 'build' / (Nume + '.o'), 'objects/' + Nume + '.o')
        for Nume in bibliotecă:
            copia_VALUE(Project_rădăcină / 'build' / Nume, 'objects/' + Path(Nume).name)
        for Nume in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     'C_compilator', 'utilizator', '명명', 'mașină', 'rețea_Teanc/rețea_Teanc.h', '부팅/Link_Aspect.ld',
                     'la_distanță_VALUE/assh_config.h', 'la_distanță_VALUE/config.h', 'la_distanță_VALUE/ctype.h', 'la_distanță_VALUE/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            copia_VALUE(Project_rădăcină / Nume, Nume)
        for Nume in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            copia_VALUE(depozit_rădăcină / Nume, Nume)
        for Cale in sorted((Project_rădăcină / 'vendor').glob('LICENSE*')):
            copia_VALUE(Cale, 'vendor/' + Cale.name)
        copia_VALUE(Project_rădăcină / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        copia_VALUE(Project_rădăcină / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        copia_VALUE(depozit_rădăcină / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        copia_VALUE(Project_rădăcină / 'Instrumente/재연결.py', 'relink.py')
        for Cale in sorted((Project_rădăcină / 'build/user').glob('*.elf')):
            copia_VALUE(Cale, 'build/user/' + Cale.name)
        for Nume in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            copia_VALUE(Project_rădăcină / 'build/user' / (Nume + '.o'), 'build/user/' + Nume + '.o')
        for Nume in ('crt', 'aot-runtime', 'CLR_suport', 'Pornește', '미리번역', 'restitui_punte'):
            copia_VALUE(Project_rădăcină / 'build/ccompiler' / (Nume + '.o'), 'build/ccompiler/' + Nume + '.o')
        명세 = dict(raport_VALUE, objects=['objects/' + Nume + '.o' for Nume in destinație_nume],
                    libraries=['objects/' + Path(Cale).name for Cale in bibliotecă])
        (grup_VALUE / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (grup_VALUE / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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

TinyCC source is included in vendor/tinycc; the native port is in C_compilator.
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
        țintă = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / țintă.name
        with tarfile.open(str(임시압축), 'w:gz') as Arhivă_VALUE:
            Arhivă_VALUE.add(str(grup_VALUE), arcname=grup_VALUE.name)
        임시압축.replace(țintă)
    raport_VALUE['relink_archive_sha256'] = cod_hash_Fișier(țintă)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(raport_VALUE, ensure_ascii=False, indent=2) + '\n')
    return țintă


if __name__ == '__main__':
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    VALUE = parser_48ee4b1b.parse_args()
    if VALUE.command == 'bundle':
        print('COSL source/relink kit:', BIND_participant())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
