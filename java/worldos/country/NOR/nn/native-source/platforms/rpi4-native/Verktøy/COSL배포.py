#!/usr/bin/env python3
"""betalt_vare 자체 ARM64 산출물을 검사하고 LGPL kjelde_tre·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

spegle_rot = Path(__file__).resolve().parents[1]
저장소 = spegle_rot.parents[1]
mål_namn = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
bibliotek = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def hash_fil(STIGE):
    return hashlib.sha256(Path(STIGE).read_bytes()).hexdigest()


def 점검():
    for Namn in ('vendor/wolfssh', 'vendor/wolfssl', 'fjern_VALUE/user_settings.h'):
        if (spegle_rot / Namn).exists():
            raise SystemExit('COSL 배포 Stopp: 이전 GPL fjern_VALUE 구현이 kjelde_tre 트리에 남아 있습니다: ' + Namn)
    kabelbasert_VALUE = (spegle_rot / 'Nettverk_Stabel/kabelbasert_Nettverk.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in kabelbasert_VALUE or 'SPDX-License-Identifier: GPL' in kabelbasert_VALUE:
        raise SystemExit('COSL 배포 Stopp: BSD GENET 구현·고지 stadfeste 필요')
    for Namn in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (저장소 / Namn).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + Namn)
    symbol_VALUE = subprocess.check_output(['aarch64-linux-gnu-nm', str(spegle_rot / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', symbol_VALUE):
        raise SystemExit('COSL 배포 Stopp: 커널에 이전 GPL passord_VALUE/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for Namn in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Namn + r'$', symbol_VALUE, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + Namn)
    with tempfile.TemporaryDirectory(dir=str(spegle_rot / 'build')) as 임시:
        IMAGE_VALUE = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(spegle_rot / 'build/kernel.elf'), str(IMAGE_VALUE)])
        if hash_fil(IMAGE_VALUE) != hash_fil(spegle_rot / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    rapport_VALUE = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': hash_fil(spegle_rot / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Namn: hash_fil(spegle_rot / 'build' / Namn) for Namn in bibliotek}}
    (spegle_rot / 'build/cosl-distribution-check.json').write_text(json.dumps(rapport_VALUE, ensure_ascii=False, indent=2) + '\n')
    return rapport_VALUE


def BIND_endepunkt():
    rapport_VALUE = 점검()
    배포 = spegle_rot / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(spegle_rot / 'build')) as 임시:
        gruppe_VALUE = Path(임시) / 'jkoros-native-relink'
        gruppe_VALUE.mkdir()
        def kopiere_VALUE(원본, node_VALUE_6a3b6fa7):
            mål_VALUE = gruppe_VALUE / node_VALUE_6a3b6fa7
            mål_VALUE.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(mål_VALUE), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(mål_VALUE))
        for Namn in mål_namn:
            kopiere_VALUE(spegle_rot / 'build' / (Namn + '.o'), 'objects/' + Namn + '.o')
        for Namn in bibliotek:
            kopiere_VALUE(spegle_rot / 'build' / Namn, 'objects/' + Path(Namn).name)
        for Namn in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'brukar', '명명', 'maskin', 'Nettverk_Stabel/Nettverk_Stabel.h', '부팅/kople_Oppsett.ld',
                     'fjern_VALUE/assh_config.h', 'fjern_VALUE/config.h', 'fjern_VALUE/ctype.h', 'fjern_VALUE/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            kopiere_VALUE(spegle_rot / Namn, Namn)
        for Namn in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            kopiere_VALUE(저장소 / Namn, Namn)
        for STIGE in sorted((spegle_rot / 'vendor').glob('LICENSE*')):
            kopiere_VALUE(STIGE, 'vendor/' + STIGE.name)
        kopiere_VALUE(spegle_rot / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        kopiere_VALUE(spegle_rot / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        kopiere_VALUE(저장소 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        kopiere_VALUE(spegle_rot / 'Verktøy/재연결.py', 'relink.py')
        for STIGE in sorted((spegle_rot / 'build/user').glob('*.elf')):
            kopiere_VALUE(STIGE, 'build/user/' + STIGE.name)
        for Namn in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            kopiere_VALUE(spegle_rot / 'build/user' / (Namn + '.o'), 'build/user/' + Namn + '.o')
        for Namn in ('crt', 'aot-runtime', 'Common_Language_Runtime_støtte', 'Køyr_2', '미리번역', 'levere_tilbake_bru'):
            kopiere_VALUE(spegle_rot / 'build/ccompiler' / (Namn + '.o'), 'build/ccompiler/' + Namn + '.o')
        명세 = dict(rapport_VALUE, objects=['objects/' + Namn + '.o' for Namn in mål_namn],
                    libraries=['objects/' + Path(STIGE).name for STIGE in bibliotek])
        (gruppe_VALUE / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (gruppe_VALUE / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        mål = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / mål.name
        with tarfile.open(str(임시압축), 'w:gz') as Arkiv_VALUE:
            Arkiv_VALUE.add(str(gruppe_VALUE), arcname=gruppe_VALUE.name)
        임시압축.replace(mål)
    rapport_VALUE['relink_archive_sha256'] = hash_fil(mål)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(rapport_VALUE, ensure_ascii=False, indent=2) + '\n')
    return mål


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    VALUE = 해석기.parse_args()
    if VALUE.command == 'bundle':
        print('COSL source/relink kit:', BIND_endepunkt())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
