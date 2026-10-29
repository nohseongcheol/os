#!/usr/bin/env python3
"""aktuellt_objekt eget ARM64 산출물을 검사하고 LGPL källa_träd·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

åtgärd_rot = Path(__file__).resolve().parents[1]
centrallager_rot = åtgärd_rot.parents[1]
mål_namn = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
bibliotek = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def hash_fil(sökväg_2):
    return hashlib.sha256(Path(sökväg_2).read_bytes()).hexdigest()


def 점검():
    for Namn in ('vendor/wolfssh', 'vendor/wolfssl', 'fjärr_värde/user_settings.h'):
        if (åtgärd_rot / Namn).exists():
            raise SystemExit('COSL fördelning_värde Stopp: Föregående_objekt GPL fjärr_värde 구현이 källa_träd 트리에 남아 있습니다: ' + Namn)
    kabelansluten_värde = (åtgärd_rot / 'nätverk_Stack/kabelansluten_nätverk.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in kabelansluten_värde or 'SPDX-License-Identifier: GPL' in kabelansluten_värde:
        raise SystemExit('COSL fördelning_värde Stopp: BSD GENET implementation·고지 verifiera 필요')
    for Namn in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (centrallager_rot / Namn).is_file():
            raise SystemExit('COSL fördelning_värde 고지 없음: ' + Namn)
    symbol_värde = subprocess.check_output(['aarch64-linux-gnu-nm', str(åtgärd_rot / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', symbol_värde):
        raise SystemExit('COSL fördelning_värde Stopp: 커널에 Föregående_objekt GPL lösenord_värde/SSH 심볼이 남아 있습니다. försöka_igen_värde 빌드하세요.')
    for Namn in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Namn + r'$', symbol_värde, re.M):
            raise SystemExit('COSL 대체 implementation 누락: ' + Namn)
    with tempfile.TemporaryDirectory(dir=str(åtgärd_rot / 'build')) as 임시:
        BILD_värde = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(åtgärd_rot / 'build/kernel.elf'), str(BILD_värde)])
        if hash_fil(BILD_värde) != hash_fil(åtgärd_rot / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    Rapport_värde = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': hash_fil(åtgärd_rot / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Namn: hash_fil(åtgärd_rot / 'build' / Namn) for Namn in bibliotek}}
    (åtgärd_rot / 'build/cosl-distribution-check.json').write_text(json.dumps(Rapport_värde, ensure_ascii=False, indent=2) + '\n')
    return Rapport_värde


def BIND_deltagare():
    Rapport_värde = 점검()
    fördelning_värde = åtgärd_rot / 'dist'
    fördelning_värde.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(åtgärd_rot / 'build')) as 임시:
        grupp_värde = Path(임시) / 'jkoros-native-relink'
        grupp_värde.mkdir()
        def kopia_värde(원본, peer_värde):
            mål_värde = grupp_värde / peer_värde
            mål_värde.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(mål_värde), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(mål_värde))
        for Namn in mål_namn:
            kopia_värde(åtgärd_rot / 'build' / (Namn + '.o'), 'objects/' + Namn + '.o')
        for Namn in bibliotek:
            kopia_värde(åtgärd_rot / 'build' / Namn, 'objects/' + Path(Namn).name)
        for Namn in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     'C_kompilerare', 'användarutrymme', '명명', 'dator', 'nätverk_Stack/nätverk_Stack.h', 'maskinstart/länkningslayout.ld',
                     'fjärr_värde/assh_config.h', 'fjärr_värde/config.h', 'fjärr_värde/ctype.h', 'fjärr_värde/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            kopia_värde(åtgärd_rot / Namn, Namn)
        for Namn in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            kopia_värde(centrallager_rot / Namn, Namn)
        for sökväg_2 in sorted((åtgärd_rot / 'vendor').glob('LICENSE*')):
            kopia_värde(sökväg_2, 'vendor/' + sökväg_2.name)
        kopia_värde(åtgärd_rot / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        kopia_värde(åtgärd_rot / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        kopia_värde(centrallager_rot / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        kopia_värde(åtgärd_rot / 'verktyg/재연결.py', 'relink.py')
        for sökväg_2 in sorted((åtgärd_rot / 'build/user').glob('*.elf')):
            kopia_värde(sökväg_2, 'build/user/' + sökväg_2.name)
        for Namn in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            kopia_värde(åtgärd_rot / 'build/user' / (Namn + '.o'), 'build/user/' + Namn + '.o')
        for Namn in ('crt', 'aot-runtime', 'CLR_stöd', 'Kör', '미리번역', 'Retur_brygga'):
            kopia_värde(åtgärd_rot / 'build/ccompiler' / (Namn + '.o'), 'build/ccompiler/' + Namn + '.o')
        명세 = dict(Rapport_värde, objects=['objects/' + Namn + '.o' for Namn in mål_namn],
                    libraries=['objects/' + Path(sökväg_2).name for sökväg_2 in bibliotek])
        (grupp_värde / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (grupp_värde / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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

TinyCC source is included in vendor/tinycc; the native port is in C_kompilerare.
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
        mål = fördelning_värde / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / mål.name
        with tarfile.open(str(임시압축), 'w:gz') as Arkiv_värde:
            Arkiv_värde.add(str(grupp_värde), arcname=grupp_värde.name)
        임시압축.replace(mål)
    Rapport_värde['relink_archive_sha256'] = hash_fil(mål)
    (fördelning_värde / 'cosl-distribution.json').write_text(json.dumps(Rapport_värde, ensure_ascii=False, indent=2) + '\n')
    return mål


if __name__ == '__main__':
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    värde = parser_48ee4b1b.parse_args()
    if värde.command == 'bundle':
        print('COSL source/relink kit:', BIND_deltagare())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
