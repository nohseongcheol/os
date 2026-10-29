#!/usr/bin/env python3
"""aktuel_vare eget ARM64 산출물을 검사하고 LGPL kilde_træ·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

To_do_rod = Path(__file__).resolve().parents[1]
lager_rod = To_do_rod.parents[1]
destination_navn = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
bibliotek = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def hash_fil(Sti):
    return hashlib.sha256(Path(Sti).read_bytes()).hexdigest()


def 점검():
    for Navn in ('vendor/wolfssh', 'vendor/wolfssl', 'fjern_VÆRDI/user_settings.h'):
        if (To_do_rod / Navn).exists():
            raise SystemExit('COSL distribution_VÆRDI Stop: Forrige_vare GPL fjern_VÆRDI 구현이 kilde_træ 트리에 남아 있습니다: ' + Navn)
    traditionel_VÆRDI = (To_do_rod / 'netværk_Stak/traditionel_netværk.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in traditionel_VÆRDI or 'SPDX-License-Identifier: GPL' in traditionel_VÆRDI:
        raise SystemExit('COSL distribution_VÆRDI Stop: BSD GENET 구현·고지 bekræfte 필요')
    for Navn in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (lager_rod / Navn).is_file():
            raise SystemExit('COSL distribution_VÆRDI 고지 없음: ' + Navn)
    symbol_VÆRDI = subprocess.check_output(['aarch64-linux-gnu-nm', str(To_do_rod / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', symbol_VÆRDI):
        raise SystemExit('COSL distribution_VÆRDI Stop: 커널에 Forrige_vare GPL adgangskode_VÆRDI/SSH 심볼이 남아 있습니다. prøve_igen_VÆRDI 빌드하세요.')
    for Navn in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Navn + r'$', symbol_VÆRDI, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + Navn)
    with tempfile.TemporaryDirectory(dir=str(To_do_rod / 'build')) as 임시:
        Image_VÆRDI = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(To_do_rod / 'build/kernel.elf'), str(Image_VÆRDI)])
        if hash_fil(Image_VÆRDI) != hash_fil(To_do_rod / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    rapport_VÆRDI = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': hash_fil(To_do_rod / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Navn: hash_fil(To_do_rod / 'build' / Navn) for Navn in bibliotek}}
    (To_do_rod / 'build/cosl-distribution-check.json').write_text(json.dumps(rapport_VÆRDI, ensure_ascii=False, indent=2) + '\n')
    return rapport_VÆRDI


def BIND_slutpunkt():
    rapport_VÆRDI = 점검()
    distribution_VÆRDI = To_do_rod / 'dist'
    distribution_VÆRDI.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(To_do_rod / 'build')) as 임시:
        gruppe_VÆRDI = Path(임시) / 'jkoros-native-relink'
        gruppe_VÆRDI.mkdir()
        def kopiere_VÆRDI(원본, peer_VÆRDI):
            destination_VÆRDI = gruppe_VÆRDI / peer_VÆRDI
            destination_VÆRDI.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(destination_VÆRDI), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(destination_VÆRDI))
        for Navn in destination_navn:
            kopiere_VÆRDI(To_do_rod / 'build' / (Navn + '.o'), 'objects/' + Navn + '.o')
        for Navn in bibliotek:
            kopiere_VÆRDI(To_do_rod / 'build' / Navn, 'objects/' + Path(Navn).name)
        for Navn in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     'C_compiler', 'bruger', '명명', 'maskine', 'netværk_Stak/netværk_Stak.h', '부팅/Link_Layout.ld',
                     'fjern_VÆRDI/assh_config.h', 'fjern_VÆRDI/config.h', 'fjern_VÆRDI/ctype.h', 'fjern_VÆRDI/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            kopiere_VÆRDI(To_do_rod / Navn, Navn)
        for Navn in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            kopiere_VÆRDI(lager_rod / Navn, Navn)
        for Sti in sorted((To_do_rod / 'vendor').glob('LICENSE*')):
            kopiere_VÆRDI(Sti, 'vendor/' + Sti.name)
        kopiere_VÆRDI(To_do_rod / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        kopiere_VÆRDI(To_do_rod / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        kopiere_VÆRDI(lager_rod / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        kopiere_VÆRDI(To_do_rod / 'Værktøjer/재연결.py', 'relink.py')
        for Sti in sorted((To_do_rod / 'build/user').glob('*.elf')):
            kopiere_VÆRDI(Sti, 'build/user/' + Sti.name)
        for Navn in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            kopiere_VÆRDI(To_do_rod / 'build/user' / (Navn + '.o'), 'build/user/' + Navn + '.o')
        for Navn in ('crt', 'aot-runtime', 'CLR_støtte', 'Kør_2', '미리번역', 'returnere_bro'):
            kopiere_VÆRDI(To_do_rod / 'build/ccompiler' / (Navn + '.o'), 'build/ccompiler/' + Navn + '.o')
        명세 = dict(rapport_VÆRDI, objects=['objects/' + Navn + '.o' for Navn in destination_navn],
                    libraries=['objects/' + Path(Sti).name for Sti in bibliotek])
        (gruppe_VÆRDI / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (gruppe_VÆRDI / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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

TinyCC source is included in vendor/tinycc; the native port is in C_compiler.
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
        mål = distribution_VÆRDI / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / mål.name
        with tarfile.open(str(임시압축), 'w:gz') as Arkiv_VÆRDI:
            Arkiv_VÆRDI.add(str(gruppe_VÆRDI), arcname=gruppe_VÆRDI.name)
        임시압축.replace(mål)
    rapport_VÆRDI['relink_archive_sha256'] = hash_fil(mål)
    (distribution_VÆRDI / 'cosl-distribution.json').write_text(json.dumps(rapport_VÆRDI, ensure_ascii=False, indent=2) + '\n')
    return mål


if __name__ == '__main__':
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    VÆRDI = parser_48ee4b1b.parse_args()
    if VÆRDI.command == 'bundle':
        print('COSL source/relink kit:', BIND_slutpunkt())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
