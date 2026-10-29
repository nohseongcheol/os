#!/usr/bin/env python3
"""dobrá_zboží vlastní ARM64 산출물을 검사하고 LGPL zdroj_strom·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

akce_kořen = Path(__file__).resolve().parents[1]
úložiště_kořen = akce_kořen.parents[1]
cíl_název = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
knihovna = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def hodnota_hash_Soubor(cesta_2):
    return hashlib.sha256(Path(cesta_2).read_bytes()).hexdigest()


def 점검():
    for Název in ('vendor/wolfssh', 'vendor/wolfssl', 'vzdálený_HODNOTA/user_settings.h'):
        if (akce_kořen / Název).exists():
            raise SystemExit('COSL distribuce_HODNOTA Zastavit: Předchozí_zboží GPL vzdálený_HODNOTA 구현이 zdroj_strom 트리에 남아 있습니다: ' + Název)
    drátový_HODNOTA = (akce_kořen / 'síť_Štos/drátový_síť.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in drátový_HODNOTA or 'SPDX-License-Identifier: GPL' in drátový_HODNOTA:
        raise SystemExit('COSL distribuce_HODNOTA Zastavit: BSD GENET implementace·고지 ověřit 필요')
    for Název in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (úložiště_kořen / Název).is_file():
            raise SystemExit('COSL distribuce_HODNOTA 고지 없음: ' + Název)
    symbol_HODNOTA = subprocess.check_output(['aarch64-linux-gnu-nm', str(akce_kořen / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', symbol_HODNOTA):
        raise SystemExit('COSL distribuce_HODNOTA Zastavit: 커널에 Předchozí_zboží GPL heslo_HODNOTA/SSH 심볼이 남아 있습니다. zkusit_znovu_HODNOTA 빌드하세요.')
    for Název in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Název + r'$', symbol_HODNOTA, re.M):
            raise SystemExit('COSL 대체 implementace 누락: ' + Název)
    with tempfile.TemporaryDirectory(dir=str(akce_kořen / 'build')) as 임시:
        image_HODNOTA = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(akce_kořen / 'build/kernel.elf'), str(image_HODNOTA)])
        if hodnota_hash_Soubor(image_HODNOTA) != hodnota_hash_Soubor(akce_kořen / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    Zpráva_HODNOTA = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': hodnota_hash_Soubor(akce_kořen / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Název: hodnota_hash_Soubor(akce_kořen / 'build' / Název) for Název in knihovna}}
    (akce_kořen / 'build/cosl-distribution-check.json').write_text(json.dumps(Zpráva_HODNOTA, ensure_ascii=False, indent=2) + '\n')
    return Zpráva_HODNOTA


def vázat_účastník():
    Zpráva_HODNOTA = 점검()
    distribuce_HODNOTA = akce_kořen / 'dist'
    distribuce_HODNOTA.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(akce_kořen / 'build')) as 임시:
        Skupina_HODNOTA = Path(임시) / 'jkoros-native-relink'
        Skupina_HODNOTA.mkdir()
        def instance_HODNOTA(원본, partner_HODNOTA):
            cíl_HODNOTA = Skupina_HODNOTA / partner_HODNOTA
            cíl_HODNOTA.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(cíl_HODNOTA), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(cíl_HODNOTA))
        for Název in cíl_název:
            instance_HODNOTA(akce_kořen / 'build' / (Název + '.o'), 'objects/' + Název + '.o')
        for Název in knihovna:
            instance_HODNOTA(akce_kořen / 'build' / Název, 'objects/' + Path(Název).name)
        for Název in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     'C_kompilátor', 'uživatelský_prostor', '명명', 'počítač', 'síť_Štos/síť_Štos.h', 'spuštění_stroje/rozvržení_spojování.ld',
                     'vzdálený_HODNOTA/assh_config.h', 'vzdálený_HODNOTA/config.h', 'vzdálený_HODNOTA/ctype.h', 'vzdálený_HODNOTA/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            instance_HODNOTA(akce_kořen / Název, Název)
        for Název in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            instance_HODNOTA(úložiště_kořen / Název, Název)
        for cesta_2 in sorted((akce_kořen / 'vendor').glob('LICENSE*')):
            instance_HODNOTA(cesta_2, 'vendor/' + cesta_2.name)
        instance_HODNOTA(akce_kořen / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        instance_HODNOTA(akce_kořen / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        instance_HODNOTA(úložiště_kořen / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        instance_HODNOTA(akce_kořen / 'nástroje/재연결.py', 'relink.py')
        for cesta_2 in sorted((akce_kořen / 'build/user').glob('*.elf')):
            instance_HODNOTA(cesta_2, 'build/user/' + cesta_2.name)
        for Název in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            instance_HODNOTA(akce_kořen / 'build/user' / (Název + '.o'), 'build/user/' + Název + '.o')
        for Název in ('crt', 'aot-runtime', 'CLR_vzpěra', 'Spustit_2', '미리번역', 'Vratka_most'):
            instance_HODNOTA(akce_kořen / 'build/ccompiler' / (Název + '.o'), 'build/ccompiler/' + Název + '.o')
        명세 = dict(Zpráva_HODNOTA, objects=['objects/' + Název + '.o' for Název in cíl_název],
                    libraries=['objects/' + Path(cesta_2).name for cesta_2 in knihovna])
        (Skupina_HODNOTA / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (Skupina_HODNOTA / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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

TinyCC source is included in vendor/tinycc; the native port is in C_kompilátor.
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
        cílová_úroveň = distribuce_HODNOTA / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / cílová_úroveň.name
        with tarfile.open(str(임시압축), 'w:gz') as Archiv_HODNOTA:
            Archiv_HODNOTA.add(str(Skupina_HODNOTA), arcname=Skupina_HODNOTA.name)
        임시압축.replace(cílová_úroveň)
    Zpráva_HODNOTA['relink_archive_sha256'] = hodnota_hash_Soubor(cílová_úroveň)
    (distribuce_HODNOTA / 'cosl-distribution.json').write_text(json.dumps(Zpráva_HODNOTA, ensure_ascii=False, indent=2) + '\n')
    return cílová_úroveň


if __name__ == '__main__':
    analyzátor_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analyzátor_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    HODNOTA = analyzátor_48ee4b1b.parse_args()
    if HODNOTA.command == 'bundle':
        print('COSL source/relink kit:', vázat_účastník())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
