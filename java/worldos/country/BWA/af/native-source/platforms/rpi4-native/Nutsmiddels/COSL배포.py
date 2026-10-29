#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL bron_boom·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

Project_wortel = Path(__file__).resolve().parents[1]
bewaarplek_wortel = Project_wortel.parents[1]
bestemming_naam = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
biblioteek = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def huts_lêer(Pad):
    return hashlib.sha256(Path(Pad).read_bytes()).hexdigest()


def 점검():
    for Naam in ('vendor/wolfssh', 'vendor/wolfssl', 'afstands_VALUE/user_settings.h'):
        if (Project_wortel / Naam).exists():
            raise SystemExit('COSL 배포 Stop: 이전 GPL afstands_VALUE 구현이 bron_boom 트리에 남아 있습니다: ' + Naam)
    bedraad_VALUE = (Project_wortel / 'Netwerk_Stapel/bedraad_Netwerk.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in bedraad_VALUE or 'SPDX-License-Identifier: GPL' in bedraad_VALUE:
        raise SystemExit('COSL 배포 Stop: BSD GENET 구현·고지 verifieer 필요')
    for Naam in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (bewaarplek_wortel / Naam).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + Naam)
    simbool_VALUE = subprocess.check_output(['aarch64-linux-gnu-nm', str(Project_wortel / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', simbool_VALUE):
        raise SystemExit('COSL 배포 Stop: 커널에 이전 GPL wagwoord_VALUE/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for Naam in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Naam + r'$', simbool_VALUE, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + Naam)
    with tempfile.TemporaryDirectory(dir=str(Project_wortel / 'build')) as 임시:
        foto_VALUE = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(Project_wortel / 'build/kernel.elf'), str(foto_VALUE)])
        if huts_lêer(foto_VALUE) != huts_lêer(Project_wortel / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    verslag_VALUE = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': huts_lêer(Project_wortel / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Naam: huts_lêer(Project_wortel / 'build' / Naam) for Naam in biblioteek}}
    (Project_wortel / 'build/cosl-distribution-check.json').write_text(json.dumps(verslag_VALUE, ensure_ascii=False, indent=2) + '\n')
    return verslag_VALUE


def 묶기():
    verslag_VALUE = 점검()
    배포 = Project_wortel / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(Project_wortel / 'build')) as 임시:
        Groep_VALUE = Path(임시) / 'jkoros-native-relink'
        Groep_VALUE.mkdir()
        def geval_VALUE(원본, portuur_VALUE):
            bestemming_VALUE = Groep_VALUE / portuur_VALUE
            bestemming_VALUE.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(bestemming_VALUE), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(bestemming_VALUE))
        for Naam in bestemming_naam:
            geval_VALUE(Project_wortel / 'build' / (Naam + '.o'), 'objects/' + Naam + '.o')
        for Naam in biblioteek:
            geval_VALUE(Project_wortel / 'build' / Naam, 'objects/' + Path(Naam).name)
        for Naam in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'gebruiker', '명명', 'masjien', 'Netwerk_Stapel/Netwerk_Stapel.h', '부팅/Skakel_Uitleg.ld',
                     'afstands_VALUE/assh_config.h', 'afstands_VALUE/config.h', 'afstands_VALUE/ctype.h', 'afstands_VALUE/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            geval_VALUE(Project_wortel / Naam, Naam)
        for Naam in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            geval_VALUE(bewaarplek_wortel / Naam, Naam)
        for Pad in sorted((Project_wortel / 'vendor').glob('LICENSE*')):
            geval_VALUE(Pad, 'vendor/' + Pad.name)
        geval_VALUE(Project_wortel / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        geval_VALUE(Project_wortel / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        geval_VALUE(bewaarplek_wortel / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        geval_VALUE(Project_wortel / 'Nutsmiddels/재연결.py', 'relink.py')
        for Pad in sorted((Project_wortel / 'build/user').glob('*.elf')):
            geval_VALUE(Pad, 'build/user/' + Pad.name)
        for Naam in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            geval_VALUE(Project_wortel / 'build/user' / (Naam + '.o'), 'build/user/' + Naam + '.o')
        for Naam in ('crt', 'aot-runtime', 'algemene_taallooptyd_Bystand', 'Loop', '미리번역', 'teruggee_brug'):
            geval_VALUE(Project_wortel / 'build/ccompiler' / (Naam + '.o'), 'build/ccompiler/' + Naam + '.o')
        명세 = dict(verslag_VALUE, objects=['objects/' + Naam + '.o' for Naam in bestemming_naam],
                    libraries=['objects/' + Path(Pad).name for Pad in biblioteek])
        (Groep_VALUE / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (Groep_VALUE / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        teiken = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / teiken.name
        with tarfile.open(str(임시압축), 'w:gz') as Argief_VALUE:
            Argief_VALUE.add(str(Groep_VALUE), arcname=Groep_VALUE.name)
        임시압축.replace(teiken)
    verslag_VALUE['relink_archive_sha256'] = huts_lêer(teiken)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(verslag_VALUE, ensure_ascii=False, indent=2) + '\n')
    return teiken


if __name__ == '__main__':
    ontleder_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ontleder_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    VALUE = ontleder_48ee4b1b.parse_args()
    if VALUE.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
