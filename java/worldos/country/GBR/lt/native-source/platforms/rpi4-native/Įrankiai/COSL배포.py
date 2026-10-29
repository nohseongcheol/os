#!/usr/bin/env python3
"""dabartinis_prekė savas ARM64 산출물을 검사하고 LGPL šaltinis_medis·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

Project_šaknis = Path(__file__).resolve().parents[1]
saugykla_šaknis = Project_šaknis.parents[1]
vieta_pavadinimas = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
biblioteka = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def maiša_Failas(KELIAS):
    return hashlib.sha256(Path(KELIAS).read_bytes()).hexdigest()


def 점검():
    for Pavadinimas_2 in ('vendor/wolfssh', 'vendor/wolfssl', 'nuotolinis_VALUE/user_settings.h'):
        if (Project_šaknis / Pavadinimas_2).exists():
            raise SystemExit('COSL paskirstymas_VALUE Sustabdyti: 이전 GPL nuotolinis_VALUE 구현이 šaltinis_medis 트리에 남아 있습니다: ' + Pavadinimas_2)
    laidinis_VALUE = (Project_šaknis / 'tinklas_eilė/laidinis_tinklas.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in laidinis_VALUE or 'SPDX-License-Identifier: GPL' in laidinis_VALUE:
        raise SystemExit('COSL paskirstymas_VALUE Sustabdyti: BSD GENET 구현·고지 patvirtinti 필요')
    for Pavadinimas_2 in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (saugykla_šaknis / Pavadinimas_2).is_file():
            raise SystemExit('COSL paskirstymas_VALUE 고지 없음: ' + Pavadinimas_2)
    simbolis_VALUE = subprocess.check_output(['aarch64-linux-gnu-nm', str(Project_šaknis / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', simbolis_VALUE):
        raise SystemExit('COSL paskirstymas_VALUE Sustabdyti: 커널에 이전 GPL slaptažodis_VALUE/SSH 심볼이 남아 있습니다. kartoti_VALUE 빌드하세요.')
    for Pavadinimas_2 in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Pavadinimas_2 + r'$', simbolis_VALUE, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + Pavadinimas_2)
    with tempfile.TemporaryDirectory(dir=str(Project_šaknis / 'build')) as 임시:
        IMAGE_VALUE = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(Project_šaknis / 'build/kernel.elf'), str(IMAGE_VALUE)])
        if maiša_Failas(IMAGE_VALUE) != maiša_Failas(Project_šaknis / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    pranešti_VALUE = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': maiša_Failas(Project_šaknis / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Pavadinimas_2: maiša_Failas(Project_šaknis / 'build' / Pavadinimas_2) for Pavadinimas_2 in biblioteka}}
    (Project_šaknis / 'build/cosl-distribution-check.json').write_text(json.dumps(pranešti_VALUE, ensure_ascii=False, indent=2) + '\n')
    return pranešti_VALUE


def BIND_dalyvis():
    pranešti_VALUE = 점검()
    paskirstymas_VALUE = Project_šaknis / 'dist'
    paskirstymas_VALUE.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(Project_šaknis / 'build')) as 임시:
        Grupė_VALUE = Path(임시) / 'jkoros-native-relink'
        Grupė_VALUE.mkdir()
        def kopijuoti_VALUE(원본, lygiavertis_mazgas_VALUE):
            vieta_VALUE = Grupė_VALUE / lygiavertis_mazgas_VALUE
            vieta_VALUE.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(vieta_VALUE), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(vieta_VALUE))
        for Pavadinimas_2 in vieta_pavadinimas:
            kopijuoti_VALUE(Project_šaknis / 'build' / (Pavadinimas_2 + '.o'), 'objects/' + Pavadinimas_2 + '.o')
        for Pavadinimas_2 in biblioteka:
            kopijuoti_VALUE(Project_šaknis / 'build' / Pavadinimas_2, 'objects/' + Path(Pavadinimas_2).name)
        for Pavadinimas_2 in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     'C_kompiliatorius', 'naudotojas', '명명', 'mašina', 'tinklas_eilė/tinklas_eilė.h', '부팅/sieti_schema.ld',
                     'nuotolinis_VALUE/assh_config.h', 'nuotolinis_VALUE/config.h', 'nuotolinis_VALUE/ctype.h', 'nuotolinis_VALUE/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            kopijuoti_VALUE(Project_šaknis / Pavadinimas_2, Pavadinimas_2)
        for Pavadinimas_2 in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            kopijuoti_VALUE(saugykla_šaknis / Pavadinimas_2, Pavadinimas_2)
        for KELIAS in sorted((Project_šaknis / 'vendor').glob('LICENSE*')):
            kopijuoti_VALUE(KELIAS, 'vendor/' + KELIAS.name)
        kopijuoti_VALUE(Project_šaknis / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        kopijuoti_VALUE(Project_šaknis / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        kopijuoti_VALUE(saugykla_šaknis / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        kopijuoti_VALUE(Project_šaknis / 'Įrankiai/재연결.py', 'relink.py')
        for KELIAS in sorted((Project_šaknis / 'build/user').glob('*.elf')):
            kopijuoti_VALUE(KELIAS, 'build/user/' + KELIAS.name)
        for Pavadinimas_2 in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            kopijuoti_VALUE(Project_šaknis / 'build/user' / (Pavadinimas_2 + '.o'), 'build/user/' + Pavadinimas_2 + '.o')
        for Pavadinimas_2 in ('crt', 'aot-runtime', 'CLR_pagalba', 'Paleisti', '미리번역', 'grąžinti_tiltas'):
            kopijuoti_VALUE(Project_šaknis / 'build/ccompiler' / (Pavadinimas_2 + '.o'), 'build/ccompiler/' + Pavadinimas_2 + '.o')
        명세 = dict(pranešti_VALUE, objects=['objects/' + Pavadinimas_2 + '.o' for Pavadinimas_2 in vieta_pavadinimas],
                    libraries=['objects/' + Path(KELIAS).name for KELIAS in biblioteka])
        (Grupė_VALUE / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (Grupė_VALUE / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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

TinyCC source is included in vendor/tinycc; the native port is in C_kompiliatorius.
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
        tikslas = paskirstymas_VALUE / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / tikslas.name
        with tarfile.open(str(임시압축), 'w:gz') as Archyvas_VALUE:
            Archyvas_VALUE.add(str(Grupė_VALUE), arcname=Grupė_VALUE.name)
        임시압축.replace(tikslas)
    pranešti_VALUE['relink_archive_sha256'] = maiša_Failas(tikslas)
    (paskirstymas_VALUE / 'cosl-distribution.json').write_text(json.dumps(pranešti_VALUE, ensure_ascii=False, indent=2) + '\n')
    return tikslas


if __name__ == '__main__':
    analizatorius_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizatorius_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    VALUE = analizatorius_48ee4b1b.parse_args()
    if VALUE.command == 'bundle':
        print('COSL source/relink kit:', BIND_dalyvis())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
