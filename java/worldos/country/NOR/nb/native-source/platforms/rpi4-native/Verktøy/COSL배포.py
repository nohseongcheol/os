#!/usr/bin/env python3
"""betalt_vare eget ARM64 산출물을 검사하고 LGPL kilde_tre·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

speile_rot = Path(__file__).resolve().parents[1]
repositorium_rot = speile_rot.parents[1]
mål_navn = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
bibliotek = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def hash_Fil(Sti):
    return hashlib.sha256(Path(Sti).read_bytes()).hexdigest()


def 점검():
    for Navn in ('vendor/wolfssh', 'vendor/wolfssl', 'ekstern_VERDI_28edcfa1/user_settings.h'):
        if (speile_rot / Navn).exists():
            raise SystemExit('COSL distribusjon_VERDI Stopp: Forrige_vare GPL ekstern_VERDI_28edcfa1 구현이 kilde_tre 트리에 남아 있습니다: ' + Navn)
    kabelbasert_VERDI = (speile_rot / 'nettverk_stakk/kabelbasert_nettverk.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in kabelbasert_VERDI or 'SPDX-License-Identifier: GPL' in kabelbasert_VERDI:
        raise SystemExit('COSL distribusjon_VERDI Stopp: BSD GENET 구현·고지 bekrefte 필요')
    for Navn in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (repositorium_rot / Navn).is_file():
            raise SystemExit('COSL distribusjon_VERDI 고지 없음: ' + Navn)
    symbol_VERDI = subprocess.check_output(['aarch64-linux-gnu-nm', str(speile_rot / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', symbol_VERDI):
        raise SystemExit('COSL distribusjon_VERDI Stopp: 커널에 Forrige_vare GPL passord_VERDI/SSH 심볼이 남아 있습니다. prøve_på_nytt_VERDI 빌드하세요.')
    for Navn in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Navn + r'$', symbol_VERDI, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + Navn)
    with tempfile.TemporaryDirectory(dir=str(speile_rot / 'build')) as 임시:
        BILDE_VERDI = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(speile_rot / 'build/kernel.elf'), str(BILDE_VERDI)])
        if hash_Fil(BILDE_VERDI) != hash_Fil(speile_rot / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    rapport_VERDI = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': hash_Fil(speile_rot / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Navn: hash_Fil(speile_rot / 'build' / Navn) for Navn in bibliotek}}
    (speile_rot / 'build/cosl-distribution-check.json').write_text(json.dumps(rapport_VERDI, ensure_ascii=False, indent=2) + '\n')
    return rapport_VERDI


def BIND_deltaker():
    rapport_VERDI = 점검()
    distribusjon_VERDI = speile_rot / 'dist'
    distribusjon_VERDI.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(speile_rot / 'build')) as 임시:
        gruppe_VERDI = Path(임시) / 'jkoros-native-relink'
        gruppe_VERDI.mkdir()
        def kopiere_VERDI(원본, node_VERDI_6a3b6fa7):
            mål_VERDI = gruppe_VERDI / node_VERDI_6a3b6fa7
            mål_VERDI.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(mål_VERDI), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(mål_VERDI))
        for Navn in mål_navn:
            kopiere_VERDI(speile_rot / 'build' / (Navn + '.o'), 'objects/' + Navn + '.o')
        for Navn in bibliotek:
            kopiere_VERDI(speile_rot / 'build' / Navn, 'objects/' + Path(Navn).name)
        for Navn in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     'C_kompilator', 'bruker', '명명', 'maskin', 'nettverk_stakk/nettverk_stakk.h', '부팅/koble_Oppsett.ld',
                     'ekstern_VERDI_28edcfa1/assh_config.h', 'ekstern_VERDI_28edcfa1/config.h', 'ekstern_VERDI_28edcfa1/ctype.h', 'ekstern_VERDI_28edcfa1/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            kopiere_VERDI(speile_rot / Navn, Navn)
        for Navn in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            kopiere_VERDI(repositorium_rot / Navn, Navn)
        for Sti in sorted((speile_rot / 'vendor').glob('LICENSE*')):
            kopiere_VERDI(Sti, 'vendor/' + Sti.name)
        kopiere_VERDI(speile_rot / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        kopiere_VERDI(speile_rot / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        kopiere_VERDI(repositorium_rot / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        kopiere_VERDI(speile_rot / 'Verktøy/재연결.py', 'relink.py')
        for Sti in sorted((speile_rot / 'build/user').glob('*.elf')):
            kopiere_VERDI(Sti, 'build/user/' + Sti.name)
        for Navn in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            kopiere_VERDI(speile_rot / 'build/user' / (Navn + '.o'), 'build/user/' + Navn + '.o')
        for Navn in ('crt', 'aot-runtime', 'CLR_støtte', 'Kjør_2', '미리번역', 'return_bro'):
            kopiere_VERDI(speile_rot / 'build/ccompiler' / (Navn + '.o'), 'build/ccompiler/' + Navn + '.o')
        명세 = dict(rapport_VERDI, objects=['objects/' + Navn + '.o' for Navn in mål_navn],
                    libraries=['objects/' + Path(Sti).name for Sti in bibliotek])
        (gruppe_VERDI / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (gruppe_VERDI / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        mål = distribusjon_VERDI / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / mål.name
        with tarfile.open(str(임시압축), 'w:gz') as Arkiv_VERDI:
            Arkiv_VERDI.add(str(gruppe_VERDI), arcname=gruppe_VERDI.name)
        임시압축.replace(mål)
    rapport_VERDI['relink_archive_sha256'] = hash_Fil(mål)
    (distribusjon_VERDI / 'cosl-distribution.json').write_text(json.dumps(rapport_VERDI, ensure_ascii=False, indent=2) + '\n')
    return mål


if __name__ == '__main__':
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    VERDI = parser_48ee4b1b.parse_args()
    if VERDI.command == 'bundle':
        print('COSL source/relink kit:', BIND_deltaker())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
